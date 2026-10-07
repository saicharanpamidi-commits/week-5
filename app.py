import streamlit as st

from apputil import (family_groups, last_names, survival_demographics,
                     visualize_demographic, visualize_families)


st.write(
    '''
# Titanic Visualization 1

'''
)
st.write("Did a better ticket help men survive as much as it helped women?")

fig1 = visualize_demographic()
st.plotly_chart(fig1, width='stretch')

st.write(
    "No. First and second class were both safe for adult women (97% and "
    "90% survived), but only first class helped adult men (43%). Men in "
    "second class survived at 5%, which is lower than men in third "
    "class (14%)."
)

st.write("The full table behind this chart:")
st.dataframe(survival_demographics())

st.write(
    '''
# Titanic Visualization 2
'''
)
st.write("How much did ticket fares vary inside one passenger class?")

fig2 = visualize_families()
st.plotly_chart(fig2, width='stretch')

st.write(
    "A lot in first class, where fares ran from 0 to 512. Second and "
    "third class varied far less, with top fares of 73.50 and 69.55. "
    "The spread also shrinks as families get bigger, because each "
    "large family shared one ticket price."
)

st.write("The full table behind this chart:")
st.dataframe(family_groups())

st.write(
    '''
## Do last names agree with family size?
'''
)
st.write("The ten most common last names:")
st.dataframe(last_names().head(10))

st.write(
    "Only partly. 537 passengers travelled alone by family size, and 534 "
    "have a last name that nobody else has, so the totals look close. But "
    "they are not the same people: 83 solo travellers share a last name "
    "with someone else, and 80 passengers with family aboard have a last "
    "name that appears only once. All 7 passengers named Sage have a "
    "family size of 11, so some relatives are missing from this data. "
    "Six passengers are named Johnson, but three of them travelled alone."
)