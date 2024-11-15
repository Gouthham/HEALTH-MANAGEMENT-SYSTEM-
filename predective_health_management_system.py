# -*- coding: utf-8 -*-
"""PREDECTIVE HEALTH MANAGEMENT SYSTEM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Kvo0EvCSzCmMjEXEi3uPmK8Ddcl8DQ_u

# IMPORTING THE FILES
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from joblib import dump
from joblib import load
import joblib

from google.colab import drive
drive.mount('/content/drive')

"""#LOADING THE "SYMPTOM LVL" FILE"""

symptoms=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/2. SYMPTOMS DATA.csv')
symptoms

"""# DATA PREPROCESSING
# EXPLORATORY DATA ANALYSIS

**# CHECKING THE TYPE OF DATA PRESENT IN THE DATASET**
"""

symptoms.dtypes

"""**# CHECKING THE NUMBER OF ROWS AND COLUMNS**"""

symptoms.shape

"""**# CHECKING IF THE DATA SET "SYMPTOM LVL" CONTAIN ANY DUPLICATES**"""

# duplicates=symptoms.duplicated(keep=False)
# print(duplicates)

# duplicate_count = duplicates.sum()
# print(f'Total duplicate rows: {duplicate_count}')

"""**# SINCE THE TOTAL DUPLICATES ROWS : 0 THERE IS NO NEED TO DROP DUPLICATES**"""

#symptoms.drop_duplicates(inplace=True)
#symptoms

"""**# CHECKING IF IS THERE ARE ANY MISSING VALUE IN THE DATASET**"""

missing_values=symptoms.isnull().sum()
print(missing_values)

"""# ENCODING THE DATA

**LABEL ENCODING FOR DISEASES COLUMN**
"""

label_encoder=LabelEncoder()
symptoms['DISEASES']=label_encoder.fit_transform(symptoms['DISEASES'])
print(symptoms.head())

"""# SPLITING THE DATA INTO TRAINING AND TESTING SETS"""

X=symptoms.drop(columns=['DISEASES'])
Y=symptoms['DISEASES']
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=42)
X_train.shape,X_test.shape,Y_train.shape,Y_test.shape

"""# TRAINING THE MODEL

# 1. SUPPORT VECTOR CLASSIFIER
"""

SVM_model=SVC(random_state=42)
SVM_model.fit(X_train,Y_train)

"""**ACCURACY OF SUPPORT VECTOR CLASSIFIER**"""

Y_pred_SVM=SVM_model.predict(X_test)
accuracy_SVM=accuracy_score(Y_test,Y_pred_SVM)
print(f'ACCURACY OF SUPPORT VECTOR MACHINE {accuracy_SVM:.2f}')

"""# 2. DECISION TREE CLASSIFIER"""

DT_model=DecisionTreeClassifier(random_state=42)
DT_model.fit(X_train,Y_train)

"""**ACCURACY OF DECISION TREE CLASSIFIER**"""

Y_pred_DT=DT_model.predict(X_test)
accuracy_DT=accuracy_score(Y_test,Y_pred_DT)
print(f'ACCURACY OF DECISION TREE CLASSIFIER: {accuracy_DT:.2f}')

"""# 3. RANDOM FOREST CLASSIFIER

"""

#Initializing the model
RF_model=RandomForestClassifier(random_state=42)
#Training the model
RF_model.fit(X_train,Y_train)

"""**ACCURACY OF RANDOM FOREST**"""

#Predicting and evaluating the accuracy
Y_pred_RF=RF_model.predict(X_test)
accuracy_RF=accuracy_score(Y_test,Y_pred_RF)
print(f'ACCURACY OF RANDOM FOREST CLASSIFIER: {accuracy_RF:.2f}')

"""# 4. K-NEAREST NEIGHBOR CLASSIFIER"""

KNN_model=KNeighborsClassifier()
KNN_model.fit(X_train,Y_train)

"""**ACCURACY OF K-NEAREST NEIGHBOR CLASSIFIER**"""

Y_pred_KNN=KNN_model.predict(X_test)
accuracy_KNN=accuracy_score(Y_test,Y_pred_KNN)
print(f'ACCURACY OF K-NEAREST NEIGHBOR CLASSIFIER: {accuracy_KNN:.2f}')

"""# 5. LOGISTIC REGRESSION"""

LR_model=LogisticRegression(max_iter=100)
LR_model.fit(X_train,Y_train)

"""**ACCURACY OF LOGISTIC REGRESSION**"""

Y_pred_LR=LR_model.predict(X_train)
accuracy_LR=accuracy_score(Y_train,Y_pred_LR)
print(f'ACCURACY OF LOGISTIC REGRESSION : {accuracy_LR:.2f}')

"""# SAVING THE TRAINED MODEL { RANDOM FOREST MODEL }"""

dump(RF_model, '/content/drive/MyDrive/Colab Notebooks/trained_random_forest_model.joblib')
print("Model saved to /content/drive/MyDrive/Colab Notebooks/trained_random_forest_model.joblib")

"""**CHECKING IF THE RANDOM FOREST MODEL IS LOADED OR NOT**"""

loaded_model = load('/content/drive/MyDrive/Colab Notebooks/trained_random_forest_model.joblib')
print(type(loaded_model))

"""**SAVING THE LOGISTIC REGRESSION MODEL**"""

# dump(LR_model, '/content/drive/MyDrive/Colab Notebooks/trained_logistic_regression_model.joblib')
# print("Model saved to /content/drive/MyDrive/Colab Notebooks/trained_logistic_regression_model.joblib")

# loaded_model = load('/content/drive/MyDrive/Colab Notebooks/trained_logistic_regression_model.joblib')
# print(type(loaded_model))

"""# LOADING THE METADATA FILES

**LOADING THE DESCRIPTION FILE**
"""

description=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/1. DESCRIPTION.csv')
description.head()

"""**LOADING THE MEDICATION FILE**"""

med=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/3. MEDICATION.csv')
med.head()

"""**LOADING THE PRECAUTIONS FILE**"""

precaution=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/4. Numbered_Precautions.csv')
precaution.head()

"""**LOADING THE DIET PLAN FILE**"""

diet=pd.read_csv('/content/drive/MyDrive/Colab Notebooks/5. DIET.csv')
diet.head()

"""#LOADING AND TESTING THE MODEL"""

model = joblib.load('/content/drive/MyDrive/Colab Notebooks/trained_random_forest_model.joblib')

input_line = input("Enter symptoms, separated by commas (e.g., itching, skin_rash): ")
entered_symptoms = [sym.strip().lower() for sym in input_line.split(',')]
user_input = {symptom: 1 if symptom in entered_symptoms else 0 for symptom in symptoms}
input_df = pd.DataFrame([user_input]).reindex(columns=model.feature_names_in_, fill_value=0)

if len(entered_symptoms) == 1:
    symptom_name = entered_symptoms[0]
    possible_diseases = symptoms[symptoms[symptom_name] == 1]['DISEASES'].unique()
    possible_diseases = label_encoder.inverse_transform(possible_diseases)

    print(f"These are the possible diseases related to '{symptom_name}':")
    for disease in possible_diseases:
        print(f"- {disease}")

    related_symptoms = set()
    for disease in possible_diseases:
        disease_symptoms = symptoms[symptoms['DISEASES'] == label_encoder.transform([disease])[0]].columns[
            symptoms[symptoms['DISEASES'] == label_encoder.transform([disease])[0]].iloc[0] == 1
        ]
        related_symptoms.update(disease_symptoms)

    suggested_symptoms = [symptom for symptom in related_symptoms if symptom != symptom_name]
    print(f"\nWould you like to refine your prediction with any of these additional symptoms? {', '.join(suggested_symptoms)}")

    add_symptom = input("Do you have any of the above symptoms? (yes/no): ").strip().lower()

    if add_symptom == 'no':
        print("It's recommended to consult a doctor for a more accurate diagnosis.")
    else:
        additional_symptom = input("Enter additional symptoms from the above list (comma-separated): ")
        new_symptoms = [sym.strip().lower() for sym in additional_symptom.split(',')]
        entered_symptoms.extend(new_symptoms)

        user_input = {symptom: 1 if symptom in entered_symptoms else 0 for symptom in symptoms}
        input_df = pd.DataFrame([user_input]).reindex(columns=model.feature_names_in_, fill_value=0)

        predicted_disease_encoded = model.predict(input_df)
        disease = label_encoder.inverse_transform(predicted_disease_encoded)[0]
        print(f'Predicted Disease: {disease}')

        description_info = description[description['DISEASES'] == disease]['DESCRIPTION'].values
        if description_info.size > 0:
            print(f"\nDescription of {disease}: {description_info[0]}")

        medications_info = med[med['DISEASES'] == disease]['Medication '].values
        if medications_info.size > 0:
            print(f"\nRecommended Medications for {disease}: {medications_info[0]}")

        precautions_info = precaution[precaution['DISEASES'] == disease]['PRECAUTION'].values
        if precautions_info.size > 0:
            print(f"\nPrecautions for {disease}: {precautions_info[0]}")

        diet_info = diet[diet['DISEASES'] == disease]['Diet'].values
        if diet_info.size > 0:
            print(f"\nDiet Recommendations for {disease}: {diet_info[0]}")

else:
    predicted_disease_encoded = model.predict(input_df)
    disease = label_encoder.inverse_transform(predicted_disease_encoded)[0]
    print(f'Predicted Disease: {disease}')

    description_info = description[description['DISEASES'] == disease]['DESCRIPTION'].values
    if description_info.size > 0:
        print(f"\nDescription of {disease}: {description_info[0]}")

    medications_info = med[med['DISEASES'] == disease]['Medication '].values
    if medications_info.size > 0:
        print(f"\nRecommended Medications for {disease}: {medications_info[0]}")

    precautions_info = precaution[precaution['DISEASES'] == disease]['PRECAUTION'].values
    if precautions_info.size > 0:
        print(f"\nPrecautions for {disease}: {precautions_info[0]}")

    diet_info = diet[diet['DISEASES'] == disease]['Diet'].values
    if diet_info.size > 0:
        print(f"\nDiet Recommendations for {disease}: {diet_info[0]}")