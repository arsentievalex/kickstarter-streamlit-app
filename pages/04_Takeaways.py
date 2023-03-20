import streamlit as st

# Create title
st.title('Most Funded US Projects on Kickstarter')
st.header('Takeaways from the analysis')


st.markdown('• The dataset consists of **1633** US projects that were successfully funded on Kickstarter.')
st.markdown('• The state with the **most funding** and the most number of projects is **California. New York and Washington** are on the 2nd and 3d places.')
st.markdown('• The **average pledged amount** per project across almost all states is around **1 million USD.**')
st.markdown('• The **average number of backers** per project varies greatrly across states **from 6,600 in New York to 12,700 in Colorado** (considering only states with more than 10 projects)')
st.markdown('• **80%** of projects from Georgia are in Games category')
st.markdown('• Utah is the state with **most funding** in Publishing category, having received **48.5 million USD** for only 2 projects')
st.markdown('• California is the state with diverse categories of projects, with **27%** of tech, and **30%** of fashion and design projects')
st.markdown('• The distribution of pledged amounts is heavily **skewed to the right**, with maximum value exceeding **40 million USD**')
st.markdown('• **Most of the data points**, however, are concentrated around **1 million USD**')
st.markdown('• Three **most funded** categories are **Games, Design and Technology**. These are also categories with the most number of projects and backers')
st.markdown('• The **most overfunded** category compared to the goal is **Fashion**, with the average goal of **32,545 USD**, and average pledged **902,340 USD**. Publishing and design are on the 2nd and 3d places')
st.markdown('• There is a **positive correlation** between both pledged amount and number of backers, and goal amount')
st.markdown('• A project with the **most funding** is Surprise! Four Secret Novels by Brandon Sanderson, collecting a whooping **41 millon USD with 185k backers**')

st.subheader('There are much more insights to uncover in this data set which is left up to the user to explore. Thanks for checking out my app!')

st.image('https://media.giphy.com/media/11AuX2SHScQumk/giphy.gif', use_column_width=True)

with st.sidebar:
    st.markdown('''The app created by [**@Oleksandr Arsentiev**](https://twitter.com/alexarsentiev) for the purpose of
    Streamlit App-A-Thon Contest''')

