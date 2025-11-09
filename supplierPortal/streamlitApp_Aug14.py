##Supplier Visibility and Collaboration Portal
##To be used by both TESLA and their Suppliers (mainly on Bespoke IT Framework)
# Import python packages
import streamlit as st
import pandas as pd
import numpy as np


from snowflake.snowpark.context import get_active_session
#Suppress errors from experiemental features
st.set_option('client.showErrorDetails', False)
st.set_page_config(layout="wide")

on = st.toggle("Supplier View")
if on:
    #Supplier CATL view
    st.image('https://i.postimg.cc/284Ps84J/CATL.png', width=150)
    st.title("Supplier Visibility and Collaboration Portal")
    st.text("")
    st.text("")
    st.write("**Application to view, and manage your supply chain planning and execution data**")
    
    # Get the current credentials
    session = get_active_session()
    
    with st.sidebar:
        st.subheader("**Collaboration widget**")
        messages = st.container(height=500)
        if prompt := st.chat_input("Enter your messages here"):
            messages.chat_message("user").write(prompt)
            messages.chat_message("supplier").write(f"Hi, there! Ok, let me take a look at that.")
    
    st.text("")
    st.divider()
    st.text("")
    
    st.subheader("**Container updates from Dun & Bradstreet**")
    shippingInsights = "select * from STREAMLIT_APPS.SLSCM.CONTAINER_STATUS where requester_country_nme='CHINA' and requester_city_nme='GUANGZHOU'"
    container_status = session.sql(shippingInsights).to_pandas()
    container_status
    st.divider()
    st.subheader("**Key Tracking Metrics**")
    FillRate = "select shipmentdate, (quantity_shipped/quantity_confirmed)*100 as Fill_Rate, (quantity_confirmed - quantity_shipped)*1000 as missed_UNITS_demand  from streamlit_apps.slscm.shipments where supplier='CATL' order by shipmentdate"
    FillRatedf = session.sql(FillRate).to_pandas()
    st.text("YTD FILL RATE IN PALLETS")
    st.line_chart(FillRatedf, x="SHIPMENTDATE", y="FILL_RATE")
    st.text("")
    st.text("")
    st.text("YTD MISSED UNITS DEMAND OVER TIME PERIOD")
    st.line_chart(FillRatedf, x="SHIPMENTDATE", y="MISSED_UNITS_DEMAND")

    st.text("")
    st.divider()
    st.text("Order Forecasts Collaboration")

    OrderForecasts = "select ofdate, supplierproductid,fromsiteid, tositeid, quantity_requested, quantity_confirmed,comments from streamlit_apps.slscm.orderforecasts where supplier='CATL' and of_status='Open'"

    
    data1 = session.sql(OrderForecasts).to_pandas()
    
    
    edited_df = st.experimental_data_editor(data1)
    st.button("Submit", type="primary", help="Click this button when done with your inputs")

else:
#Tesla View
    st.image('https://i.postimg.cc/y6wKqb2J/TESLA.png', width=150)
    st.title("Supplier Visibility and Collaboration Portal")
    st.text("")
    st.text("")
    st.write("**Application to view, and manage your supply chain planning and execution data**")
    
    # Get the current credentials
    session = get_active_session()
    
    with st.sidebar:
        st.subheader("**Collaboration widget**")
        messages = st.container(height=500)
        if prompt := st.chat_input("Enter your messages here"):
            messages.chat_message("user").write(prompt)
            messages.chat_message("supplier").write(f"Hi, there! Ok, let me take a look at that.")
    
    st.text("")
    
    supplier_selection = st.selectbox('Let us begin with a supplier:', ('select value','PENA', 'CATL'))
    st.divider()
    
    if supplier_selection != 'select value':
        st.text("")
            
        st.subheader("**Key Tracking Metrics**")
    
        FillRate = "select shipmentdate, (quantity_shipped/quantity_confirmed)*100 as Fill_Rate, (quantity_confirmed - quantity_shipped)*1000 as missed_UNITS_demand  from streamlit_apps.slscm.shipments where supplier='" + supplier_selection +"' order by shipmentdate"
        FillRatedf = session.sql(FillRate).to_pandas()
        st.text("YTD FILL RATE IN PALLETS")
        st.line_chart(FillRatedf, x="SHIPMENTDATE", y="FILL_RATE")
        st.text("")
        st.text("")
        st.text("YTD MISSED UNITS DEMAND OVER TIME PERIOD")
        st.line_chart(FillRatedf, x="SHIPMENTDATE", y="MISSED_UNITS_DEMAND")
    
        st.text("")
        st.divider()
        st.text("Order Forecasts Collaboration")
    
        OrderForecasts = "select ofdate, supplierproductid,fromsiteid, tositeid, quantity_requested, quantity_confirmed,comments from streamlit_apps.slscm.orderforecasts where supplier='"+ supplier_selection +"' and of_status='Open'"
    
        
        data1 = session.sql(OrderForecasts).to_pandas()
        
        
        edited_df = st.experimental_data_editor(data1)

        #SiteInformation = "select SiteId, City, Latitude, Longitude from siteinformation"

        #sitedf = session.sql(SiteInformation).to_pandas()

        #st.map(sitedf,
            #latitude='LATITUDE',
            #longitude='LONGITUDE',size=20, color='#0044ff')

