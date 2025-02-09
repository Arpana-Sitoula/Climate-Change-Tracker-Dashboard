import streamlit as st
from streamlit_option_menu import option_menu
from Fun import fun
from Dashboard import dash
from Analytics import analytics

#Page configuration
st.set_page_config(
    page_title="Climate Change Tracker Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Analytics", "Fun"],
    default_index=0,
    orientation="horizontal",
    styles= {
       "container" : {"padding": "0!important"},
       "nav-link": {
           "font-size": "25px",
            "text-align" : "left",
            "margin": "0px"   
            },
    },
)

if selected == "Dashboard":
    dash()
if selected == "Fun":
    fun()
if selected == "Analytics":
    analytics()