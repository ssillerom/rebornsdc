import streamlit as st
import sqlite3
import hashlib



def app():

        def create_usertable():
            conn = sqlite3.connect('/home/dakeh/Escritorio/rebornsdc/app/data/bin/greenchain_users.db')
            c = conn.cursor()
            c.execute(
                'CREATE TABLE IF NOT EXISTS tablaUsuarios(username TEXT,password TEXT)')


        def add_userdata(username, password):
            conn = sqlite3.connect('/home/dakeh/Escritorio/rebornsdc/app/data/bin/greenchain_users.db')
            c = conn.cursor()
            c.execute('INSERT INTO tablaUsuarios(username,password) VALUES (?,?)',
                    (username, password))
            conn.commit()


        def login_user(username, password):
            conn = sqlite3.connect('/home/dakeh/Escritorio/rebornsdc/app/data/bin/greenchain_users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM tablaUsuarios WHERE username =? AND password = ?',
                    (username, password))
            data = c.fetchall()
            return data


        def make_hashes(password):
            return hashlib.sha256(str.encode(password)).hexdigest()


        def check_hashes(password, hashed_text):
            if make_hashes(password) == hashed_text:
                return hashed_text
            return False

        st.subheader(
            "Intranet: Crear nuevo usuario para Green Chain")
        new_user = st.text_input("Usuario")
        new_password = st.text_input("Contraseña", type='password')

        if st.button("Registrar"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("Se ha creado satisfactoriamente tu cuenta {} !".format(new_user))