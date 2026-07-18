import pathlib
import streamlit as st

def load_css():
    """Load the custom CSS file if it exists."""
    css_path = pathlib.Path(__file__).parent / "style.css"
    if css_path.is_file():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
