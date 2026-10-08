import plotly.express as px
import pandas as pd

URL = ('https://raw.githubusercontent.com/leontoddjohnson/datasets/'
       'main/data/titanic.csv')


def clean_column_names(df):
    """Rename columns to lowercase-underscore format.

    For example, "Age Group" becomes "age_group" and "Pclass"
    becomes "pclass".
    """
    df = df.copy()
    df.columns = (df.columns.str.strip()
                            .str.lower()
                            .str.replace(' ', '_'))
    return df


def load_data():
    """Load the Titanic data with clean column names."""
    return clean_column_names(pd.read_csv(URL))


def survival_demographics():
    """Summarize survival by passenger class, sex and age group.

    Returns one row for every combination of class, sex and age
    group, including combinations that have no passengers.
    """
    df = load_data()

    # sort each passenger into an age category. the bins are closed
    # on the right, so (0, 12] is Child and (12, 19] is Teen.
    df['age_group'] = pd.cut(df['age'],
                             bins=[0, 12, 19, 59, float('inf')],
                             labels=['Child', 'Teen', 'Adult', 'Senior'])

    # observed=False keeps every age group in the result, even when
    # no passenger falls into it
    groups = df.groupby(['pclass', 'sex', 'age_group'], observed=False)

    table = groups['survived'].agg(n_passengers='count',
                                   n_survivors='sum').reset_index()
    table['survival_rate'] = table['n_survivors'] / table['n_passengers']

    return table.sort_values(['pclass', 'sex', 'age_group'],
                             ignore_index=True)


def visualize_demographic():
    """Bar chart of adult survival rate by passenger class and sex.

    Shows whether a better ticket helped men survive as much as it
    helped women.
    """
    table = survival_demographics()

    # compare adults only. children were treated differently, and the
    # adult groups are the largest, so their rates are the most reliable.
    adults = table[table['age_group'] == 'Adult'].copy()

    class_names = {1: 'First class', 2: 'Second class', 3: 'Third class'}
    adults['class'] = adults['pclass'].map(class_names)

    fig = px.bar(
        adults,
        x='class',
        y='survival_rate',
        color='sex',
        barmode='group',
        color_discrete_map={'female': '#2ca02c', 'male': '#d62728'},
        hover_data={'survival_rate': ':.0%',
                    'n_passengers': True,
                    'n_survivors': True},
        labels={'class': 'Passenger class',
                'survival_rate': 'Survival rate',
                'sex': 'Sex',
                'n_passengers': 'Passengers',
                'n_survivors': 'Survivors'},
        title='Survival rate of adult passengers (ages 20-59) '
              'by class and sex',
    )

    # show percentages on the axis and on top of each bar
    fig.update_yaxes(tickformat='.0%', range=[0, 1.1])
    fig.update_traces(texttemplate='%{y:.0%}', textposition='outside',
                      cliponaxis=False)
    fig.update_layout(bargap=0.35, bargroupgap=0.08)

    return fig


def family_groups():
    """Summarize ticket fares by family size and passenger class."""
    df = load_data()

    # siblings/spouses + parents/children + the passenger themselves
    df['family_size'] = df['sibsp'] + df['parch'] + 1

    groups = df.groupby(['family_size', 'pclass'])

    table = groups['fare'].agg(n_passengers='count',
                               avg_fare='mean',
                               min_fare='min',
                               max_fare='max').reset_index()

    return table.sort_values(['pclass', 'family_size'], ignore_index=True)


def last_names():
    """Count how many passengers share each last name.

    Names look like "Braund, Mr. Owen Harris", so the last name is
    everything before the first comma.
    """
    df = load_data()

    last_name = df['name'].str.split(',').str[0].str.strip()

    return last_name.value_counts()


def visualize_families():
    """Plot the fare range for each family size, one panel per class.

    Shows how much ticket fares varied inside one passenger class.
    """
    table = family_groups()

    class_names = {1: 'First class', 2: 'Second class', 3: 'Third class'}
    table['class'] = table['pclass'].map(class_names)

    # the dot sits at the average fare. these two columns say how far
    # the line reaches up to the highest fare and down to the lowest.
    table['above_avg'] = table['max_fare'] - table['avg_fare']
    table['below_avg'] = table['avg_fare'] - table['min_fare']

    fig = px.scatter(
        table,
        x='family_size',
        y='avg_fare',
        error_y='above_avg',
        error_y_minus='below_avg',
        facet_col='class',
        hover_data={'avg_fare': ':.2f',
                    'min_fare': ':.2f',
                    'max_fare': ':.2f',
                    'n_passengers': True,
                    'above_avg': False,
                    'below_avg': False},
        labels={'family_size': 'Family size',
                'avg_fare': 'Ticket fare (£)',
                'min_fare': 'Lowest fare',
                'max_fare': 'Highest fare',
                'n_passengers': 'Passengers'},
        title='Ticket fares by family size and class: '
              'average (dot) and lowest to highest (line)',
    )

    fig.update_traces(marker={'size': 9, 'color': '#3987e5'},
                      error_y={'color': '#3987e5', 'thickness': 2,
                               'width': 5})

    # one tick for every family size
    fig.update_xaxes(dtick=1)

    # facet titles come out as "class=First class". keep the name only.
    fig.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))

    return fig
