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

def compress_code(code):
    # Remove comments
    tokens = [tok for tok in tokenize.generate_tokens(code.splitlines(True).__next__)]
    # Combine tokens into chunks of up to 2000 tokens
    chunks = [tokens[i:i+2000] for i in range(0, len(tokens), 2000)]
    # Convert chunks back into code strings
    compressed_code = [''.join([t[1] for t in chunk]) for chunk in chunks]
    return compressed_code

def main():
    st.title('My Streamlit App')
    
    # Add a selectbox to the sidebar:
    language = st.sidebar.selectbox(
        'Select a language',
        ['English', 'Czech', 'German', 'Spanish', 'French', 'Italian', 'Dutch', 'Polish', 'Portuguese', 'Slovak', 'Swedish']
    )
    
    # Add a textarea to the app:
    code = st.text_area('Enter some Python code')
    
    # Add a button to the app:
    if st.button('Compress Code'):
        compressed_code = compress_code(code)
        st.write(compressed_code)
    
    prompt = st.text_input('Enter a prompt:')
    
    if st.button('Generate Text'):
        text = generate_text(prompt)
        st.write(text)
        
        if st.button('Summarize Text'):
            summary = summarize_text(text)
            st.write(summary)

if __name__ == '__main__':
    main()