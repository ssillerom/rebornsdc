import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
import json
import pandas as pd
import numpy as np

def app():


    st.title("¡Bienvenidos a Green Energy Chain $GEC!")

    my_bar = st.progress(0)

    for percent_complete in range(100):
     time.sleep(0.1)
     my_bar.progress(percent_complete + 1)

    col1, col2, col3 = st.columns(3)
    col1.metric(" 1 $GEC", "0.000002 ETH", "EUR: 0.07")
    col2.metric("Energia Comprada", "500 Kw", "+5%")
    col3.metric("CO2 Ahorrado", "245 Kg", "4%")

    renewable_madrid = requests.get("https://apidatos.ree.es/es/datos/generacion/estructura-generacion?start_date=2017-01-01T00:00&end_date=2020-11-21T23:59&time_trunc=year&geo_trunc=electric_system&geo_limit=ccaa&geo_ids=13").json()
    

    hidraulica = renewable_madrid['included'][0]['attributes']['values'][3]['value']
    solar = renewable_madrid['included'][1]['attributes']['values'][3]['value']
    otrasRenovables = renewable_madrid['included'][2]['attributes']['values'][3]['value']

    col4, col5, col6 = st.columns(3)

    st.subheader("Energía renovable generada en Madrid 2021 (Kw/h)")

    col4,col5,col6 = st.columns(3)

    col4.metric("Hidraulica", str(hidraulica) + " Kw/h")
    col5.metric("Solar", str(solar) + " Kw/h")
    col6.metric("Eólica", str(otrasRenovables) + ' Kw/h')
    
    st.text("Clientes vendiendo energía a la red GreenChain (Microgrid): ")
    
    df = pd.DataFrame(
    np.random.randn(200, 2) / [25, 25] + [40.4046, -3.88469],
           columns=['lat', 'lon'])

    
    st.map(df)

    st.text("Clientes comprando energía a través de Green Chain: ")
    
    df = pd.DataFrame(
    np.random.randn(200, 2) / [25, 25] + [40.41831, -3.70275],
           columns=['lat', 'lon'])

    st.map(df)

    





    