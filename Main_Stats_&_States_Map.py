import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# function to load data
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df


st.set_page_config(
    page_title="Kickstarter Projects")

# Load data
df = load_data('most_funded_feb_2023.csv')

# filter out only US projects
df = df[df['location_country'] == 'US']

# rename null values to 'Other'
df['category_parent_name'].fillna('Other', inplace=True)

# get unique categories
unique_categories = df['category_parent_name'].unique()


# Create title
st.title('Most Funded US Projects on Kickstarter')
st.write('')

# create sidebar
st.sidebar.header('About')
with st.sidebar:
    st.markdown('''
    This app presents the analysis of the most funded projects on Kickstarter in the US.
    The dataset is taken from Kaggle - [URL](https://www.kaggle.com/datasets/patkle/most-funded-kickstarter-projects)
    ''', unsafe_allow_html=True)

    st.markdown('''The main page represents the basic statistics of the data set and the maps of the US with the total amount of pledged money per state and a total number of projects.
    ''')

    # create multiselect for categories
    selected_categories = st.multiselect('Select categories', sorted(unique_categories), default=sorted(unique_categories))

    if selected_categories:
        # filter df using selected categories
        df = df[df['category_parent_name'].isin(selected_categories)]


# group and calculate sum, count, and average
grouped_df = df.groupby("location_state").agg({"converted_pledged_amount": ["sum", "count", "mean"]}).reset_index()

# rename columns
grouped_df.columns = ["state_code", "total_pledged", "count", "average_pledged"]


# group by state and calculate sum and average of backers_count
grouped_df_backers = df.groupby("location_state").agg({"backers_count": ["sum", "mean"]}).reset_index()

# rename columns
grouped_df_backers.columns = ["state_code", "total_backers", "average_backers"]

# merge grouped_df and grouped_df_backers
grouped_df = pd.merge(grouped_df, grouped_df_backers, on="state_code")


# Add hover text with additional information
hover_text = []
for index, row in grouped_df.iterrows():
    hover_text.append("State: {}<br>Total pledged: ${:,.0f}"
                      "<br>Average pledged per project: ${:,.0f}"
                      "<br>Total backers: {:,.0f}"
                      "<br>Average backers per project: {:,.0f}"
                      "<br>Count of projects: {:,.0f}"
                      .format(row["state_code"], row['total_pledged'], row["average_pledged"], row['total_backers'], row['average_backers'], row["count"]))


# Add hover text to DataFrame
grouped_df["hover_text"] = hover_text

# Get min and max values for sliders
min_pledged = int(grouped_df['total_pledged'].min())
max_pledged = int(grouped_df['total_pledged'].max())

min_count = int(grouped_df['count'].min())
max_count = int(grouped_df['count'].max())

# create columns and display metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Projects", value=df.shape[0], delta=None)
    st.metric("Average Pledged per Project", value="${:,.0f}".format(df['converted_pledged_amount'].mean()), delta=None)
with col2:
    st.metric("Total Pledged", value="${:,.0f}".format(df['converted_pledged_amount'].sum()), delta=None)
    st.metric("Average Backers per Project", value="{:,.0f}".format(df['backers_count'].mean()), delta=None)


# create divider
st.write('')

st.header('Apply filters to explore data 🔍')
if max_pledged > min_pledged:
    slider_input_pledged = st.slider('Filter by Total Pledged', min_value=min_pledged, max_value=max_pledged, step=10000000,
                                     value=(min_pledged, max_pledged), format='$%d')
    # filter grouped_df using slider input
    grouped_df = grouped_df[(grouped_df['total_pledged'] >=
                             slider_input_pledged[0]) & (grouped_df['total_pledged'] <= slider_input_pledged[1])]


# Create choropleth map with total pledged by state
fig = px.choropleth(grouped_df,
                    locations="state_code",
                    locationmode="USA-states",
                    color="total_pledged",
                    scope="usa",
                    custom_data=["hover_text"],
                    hover_name=None,
                    title="US States by Total $ Pledged")

# Update hover text template to use custom hover text
fig.update_traces(hovertemplate="%{customdata[0]}")


# Apply custom template and styling options
fig.update_layout(template="plotly_white",
                  geo=dict(bgcolor="#f2f2f2",
                           lakecolor="#ffffff",
                           landcolor="#f2f2f2",
                           coastlinewidth=0.5,
                           projection=dict(type="albers usa"),
                           showlakes=True),
                  coloraxis=dict(colorbar=dict(title=dict(text="USD",
                                                           font=dict(size=18))),
                                 colorscale="Greens",
                                 showscale=True),
                  font=dict(size=14))

# Show figure
st.plotly_chart(fig)

# create second copy of grouped_df
grouped_df_count = grouped_df.copy()

if max_count > min_count:
    slider_input_count = st.slider('Filter by Total Projects', min_value=min_count, max_value=max_count, step=10,
                                 value=(min_count, max_count), format='%d')

    # filter grouped_df using slider input
    grouped_df_count = grouped_df_count[(grouped_df_count['count']
                                         >= slider_input_count[0]) & (grouped_df_count['count'] <= slider_input_count[1])]

# Create choropleth map with number of projects by state
fig_2 = px.choropleth(grouped_df_count,
                    locations="state_code",
                    locationmode="USA-states",
                    color="count",
                    scope="usa",
                    custom_data=["hover_text"],
                    hover_name=None,
                    title="US States by Number of Projects")

# Update hover text template to use custom hover text
fig_2.update_traces(hovertemplate="%{customdata[0]}")

# Apply custom template and styling options
fig_2.update_layout(template="plotly_white",
                  geo=dict(bgcolor="#f2f2f2",
                           lakecolor="#ffffff",
                           landcolor="#f2f2f2",
                           coastlinewidth=0.5,
                           projection=dict(type="albers usa"),
                           showlakes=True),
                  coloraxis=dict(colorbar=dict(title=dict(text="N",
                                                           font=dict(size=18))),
                                 colorscale="Blues",
                                 showscale=True),
                  font=dict(size=14))


# Show figure
st.plotly_chart(fig_2)

with st.sidebar:
    st.markdown('''The app created by [**@Oleksandr Arsentiev**](https://twitter.com/alexarsentiev) for the purpose of
Streamlit App-A-Thon Contest''')
