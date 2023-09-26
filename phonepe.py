import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import mysql.connector as sql
import geopandas as gpd
import requests
import matplotlib.pyplot as plt
import PIL
from PIL import Image

# connecting to sql database
st.set_page_config(page_title= "Phonepe Pulse Data Visualization and Exploration:",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """#Created by *M K KOWSHIK BALAJI!*"""})
mydb=sql.connect(host="localhost",
                   user="kowshik",
                   password='iamkowshik',
                   database= "phonepe",
                   port = "3306"
                )
my_cursor = mydb.cursor(buffered=True)

#creating option menu
select=option_menu(
    menu_title = None,
    options = ["Home","About","Charts","Explore","Created By"],
    icons =["house","patch-question","bar-chart","search","person-circle"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "40px"},
            
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})

#creating home menu
if select=='Home':
    st.write("-------------------")     
    col1,col2 = st.columns(2,gap= 'small')
    col1.markdown("## :violet[Domain] : Fintech")
    col1.markdown("## :violet[Technologies used] : Github Cloning, Python, Pandas, MySQL,mysql-connector-python, Streamlit, and Plotly,Geopandas,Matplotlib.pyplot.")
    col1.markdown("## :violet[Overview] : The Phonepe pulse Github repository contains a large amount of data related tovarious metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.")

#creating About option
if select=='About':
   st.write("-----------")
   col1,col2=st.columns([1,1],gap='small')
   with col1:
       st.video("D:\Phonepe project\Pulse.mp4")
   with col2:
      st.image(Image.open('D:\Phonepe project\phonepe.png'),width = 350)
      st.write("---")
      st.markdown("# :The Indian digital payments story has truly captured the world's imagination."
                 "  From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 "  Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 " PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
   st.write("---")
   col3,col4=st.columns([1,1],gap='small')
   with col3:
       st.markdown("# :violet[THE BEAT OF PHONEPE]")
       st.write("---")
       st.markdown("# Phonepe became a leading digital payments company")
       image=Image.open('phonepe logo.jpg',)
       st.image(image,width=450)
       with open('annual report.pdf','rb') as f:
           data=f.read()
       st.download_button('Download Report',data,file_name="phonepe.pdf")
   with col4:
       st.video('D:\Phonepe project\phone.mp4') 
   st.write('---------------')   
   col5,col6=st.columns(2)
   with col5:
       st.markdown('# :violet[LICENSE]')
       st.write('--------------')
       st.markdown('## As per the guidelines of Phonepe')
       with open('license.pdf.pdf','rb') as f:
           data=f.read()
       st.download_button('Download license and guidelines',data,file_name="liscense.pdf")

#creating Charts option
if select=='Charts':
    st.markdown("## :violet[Charts]")
    st.write("----")
    Type = st.selectbox("**Type**", ("--select--","Transactions", "Users"))
    colum1,colum2= st.columns([1,1.8],gap="medium")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """
                )
    if Type == "Transactions": #Creating pie charts for Transaction count for State and District
        col1,col2 = st.columns([4,4],gap="medium")
        with col1:
            st.markdown("### :violet[State]")
            my_cursor.execute(f"select State, sum(Transactions_count) as Transactions_count, sum(Amount) as total from data_aggregated_transaction where year = {Year} and quarter = {Quarter} group by State order by total desc limit 10")
            df = pd.DataFrame(my_cursor.fetchall(), columns=['State', 'Transactions_count','Total_amount'])
            fig = px.pie(df, values='Total_amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Aggrnyl,
                             hover_data=['Transactions_count'],
                             labels={'Transactions_count':'Transactions_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.markdown("### :violet[District]")
            my_cursor.execute(f"select District , sum(Transaction_count) as Transaction_count, sum(Transaction_amount) as Total from data_map_transaction where year = {Year} and quarter = {Quarter} group by District order by Total desc limit 10")
            df = pd.DataFrame(my_cursor.fetchall(), columns=['District', 'Transaction_count','Total_amount'])

            fig = px.pie(df, values='Total_amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Aggrnyl,
                             hover_data=['Transaction_count'],
                             labels={'Transaction_count':'Transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
    
    if Type == "Users":#Creating Bar chart for Brands,Districts wrt to total_users and pie chart for total no of users opeming the app
        col1,col2,col3 = st.columns([2,2,2],gap="medium")
        with col1:
             st.markdown("### :violet[Brands]")   
             if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
             else:
                my_cursor.execute(f"select Brands, sum(Count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from user_table where year = {Year} and quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
                df = pd.DataFrame(my_cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)    
        with col2:
            st.markdown("### :violet[District]")
            my_cursor.execute(f"select District, sum(RegisteredUsers) as Total_Users, sum(App_opens) as Total_App_opens from data_map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(my_cursor.fetchall(), columns=['District', 'Total_Users','Total_App_opens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)                
        with col3:
            st.markdown("### :violet[State]")
            my_cursor.execute(f"select State, sum(RegisteredUsers) as Total_Users, sum(App_opens) as Total_App_opens from  data_map_user where year = {Year} and quarter = {Quarter} group by State order by Total_Users desc limit 10")
            df = pd.DataFrame(my_cursor.fetchall(), columns=['State', 'Total_Users','Total_App_opens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_App_opens'],
                             labels={'Total_App_opens':'Total_App_opens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

#creating explore option
if select == "Explore":
    st.markdown("## :violet[Explore]")
    st.write("----")
    st.subheader("Let's explore some Data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District",
               "Overall state Transaction Amount Data",
               "Overall state Transaction Count Data"]
    select = st.selectbox("Select the option",options)
    
    if select=="Top 10 states based on year and amount of transaction":
        my_cursor.execute("SELECT State, Year, SUM(Amount) AS Total_Transaction_Amount FROM data_aggregated_transaction GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10")
        
        df = pd.DataFrame(my_cursor.fetchall(), columns=['State','Transaction_Year', 'Transaction_Amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### Top 10 states and amount of transaction")
            st.bar_chart(data=df,x="Transaction_Amount",y="State")
    elif select=="List 10 states based on type and amount of transaction":
        my_cursor.execute("SELECT State, SUM(Transactions_count) as Total FROM data_aggregated_transaction GROUP BY State ORDER BY Total ASC LIMIT 10")
        df = pd.DataFrame(my_cursor.fetchall(),columns=['States','Total'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### List 10 states based on type and amount of transaction")
            st.bar_chart(data=df,x="Total",y="States")
    elif select == "Top 5 Transaction_Type based on Amount":
        my_cursor.execute("SELECT Transacton_type, SUM(Amount) AS Transaction_Amount FROM data_aggregated_transaction GROUP BY Transacton_type ORDER BY Transaction_Amount DESC LIMIT 5")
        df = pd.DataFrame(my_cursor.fetchall(), columns=['Transacton_type', 'Transaction_Amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### Top 5 Transacton_type based on Amount")
            st.bar_chart(data=df, y="Transacton_type", x="Transaction_Amount")
    elif select=="Top 10 Registered-users based on States and District":
        my_cursor.execute("SELECT  State, District, SUM(RegisteredUsers) AS Users FROM data_map_user GROUP BY State, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(my_cursor.fetchall(),columns=['State','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### Top 10 Registered-users based on States and District")
            st.bar_chart(data=df,y="State",x="RegisteredUsers")
    elif select=="Top 10 Districts based on states and Count of transaction":
        my_cursor.execute("SELECT State,District,SUM(Transaction_count) AS Counts FROM data_map_transaction GROUP BY State,District ORDER BY Counts DESC LIMIT 10")
        df = pd.DataFrame(my_cursor.fetchall(),columns=['States','District','Transaction_count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### Top 10 Districts based on states and Count of transaction")
            st.bar_chart(data=df,y="States",x="Transaction_count")
    elif select=="List 10 Districts based on states and amount of transaction":
        my_cursor.execute("SELECT DISTINCT State,Year,SUM(Transaction_amount) AS Amount FROM data_map_transaction GROUP BY State, Year ORDER BY Amount ASC LIMIT 10")
        df = pd.DataFrame(my_cursor.fetchall(),columns=['States','Transaction_year','Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### Least 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,y="States",x="Transaction_amount")
    elif select=="List 10 Transaction_Count based on Districts and states":
        my_cursor.execute("SELECT State, District, SUM(Transaction_Count) AS Counts FROM data_map_transaction GROUP BY State,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(my_cursor.fetchall(),columns=['States','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### List 10 Transaction_Count based on Districts and states")
            st.bar_chart(data=df,y="States",x="Transaction_Count")
    elif select=="Top 10 RegisteredUsers based on states and District":
        my_cursor.execute("SELECT State,District, SUM(RegisteredUsers) AS Users FROM data_map_user GROUP BY State,District ORDER BY Users DESC LIMIT 10")
        df = pd.DataFrame(my_cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.markdown("### Top 10 RegisteredUsers based on states and District")
            st.bar_chart(data=df,y="States",x="RegisteredUsers")
    elif select=='Overall state Transaction Amount Data':
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
        st.markdown("### :violet[Overall State Data - Transactions Amount]")
        my_cursor.execute(f"select State, sum(Transactions_count) as Total_Transactions, sum(Amount) as Total_amount from data_aggregated_transaction where year = {Year} and quarter = {Quarter} group by State order by State") 
        df1 = pd.DataFrame(my_cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv(r"D:\Phonepe project\Statenames.csv")
        df1.State=df2
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_amount',
                            color_continuous_scale='rainbow')
        fig.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig,use_container_width=True)
    elif select=='Overall state Transaction Count Data':
         Year = st.slider("**Year**", min_value=2018, max_value=2022)
         Quarter = st.slider("Quarter", min_value=1, max_value=4)
         st.markdown("## :violet[Overall State Data - Transactions Count]")
         my_cursor.execute(f"select State, sum(Transactions_count) as Total_Transactions, sum(Amount) as Total_amount from data_aggregated_transaction where year = {Year} and quarter = {Quarter} group by State order by State") 
         df1 = pd.DataFrame(my_cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
         df2 = pd.read_csv(r"D:\Phonepe project\Statenames.csv")
         df1.Total_Transactions = df1.Total_Transactions.astype(int)
         df1.State = df2
         fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='rainbow')

         fig.update_geos(fitbounds="locations", visible=False)
         st.plotly_chart(fig,use_container_width=True)
        
#creating creator option
if select=='Created By':
    st.write('------------------')
    col3,col4=st.columns(2)
    image=Image.open('photo_2023-09-24_08-14-26.jpg')
    with col3:
     col3.markdown("## :violet[NAME] : ***M K KOWSHIK BALAJI***")
     col3.markdown("## :violet[Mail ID] : ***balajikowshik@gmail.com***")
     col3.markdown("## :violet[GITHUB URL] : ***https://github.com/BALAJIKOWSHIK***")
     col3.markdown('## :violet[ ***Data Scientist Aspirant***]')
    with col4:
        st.image(image)
