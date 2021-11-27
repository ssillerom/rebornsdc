import streamlit as st
from web3 import Web3
import time
import json

def app():
    st.header("PoC of Green Chain 2021")

    menu_demo = ['Comprar Energía', 'Vender Energía']

    choice = st.selectbox('Seleccione la orden a realizar en la red: ',menu_demo)

    if choice == 'Comprar Energía':
        col1,col2,col3 = st.columns(3)
        col1.metric("Energia Disponible", "500",'kWh')
        col2.metric("Precio $GEC / kWh", "0.00005 $GEC", "EUR: 0,2258 €/kWh")
        col3.metric("Energia disponible", "500 kWh", "+5%")
        # Giving a title 
        st.title("Energy Buyer's form with $GEC")
        # creating a form

        my_form=st.form(key='form-1')
        # creating input fields
        fname=my_form.text_input('Nombre: ')
        lname=my_form.text_input('Apellido: ')
        email=my_form.text_input('Mail: ')

        # creating a text area
        address=my_form.text_area('Dirección del monedero virtual:')
        # creating a submit button
        submit=my_form.form_submit_button('Comprar')
        # the following gets updated after clicking on submit, printing the details of the fields that are submitted in the form

        with st.spinner('Wait for it...'):
            time.sleep(5)
            st.success('Done!')

    elif choice == 'Vender Energía':
        col1,col2,col3 = st.columns(3)
        col1.metric("Energia Vendida", "0",'kWh')
        col2.metric("Precio $GEC / kWh", "0.00005 $GEC", "EUR: 0,2258 €/kWh")
        col3.metric("Energia disponible", "500 kWh", "+5%")
        # Giving a title 
        st.title("Energy Seller's form with $GEC")
        # creating a form

        my_form=st.form(key='form-2')
        # creating input fields
        fname=my_form.text_input('Nombre: ')
        lname=my_form.text_input('Apellido: ')
        email=my_form.text_input('Mail: ')

        # creating a text area
        address=my_form.text_area('Dirección del monedero virtual:')
        # creating a submit button
        submit=my_form.form_submit_button('Comprar')
        # the following gets updated after clicking on submit, printing the details of the fields that are submitted in the form

        with st.spinner('Wait for it...'):
            time.sleep(5)
            st.success('Done!')

