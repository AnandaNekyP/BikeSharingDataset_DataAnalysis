import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

day_data = pd.read_csv("dashboard/main_data_day.csv")
hour_data = pd.read_csv("dashboard/main_data_hour.csv")

st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Select Analysis", ["Seasonal Analysis", "Monthly Analysis", "Weekly Analysis", "Hourly Analysis", "Cluster Analysis", "Anomalies"])

def cluster_count(x, max_value):
    if x < (max_value / 3):
        return 'Low'
    elif (max_value / 3) <= x < (max_value / 2):
        return 'Medium'
    elif (max_value / 2) <= x <= max_value:
        return 'High'
    else:
        return 'Out of Range'

if selected_page == "Seasonal Analysis":
    st.title("Optimal Seasonal Rental Conditions by Weather")
    
    date_range = st.sidebar.date_input("Select Date Range", [pd.to_datetime('2011-01-01'), pd.to_datetime('2012-12-31')])
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_day_data = day_data[(pd.to_datetime(day_data['date']) >= start_date) & (pd.to_datetime(day_data['date']) <= end_date)]
    
    average_day_conditions = filtered_day_data.groupby(['date', 'season', 'month', 'weekday', 'weathersit'])['total_rentals'].mean().reset_index()
    optimal_day_conditions = average_day_conditions.sort_values(by='total_rentals', ascending=False)
    
    weather_filter = st.sidebar.multiselect("Filter by Weather", options=optimal_day_conditions['weathersit'].unique())
    if weather_filter:
        optimal_day_conditions = optimal_day_conditions[optimal_day_conditions['weathersit'].isin(weather_filter)]
    
    st.subheader("Rental Conditions by Season and Weather")
    fig = plt.figure(figsize=(6, 6))
    sns.boxplot(x='season', y='total_rentals', hue='weathersit', data=optimal_day_conditions, palette='Set2')
    plt.title('Optimal Daily Rental Conditions')
    plt.xlabel('Season')
    plt.ylabel('Total Rentals')
    st.pyplot(fig)

if selected_page == "Monthly Analysis":
    st.title("Optimal Monthly Rental Conditions by Weather")
    
    date_range = st.sidebar.date_input("Select Date Range", [pd.to_datetime('2011-01-01'), pd.to_datetime('2012-12-31')])
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_day_data = day_data[(pd.to_datetime(day_data['date']) >= start_date) & (pd.to_datetime(day_data['date']) <= end_date)]
    
    average_day_conditions = filtered_day_data.groupby(['date', 'season', 'month', 'weekday', 'weathersit'])['total_rentals'].mean().reset_index()
    optimal_day_conditions = average_day_conditions.sort_values(by='total_rentals', ascending=False)
    
    weather_filter = st.sidebar.multiselect("Filter by Weather", options=optimal_day_conditions['weathersit'].unique())
    if weather_filter:
        optimal_day_conditions = optimal_day_conditions[optimal_day_conditions['weathersit'].isin(weather_filter)]
    
    st.subheader("Rental Conditions by Month and Weather")
    fig = plt.figure(figsize=(16, 6))
    sns.boxplot(x='month', y='total_rentals', hue='weathersit', data=optimal_day_conditions, palette='Set2')
    plt.title('Optimal Monthly Rental Conditions')
    plt.xlabel('Month')
    plt.ylabel('Total Rentals')
    st.pyplot(fig)

if selected_page == "Weekly Analysis":
    st.title("Optimal Weekly Rental Conditions by Weather")
    
    date_range = st.sidebar.date_input("Select Date Range", [pd.to_datetime('2011-01-01'), pd.to_datetime('2012-12-31')])
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_day_data = day_data[(pd.to_datetime(day_data['date']) >= start_date) & (pd.to_datetime(day_data['date']) <= end_date)]
    
    average_day_conditions = filtered_day_data.groupby(['date', 'season', 'month', 'weekday', 'weathersit'])['total_rentals'].mean().reset_index()
    optimal_day_conditions = average_day_conditions.sort_values(by='total_rentals', ascending=False)
    
    weather_filter = st.sidebar.multiselect("Filter by Weather", options=optimal_day_conditions['weathersit'].unique())
    if weather_filter:
        optimal_day_conditions = optimal_day_conditions[optimal_day_conditions['weathersit'].isin(weather_filter)]
    
    st.subheader("Rental Conditions by Weekday and Weather")
    fig = plt.figure(figsize=(9, 6))
    sns.boxplot(x='weekday', y='total_rentals', hue='weathersit', data=optimal_day_conditions, palette='Set2')
    plt.title('Optimal Weekly Rental Conditions')
    plt.xlabel('Weekday')
    plt.ylabel('Total Rentals')
    st.pyplot(fig)

elif selected_page == "Hourly Analysis":
    st.title("Optimal Hourly Rental Conditions by Weather")
    
    date_range = st.sidebar.date_input("Select Date Range", [pd.to_datetime('2011-01-01'), pd.to_datetime('2012-12-31')])
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_hour_data = hour_data[(pd.to_datetime(hour_data['date']) >= start_date) & (pd.to_datetime(hour_data['date']) <= end_date)]
    
    average_hour_conditions = filtered_hour_data.groupby(['date', 'season', 'month', 'hour', 'weekday', 'weathersit'])['total_rentals'].mean().reset_index()
    optimal_hour_conditions = average_hour_conditions.sort_values(by='total_rentals', ascending=False)
    
    weather_filter = st.sidebar.multiselect("Filter by Weather", options=optimal_hour_conditions['weathersit'].unique())
    if weather_filter:
        optimal_hour_conditions = optimal_hour_conditions[optimal_hour_conditions['weathersit'].isin(weather_filter)]
    
    st.subheader("Rental Conditions by Hour and Weather")
    fig = plt.figure(figsize=(18, 6))
    sns.barplot(x='hour', y='total_rentals', hue='weathersit', data=optimal_hour_conditions, palette='Set2')
    plt.title('Optimal Hourly Rental Conditions')
    plt.xlabel('Hour')
    plt.ylabel('Total Rentals')
    st.pyplot(fig)

elif selected_page == "Cluster Analysis":
    st.title("Rental Clustering")
    
    min_threshold = st.sidebar.slider("Min Rental Threshold", min_value=0, max_value=int(day_data['total_rentals'].max()), value=0)
    max_threshold = st.sidebar.slider("Max Rental Threshold", min_value=0, max_value=int(day_data['total_rentals'].max()), value=int(day_data['total_rentals'].max()))
    
    max_value = day_data['total_rentals'].max()
    day_data['Cluster'] = day_data['total_rentals'].apply(lambda x: cluster_count(x, max_value))
    
    filtered_cluster_data = day_data[(day_data['total_rentals'] >= min_threshold) & (day_data['total_rentals'] <= max_threshold)]
    
    st.subheader("Distribution of Rental Clusters")
    cluster_counts = filtered_cluster_data['Cluster'].value_counts()
    fig = plt.figure(figsize=(8, 6))
    cluster_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribution of Bike Rental Clusters')
    plt.xlabel('Cluster')
    plt.ylabel('Count')
    st.pyplot(fig)

elif selected_page == "Anomalies":
    st.title("Rental Anomalies")
    
    anomaly_week = day_data[(pd.to_datetime(day_data['date']) >= '2012-10-28') & (pd.to_datetime(day_data['date']) <= '2012-11-03')]
    
    average_day_conditions = anomaly_week.groupby(['date', 'season', 'month', 'weekday', 'weathersit'])['total_rentals'].mean().reset_index()
    anomaly_day_conditions = average_day_conditions.sort_values(by='date')
    
    st.subheader("Low Rental Anomaly")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='date', y='total_rentals', hue='weathersit', data=anomaly_day_conditions, palette='Set1', ax=ax)
    ax.set_title('Low Rental Day Anomaly')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rental Count')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)


