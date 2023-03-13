import streamlit as st 
from PIL import Image 
import time

st.set_page_config(menu_items={"Get Help":"https://www.google.com", "Report a Bug":"https://www.google.com", "About":"https://www.google.com" }, page_title='Bitirme Projesi', page_icon='🚀', layout='wide')

st.title('Yasin Ünal')

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")


c1, c2, c3, c4 = st.columns(4)
c1.image(Image.open('images/1.jpg'))
c2.image(Image.open('images/2.jpg'))
c3.image(Image.open('images/3.jpg'))
c4.image(Image.open('images/4.jpg'))

st.write(
    """
    The crypto industry continues to progress and its development has never stopped. Contributors
    of each blockchain keep developing each segment of the industry and the whole crypto ecosystem.
    # Deneme  
    
    * Burada text kısmı bildiğimiz Markdown syntax

    [](2.jpg)

    Each of these Pages addresses a different segment of the crypto industry. Within each segment
    (Macro, Transfers, Swaps, NFTs, etc.) you are able to filter your desired blockchains to
    narrow/expand the comparison. By selecting a single blockchain, you can observe a deep dive
    into that particular network.
    All values for amounts, prices, and volumes are in **U.S. dollars** and the time frequency of the
    analysis was limited to the last **30 days**.
    """
)

st.subheader('Methodology')

st.write(
    """ 
    ### Methodology \n deneme
    """
)

