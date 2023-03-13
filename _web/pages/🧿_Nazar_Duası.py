import streamlit as st 
from PIL import Image
import numpy as np

st.set_page_config(layout="wide")

st.title("Nazar Duası")

st.write(
    """
    ## Neyse Halim Çıksın Falım

    ### Okunuşu 

    Euzu bi kelimâtillâhi't-tâmmeti min kulli şeytanin ve hammetin ve min külli aynin lammeh.

    ### Anlamı 

    Her türlü şeytandan, zararlı şeylerden ve kem gözlerden bütün kelimeleri yüzü hürmetine Allah'a sığınırım.

    """
)
st.write("--------------------------------")
# -------------------------------------------------------------------------

option = st.selectbox('Seç birini', ('Email','Home Phone', 'Mobile Phone'))

st.write('Your select : ',option)

# -------------------------------------------------------------------------

if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

st.write("--------------------------------")
# ------------------------------------------------------------------------- 

st.write("resim indirme :")
with open("images/3.jpg", "rb") as file:
    btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

st.write("--------------------------------")
# -------------------------------------------------------------------------

options2 = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('You selected:', options2)

st.write("--------------------------------")
# -------------------------------------------------------------------------

values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

st.write("--------------------------------")
# -------------------------------------------------------------------------

title = st.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)

# -------------------------------------------------------------------------

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Check the type of img_array:
    # Should output: <class 'numpy.ndarray'>
    st.write(type(img_array))

    # Check the shape of img_array:
    # Should output shape: (height, width, channels)
    st.write(img_array.shape)

# -------------------------------------------------------------------------

import streamlit.components.v1 as components 

components.html(
    """
        <div> 
            <i> <p> Selam burası html içerik </p> </i>
        </div>
    """
)

components.iframe(src="https://docs.streamlit.io/en/latest",width=500,height=500)

# -------------------------------------------------------------------------
