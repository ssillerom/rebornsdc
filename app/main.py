import streamlit as st
import requests

from data.bin.multiApp import MultiApp
from data.bin import landing, admin_panel, playground, demo

app = MultiApp()

app.add_app("Landing", landing.app)
app.add_app("Admin", admin_panel.app)
app.add_app("Playground", playground.app )
app.add_app("Demo", demo.app )

app.run()

