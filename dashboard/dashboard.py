import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



##LOAD DATA
df_day = pd.read_csv('dashboard\day_clean.csv')
df_hour = pd.read_csv('dashboard\hour_clean.csv')



min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()
#SIDEBAR=====
with st.sidebar:
    st.header('Bike Rentals Company')
    st.subheader('Filters')
    date_range = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

main_df_day = df_day[(df_day["dteday"] >= str(start_date)) & 
                (df_day["dteday"] <= str(end_date))]

main_df_hour = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                (df_hour["dteday"] <= str(end_date))]



##MAIN CONTENT====

bike_rented = main_df_day.groupby('instant').agg({
    'cnt' : 'sum',
    'casual' : 'sum',
    'registered' : 'sum'
}).reset_index()

most_rented_season = main_df_day.groupby('season').agg({
    'cnt' : 'sum'
}).reset_index().sort_values(by='cnt', ascending=False).iloc[0]

most_rented_time = main_df_hour.groupby('hr_group').agg({
    'cnt' : 'sum'
}).reset_index().sort_values(by='cnt', ascending=False).iloc[0]

st.title('Bike Rentals Analysis Dashboard:sparkles:')
tab1, tab2 = st.tabs(["Visual", "Data"])

with tab1:
    st.header('Bike Rented (Day)')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Rentals", value=f"{bike_rented['cnt'].sum():,}")
    with col2:
        st.metric(label="Casual Rentals", value=f"{bike_rented['casual'].sum():,}")
    with col3:
        st.metric(label="Registered Rentals", value=f"{bike_rented['registered'].sum():,}")

    st.header('Most Condition Rented')
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Most Rented Season', value=most_rented_season['season'])
    with col2:
        st.metric(label='Most Rented Time of Day', value=most_rented_time['hr_group'])



    st.header('Total Number of Rentals per Season')
    # START
    df_season_sum_day = main_df_day.groupby('season')['cnt'].sum().reset_index()
    df_season_sum_hour = main_df_hour.groupby('season')['cnt'].sum().reset_index()
    df_merged = df_season_sum_day.merge(df_season_sum_hour, on='season', suffixes=('_day', '_hour')).sort_values(by='cnt_day', ascending=False)
    colors = ["#FF4B4B", "#1F77B4"]
    text_color = "#ffff" 

    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.4 

    x = np.arange(len(df_merged['season']))

    ax.bar(x - width/2, df_merged['cnt_day'], width=width, label='Daily Rentals', color=colors[0], alpha=0.85)
    ax.bar(x + width/2, df_merged['cnt_hour'], width=width, label='Hourly Rentals', color=colors[1], alpha=0.85)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticks(x)
    ax.set_xticklabels(df_merged['season'], rotation=45, fontsize=12, color=text_color)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))  # Format angka
    ax.tick_params(axis='y', colors=text_color)  # Change y-axis tick color

    sns.despine(left=True, bottom=True)
    ax.legend(frameon=False, fontsize=12, facecolor='white', edgecolor='white', labelcolor=text_color, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    st.pyplot(fig, transparent=True)
    #END

    st.title("Average Bike Rentals per Weather Condition")
    #START
    st.subheader('Daily Data')
    palette = ["#8B0000", "#FF4B4B", "#FF4B4B"]
    fig, ax = plt.subplots(figsize=(10, 6))

    df_day_weather_mean = main_df_day.groupby('weathersit').agg({'cnt': 'mean'}).reset_index().sort_values(by='cnt',ascending=False)

    sns.barplot(x="weathersit", y="cnt", data=df_day_weather_mean, palette=palette, ax=ax)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis='x', rotation=0)
    ax.tick_params(axis='y', colors=text_color)
    ax.tick_params(axis='x', colors=text_color)

    st.pyplot(fig, transparent=True)
    #END

    #START
    st.subheader('Hourly Data')
    palette = ["#8B0000", "#FF4B4B", "#FF4B4B"]
    fig, ax = plt.subplots(figsize=(10, 6))

    df_hour_weather_mean = main_df_hour.groupby('weathersit').agg({'cnt': 'mean'}).reset_index().sort_values(by='cnt',ascending=False)

    sns.barplot(x="weathersit", y="cnt", data=df_hour_weather_mean, palette=palette, ax=ax)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis='x', rotation=0)
    ax.tick_params(axis='y', colors=text_color)
    ax.tick_params(axis='x', colors=text_color)

    st.pyplot(fig, transparent=True)
    #END

    st.title('Hourly Bicycle Rental Pattern in a Day')

    #START
    df_hour_filter = df_hour[df_hour['dteday'] == min_date]

    # Create figure and plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=df_hour_filter, marker='o', linewidth=2)
    plt.xlabel('Hour (0-23)', fontsize=12, color=text_color)
    plt.ylabel('Number of Rentals', fontsize=12, color=text_color)
    plt.xticks(range(0, 24))
    plt.tick_params(axis='x',colors=text_color)
    plt.tick_params(axis='y',colors=text_color)
    plt.grid(False)

    # Display plot in Streamlit with the title
    st.pyplot(plt, transparent=True)
    st.caption(f'Hourly Bike Rental Patterns for the Day ({start_date})')
    #END

    st.title("Total Bike Rentals per Time of Day")
    #START
    palette = ["#8B0000", "#FF4B4B", "#FF4B4B", "#FF4B4B"]
    df_hour_group_sum = main_df_hour.groupby(by='hr_group')['cnt'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    df_hour_group_sum.plot(kind='bar', ax=ax, color=palette)
    time_ranges = {
        'Midnight': 'Midnight (0-6)',
        'Morning': 'Morning (6-12)',
        'Noon': 'Noon (12-18)',
        'Afternoon': 'Afternoon (18-24)'
    }
    ax.set_xticklabels([time_ranges[label.get_text()] for label in ax.get_xticklabels()])

    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))


    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', colors=text_color)
    ax.tick_params(axis='x', colors=text_color)

    fig.tight_layout()

    st.pyplot(fig, transparent = True)
    #END

    st.title("Average Bike Rentals per Hour")
    #START

    hourly_rentals = main_df_hour.groupby('hr')['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(x='hr', y='cnt', data=hourly_rentals, palette=colors, ax=ax)

    sns.lineplot(x='hr', y='cnt', data=hourly_rentals, color='#1F4E79', marker='o', linewidth=2, ax=ax)

    max_rental = hourly_rentals['cnt'].max()
    max_hour = hourly_rentals.loc[hourly_rentals['cnt'] == max_rental, 'hr'].values[0]

    ax.set_xlabel('Hour (24-hour format)', fontsize=12,color=text_color)
    ax.set_ylabel('Average Rentals', fontsize=12, color=text_color)

    ax.set_xticks(hourly_rentals['hr'])
    ax.set_xticklabels(hourly_rentals['hr'], rotation=0)

    ax.grid(axis='y', linestyle='--', alpha=0.7)

    ax.tick_params(axis='y', colors=text_color)
    ax.tick_params(axis='x', colors=text_color)


    st.pyplot(fig, transparent = True)





 

with tab2:
    st.title('Data per Hari')
    st.dataframe(main_df_day)

    st.title('Data per Jam')
    st.dataframe(main_df_hour)
