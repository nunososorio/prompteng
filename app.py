import streamlit as st
from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def generate_text(prompt):
    generator = pipeline('text-generation', model='gpt2')
    text = generator(prompt, max_length=2000)[0]['generated_text']
    return text

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=3)
    return ' '.join([str(sentence) for sentence in summary])

st.title('Text Generation and Summarization')
prompt = st.text_input('Enter a prompt:')
if st.button('Generate Text'):
    text = generate_text(prompt)
    st.write(text)
if st.button('Summarize Text'):
    summary = summarize_text(text)
    st.write(summary)