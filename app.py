import nltk
nltk.download('punkt')
import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pyperclip

def summarize_text(text, language):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 10)
    return ' '.join([str(sentence) for sentence in summary])

def remove_annotations(code):
    lines = code.split('\n')
    lines = [line for line in lines if not line.strip().startswith('#')]
    return '\n'.join(lines)

st.set_page_config(page_title="AI Prompt Engineering", page_icon=":memo:", layout="wide")

st.sidebar.title("AI Prompt Engineering")
prompt_type = st.sidebar.selectbox("Select prompt type", ["Text", "Code"])

if prompt_type == "Text":
    st.header("Text")
    language = st.selectbox("Select language", ["czech", "dutch", "english", "french", "german", "italian", "portuguese", "romanian", "russian", "slovak", "spanish"])
    text = st.text_area("Enter text to summarize")
    if st.button("Summarize"):
        summary = summarize_text(text, language)
        st.write(summary)
        #pyperclip.copy(summary)
        st.write(f"Token size: {len(summary.split())}")          

elif prompt_type == "Code":
    st.header("Code")
    code = st.text_area("Enter Python code")
    if st.button("Clean the code"):
        cleaned_code = remove_annotations(code)
        st.code(cleaned_code)
        st.write(f"Token size: {len(cleaned_code.split())}")
