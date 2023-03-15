import streamlit as st 
from PIL import Image 
import time
import streamlit.components.v1 as component
st.set_page_config(menu_items={"Get Help":"https://www.google.com", "Report a Bug":"https://www.google.com", "About":"https://www.google.com" }, page_title='Bitirme Projesi', page_icon='🚀', layout='wide')

st.title('Yasin Ünal')

component.iframe(src="https://dawn-squash-710.notion.site/Bitirme-Projesi-d508765de5d54b70a099ac8eccdea5c2")

# Using "with" notation
def sidebarIcin():
    """
    with st.sidebar:
        add_radio = st.radio(
            "Choose a shipping method",
            ("Standard (5-15 days)", "Express (2-5 days)")
        )
        with st.spinner("Loading..."):
            time.sleep(5)
        st.success("Done!")

    add_selectbox = st.sidebar.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone")
    )
    """

c1, c2, c3, c4 = st.columns(4)
c1.image(Image.open('images/1.jpg'))
c2.image(Image.open('images/2.jpg'))
c3.image(Image.open('images/3.jpg'))
c4.image(Image.open('images/4.jpg'))

st.write()




