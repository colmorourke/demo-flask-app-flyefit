# render_template lets us change HTML page dynamically
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from joblib import load
import uuid # need to generate unique names for images to avoid caching

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html')
    else:
        model_in = load('app/model_pickle.pkl')
        # text_list = request.form['text-property']
        # X_user = construct_df(text_list)
        # cost_pred = model_in.predict(X_user)[0]
        ip_subs = request.form['subs']
        ip_lat = request.form['lat']
        ip_long = request.form['long']
        ip_type = request.form['house_type']
        ip_beds = request.form['bedrooms']
        ip_baths = request.form['bathrooms']
        ip_ber = request.form['ber']
        ip_size = request.form['size']
        text_list = ip_lat + ', ' + ip_long + ', ' + ip_type + ', ' + ip_beds + ', ' + ip_baths + ', ' + ip_ber + ', ' + ip_size
        X_user = construct_df(text_list)
        cost_pred = model_in.predict(X_user)[0]
        annual_revenue = 35*12*float(ip_subs)
        roi = cost_pred/annual_revenue
        return render_template('index.html', out00=ip_subs, out0= text_list, out1=cost_pred, out2 = annual_revenue, out3=roi)

def construct_df(property_inputs):
    df = pd.DataFrame(columns= ['latitude', 'longitude', 'house_type', 'bedrooms', 'bathrooms', 'ber', 'size'])
    df.loc[0, :] = property_inputs.replace(" ", "").split(',')
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    df['bedrooms'] = df['bedrooms'].astype(float)
    df['bathrooms'] = df['bathrooms'].astype(float)
    df['ber'] = df['ber'].astype(float)
    df['size'] = df['size'].astype(float)
    return df

