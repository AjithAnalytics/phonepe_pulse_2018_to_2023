import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import numpy as np
import mysql.connector
from sqlalchemy import create_engine

#number conversion
def Number_Conversion(number):
    if number // 10**7:
        number = f'{round(number / 10**7,2)} Crores'
    elif number // 10**5:
        number = f'{round(number / 10**5,2)} Lakhs'
    elif number // 10**3:
        number = f'{round(number / 10**3,2)} K'
    return number

def display_dashboard():
  # sets the padding around the content in the app to zero
  padding = 0
  # is a method from the Streamlit library that allows the user to set various page-level options for the app
  st.set_page_config(page_title="PhonePe Pulse", layout="wide", page_icon="₹")
  
  # setting page title

  with st.sidebar:
    
    selected = option_menu(
    menu_title = "Welcome to PhonePe Pulse Dashboard",  
    options = ['India state-wise Data','India district-wise Data'],
    default_index=0
    )
    # getting the inputs from user
  if selected == 'India state-wise Data':
    YEAR = ['2018','2019','2020','2021','2022','2023']
    year = st.sidebar.selectbox("Select a year:",YEAR)
    QUARTER = ['1','2','3','4']
    quarter = st.sidebar.selectbox("Select Quarter:",QUARTER)

  # with st.sidebar:
    selected = option_menu(
        menu_title = "Geo Visualization",
        options = ['Transaction','User'],
        icons = ['wallet','people'],
        menu_icon = 'geo-alt',
        default_index=0
      )
    
    if selected == "Transaction":
      with st.container():
        # MySQL database connection
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phonepe"
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("USE phonepe")
        mydb.commit()

        # Assuming 'mydb' is a MySQL database connection
        # Convert it to an SQLAlchemy engine
        engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/phonepe')

        # Define the SQL query using parameters to prevent SQL injection
        sql = f"SELECT * FROM aggregated_transaction WHERE year={year} AND Quarter={quarter}"

        # Read data using pandas.read_sql and the SQLAlchemy engine
        aggregated_transaction = pd.read_sql(sql, con=engine)

        india_map = aggregated_transaction[['state', 'Transaction_amount','Transaction_count']].groupby(['state']).sum().reset_index()

        fig = px.choropleth(india_map,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='state',
                        color='Transaction_amount',
                        hover_data=['state','Transaction_count','Transaction_amount'],
                        projection="robinson",
                        color_continuous_scale='YlGnBu')
        fig.update_geos(fitbounds = 'locations',visible = False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # Display the map in the Streamlit app
        st.plotly_chart(fig,theme="streamlit",use_container_width=True)

        mycursor.execute(f"""SELECT g.Transaction_type, g.Total_Amount, g.Total_Count,  round((g.Total_Amount / g.Total_Count),2) as Average_Transaction
                                FROM (SELECT Transaction_type, sum(Transaction_amount)as Total_Amount, sum(Transaction_Count) as Total_Count FROM aggregated_transaction 
                                WHERE year = {year} AND Quarter = {quarter} GROUP BY Transaction_type) as g;""")
        data = mycursor.fetchall()
        df1=pd.DataFrame(data, columns = [i[0] for i in mycursor.description])

        st.sidebar.markdown('#### :green [All PhonePe transactions]' )
        st.sidebar.markdown(':green[(UPI + Cards + Wallets)]')
        totalTransactioncount=df1['Total_Count'].sum()
        st.sidebar.markdown(f'## :red[{ totalTransactioncount}]')

        st.sidebar.markdown('#### :blue[***Total payment value***]')
        totalTransactionamount=df1['Total_Amount'].sum()
        st.sidebar.markdown(f'#### :red[{Number_Conversion(totalTransactionamount)}]')

        st.sidebar.markdown('#### :green[***Avg. transaction value***]')
        # average=totalamount//totalcount
        average= df1['Average_Transaction'].mean()
        st.sidebar.markdown(f'### :red[{round(average)}]')
        # st.write(average) 


        st.table(df1)   
        col1, col2 = st.columns([2,2])  # Adjust the size ratios here
        with col1:
            fig1 = px.bar(df1, y='Total_Count', x='Transaction_type', title=f"Year:{year}-Q{quarter} wise Transaction Count", color='Transaction_type')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.bar(df1, y='Total_Amount', x='Transaction_type', title=f"Year:{year}-Q{quarter} wise Transaction Amount", color='Transaction_type')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('#### :green[***Top 10 Transaction_Count & Transaction_Amount***]')
        col3, col4, col5 = st.columns([1, 1, 2])

        with col3:
          st.markdown('<span style="color: blue; font-size:12px">Select State</span>', unsafe_allow_html=True)
          Tran_state= st.button('State', key='btn_state')
        with col4:
          st.markdown('<span style="color: green; font-size:12px">Select District</span>', unsafe_allow_html=True)
          Tran_district= st.button('District', key='btn_district')
        with col5:
          st.markdown('<span style="color: purple; font-size:12px">Select Postal Code</span>', unsafe_allow_html=True)
          Tran_pincode= st.button('Postal Code', key='btn_pincode')

        if Tran_state:
          col6, col7 = st.columns([2,2]) 
          with col6:
            sql1=(f"""SELECT state, Transaction_count, Transaction_amount FROM top_trans_district
                            WHERE year = {year} AND Quarter = {quarter}
                        ORDER BY Transaction_count desc limit 10;""")
          
            # Read data using pandas.read_sql and the SQLAlchemy engine
            data= pd.read_sql(sql1, con=engine)
            fig3 = px.bar(data, x = 'state', y = 'Transaction_count', text = 'Transaction_count', color = 'Transaction_count',
            color_continuous_scale = 'YlGnBu', title = f'year{year} & Q{quarter} Top 10 State Transaction Count Analysis', height = 600)
            st.plotly_chart(fig3,use_container_width=True)
          with col7:
            fig4= px.bar(data, x = 'state', y = 'Transaction_amount', text = 'Transaction_amount', color = 'Transaction_amount',
            color_continuous_scale = 'thermal', title = f'year{year} & Q{quarter} Top 10 State Transaction Amount Analysis', height = 600)
            st.plotly_chart(fig4,use_container_width=True)

        elif Tran_district:
          col8, col9 = st.columns([2,2]) 
          with col8: 
            sql2=(f"""SELECT top10.District, top10.Total_Transaction_Count,top10.Total_Transaction_amount
                        FROM (
                            SELECT District, SUM(Transaction_count) as Total_Transaction_Count,SUM(Transaction_amount) as Total_Transaction_amount
                            FROM top_trans_district
                            WHERE year = {year} AND Quarter = {quarter}
                            GROUP BY District
                        ) as top10
                        ORDER BY top10.Total_Transaction_Count desc , top10.Total_Transaction_amount desc limit 10;""")
            data1= pd.read_sql(sql2, con=engine)
            data1['Total_Transaction_Count'] = data1['Total_Transaction_Count'].astype(int)
            data1['Total_Transaction_amount']= data1['Total_Transaction_amount'].astype(float)
            fig5 = px.bar(data1, x = 'District', y = 'Total_Transaction_Count', text = 'Total_Transaction_Count', color = 'Total_Transaction_Count',
            color_continuous_scale = 'Viridis', title = f'year{year} & Q{quarter} Top 10 District Transaction Count Analysis', height = 600)
            st.plotly_chart(fig5,use_container_width=True)
          with col9:
            fig6= px.bar(data1, x = 'District', y = 'Total_Transaction_amount', text = 'Total_Transaction_amount', color = 'Total_Transaction_amount',
            color_continuous_scale ='Inferno', title = f'year{year} & Q{quarter} Top 10 District Transaction Amount Analysis', height = 600)
            st.plotly_chart(fig6,use_container_width=True)

        elif Tran_pincode:
          col10, col11 = st.columns([2,2]) 
          with col10:
            sql3=(f"""SELECT Pincode, Transaction_count,Transaction_amount
                    FROM top_trans_pincode
                    WHERE year = {year} AND Quarter = {quarter}
                    ORDER BY Transaction_count,Transaction_amount DESC LIMIT 10;""")
            data2= pd.read_sql(sql3, con=engine)
            data2['Pincode'] = data2['Pincode'].astype(str)
            data2['Pincode'] = data2['Pincode']+'-'
            fig7= px.bar(data2, x ='Pincode', y = 'Transaction_count', text = 'Transaction_count', color = 'Transaction_count',
                color_continuous_scale = 'Greens', title = f'year{year} & Q{quarter} Top 10 Pincode Transaction Count Analysis', height = 600)
            st.plotly_chart(fig7,use_container_width=True)
          with col11:
            fig8= px.bar(data2, x ='Pincode', y = 'Transaction_amount', text = 'Transaction_amount', color = 'Transaction_amount',
                color_continuous_scale = 'Teal', title = f'year{year} & Q{quarter} Top 10 Pincode Transaction amount Analysis', height = 600)
            st.plotly_chart(fig8,use_container_width=True)
        
        else:
          col6, col7 = st.columns([2,2]) 
          with col6:
            sql1=(f"""SELECT state, Transaction_count, Transaction_amount FROM top_trans_district
                            WHERE year = {year} AND Quarter = {quarter}
                        ORDER BY Transaction_count desc limit 10;""")
          
            # Read data using pandas.read_sql and the SQLAlchemy engine
            data= pd.read_sql(sql1, con=engine)
            fig3 = px.bar(data, x = 'state', y = 'Transaction_count', text = 'Transaction_count', color = 'Transaction_count',
            color_continuous_scale = 'YlGnBu', title = f'year{year} & Q{quarter} Top 10 State Transaction Count Analysis', height = 600)
            st.plotly_chart(fig3,use_container_width=True)
          with col7:
            fig4= px.bar(data, x = 'state', y = 'Transaction_amount', text = 'Transaction_amount', color = 'Transaction_amount',
            color_continuous_scale = 'thermal', title = f'year{year} & Q{quarter} Top 10 State Transaction Amount Analysis', height = 600)
            st.plotly_chart(fig4,use_container_width=True)

    if selected == "User":
      with st.container():
         # MySQL database connection
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phonepe"
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("USE phonepe")
        mydb.commit()

        # Assuming 'mydb' is a MySQL database connection
        # Convert it to an SQLAlchemy engine
        engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/phonepe')
    
        sql=f"""SELECT State, sum(Registered_user) as Registered_PhonePe_Users, sum(App_opens) as PhonePe_App_Opens FROM map_user 
                                 WHERE Year = {year} AND Quarter = {quarter} GROUP BY State ORDER BY State;"""
        data= pd.read_sql(sql, con=engine)
        data['Registered_PhonePe_Users'] = data['Registered_PhonePe_Users'].astype(str).str.replace(r'\D', '', regex=True).astype(int)

        fig = px.choropleth(data,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Registered_PhonePe_Users',
                        hover_data=['State', 'PhonePe_App_Opens'],
                        projection="robinson",
                        color_continuous_scale='Plasma')
        fig.update_geos(fitbounds = 'locations',visible = False )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
      
        # Display the map in the Streamlit app
        st.plotly_chart(fig,theme="streamlit",use_container_width=True)
        
        st.sidebar.markdown(f'##### :green[***Registered PhonePe users year{year} & Q{quarter}***]')
        Registered_count=data['Registered_PhonePe_Users'].sum()
        st.sidebar.markdown(Registered_count)
        st.sidebar.markdown(f'##### :green[***PhonePe app opens in year{year} & Q{quarter} ***]')
        appo_pens=data['PhonePe_App_Opens'].sum()
        st.sidebar.markdown(f':Red {Number_Conversion(appo_pens)}')

        st.header(f':green[***Year [{year} & Q{quarter}] Brand  users Analysis ***]')
        sql2=(f"""SELECT g.Brands, g.Total_User_Count
                                FROM (SELECT Brands, sum(Count) as Total_User_Count FROM agg_user 
                                WHERE Year = {year} AND Quarter = {quarter} GROUP BY Brands) as g
                                ORDER BY Total_User_Count DESC LIMIT 10;""")
        data2= pd.read_sql(sql2, con=engine) 
        col1, col2= st.columns([1,2]) 
        with col1:
          st.table(data2)
        with col2:
          #pi chart
          fig2 = px.pie(data2, values='Total_User_Count', names='Brands',
             #title=f'Top 10 Brands based on User Count for year {year} & Q{quarter}')
              color_discrete_sequence=px.colors.sequential.Plasma)
          st.plotly_chart(fig2, use_container_width=True)

        st.header(':green[***Top 10  User Analysis***]')
        col1,col2,col3 =st.columns([1,1,1])
        with col1:
          st.markdown('<span style="color: blue; font-size:12px">Select State</span>', unsafe_allow_html=True)
          Trans_state= st.button('State', key='btn_state')
        with col2:
          st.markdown('<span style="color: green; font-size:12px">Select District</span>', unsafe_allow_html=True)
          Trans_district= st.button('District', key='btn_district')
        with col3:
          st.markdown('<span style="color: purple; font-size:12px">Select Postal Code</span>', unsafe_allow_html=True)
          Trans_pincode= st.button('Pin Code', key='btn_pincode')

        if  Trans_state:
          # Execute SQL and read the data into a DataFrame
          sql3 = f"""SELECT State, sum(Registered_users) as Registered_users_sum FROM top_user_district
              WHERE Year = {year} AND Quarter = {quarter}
              GROUP BY State
              ORDER BY Registered_users_sum DESC
              LIMIT 10;"""

          data3 = pd.read_sql(sql3, con=engine)
          #data3['Registered_users_sum']=data3['Registered_users_sum'].apply(Number_Conversion)
          fig3 = px.bar(data3, x='State', y='Registered_users_sum', text='Registered_users_sum', color='Registered_users_sum',
              color_continuous_scale='Plasma', title=f'year {year} & Q{quarter} Top 10 State users Count Analysis', height=600)
          st.plotly_chart(fig3, use_container_width=True)

        elif Trans_district:
          sql4=(f"""SELECT District, sum(Registered_users) as Registered_user FROM top_user_district 
                                 WHERE Year = {year} AND Quarter = {quarter} GROUP BY District ORDER BY Registered_users DESC LIMIT 10;""")
          data4=pd.read_sql(sql4, con=engine)
          data4['Registered_user']=data4['Registered_user'].apply(Number_Conversion)

          fig4 = px.bar(data4, x='District', y='Registered_user', text='Registered_user', color='Registered_user',
          title=f'year {year} & Q{quarter} Top 10 District users Count Analysis', height=600)
          st.plotly_chart(fig4, use_container_width=True)

        elif Trans_pincode:
          sql5=(f"""SELECT Pincode, Registered_users FROM top_user_pincode
                                 WHERE Year = {year} AND Quarter = {quarter} ORDER BY Registered_users DESC LIMIT 10;""")
          data5=pd.read_sql(sql5, con=engine)
          data5['Pincode'] = data5['Pincode'].astype(str)
          data5['Pincode'] = data5['Pincode']+'-'

          fig5= px.bar(data5, x='Pincode', y='Registered_users', text='Registered_users', color='Registered_users',
          color_continuous_scale='YlGnBu_r',title=f'year {year} & Q{quarter} Top 10 Pincode users Count Analysis', height=600)
          st.plotly_chart(fig5, use_container_width=True)

        else:
          # Execute SQL and read the data into a DataFrame
          sql3 = f"""SELECT State, sum(Registered_users) as Registered_users_sum FROM top_user_district
              WHERE Year = {year} AND Quarter = {quarter}
              GROUP BY State
              ORDER BY Registered_users_sum DESC
              LIMIT 10;"""

          data3 = pd.read_sql(sql3, con=engine)
          #data3['Registered_users_sum']=data3['Registered_users_sum'].apply(Number_Conversion)
          fig3 = px.bar(data3, x='State', y='Registered_users_sum', text='Registered_users_sum', color='Registered_users_sum',
              color_continuous_scale='Plasma', title=f'year {year} & Q{quarter} Top 10 State users Count Analysis', height=600)
          st.plotly_chart(fig3, use_container_width=True)

  #district wise analisys
  if selected == 'India district-wise Data':
    STATE=["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam",
    "Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh",
    "Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh",
    "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan",
    "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
    
    state = st.sidebar.selectbox("Select a state:",STATE)
    YEAR = ['2018','2019','2020','2021','2022','2023']
    year = st.sidebar.selectbox("Select a year:",YEAR)
    QUARTER = ['1','2','3','4']
    quarter = st.sidebar.selectbox("Select Quarter:",QUARTER)

    selected = option_menu(
        menu_title = "Geo Visualization",
        options = ['Transaction','User'],
        icons = ['wallet','people'],
        menu_icon = 'geo-alt',
        default_index=0
      )
    if selected == 'Transaction':
      with st.container():
           # MySQL database connection
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phonepe"
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("USE phonepe")
        mydb.commit()

        # Assuming 'mydb' is a MySQL database connection
        # Convert it to an SQLAlchemy engine
        engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/phonepe')

    
        sql = f"""SELECT State, District, sum(Count) as Total_trans_count, sum(Amount) as Total_trans_amount
            FROM map_trans
            WHERE Year={year} AND Quarter={quarter} AND State='{state}'
            GROUP BY District ORDER BY District"""
        data = pd.read_sql(sql, con=engine)
    
        # Choropleth map for the specific state
        fig = px.choropleth(data,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_trans_amount',
                    hover_data=['State', 'Total_trans_count'],
                    projection="robinson",
                    color_continuous_scale='Rainbow')
        fig.update_geos(fitbounds='locations', visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
        # Bar chart for the districts of the selected state
        data = data.sort_values(by='Total_trans_amount', ascending=False).reset_index(drop=True)
        fig = px.bar(data, x='District', y='Total_trans_amount', color_continuous_scale='Plasma',hover_data=['Total_trans_count'], color='Total_trans_amount', labels={'Total_trans_amount': 'Total_trans_amount'}, height=400)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    if selected == 'User':
      with st.container():
            # MySQL database connection
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="phonepe"
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("USE phonepe")
        mydb.commit()

        # Assuming 'mydb' is a MySQL database connection
        # Convert it to an SQLAlchemy engine
        engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/phonepe')

        sql=f"""SELECT State,District,sum(Registered_user) as Registered_users,sum(App_opens) as App_open 
        FROM map_user   
        WHERE Year={year} AND Quarter={quarter} AND State='{state}'
        GROUP BY District ORDER BY District""" 
        data = pd.read_sql(sql, con=engine)
        
        fig = px.choropleth(data,
                          geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                          featureidkey='properties.ST_NM',
                          locations='State',
                          color='Registered_users',
                          hover_data=['State','App_open'],
                          projection="robinson",
                          color_continuous_scale='YlGnBu')
        fig.update_geos(fitbounds = 'locations',visible = False )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig,theme="streamlit",use_container_width=True)

        # Bar chart for the districts of the selected state
        data = data.sort_values(by='Registered_users', ascending=False).reset_index(drop=True)
        fig = px.bar(data, x='District', y='Registered_users', color_continuous_scale='Plasma',hover_data=['Registered_users','App_open'], color='Registered_users', labels={'Registered_users': 'Registered_users'}, height=400)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

  expander = st.sidebar.expander("About Pulse")
  expander.write(
        """
    The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.

    When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?
    This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.

    This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.

    PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.
    """
    )


display_dashboard()
