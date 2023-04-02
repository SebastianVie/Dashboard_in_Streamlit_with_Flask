from sqlalchemy import create_engine, engine, text
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import streamlit_authenticator as stauth
import altair as alt
import requests
import matplotlib.pyplot as plt
from yaml.loader import SafeLoader
import yaml

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

# Define the API key
headers = {'x-api-key': 'Capstone2023'}

@st.experimental_memo 
def load_data(path):
    try:
        response = requests.get(path, headers=headers)
        json_data = response.json()
        data = pd.DataFrame(json_data['result'])
    except Exception as e:
        print(e)
    return data 

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Hello *{name}*')
    st.title('My Capstone for H&M')
    st.title('Student: Sebastian')

    st.image('HM.jpg')

    path = "https://api-dot-capston1-376415.oa.r.appspot.com/api/v1/customers"
    customers_df = load_data(path)

    path1 = "https://api-dot-capston1-376415.oa.r.appspot.com/api/v1/transactions"
    transactions_df = load_data(path1)

    path2 = 'https://api-dot-capston1-376415.oa.r.appspot.com/api/v1/articles'
    articles_df = load_data(path2)

    #At the beginning I used the full dataset and merged the tables in the code. SInce the loading took to long, I also added the merged Data here.

    path3 = 'https://api-dot-capston1-376415.oa.r.appspot.com/api/v1/merged'
    merged_data = load_data(path3)

    age_lst = customers_df["age"].unique().tolist()

    membership_status_lst = customers_df["club_member_status"].unique().tolist()

    
    fashion_news_frequency_lst = customers_df["fashion_news_frequency"].unique().tolist()


    st.sidebar.write("FILTERS")

    age_filtered_lst = st.sidebar.slider(
        'Select a range of ages',
        0, 100, (10, 100))

    st.sidebar.write('Ages range selected:', age_filtered_lst)

    membership_status_filtered_lst = st.sidebar.multiselect(
        label = "Club Membership Status",
        options = membership_status_lst,
        default = membership_status_lst
    )

    st.sidebar.write('Membership statuses selected:', membership_status_filtered_lst)

    fashion_news_frequency_filtered_lst = st.sidebar.multiselect(
        label = "Fashion News Frequency",
        options = fashion_news_frequency_lst,
        default = fashion_news_frequency_lst
    )

    st.sidebar.write('Fashion News Frequencies selected:', fashion_news_frequency_filtered_lst)

    filtered_membership_status_str = ', '.join(
        "'{0}'".format(status) for status in membership_status_filtered_lst)

    if len(filtered_membership_status_str) == 0:
        filtered_membership_status_str = "LIKE '%%'"
    else:
        filtered_membership_status_str = "IN (" + filtered_membership_status_str + ")"

    filtered_fashion_news_frequency_str = ', '.join(
        "'{0}'".format(freq) for freq in fashion_news_frequency_filtered_lst)

    if len(filtered_fashion_news_frequency_str) == 0:
        filtered_fashion_news_frequency_str = "LIKE '%%'"
    else:
        filtered_fashion_news_frequency_str = "IN (" + filtered_fashion_news_frequency_str + ")"

    num_customers = len(merged_data["customer_id"].unique())
    avg_age = np.mean(merged_data["age"])
    num_club_members = len(merged_data[merged_data["club_member_status"] == "Club Member"]["customer_id"].unique())
    avg_articles = merged_data.groupby("customer_id")["article_id"].count().mean()
    total_revenue = merged_data["price"].sum()
    avg_price = merged_data["price"].mean()

    st.write("# KPI Dashboard")

    row1 = st.container()
    row2 = st.container()

    with row1:
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            label="Number of different customers",
            value=num_customers,
            delta=num_customers,
        )

        kpi2.metric(
            label="Average age",
            value=round(avg_age, 2),
            delta=round(-10 + avg_age, 2),
        )

        kpi3.metric(
            label="Number of club members",
            value=num_club_members,
            delta=num_club_members,
        )

    with row2:
        kpi4, kpi5, kpi6 = st.columns(3)

        kpi4.metric(
            label="Average articles per customer",
            value=round(avg_articles, 2),
            delta=round(avg_articles - 5, 2),  # Example delta, adjust as needed
        )

        kpi5.metric(
            label="Total revenue",
            value=f"${total_revenue:,.2f}",
            delta=f"${total_revenue - 100000:,.2f}",  # Example delta, adjust as needed
        )

        kpi6.metric(
            label="Average price of articles sold",
            value=f"${avg_price:.2f}",
            delta=f"${avg_price - 50:.2f}",  # Example delta, adjust as needed
        )


    st.bar_chart(customers_df.groupby(["age"])["customer_id"].count())

    st.write("Age vs Club Member Status")
    fig = px.scatter(customers_df, x="age", y="club_member_status", color="FN", symbol="Active", hover_data=["customer_id"])
    st.plotly_chart(fig)


    sales_channel_lst = transactions_df["sales_channel_id"].unique().tolist()


    # Add sales channel filter to the sidebar
    sales_channel_filtered_lst = st.sidebar.multiselect(
        label = "Sales Channel ID",
        options = sales_channel_lst,
        default = sales_channel_lst
    )

    st.sidebar.write('Sales Channels selected:', sales_channel_filtered_lst)

    # Process the filtered sales channels to create SQL query-compatible strings
    filtered_sales_channel_str = ', '.join(
        "{0}".format(channel) for channel in sales_channel_filtered_lst)

    if len(filtered_sales_channel_str) == 0:
        filtered_sales_channel_str = "LIKE '%%'"
    else:
        filtered_sales_channel_str = "IN (" + filtered_sales_channel_str + ")"


    #merge transactions with customers
    transactions_df = pd.merge(transactions_df, customers_df, on='customer_id', how='left')
    # filter transactions based on age_filtered_lst
    transactions_df = transactions_df[(transactions_df['age'] >= age_filtered_lst[0]) & (transactions_df['age'] <= age_filtered_lst[1])]
    # #filter transactions based on filtered_membership_status_str
    transactions_df = transactions_df[transactions_df['club_member_status'].isin(membership_status_filtered_lst)]
    # #filter transactions based on filtered_fashion_news_frequency_str
    transactions_df = transactions_df[transactions_df['fashion_news_frequency'].isin(fashion_news_frequency_filtered_lst)]
    # #filter transactions based on filtered_sales_channel_str
    transactions_df = transactions_df[transactions_df['sales_channel_id'].isin(sales_channel_filtered_lst)]


    st.write("Sales Channel Distribution. 1=Online, 2=Store")
    sales_channel_distribution = transactions_df.groupby(["sales_channel_id"])["price"].sum().reset_index()
    fig_sales_channel = px.pie(sales_channel_distribution, names="sales_channel_id", values="price")
    st.plotly_chart(fig_sales_channel)
                        
    # from articles filter by product_type_name
    product_type_lst = articles_df["product_type_name"].unique().tolist()
    

    # filter articles by department_name
    department_name_lst = articles_df["department_name"].unique().tolist()

    # filter articles by colour_group_name
    colour_group_name_lst = articles_df["colour_group_name"].unique().tolist()

    # Add filters for product_type_name, department_name, and colour_group_name
    product_type_filtered_lst = st.sidebar.multiselect(
        label="Product Type",
        options=product_type_lst,
        default=product_type_lst
    )

    department_name_filtered_lst = st.sidebar.multiselect(
        label="Department Name",
        options=department_name_lst,
        default=department_name_lst
    )

    colour_group_name_filtered_lst = st.sidebar.multiselect(
        label="Colour Group Name",
        options=colour_group_name_lst,
        default=colour_group_name_lst
    )

    # Construct strings based on the selected filters
    filtered_product_type_str = ', '.join(
        "'{0}'".format(pt) for pt in product_type_filtered_lst)

    if len(filtered_product_type_str) == 0:
        filtered_product_type_str = "LIKE '%%'"
    else:
        filtered_product_type_str = "IN (" + filtered_product_type_str + ")"

    filtered_department_name_str = ', '.join(
        "'{0}'".format(dn) for dn in department_name_filtered_lst)

    if len(filtered_department_name_str) == 0:
        filtered_department_name_str = "LIKE '%%'"
    else:
        filtered_department_name_str = "IN (" + filtered_department_name_str + ")"

    filtered_colour_group_name_str = ', '.join(
        "'{0}'".format(cgn) for cgn in colour_group_name_filtered_lst)

    if len(filtered_colour_group_name_str) == 0:
        filtered_colour_group_name_str = "LIKE '%%'"
    else:
        # filter by articles_df by filtered_product_type_str
        articles_df = articles_df[articles_df['product_type_name'].isin(product_type_filtered_lst)]
        # filter by articles_df by filtered_department_name_str
        articles_df = articles_df[articles_df['department_name'].isin(department_name_filtered_lst)]
        # filter by articles_df by filtered_colour_group_name_str
        articles_df = articles_df[articles_df['colour_group_name'].isin(colour_group_name_filtered_lst)]

    #st.dataframe(articles_df)

    product_type_count_df = articles_df.groupby("product_type_name").size().reset_index(name="count")
    fig1 = px.bar(product_type_count_df, x="product_type_name", y="count", 
                labels={"product_type_name": "Product Type", "count": "Count"})
    st.plotly_chart(fig1)

    department_count_df = articles_df.groupby("department_name").size().reset_index(name="count")
    fig2 = px.bar(department_count_df, x="department_name", y="count", 
                labels={"department_name": "Department", "count": "Count"})
    st.plotly_chart(fig2)

    colour_group_count_df = articles_df.groupby("colour_group_name").size().reset_index(name="count")
    fig3 = px.bar(colour_group_count_df, x="colour_group_name", y="count", 
                labels={"colour_group_name": "Colour Group", "count": "Count"})
    st.plotly_chart(fig3)

    fig4 = px.scatter(articles_df, x="perceived_colour_value_name", y="product_type_name", 
                    color="department_name", hover_data=["prod_name", "colour_group_name"],
                    labels={"perceived_colour_value_name": "Perceived Colour Value",
                            "product_type_name": "Product Type"})
    st.plotly_chart(fig4)
    st.write("this scatter plot provides a visual representation of the relationship between the perceived color value and product type of articles, while also showing information about the department and color group. It allows users to explore the data interactively and discover any patterns or trends that may exist.")

    articles_df['index_code'] = articles_df['index_code'].astype('category')
    fig5 = px.treemap(articles_df, path=["index_group_name", "product_group_name"], values="article_id", color="index_code")
    st.plotly_chart(fig5)
    st.write("The treemap provides a visual representation of the hierarchical structure of the data, with each rectangle representing a combination of index_group_name and product_group_name. The size of the rectangles is proportional to the count of article_id within each group, and the color is determined by the index_code values. This visualization allows users to easily identify patterns and relationships between the different groups of articles.")

    # Streamlit app
    st.title('Customer Transactions and Articles Data')

    # KPIs
    # a. Number of active customers
    active_customers = merged_data['customer_id'].nunique()

    # b. Percentage of customers with club memberships
    club_membership_pct = (merged_data[merged_data['club_member_status'] == 1]['customer_id'].nunique() / active_customers) * 100

    # c. Average age of customers
    average_age = merged_data['age'].mean()

    # d. Average number of articles purchased per customer
    average_articles = merged_data.groupby('customer_id')['article_id'].count().mean()

    # e. Total revenue generated
    total_revenue = merged_data['price'].sum()

    # f. Average price of articles sold
    average_price = merged_data['price'].mean()

    # g. Sales distribution by sales channels
    sales_by_channel = merged_data.groupby('sales_channel_id')['price'].sum()

   # Visualizations

    # a. Age distribution of customers (Histogram)
    fig1, ax1 = plt.subplots()
    ax1.hist(merged_data['age'], bins=20)
    ax1.set(xlabel='Age', ylabel='Frequency', title='Age Distribution of Customers')
    st.pyplot(fig1)

    # b. Club membership status distribution (Bar chart)
    fig2, ax2 = plt.subplots()
    membership_count = merged_data.groupby('club_member_status')['customer_id'].nunique()
    membership_count.plot(kind='bar', ax=ax2)
    ax2.set(xlabel='Club Membership Status', ylabel='Number of Customers', title='Club Membership Status Distribution')
    st.pyplot(fig2)

    # c. Fashion news frequency distribution (Bar chart)
    fig3, ax3 = plt.subplots()
    news_count = merged_data['fashion_news_frequency'].value_counts()
    news_count.plot(kind='bar', ax=ax3)
    ax3.set(xlabel='Fashion News Frequency', ylabel='Number of Customers', title='Fashion News Frequency Distribution')
    st.pyplot(fig3)

    # d. Top 10 most frequently purchased articles (Bar chart)
    fig4, ax4 = plt.subplots()
    top_articles = merged_data['article_id'].value_counts().head(10)
    top_articles.plot(kind='bar', ax=ax4)
    ax4.set(xlabel='Article ID', ylabel='Frequency', title='Top 10 Most Frequently Purchased Articles')
    st.pyplot(fig4)

    # e. Sales over time (Line chart)
    fig5, ax5 = plt.subplots()
    sales_over_time = merged_data.groupby('t_dat')['price'].sum()
    sales_over_time.plot(kind='line', ax=ax5)
    ax5.set(xlabel='Date', ylabel='Sales', title='Sales Over Time')
    st.pyplot(fig5)

    st.title('Additional KPIs')

    # Additional KPIs with Combination of KPIs from the different tables

    # b. Total revenue generated per customer
    revenue_per_customer = merged_data.groupby('customer_id')['price'].sum()
    average_revenue_per_customer = revenue_per_customer.mean()
    st.subheader('Average revenue generated per customer')
    st.markdown(f'**${average_revenue_per_customer:.2f}**')

    # c. Average price of articles sold by sales channel
    average_price_by_channel = merged_data.groupby('sales_channel_id')['price'].mean()
    st.subheader('Average price of articles sold by sales channel')
    st.table(average_price_by_channel.reset_index().rename(columns={'price': 'Average Price'}))


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
