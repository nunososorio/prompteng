import nltk
nltk.download('punkt')
import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.kl import KLSummarizer
import black

def summarize_text(text, language, summary_size, summarizer_type):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    if summarizer_type == 'LsaSummarizer':
        summarizer = LsaSummarizer()
    elif summarizer_type == 'LexRankSummarizer':
        summarizer = LexRankSummarizer()
    elif summarizer_type == 'LuhnSummarizer':
        summarizer = LuhnSummarizer()
    elif summarizer_type == 'KLSummarizer':
        summarizer = KLSummarizer()
    summary = summarizer(parser.document, summary_size)
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
    summary_size = st.slider('Summary size', 1, 20, 10)
    summarizer_type = st.selectbox("Select Sumy summarizer type", ["LsaSummarizer", "LexRankSummarizer", "LuhnSummarizer", "KLSummarizer"])
    if st.button("Summarize"):
        summary = summarize_text(text, language, summary_size, summarizer_type)
        st.write(summary)
        st.write(f"Token size: {len(summary.split())}")
        scaffolding_sentences = ["Perform sentiment analysis", "The main point of this text is", "The purpose of this research is to", "Generate a 100chr summary", "This topic is important because", "A common misconception related to this text is:", "The most significant factor in the text is", "One possible solution to this problem is", "The most important thing to remember about this text is", "Another way to think about this text is", "Rewrite for clarity", "The key takeaway from this article is", "Copy-edit", "One limitation of this study is that", "The implications of the text are", "This research contributes to our understanding of", "Proofread", "Revise", "Format", "Proofread, revise, copy-edit and format"]
        selected_sentence = st.selectbox("Select scaffolding sentence", scaffolding_sentences)
        text = st.text_area("Formulate your prompt", f'{selected_sentence}: {summary}')
        
elif prompt_type == "Code":
    st.header("Code")
    code = st.text_area("Enter Python code")
    if st.button("Format the code"):
        try:
            formatted_code = black.format_str(code, mode=black.Mode())
            st.code(formatted_code)
            st.write(f"Token size: {len(formatted_code.split())}")
            scaffolding_sentences = ["Let’s take a step back and think about what we want to achieve.", "What are the inputs we need to consider?", "What are the outputs we expect?", "How can I alter the code to help debugging?", "Let’s write some pseudocode to help us think through the problem.", "Add print statements to the code to track progress.", "Let’s start by writing some tests to make sure our code works.", "What are some potential issues with our code?", "How can we make our code more efficient?", "How can we make our code more readable?", "What are some ways we can improve our code?", "Let’s refactor our code to make it more modular.", "What are some ways we can optimize our code?", "Let’s add some error handling to our code.", "How can we make our code more maintainable?", "Does the code below follows best practices for writing clean code?", "Let’s review our code and make sure it meets our requirements."]
            selected_sentence = st.selectbox("Select scaffolding sentence", scaffolding_sentences)
            text = st.text_area("Formulate your prompt", f'{selected_sentence}: {formatted_code}')
        except Exception as e:
            st.write(f"Error: {e}")
