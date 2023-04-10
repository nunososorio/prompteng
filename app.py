
import nltk
nltk.download('punkt')
import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from abbreviate import abbreviate

def summarize_text(text, language):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 10)
    return ' '.join([str(sentence) for sentence in summary])

def abbreviate_text(text):
    return abbreviate(text)

def remove_annotations(code):
    cleaned_code = ""
    for line in code.split("\n"):
        if "#" in line:
            cleaned_code += line[:line.index("#")] + "\n"
        else:
            cleaned_code += line + "\n"
    return cleaned_code

st.set_page_config(page_title="AI Prompt Engineering", page_icon=":memo:", layout="wide")

st.sidebar.title("AI Prompt Engineering")
prompt_type = st.sidebar.selectbox("Select prompt type", ["Text", "Code"])

if prompt_type == "Text":
    st.header("Text")
    language = st.selectbox("Select language", ["czech", "dutch", "english", "french", "german", "italian", "portuguese", "romanian", "russian", "slovak", "spanish"])
    action = st.selectbox("Select action", ["Summarize", "Abbreviate", "Summarize+Abbreviate"])
    text = st.text_area("Enter text to summarize/abbreviate")
    if st.button(action):
        if action == "Summarize":
            output_text = summarize_text(text, language)
        elif action == "Abbreviate":
            output_text = abbreviate_text(text)
        else:
            summarized_text = summarize_text(text, language)
            output_text = abbreviate_text(summarized_text)
        st.write(output_text)
        st.write(f"Output token size: {len(output_text.split())}")
        if st.button("Copy to clipboard"):
            st.clipboard.write_text(output_text)
            st.write(f"Copied {len(output_text)} characters to clipboard")
elif prompt_type == "Code":
    st.header("Code")
    code = st.text_area("Enter Python code")
    if st.button("Clean the code"):
        cleaned_code = remove_annotations(code)
        st.code(cleaned_code)
        st.write(f"Output token size: {len(cleaned_code.split())}")
        if st.button("Copy to clipboard"):
            st.clipboard.write_text(cleaned_code)
            st.write(f"Copied {len(cleaned_code)} characters to clipboard")