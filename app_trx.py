import pandas as pd
import numpy as np
#import ast
import seaborn as sns

from matplotlib.pyplot import figure, xcorr, xlabel


import matplotlib.pyplot as plt
from matplotlib import cm
from collections import Counter

from sklearn import preprocessing 
from sklearn.cluster import KMeans

from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


from statsmodels.discrete.discrete_model import Logit
import statsmodels.api as sm
from sklearn import metrics

import lightgbm as lgbm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score, precision_recall_curve, roc_curve, average_precision_score,f1_score

#Para interpretar el sentido de las variables en ML
#import shap
#Para guardar
import joblib


from flask import Flask, request, jsonify, render_template, url_for
import pickle

import streamlit as st


# Path del modelo preentrenado
#var0 = 'Modelos/var_model_trxs.pkl'
#model0 = 'Modelos/reg_log_trxs.pkl'
#scaler0 = 'Modelos/scale_reg_log_trxs.pkl'

#var_model1 = joblib.load('/Modelos/var_model_trxs.pkl')
# Cargando modelo
#model1 = joblib.load('/Modelos/reg_log_trxs.pkl')
#scaler = joblib.load('Modelos/scale_reg_log_trxs.pkl')

with open('Pkls/var_model_trxs.pkl', 'rb') as f:
    var_model1 = pickle.load(f)

with open('Pkls/reg_log_trxs.pkl', 'rb') as f:
    model1 = pickle.load(f)

#with open('Pkls/scale_reg_log_trxs.pkl', 'rb') as f:
 #   scaler = pickle.load(f)



# Se recibe la imagen y el modelo, devuelve la predicción
def model_prediction(x_in, model):

    x = np.asarray(x_in).reshape(1,-1)
    
        

    pred_model1 = model.predict(x)
    pred_model1 = np.where(pred_model1>0.515,"Fraudulenta","No Fraudulenta") 
#    preds=model.predict(x)

    return  pred_model1 



def main():
    

    
    # Título
    html_temp = """
    <h1 style="color:#181082;text-align:center;">Modelo de Fraude transaccional </h1>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    # Lecctura de datos
    #Datos = st.text_input("Ingrese los valores : N P K Temp Hum pH lluvia:")
    monto = st.text_input("Monto:")
    hora = st.text_input("hora (1-24):")
    linea_tc = st.text_input("Linea TC:")
    is_prime = st.text_input("Es prime? (0/1):")
    dcto = st.text_input("Descuento:")
    cashback = st.text_input("Cashback:")
    tipo_tc_Física = st.text_input("TC Fisico? (0/1):")
    os_ANDROID = st.text_input("Andriod? (0/1):")
    os_WEB = st.text_input("Web (0/1):")
    
    # El botón predicción se usa para iniciar el procesamiento
    if st.button("Predicción :"): 
        #x_in = list(np.float_((Datos.title().split('\t'))))
        x_in =[np.float_(monto.title()),
                    np.float_(hora.title()),
                    np.float_(linea_tc.title()),
                    np.float_(is_prime.title()),
                    np.float_(dcto.title()),
                    np.float_(cashback.title()),
                    np.float_(tipo_tc_Física.title()),
                    np.float_(os_ANDROID.title()),
                    np.float_(os_WEB.title())]

        predictS = model_prediction(x_in, model1)
        st.success('La transaccion es: {}'.format(predictS).upper())

if __name__ == '__main__':
    main()
