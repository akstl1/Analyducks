# Improt libraries
import streamlit as st
import pandas as pd
import joblib

import datetime as dt
from datetime import date
import os
# import requests

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image

## read in excel dataset
df = pd.read_excel("data/data.xlsx", sheet_name="Ducks")

## convert date bought col to date, and extract year into a column
df['Date_Bought'] = pd.to_datetime(df['Date_Bought']).dt.date
df['Year'] = pd.DatetimeIndex(df['Date_Bought']).year
df = df.sort_values(by=['Date_Bought'], ascending=True)

## find avg weight measure, needed for rows where more than 1 duck is included in the total weight
df['Avg_Weight'] = np.round(df.Total_Weight/df.Quantity,2)

## transform and create new dfs to find ducks bought by state, country, purchase method, buyer, year, weight, and cumulative weight
state_df = df.groupby(["Purchase_State"]).agg({"Quantity":"sum"}).reset_index()
state_df = state_df[state_df["Purchase_State"]!=""]

county_df = df.groupby(["ISO_Code","Purchase_Country"]).agg({"Quantity":"sum"}).reset_index()

purchase_method_df = df.groupby(["Purchase_Method"]).agg({"Quantity":"sum"}).reset_index()

buyer_df = df.groupby(["Buyer"]).agg({"Quantity":"sum"}).reset_index()

yearly_df = df.groupby(["Year"]).agg({"Quantity":"sum"}).reset_index()

weight_df = df.groupby(["Year"]).agg({"Total_Weight":"sum"}).reset_index()

weight_cum_df = df.groupby(['Year']).sum().cumsum().reset_index()

# insert a title for the app and instructions

st.title("Customer Churn Prediction Model")
st.subheader("Enter customer information and submit for likelihood of churn")


# chest pain input form

SeniorCitizen = st.number_input(
    label = "Enter whether the customer is a senior citizen [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )

tenure = st.number_input(
    label = "Enter the customer's tenure (in years) with our service [1-72]",
    min_value = 1,
    max_value = 72,
    value = 12,
    )

MonthlyCharges = st.number_input(
    label = "Enter the customers's monthly charge amount [0-150]",
    min_value = 0.00,
    max_value = 150.00,
    value = 75.00,
    step=0.01,
    format="%0.2f"
    )

TotalCharges = st.number_input(
    label = "Enter the customers's total lifetime charge amount [0-9000]",
    min_value = 0.00,
    max_value = 9000.00,
    value = 4500.00,
    step=0.01,
    format="%0.2f"
    )

gender_Male = st.number_input(
    label = "Enter whether the customer is male [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
Partner_Yes = st.number_input(
    label = "Enter whether the customer has a partner [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
Dependents_Yes = st.number_input(
    label = "Enter whether the customer has dependents [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
PhoneService_Yes = st.number_input(
    label = "Enter whether the customer has phone service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
MultipleLines_No_phone_service = st.number_input(
    label = "Enter whether the customer both: (1) does not have multiple lines and (2) has phone service  [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
MultipleLines_Yes = st.number_input(
    label = "Enter whether the customer has multiple lines [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
InternetService_Fiber_optic = st.number_input(
    label = "Enter whether the customer has fiber optic service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
InternetService_No = st.number_input(
    label = "Enter whether the customer has internet service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
OnlineSecurity_No_internet_service = st.number_input(
    label = "Enter whether the customer has both: (1) not purchased online security and (2) has internet service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
OnlineSecurity_Yes = st.number_input(
    label = "Enter whether the customer has purchased online security [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
OnlineBackup_No_internet_service = st.number_input(
    label = "Enter whether the customer both: (1) has no online backup and (2) has no internet service package [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
OnlineBackup_Yes = st.number_input(
    label = "Enter whether the customer purchased online backup service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
DeviceProtection_No_internet_service = st.number_input(
    label = "Enter whether the customer both: (1) has device protection and (2) does not have internet service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
DeviceProtection_Yes = st.number_input(
    label = "Enter whether the customer has device protection [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
TechSupport_No_internet_service = st.number_input(
    label = "Enter whether the customer both: (1) has tech support package and (2) does not have internet service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
TechSupport_Yes = st.number_input(
    label = "Enter whether the customer has a tech support package [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
StreamingTV_No_internet_service = st.number_input(
    label = "Enter whether the customer both (1) has TV streaming service and (2) doesn't have internet service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
StreamingTV_Yes = st.number_input(
    label = "Enter whether the customer has TV streaming service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
StreamingMovies_No_internet_service = st.number_input(
    label = "Enter whether the customer both (1) has movie streaming service and (2) doesn't have internet service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
StreamingMovies_Yes = st.number_input(
    label = "Enter whether the customer has movie streaming service [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
Contract_One_year = st.number_input(
    label = "Enter whether the customer is in a one year contract [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
Contract_Two_year = st.number_input(
    label = "Enter whether the customer is in a two year contract [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
PaperlessBilling_Yes = st.number_input(
    label = "Enter whether the customer is enrolled in paperless billing [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
PaymentMethod_Credit_card_automatic = st.number_input(
    label = "Enter whether the customer pays via credit card autopay [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
PaymentMethod_Electronic_check = st.number_input(
    label = "Enter whether the customer pays via e-check payment [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
PaymentMethod_Mailed_check = st.number_input(
    label = "Enter whether the customer pays via mailed check [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
tenure_cohort_12_24_months = st.number_input(
    label = "Enter whether the customer has had service for 12-24 months [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
tenure_cohort_24_48_months = st.number_input(
    label = "Enter whether the custmoer has had service for 24-48 months [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 
tenure_cohort_over_48_months = st.number_input(
    label = "Enter whether the customer has had service for more than 48 months [0-1]",
    min_value = 0,
    max_value = 1,
    value = 1,
    )
 


#({"SeniorCitizen" :[SeniorCitizen],
# "tenure" : [tenure],
# "MonthlyCharges" : [MonthlyCharges],
# "TotalCharges" :[TotalCharges],
# "gender_Male" : [gender_Male],
# "Partner_Yes" : [Partner_Yes],
# "Dependents_Yes" : [Dependents_Yes],
# "PhoneService_Yes" : [PhoneService_Yes],
# "MultipleLines_No phone service" : [MultipleLines_No_phone_service],
# "MultipleLines_Yes" : [MultipleLines_Yes],
# "InternetService_Fiber optic" : [InternetService_Fiber_optic],
# "InternetService_No" : [InternetService_No],
# "OnlineSecurity_No internet service" : [OnlineSecurity_No_internet_service],
# "OnlineSecurity_Yes" : [OnlineSecurity_Yes],
# "OnlineBackup_No internet service" : [OnlineBackup_No_internet_service],
# "OnlineBackup_Yes" : [OnlineBackup_Yes],
# "DeviceProtection_No internet service" : [DeviceProtection_No_internet_service],
# "DeviceProtection_Yes" : [DeviceProtection_Yes],
# "TechSupport_No internet service" : [TechSupport_No_internet_service],
# "TechSupport_Yes" : [TechSupport_Yes],
# "StreamingTV_No internet service" : [StreamingTV_No_internet_service],
# "StreamingTV_Yes" : [StreamingTV_Yes],
# "StreamingMovies_No internet service" : [StreamingMovies_No_internet_service],
# "StreamingMovies_Yes" : [StreamingMovies_Yes],
# "Contract_One year" : [Contract_One_year],
# "Contract_Two year" : [Contract_Two_year],
# "PaperlessBilling_Yes" : [PaperlessBilling_Yes],
# "PaymentMethod_Credit card (automatic)" : [PaymentMethod_Credit_card_automatic],
# "PaymentMethod_Electronic check" : [PaymentMethod_Electronic_check],
# "PaymentMethod_Mailed check" : [PaymentMethod_Mailed_check],
# "tenure_cohort_12-24 months" : [tenure_cohort_12_24_months],
# "tenure_cohort_24-48 months" : [tenure_cohort_24_48_months],
# "tenure_cohort_over 48 months" : [tenure_cohort_over_48_months]})


# submit inputs to model

if st.button("Submit For Prediction"):
    # store data into df for prediction
    new_data = pd.DataFrame({"SeniorCitizen" :[SeniorCitizen],
    "tenure" : [tenure],
    "MonthlyCharges" : [MonthlyCharges],
    "TotalCharges" :[TotalCharges],
    "gender_Male" : [gender_Male],
    "Partner_Yes" : [Partner_Yes],
    "Dependents_Yes" : [Dependents_Yes],
    "PhoneService_Yes" : [PhoneService_Yes],
    "MultipleLines_No phone service" : [MultipleLines_No_phone_service],
    "MultipleLines_Yes" : [MultipleLines_Yes],
    "InternetService_Fiber optic" : [InternetService_Fiber_optic],
    "InternetService_No" : [InternetService_No],
    "OnlineSecurity_No internet service" : [OnlineSecurity_No_internet_service],
    "OnlineSecurity_Yes" : [OnlineSecurity_Yes],
    "OnlineBackup_No internet service" : [OnlineBackup_No_internet_service],
    "OnlineBackup_Yes" : [OnlineBackup_Yes],
    "DeviceProtection_No internet service" : [DeviceProtection_No_internet_service],
    "DeviceProtection_Yes" : [DeviceProtection_Yes],
    "TechSupport_No internet service" : [TechSupport_No_internet_service],
    "TechSupport_Yes" : [TechSupport_Yes],
    "StreamingTV_No internet service" : [StreamingTV_No_internet_service],
    "StreamingTV_Yes" : [StreamingTV_Yes],
    "StreamingMovies_No internet service" : [StreamingMovies_No_internet_service],
    "StreamingMovies_Yes" : [StreamingMovies_Yes],
    "Contract_One year" : [Contract_One_year],
    "Contract_Two year" : [Contract_Two_year],
    "PaperlessBilling_Yes" : [PaperlessBilling_Yes],
    "PaymentMethod_Credit card (automatic)" : [PaymentMethod_Credit_card_automatic],
    "PaymentMethod_Electronic check" : [PaymentMethod_Electronic_check],
    "PaymentMethod_Mailed check" : [PaymentMethod_Mailed_check],
    "tenure_cohort_12-24 months" : [tenure_cohort_12_24_months],
    "tenure_cohort_24-48 months" : [tenure_cohort_24_48_months],
    "tenure_cohort_over 48 months" : [tenure_cohort_over_48_months]})
    
    # apply model pipeline to the input data and extract probability prediction
    pred_proba = model.predict_proba(new_data)[0][1]
    
    # output prediction
    st.subheader(f"Based on these customer attributes, our model predicts a churn probability of {pred_proba: .0%}")