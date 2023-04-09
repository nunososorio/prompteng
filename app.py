
import streamlit as st
from huffman import HuffmanCoding

def encode_text(text):
    h = HuffmanCoding(text)
    output = h.compress()
    return [output[i:i+2000] for i in range(0, len(output), 2000)]

st.title("AI Pront Engineering - give more info using less characters")
input_text = st.text_input("Enter text to encode:")
if input_text:
    encoded_text = encode_text(input_text)
    st.write("Encoded text:")
    for chunk in encoded_text:
        st.write(chunk)