import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# function to load data
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df


# Load data
df = load_data('most_funded_feb_2023.csv')

# filter out only US projects
df = df[df['location_country'] == 'US']

# rename null values to 'Other'
df['category_parent_name'].fillna('Other', inplace=True)

# rename converted_pledged_amount to pledged_usd
df.rename(columns={'converted_pledged_amount': 'pledged_usd'}, inplace=True)

# get unique categories
unique_categories = df['category_parent_name'].unique()

# group by category and calculate sum, count, and average
grouped_df_category = df.groupby("category_parent_name").agg({"pledged_usd": ["sum", "count", "mean"]}).reset_index()

# rename columns
grouped_df_category.columns = ["Category", "Total pledged", "Total projects", "Average pledged per project"]


# Create title
st.title('Most Funded US Projects on Kickstarter')
st.write('')

# create sidebar
st.sidebar.header('About')
with st.sidebar:
    st.markdown('''
    This page dives deeper into the distribution of total pledged amounts. A user can filter by category and pledged amount to dynamically show data.
    ''')
    # create multiselect for categories
    selected_categories = st.multiselect('Select categories', sorted(unique_categories), default=sorted(unique_categories))

    if selected_categories:
        # filter df using selected categories
        df = df[df['category_parent_name'].isin(selected_categories)]

# Get min and max values for sliders
min_pledged = int(df['pledged_usd'].min())
max_pledged = int(df['pledged_usd'].max())

# create columns that will hold metrics
col1, col2 = st.columns(2)

st.header('Apply filters to explore data 🔍')
if max_pledged > min_pledged:
    slider_input_pledged = st.slider('Filter by Pledged Amount', min_value=min_pledged, max_value=max_pledged, step=1000000,
                                     value=(min_pledged, max_pledged), format='$%d')
    # filter grouped_df using slider input
    df = df[(df['pledged_usd'] >=
                             slider_input_pledged[0]) & (df['pledged_usd'] <= slider_input_pledged[1])]

# display metrics
with col1:
    st.metric("Median Pledged per Project", value="${:,.0f}".format(df['pledged_usd'].median()), delta=None)
    st.metric("Average Pledged per Project", value="${:,.0f}".format(df['pledged_usd'].mean()), delta=None)
with col2:
    st.metric("25th Pct", value="${:,.0f}".format(np.percentile(df['pledged_usd'], 0.25)), delta=None)
    st.metric("75th Pct", value="${:,.0f}".format(np.percentile(df['pledged_usd'], 0.75)), delta=None)

# create histogram
fig = px.histogram(df, x="pledged_usd", title="Distribution of Pledged Amounts")

# update xaxis title
fig.update_xaxes(title_text="Pledged Amount (USD)", showgrid=False)
# update yaxis title
fig.update_yaxes(title_text="N", showgrid=False)
# update on hover text
fig.update_traces(hovertemplate="Pledged Amount: %{x:.2s}<extra></extra>")
# set background color to gray
fig.update_layout(plot_bgcolor='#f2f2f2', font=dict(size=14))

st.plotly_chart(fig, use_container_width=True)



selected_metric = st.selectbox("Select a metric", ["Total pledged", "Average pledged per project", "Total projects"])

if selected_metric == "Total pledged":
    # create a horizontal bar chart with categories
    fig_2 = px.bar(grouped_df_category, x="Total pledged", y="Category", color="Total pledged", orientation='h',
                   color_continuous_scale=px.colors.sequential.algae, title='Total Pledged per Category')

    # sort bar chart by total pledged
    fig_2.update_layout(yaxis={'categoryorder': 'total ascending'},
                        plot_bgcolor='#f2f2f2', font=dict(size=14))

    # update on hover text
    fig_2.update_traces(hovertemplate="Total Pledged: %{x:.2s}<extra></extra>")
    fig_2.update_coloraxes(showscale=False)

    # show chart
    st.plotly_chart(fig_2, use_container_width=True)

elif selected_metric == "Average pledged per project":
    # create a horizontal bar chart with categories
    fig_2 = px.bar(grouped_df_category, x="Average pledged per project", y="Category", color="Average pledged per project", orientation='h',
                   color_continuous_scale=px.colors.sequential.Brwnyl, title='Average Pledged per Category')

    # sort bar chart by total pledged
    fig_2.update_layout(yaxis={'categoryorder': 'total ascending'},
                        plot_bgcolor='#f2f2f2', font=dict(size=14))

    # update on hover text
    fig_2.update_traces(hovertemplate="Avg Pledged: %{x:.2s}<extra></extra>")
    fig_2.update_coloraxes(showscale=False)

    # show chart
    st.plotly_chart(fig_2, use_container_width=True)

elif selected_metric == "Total projects":
    # create a horizontal bar chart with categories
    fig_2 = px.bar(grouped_df_category, x="Total projects", y="Category", color="Total projects", orientation='h',
                   color_continuous_scale=px.colors.sequential.Teal, title='Total Projects per Category')

    # sort bar chart by total pledged
    fig_2.update_layout(yaxis={'categoryorder': 'total ascending'},
                        plot_bgcolor='#f2f2f2', font=dict(size=14))

    # update on hover text
    fig_2.update_traces(hovertemplate="Total projects: %{x:.2s}<extra></extra>")
    fig_2.update_coloraxes(showscale=False)

    # show chart
    st.plotly_chart(fig_2, use_container_width=True)


with st.sidebar:
    st.markdown('''The app created by [**@Oleksandr Arsentiev**](https://twitter.com/alexarsentiev) for the purpose of
Streamlit App-A-Thon Contest''')