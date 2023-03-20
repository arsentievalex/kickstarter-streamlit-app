import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import statsmodels

# function to load data
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df


#wide layout
st.set_page_config(layout="wide")

# Load data
df = load_data('most_funded_feb_2023.csv')

# filter out only US projects
df = df[df['location_country'] == 'US']

# rename null values to 'Other'
df['category_parent_name'].fillna('Other', inplace=True)

# rename converted_pledged_amount to pledged_usd
df.rename(columns={'converted_pledged_amount': 'pledged_usd'}, inplace=True)
df.rename(columns={'category_parent_name': 'Category'}, inplace=True)

# group by category and count of projects
grouped_df_count = df.groupby("Category").agg({"id": ["count"]}).reset_index()

# rename columns
grouped_df_count.columns = ["Category", "Count"]

# filter df to keep only categories with more than 10 projects
df = df[df['Category'].isin(grouped_df_count[grouped_df_count['Count'] > 10]['Category'])]

# drop Other category
df = df[df['Category'] != 'Other']

# group by category and calculate mean of pledged usd
grouped_df_category = df.groupby("Category").agg({"pledged_usd": ["mean"]}).reset_index()

# rename columns
grouped_df_category.columns = ["Category", "Avg pledged"]

# group by category and calculate mean of goal
grouped_df_goal = df.groupby("Category").agg({"goal": ["mean"]}).reset_index()

# rename columns
grouped_df_goal.columns = ["Category", "Avg goal"]

# merge grouped_df_category and grouped_df_goal
grouped_df = pd.merge(grouped_df_category, grouped_df_goal, on="Category")

# calculate percentage of goal
grouped_df['Percentage of goal'] = round(grouped_df['Avg pledged'] / grouped_df['Avg goal'] * 100, 0)

# round avg pledged and avg goal to zero decimals
grouped_df['Avg pledged'] = grouped_df['Avg pledged'].round(0)
grouped_df['Avg goal'] = grouped_df['Avg goal'].round(0)

# sort df by percentage of goal
grouped_df.sort_values(by='Percentage of goal', ascending=False, inplace=True)

# Create title
st.title('Most Funded US Projects on Kickstarter')

# create sidebar
st.sidebar.header('About')
with st.sidebar:
    st.markdown('''This page shows comparison between average pledged and goal amount by category for categories with more than 10 projects.''')
    st.markdown('''A user can filter the bullet chart by category to dynamically show data.''')
    st.markdown('''The first scatterplot shows the relationship between pledged and goal amount by category.''')
    st.markdown('''The second scatterplot shows the relationship between pledged amount and a number of backers by category.''')

# insert html break into markdow

with st.expander('Expand to see the data'):
    st.dataframe(grouped_df, use_container_width=True)


selected_category = st.selectbox('Select category', grouped_df['Category'].unique())

# total pledged in selected category
avg_pledged = grouped_df[grouped_df['Category'] == selected_category]['Avg pledged'].values[0]
avg_goal = grouped_df[grouped_df['Category'] == selected_category]['Avg goal'].values[0]
pct = grouped_df[grouped_df['Category'] == selected_category]['Percentage of goal'].values[0]


formatted_avg_pledged = "{:.1f}M".format(avg_pledged / 1000000)

st.subheader('The average pledged amount per project in {} category is {} USD, which is {}% of the average goal of {} USD'
             .format(selected_category.lower(), formatted_avg_pledged, int(pct), '{:0,.0f}'.format(avg_goal)))

fig = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = avg_pledged,
    domain = {'x': [0.1, 1], 'y': [0, 1]},
    title = {'text' :"<b>{}</b>".format(selected_category), 'font': {'size': 16}},
    delta = {'reference': avg_goal},
    number=dict(font=dict(size=26)),
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, avg_pledged + avg_pledged * 0.1]},
        'threshold': {
            'line': {'color': "black", 'width': 2},
            'thickness': 0.8,
            'value': avg_goal}}))


fig.update_layout(height=115, width=1200)

# change top margin to bring graph closer to top
fig.update_layout(margin=dict(t=30, b=20, l=0, r=0))

st.plotly_chart(fig, use_container_width=False)


# create scatter plot of pledged and goal amounts
fig_2 = px.scatter(df, x='pledged_usd', y='goal', color='Category', hover_data=['Category'],
                   title='Distribution of pledged and goal amounts', trendline='ols')

# update axes names
fig_2.update_xaxes(title_text='Pledged amount (USD)')
fig_2.update_yaxes(title_text='Goal amount (USD)')

# display chart
st.plotly_chart(fig_2, use_container_width=True)


# create scatter plot of pledged amount and number of backers
fig_3 = px.scatter(df, x='pledged_usd', y='backers_count', color='Category', hover_data=['Category'],
                   title='Distribution of pledged amount and number of backers', trendline='ols')

# update axes names
fig_3.update_xaxes(title_text='Pledged amount (USD)')
fig_3.update_yaxes(title_text='Number of backers')

# display chart
st.plotly_chart(fig_3, use_container_width=True)

with st.sidebar:
    st.markdown('''The app created by [**@Oleksandr Arsentiev**](https://twitter.com/alexarsentiev) for the purpose of
    Streamlit App-A-Thon Contest''')