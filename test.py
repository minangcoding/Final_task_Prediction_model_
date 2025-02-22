# -*- coding: utf-8 -*-
"""CREDIT RISK LOAN PREDICTION MODELLING.ipynb

Automatically generated by Colaboratory.



#CREDIT RISK LOAN PREDICTION MODELLING
## RAKAMIN ACADEMY ID/X PARTNERS VIRTUAL INTERNSHIP EXPERIENCE PROGRAM

"""

#import python library
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('loan_data_2007_2014.csv')
df.head()

df_FE = df.copy()

loanstatus_condition_drop = df_FE[(df_FE['loan_status'] == 'Current') | (df_FE['loan_status'] == 'Late (31-120 days)') | (df_FE['loan_status'] == 'In Grace Period')
                            | (df_FE['loan_status'] == 'Late (16-30 days)') | (df_FE['loan_status'] == 'Default')]

df_FE = df_FE.drop(loanstatus_condition_drop.index, axis=0)

df_FE = df_FE.drop(['desc','mths_since_last_record','annual_inc_joint','dti_joint','verification_status_joint','open_acc_6m',
                    'open_il_6m','open_il_12m','open_il_24m','mths_since_rcnt_il','total_bal_il','il_util','open_rv_12m',
                    'open_rv_24m','int_rate','max_bal_bc','all_util', 'inq_fi','total_rec_int','total_cu_tl','inq_last_12m',
                    'mths_since_last_major_derog','mths_since_last_delinq','next_pymnt_d'], axis=1)

df_FE = df_FE.drop(['Unnamed: 0', 'id', 'member_id', 'emp_title', 'issue_d', 'url', 'title', 'addr_state', 'zip_code',
                   'earliest_cr_line', 'last_pymnt_d', 'last_credit_pull_d'], axis=1)

df_FE = df_FE.drop(['collections_12_mths_ex_med', 'policy_code', 'acc_now_delinq', 'out_prncp', 'out_prncp_inv', 'application_type',
                   'collection_recovery_fee', 'recoveries', 'tot_coll_amt', 'total_rec_late_fee', 'pub_rec', 'delinq_2yrs'], axis=1)

df_FE = df_FE.dropna(axis=0)

df_CM = df_FE.copy()

df_CM['term_mths'] = df_CM['term'].str.split().str[0]

df_CM['term_mths'].value_counts()

df_CM['term_mths'] = df_CM['term_mths'].astype('int64')

df_CM = df_CM.drop(['term'], axis=1)

df_CM['total_pymnt'] = np.round(df_CM['total_pymnt'].values,2)

df_CM['loan_status'].value_counts()

loan_status_group = {'Does not meet the credit policy. Status:Fully Paid' : 'Fully Paid',
                    'Does not meet the credit policy. Status:Charged Off' : 'Charged Off'}

df_CM['loan_status'] = df_CM['loan_status'].replace(loan_status_group)

df_LE = df_CM.copy()

features_nominal = ['pymnt_plan','home_ownership','purpose','initial_list_status']
features_ordinal = ['grade','sub_grade','emp_length','verification_status']

ordinal_LE = {'grade' : {'A' : 7, 'B' : 6, 'C' : 5, 'D' : 4, 'E' : 3, 'F' : 2, 'G' : 1},
              'sub_grade' : {'A1' : 35, 'A2' : 34, 'A3' : 33, 'A4' : 32, 'A5': 31,
                            'B1' : 30, 'B2' : 29, 'B3' : 28, 'B4' : 27, 'B5': 26,
                            'C1' : 25, 'C2' : 24, 'C3' : 23, 'C4' : 22, 'C5': 21,
                            'D1' : 20, 'D2' : 19, 'D3' : 18, 'D4' : 17, 'D5': 16,
                            'E1' : 15, 'E2' : 14, 'E3' : 13, 'E4' : 12, 'E5': 11,
                            'F1' : 10, 'F2' : 9, 'F3' : 8, 'F4' : 7, 'F5': 6,
                            'G1' : 5, 'G2' : 4, 'G3' : 3, 'G4' : 2, 'G5': 1,},
              'emp_length' : {'10+ years' : 11, '9 years' : 10, '8 years' : 9, '7 years' : 8,
                             '6 years' : 7, '5 years' : 6, '4 years' : 5, '3 years' : 4,
                             '2 years' : 3, '1 year' : 2, '< 1 year' : 1},
              'verification_status' : {'Verified' : 3, 'Source Verified' : 2, 'Not Verified' : 1}}

df_LE = df_LE.replace(ordinal_LE)

df_LE = pd.get_dummies(df_LE, columns=features_nominal, drop_first=True)

# pd.set_option('max_column', 50)
pd.set_option('display.max_columns', 50)

df_LE.head()

df_final = df_LE.copy()

loan_status_change = {'Fully Paid' : 1, 'Charged Off' : 0}

df_final['loan_status'] = df_final['loan_status'].replace(loan_status_change)

df_final['loan_status'].value_counts()

X = df_final.drop(['loan_status'], axis=1, inplace=False)
y = df_final['loan_status']

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold,cross_val_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

algorithms = [LogisticRegression, DecisionTreeClassifier, RandomForestClassifier]
algorithms_name = ['LogisticRegression','DecisionTreeClassifier','RandomForestClassifier']

Algorithms_Score = []

KFold_models = KFold(10)

for i in algorithms:
    model = i()
    model.fit(X_train_scaled,y_train)
    prediction = model.predict(X_test_scaled)
    score = cross_val_score(model,X,y,cv=KFold_models).mean()
    
    Algorithms_Score.append(score)
    
    
model_score = pd.DataFrame({
    'Algorithms' : algorithms_name,
    'Score' : Algorithms_Score
})

model_score