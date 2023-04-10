import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

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
    language = st.selectbox("Select language", ["english", "french", "german", "spanish"])
    text = st.text_area("Enter text to summarize")
    if st.button("Summarize"):
        summary = summarize_text(text, language)
        chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]
        for chunk in chunks:
            st.write(chunk)
elif prompt_type == "Code":
    st.header("Code")
    code = st.text_area("Enter Python code")
    if st.button("Remove annotations"):
        cleaned_code = remove_annotations(code)
        chunks = [cleaned_code[i:i+2000] for i in range(0, len(cleaned_code), 2000)]
        for chunk in chunks:
            st.code(chunk)