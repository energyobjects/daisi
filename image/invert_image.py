import numpy as np
import streamlit as st
from PIL import Image, ImageOps

def invert(image):
    img = np.array(image)
    img = 255 - img
    pil_img = Image.fromarray(img)
    return pil_img

def st_ui():
    st.title("Image Inversion")
    user_image = st.sidebar.file_uploader("Load your own image")
    if user_image is not None:
        i = Image.open(user_image)
    else:
        i = Image.open('daisy.jpg')
    w, h = i.size
    if h > 720:
        i = i.resize((int((float(i.size[0]) * float((720 / float(i.size[1]))))), 720), Image.NEAREST)
    st.header("Original image")
    st.image(i)
    draw_landmark_button = st.button('Invert Image')
    result = invert(i)
    if draw_landmark_button:
        st.header("Inverted Image")
        st.image(result)


if __name__ == '__main__':
    st_ui()
