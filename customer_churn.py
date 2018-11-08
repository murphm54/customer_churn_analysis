import numpy as np
import pandas as pd

def map_yes_no(map_tab,map_col,new_col_name):
	
	
	map_tab[new_col_name]=map_tab[map_col].map({'Yes':1,'No':0}).fillna(0).astype(int)
	revised_tab=map_tab.drop([map_col],axis=1)
	return revised_tab

def map_one_hot(map_tab,map_col,map_prefix):
	return pd.concat([map_tab,pd.get_dummies(map_tab[map_col], prefix=map_prefix,dummy_na=False).astype(int)],axis=1).drop([map_col],axis=1)

def clean_churn_data(raw_data):

	#Create Mapping for 'gender' field
	raw_data['is_Male']=raw_data['gender'].map({'Male':1,'Female':0})
	raw_data=raw_data.drop(['gender'],axis=1)

        #Configuration of new field names once mapped
	map_col_config=[['Partner','has_Partner'],['Dependents','has_Dependents'],['PhoneService','has_PhoneService'],['MultipleLines','has_MultipleLines'],['OnlineSecurity','has_OnlineSecurity'],['OnlineBackup','has_OnlineBackup'],['DeviceProtection','has_DeviceProtection'],['TechSupport','has_TechSupport'],['StreamingTV','has_StreamingTV'],['StreamingMovies','has_StreamingMovies'],['PaperlessBilling','has_PaperlessBilling'],['Churn','has_Churned']]

        #Map all yes/no/other value fields
	for i in range(len(map_col_config)):

		raw_data=map_yes_no(raw_data,map_col_config[i][0],map_col_config[i][1])

        #Apply one hot encoding
	for i,j in [['InternetService','internet'],['Contract','contract'],['PaymentMethod','payment']]:
		raw_data=map_one_hot(raw_data,i,j)

        #Perform additional formatting on fields
	clean_cols=raw_data.columns
	clean_cols=[s.replace(' ', '') for s in clean_cols]
	clean_cols=[s.replace(')', '') for s in clean_cols]
	clean_cols=[s.replace('(', '_') for s in clean_cols]
	raw_data.columns=clean_cols
	raw_data['MonthlyCharges']=raw_data['MonthlyCharges'].astype(float)
	raw_data['TotalCharges']=(raw_data['TotalCharges'].replace(' ','0.0',regex=True)).astype(float)
	
	raw_data['customerID'] = raw_data['customerID'].astype(str)
	raw_data['customerID'] = raw_data['customerID'].str.replace('-','')

	
	return raw_data
