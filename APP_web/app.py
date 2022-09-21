from webbrowser import get
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
from sklearn import svm
import streamlit as st
from PIL import Image
import pandas as pd

# Path  pretrained model
MODEL_PATH = 'models/model_.pkl'
ENCODE_PATH = 'models/mean_encode.pkl'
SCALER_PATH = 'models/scaler.pkl'
QT_TRANFORM_PATH = 'models/quantile_transformer.pkl'


def getExpLevel(exp):

    if exp == "Entry-level":
        return "EN" 
    elif exp == "Mid-level":
        return "MI"
    elif exp == "Senior":
        return "SE"
    else:
        return "EX"


def getEmpType(emp):

    if emp == "Part-time":
        return "PT" 
    elif emp == "Contract":
        return "CT"
    elif emp == "Freelance":
        return "FL"
    else:
        return "FT"





def model_prediction(x_in, model):

    x = np.asarray(x_in).reshape(1,-1)
    preds=model.predict(x)

    return preds


def main():
    logo = Image.open("img/topjob-logo2.png")
    model=''
    encode = ''
    scaler = ''
    qt = ''
    # load model
    if model=='':
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)

    if encode=='':
        with open(ENCODE_PATH, 'rb') as file:
            encode = pickle.load(file)

    if scaler=='':
        with open(SCALER_PATH, 'rb') as file:
            scaler = pickle.load(file)
    if qt =='':
        with open(QT_TRANFORM_PATH, 'rb') as file:
            qt = pickle.load(file)
    
      #Head

    st.image(logo)
    
    html_temp =  """
   
    <hr>
    <div>

    <h2 style="color:#7DA4D6;text-align:center;">GET YOUR PREDICTION...</h2>   
    """

   

     #form
    st.markdown(html_temp,unsafe_allow_html=True)
   

    
    work_year = st.selectbox('Work year:',('2020','2021','2022'))
    employment_type = st.selectbox('Employment type:',('Contract','Freelance','Full-time','Part-time'))
    job = st.selectbox('Job:',('Data Scientist','Web Developer','Cyber Security','DevOps','Mobile Developer'))
    experience_level = st.selectbox('Experience Level:',('Entry-level','Mid-level','Senior','Expert'))
    remote_ratio = st.selectbox('Remote ratio:',('0%','50%','100%'))
    company_location = st.selectbox('Company country:',('Australia','Belgium','Brazil','Canada','France','Germany','Greece','India','Ireland','Italy','Japan','Mexico','Netherlands','New Zealand','Portugal','Singapore','Spain','Switzerland','United Kingdom','United States'))
    
    remote_ratio = remote_ratio.replace("%","")
    employment_type2 = getEmpType(employment_type)
    experience_level2 = getExpLevel(experience_level)
    
    
    if st.button("Predict"): 
      
        colum_name = ['work_year','experience_level','employment_type', 'job', 'remote_ratio', 'company_location']
        matrix = [[int(work_year),experience_level2,employment_type2,job,int(remote_ratio),company_location]]
        
        dt = pd.DataFrame(matrix)
        
        for i in range(len(colum_name)):
            dt[i] = dt[i].map(encode[colum_name[i]])
            

        dt_scaled = scaler.transform(dt)
        df2 = pd.DataFrame(dt_scaled)

    

        predictS = model_prediction(df2, model)

        predict=predictS.reshape(-1, 1)
        predict=qt.inverse_transform(predict)
        
        st.info('{:20,.2f} $'.format(round(predict[0][0],2)))
        #st.info('{:20,.2f} $'.format(round(predictS[0],2)))
       

    st.markdown("""</div>""",unsafe_allow_html=True)

    #connection data studio
    htlm2 = """<section style="display:flex;margin:0;width:important 100%;" > <iframe width="898" height="649" src="https://datastudio.google.com/embed/reporting/a1cf6a8c-2104-4be2-a119-d5fb9707e6d5/page/K4U2C" frameborder="0" style="border:0" allowfullscreen></iframe> </section>"""
    
    st.markdown(htlm2,unsafe_allow_html=True)
        

if __name__ == '__main__':
    main()
