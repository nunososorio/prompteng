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
        st.write(f"Examples of scaffolding sentences: \n1. \"In this essay, I will argue that...\"\n2. \"The main point of this article is...\"\n3. \"The purpose of this research is to...\"\n4. \"One way to approach this problem is to...\"\n5. \"This topic is important because...\"\n6. \"The main difference between X and Y is...\"\n7. \"A common misconception about X is...\"\n8. \"The most significant factor in X is...\"\n9. \"One possible solution to this problem is...\"\n10. \"The most important thing to remember about X is...\"\n11. \"Another way to think about X is...\"\n12. \"X can be defined as...\"\n13. \"The key takeaway from this article is...\"\n14. \"X has been shown to have a significant impact on Y...\"\n15. \"One limitation of this study is that...\"\n16. \"The implications of X are...\"\n17. \"This research contributes to our understanding of X by...\"\n18. \"X has been the subject of much debate in recent years because...\"\n19. \"One potential application of X is...\"\n20. \"The results of this study suggest that...\"")

elif prompt_type == "Code":
    st.header("Code")
    code = st.text_area("Enter Python code")
    if st.button("Format the code"):
        try:
            formatted_code = black.format_str(code, mode=black.Mode())
            st.code(formatted_code)
            st.write(f"Token size: {len(formatted_code.split())}")
            st.write(f"Examples of scaffolding sentences for code: \n1. \"Let’s take a step back and think about what we want to achieve.\"\n2. \"What are the inputs we need to consider?\"\n3. \"What are the outputs we expect?\"\n4. \"How can I alter the code to add new functionality?\"\n5. \"Let’s write some pseudocode to help us think through the problem.\"\n6. \"Now that we have a plan, give an example of the code.\"\n7. \"Let’s start by writing some tests to make sure our code works.\"\n8. \"What are some potential issues with our code?\"\n9. \"How can we make our code more efficient?\"\n10. \"How can we make our code more readable?\"\n11. \"What are some ways we can improve our code?\"\n12. \"Let’s refactor our code to make it more modular.\"\n13. \"What are some ways we can optimize our code?\"\n14. \"Let’s add some error handling to our code.\"\n15. \"How can we make our code more maintainable?\"\n16. \"What are some best practices for writing clean code?\"\n17. \"Let’s review our code and make sure it meets our requirements.\"")
        except Exception as e:
            st.write(f"Error: {e}")
