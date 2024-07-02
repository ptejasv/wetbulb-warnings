import streamlit as st
import requests

@st.cache_data
def intro():
    st.title("Live Wet-Bulb temperature in Singapore")

if __name__ == "__main__":
    intro()
