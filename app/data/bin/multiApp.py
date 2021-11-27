
import streamlit as st
import sqlite3
import re 
import base64
import uuid
import pandas as pd
import hashlib

# Clase constructora para poner todos los servicios en linea a la vez llama a app.py donde están registradas todas las "apps" que componen la plataforma


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
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


        def open_link(url, new_tab=True):
            """Dirty hack to open a new web page with a streamlit button."""
            if new_tab:
                js = f"window.open('{url}')"  # New tab or window
            else:
                js = f"window.location.href = '{url}'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)


        def download_button(object_to_download, download_filename, button_text):
            """
            Generates a link to download the given object_to_download.
            From: https://discuss.streamlit.io/t/a-download-button-with-custom-css/4220
            Params:
            ------
            object_to_download:  The object to be downloaded.
            download_filename (str): filename and extension of file. e.g. mydata.csv,
            some_txt_output.txt download_link_text (str): Text to display for download
            link.
            button_text (str): Text to display on download button (e.g. 'click here to download file')
            pickle_it (bool): If True, pickle file.
            Returns:
            -------
            (str): the anchor tag to download object_to_download
            Examples:
            --------
            download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
            download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
            """
            # if pickle_it:
            #     try:
            #         object_to_download = pickle.dumps(object_to_download)
            #     except pickle.PicklingError as e:
            #         st.write(e)
            #         return None

            # else:
            #     if isinstance(object_to_download, bytes):
            #         pass

            #     elif isinstance(object_to_download, pd.DataFrame):
            #         object_to_download = object_to_download.to_csv(index=False)

            #     # Try JSON encode for everything else
            #     else:
            #         object_to_download = json.dumps(object_to_download)

            try:
                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(object_to_download.encode()).decode()
            except AttributeError as e:
                b64 = base64.b64encode(object_to_download).decode()

            button_uuid = str(uuid.uuid4()).replace("-", "")
            button_id = re.sub("\d+", "", button_uuid)

            custom_css = f""" 
                <style>
                    #{button_id} {{
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        background-color: rgb(255, 255, 255);
                        color: rgb(38, 39, 48);
                        padding: .25rem .75rem;
                        position: relative;
                        text-decoration: none;
                        border-radius: 4px;
                        border-width: 1px;
                        border-style: solid;
                        border-color: rgb(230, 234, 241);
                        border-image: initial;
                    }} 
                    #{button_id}:hover {{
                        border-color: rgb(246, 51, 102);
                        color: rgb(246, 51, 102);
                    }}
                    #{button_id}:active {{
                        box-shadow: none;
                        background-color: rgb(246, 51, 102);
                        color: white;
                        }}
                </style> """

            dl_link = (
                custom_css
                + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
            )
            # dl_link = f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}"><input type="button" kind="primary" value="{button_text}"></a><br></br>'

            st.markdown(dl_link, unsafe_allow_html=True)


        @st.cache(allow_output_mutation=True, suppress_st_warning=True)
        def load_csv(upload_file):
            csv = pd.read_csv(upload_file)
            return csv

        st.set_page_config(page_title="Green Energy Platform - Conectando Energía Verde", page_icon="/home/dakeh/Escritorio/rebornsdc/app/data/img/greenChain.png",layout='wide', initial_sidebar_state='expanded')
        
        st.sidebar.image('/home/dakeh/Escritorio/rebornsdc/app/data/img/greenChain.png', width=150)

        username = st.sidebar.text_input("Introduzca su usuario:")
        password = st.sidebar.text_input(
            "Introduzca su contraseña:", type='password')
            
        # Se hashea la contraseña introducida y se comprueba que coincide con el hash registrado para ese usuario en la base de datos

        if st.sidebar.checkbox("Iniciar Sesión"):
            create_usertable()

            hash_passwd = make_hashes(password)

            result = login_user(username, check_hashes(password, hash_passwd))
        # Si el resultado es positivo, se muestra el menú principal con todos los servicios
            if result:

                st.success("¡Bienvenid@ de nuevo {}!".format(username))
                app = st.sidebar.selectbox(
                    'Menú Principal',
                    self.apps,
                    format_func=lambda app: app['title'])
                app['function']()
            else:
                st.warning("Usuario/Contraseña incorrectos")

        else:
            st.info(
                "Por favor, inicia sesión para ver el menú de usuario. Recuerde que tiene el usuario en el email")

        st.sidebar.warning(
            "* Mantenga marcada la casilla para conservar la sesión.")

        hide_footer_style = """
        <style>
        .reportview-container .main footer {visibility: hidden;}    
        """
        st.markdown(hide_footer_style, unsafe_allow_html=True)