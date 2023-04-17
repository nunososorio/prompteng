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
import autopep8
import re
import ast
import astunparse


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
    scaffolding_sentences = ["develop+extend+support(ideas), vocab(wide+natural+sophisticated), grammar(wide+flexible), cohesion(logical+smooth), clarity(precise+concise), engagement(attention+interest), mood(objective+explanatory), viewpoint(forward_looking)", "The main point of this text is", "The purpose of this research is to", "Generate a 100chr summary", "This topic is important because", "A common misconception related to this text is:", "The most significant factor in the text is", "One possible solution to this problem is", "The most important thing to remember about this text is", "Another way to think about this text is", "Rewrite for clarity", "The key takeaway from this article is", "Copy-edit", "One limitation of this study is that", "The implications of the text are", "This research contributes to our understanding of", "Proofread", "Revise", "Format", "Proofread, revise, copy-edit and format"]
    selected_sentence = st.selectbox("Select scaffolding sentence", scaffolding_sentences)
    
    prompt_text = st.text_area("Formulate your prompt", value=selected_sentence)
    
    languages = ["czech", "dutch", "english", "french", "german", "italian", "portuguese", "romanian", "russian", "slovak", "spanish"]
    language = st.selectbox("Select language", languages)
    text = st.text_area("Enter text to summarize")
    summary_size = st.slider('Summary size', 1, 20, 10)
    summarizer_type = st.selectbox("Select Sumy summarizer type", ["LsaSummarizer", "LexRankSummarizer", "LuhnSummarizer", "KLSummarizer"])
    if st.button("Summarize"):
        summary = summarize_text(text, language, summary_size, summarizer_type)
        st.write(summary)
        st.write(f"Token size: {len(summary.split())}")
        
elif prompt_type == "Code":
    st.header("Code")
    
    scaffolding_sentences = ["Let’s step back & think about our goal:", "What inputs we need:", "What outputs we expect:", "How can I change the code for debugging:", "Write pseudocode to think the problem:", "Add print statements to track progress:", "Write tests to ensure code works:", "What potential code issues:", "How can code be efficient:", "How can code be more readable:", "How can we improve code:", "Let’s refactor code to make it modular:", "What ways can we optimize code:", "Add error handling to code:", "How to make our code more maintainable:", "Does code follow best practices for clean code:", "Review code & ensure it meets requirements:", "Break down problem into smaller parts:", "Identify edge cases:", "Check for common errors:", "Use version control:", "Document code clearly:", "Use consistent coding style:", "Write clear & concise GitHub README:", "Include installation & usage instructions:", "Write step-by-step tutorial:", "Explain concepts & features in vignette:", "Include detailed info in manual:", "Document code & API clearly:", "Generate requirements.txt with dependencies:", "Ensure it is up-to-date:", "Use clear formatting & structure:", "Provide troubleshooting info:"]    
    selected_sentence = st.selectbox("Select scaffolding sentence", scaffolding_sentences)
    
    prompt_text = st.text_area("Formulate your prompt", value=selected_sentence)
    
    code = st.text_area("Enter Python code to compress")
    original_code_length = len(code)
    if st.button("Shogtongue the code!"):
        try:
            # Remove unnecessary white space
            code = autopep8.fix_code(code)

            # Use list comprehension
            formatted_code = ''.join([line.strip() for line in black.format_str(code, mode=black.Mode(target_versions={black.TargetVersion.PY38})).split('\n')])

            st.code(formatted_code)

            # Use f-strings
            compression_ratio = (1 - len(formatted_code) / original_code_length) * 100
            st.success(f'Compression ratio: {compression_ratio:.2f}%')
            st.write(f"Token size: {len(formatted_code.split())}")
            st.write(f"Length: {len(formatted_code)}")
        except Exception as e:
            st.write(f"Error: {e}")
            
    def shorten_names(node):
        if isinstance(node, ast.Name):
            node.id = node.id[0]
        for child in ast.iter_child_nodes(node):
            shorten_names(child)

    if st.button("Jungle mode-Shogtongue the code!"):
        try:
            # Parse the code into an AST
            tree = ast.parse(code)

            # Shorten variable and function names
            shorten_names(tree)

            # Unparse the modified AST back into code
            code = astunparse.unparse(tree)

            # Remove comments
            code = re.sub(r'#.*', '', code)

            # Remove unnecessary white space
            code = re.sub(r'\s+', ' ', code)

            # Remove line breaks
            junglecode = re.sub(r'\n', '', code)

            st.code(junglecode)

            # Use f-strings
            compression_ratio = (1 - len(junglecode) / original_code_length) * 100
            st.success(f'Compression ratio: {compression_ratio:.2f}%')
            st.write(f"Token size: {len(junglecode.split())}")
            st.write(f"Length: {len(junglecode)}")
            
        except Exception as e:
            st.write(f"Error: {e}")
