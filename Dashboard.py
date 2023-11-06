#Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np



#Define Main Helper Function (Affected by filter)
#Counting Total Bike Sharing User 
def Create_daily_User_Total_df(df):
    daily_user_df = df.groupby(by='dteday').cnt_y.sum().reset_index()
    daily_user_df.rename(columns={
        "cnt_y": "Total_User"
    }, inplace=True)
    return daily_user_df

#Counting Total Unregistered Bike Sharing User
def Create_daily_casual_Total_df(df):
    daily_casual_df = df.groupby(by='dteday').casual_y.sum().reset_index()
    daily_casual_df.rename(columns={
        "casual_y": "Total_Unregistered_User"
    }, inplace=True)
    return daily_casual_df

#Counting Total Registered Bike Sharing User
def Create_daily_registered_Total_df(df):
    daily_registered_df = df.groupby(by='dteday').registered_y.sum().reset_index()
    daily_registered_df.rename(columns={
        "registered_y": "Total_Registered_User"
    }, inplace=True)
    return daily_registered_df

#Define Summary Helper Function (Doesn't affected by filter)
#Counting Total Bike Sharing User in 2011
#According to Month 
def create_Y2011_Mnth_Pivot_df(df):
    Y2011_df = df.query('yr == 0')
    Y2011_Mnth_Pivot_df = Y2011_df.groupby(by=['yr',"mnth"]).cnt_y.sum().reset_index()
    return Y2011_Mnth_Pivot_df

#According to Season 
def create_Y2011_Season_df(df):
    Y2011_df = df.query('yr == 0')
    Y2011_Season_df = Y2011_df.groupby(by=['yr','season']).cnt_y.sum().reset_index()
    return Y2011_Season_df

#Counting Total Bike Sharing User in 2012
#According to Month 
def create_Y2012_Mnth_Pivot_df(df):
    Y2012_df = df.query('yr == 1')
    Y2012_Mnth_Pivot_df = Y2012_df.groupby(by=['yr',"mnth"]).cnt_y.sum().reset_index()
    return Y2012_Mnth_Pivot_df

#According to Season
def create_Y2012_Season_df(df):
    Y2012_df = df.query('yr == 1')
    Y2012_Season_df = Y2012_df.groupby(by=['yr','season']).cnt_y.sum().reset_index()
    return Y2012_Season_df

#Defining Data Source Used
all_df = pd.read_csv("all_data.csv")
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

#Creating filter for Main Helper Function
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min() #Defining when data starts
max_date = all_df["dteday"].max() #Defining when data ends

#A little user interface
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://www.sefiles.net/images/library/zoom/se-bikes-wildman-388830-17.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#Stating Main and Summary Function
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]
sum_df = all_df

#List of main and summary helper function 
daily_user_df = Create_daily_User_Total_df(main_df)
daily_casual_df = Create_daily_casual_Total_df(main_df)
daily_registered_df = Create_daily_registered_Total_df(main_df)
Y2011_Mnth_Pivot_df = create_Y2011_Mnth_Pivot_df(sum_df)
Y2011_Season_df = create_Y2011_Season_df(sum_df)
Y2012_Mnth_Pivot_df = create_Y2012_Mnth_Pivot_df(sum_df)
Y2012_Season_df = create_Y2012_Season_df(sum_df)

#Dashboard
st.header('Dicoding Bike Sharing Corporation Dashboard :sparkles:')

#1st Section, Daily summary which can be change by Dashboard User
st.subheader('Daily Orders')

#Showing Total (Accumulated) Bike Sharing User according to filtered period
col1, col2, col3 = st.columns(3)
with col1:
    total_user = daily_user_df.Total_User.sum()
    st.metric("Total Users", value=total_user)
with col2:
    total_registered_user = daily_registered_df.Total_Registered_User.sum()
    st.metric("Registered", value=total_registered_user)
with col3:
    total_unregistered_user = daily_casual_df.Total_Unregistered_User.sum()
    st.metric("Unregistered", value=total_unregistered_user)

#Defining data source used to show comparison of registered and unregistered user
fig, ax = plt.subplots(figsize=(5,1))
registered = daily_registered_df.Total_Registered_User.sum()
unregistered = daily_casual_df.Total_Unregistered_User.sum()
total = daily_user_df.Total_User.sum()
raw_data = {'registered': [daily_registered_df.Total_Registered_User.sum()],'unregistered': [daily_casual_df.Total_Unregistered_User.sum()]}
df1 = pd.DataFrame(raw_data)

#Turning datas into percentage
totals = [i+j for i,j in zip(df1['registered'],df1['unregistered'])]
regist_plot = [i/j*100 for i,j in zip(df1['registered'],totals)] 
unregist_plot = [i/j*100 for i,j in zip(df1['unregistered'],totals)] 

#Bar Chart Customization
BarHeight = 1
names = ('Comparison')
ax.barh(1,regist_plot, color='red',edgecolor='white',height=BarHeight)
ax.barh(1, unregist_plot,left=regist_plot,color='blue',edgecolor='white',height=BarHeight)
ax.set_xticks([0,25,50,75,100])
ax.set_yticks([])
ax.legend(['Registered', 'Unregistered'],fontsize=5)
ax.set_title("Total Registered vs Unregistered Users (%)", loc="center", fontsize=10)
st.pyplot(fig)

#Bar Chart Showing Total (Daily) Bike Sharing Users from filtered period 
fig, ax = plt.subplots(figsize=(16, 10))
ax.plot(
    daily_user_df["dteday"],
    daily_user_df["Total_User"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation = 20)
st.pyplot(fig)

#2nd Section, Summary of Bike Sharing Usage from 2011 to 2012 by Months
st.subheader("Bike Sharing Performance in 2011 and 2012")
fig,ax = plt.subplots(figsize=(12, 10))

#Creating 2 ax.plot so it will superimposed each other
ax.plot(
    Y2011_Mnth_Pivot_df["mnth"],
    Y2011_Mnth_Pivot_df["cnt_y"],
    marker='o', 
    linewidth=2,
    color="Blue"
)
ax.plot(
    Y2012_Mnth_Pivot_df["mnth"],
    Y2012_Mnth_Pivot_df["cnt_y"],
    marker='x',
    linewidth=2,
    color="red"
)

#Chart Customization
ax.set_xlabel("Months")
ax.set_ylabel("Total Users")
ax.set_xticks(np.arange(1, 13, step=1))
ax.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12,13], ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', ''],
       rotation=20)
ax.legend(['Year 2011', 'Year 2012'])
ax.set_title("Bike Sharing 2011 VS 2012", loc="center", fontsize=20)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)


#3rd Section, Summary of Bike Sharing Usage from 2011 to 2012 by Season
st.subheader("Bike Sharing Performance Differ by Seasons")


x = Y2011_Season_df["season"]
width = 0.35
fig, ax = plt.subplots(figsize=(8, 7))

#Creating 2 Bar Chart side to side
Y2011 = ax.bar(x - width/2, Y2011_Season_df["cnt_y"], width, label='Year 2011', color='blue')
Y2012 = ax.bar(x + width/2, Y2012_Season_df["cnt_y"], width, label='Year 2012', color='red')

ax.set_title("Bike Sharing by Seasons", loc="center", fontsize=20)
ax.set_ylabel("Total Users")
ax.set_xlabel("Season")
ax.set_xticks(np.arange(1, 5, step=1))
ax.legend(fontsize=12)
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'],
       rotation=20)
st.pyplot(fig)



