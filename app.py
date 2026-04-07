import streamlit as st 
from PIL import Image 
import numpy as np
import cv2
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    h1 {
        color: #00ffcc;
        text-align: center;
    }
    .stButton>button {
        background-color: #00ffcc;
        color: black;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)
def compare_images(img1, img2):
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    error = np.sum((img1 - img2) ** 2)
    mse = error / float(img1.shape[0] * img1.shape[1])
    similarity = 1 - (mse / 255)
    return similarity

st.set_page_config(page_title="Content Misuse Detection", layout="centered")

st.title("Content Misuse Detection System")
st.header("Upload Original Content")
original = st.file_uploader("Upload Original Image", type=["jpg", "jpeg", "png", "txt", "pdf"])

st.header("Upload Suspected Content")
suspect = st.file_uploader("Upload Suspected Image", type=["jpg", "jpeg", "png", "txt", "pdf"])

if original is not None and suspect is not None:
    img1 = Image.open(original)
    img2 = Image.open(suspect)

    st.image([img1, img2], caption=["Original Content", "Suspected"], width=300)
    img1_np = np.array(img1)
    img2_np = np.array(img2)
    similarity = compare_images(img1_np, img2_np)
    st.subheader(f"Similarity Score: {similarity:.2f}")

    if similarity > 0.7:
        st.error("Unauthorized Use Detected!")
    else:
        st.success("No Match Found")

    