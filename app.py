import streamlit as st
import heapq
from collections import defaultdict


def huffman_encoding(text):
    # Calculate frequency of characters in text
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    # Create a min heap of character frequencies
    heap = [[f, [char, ""]] for char, f in freq.items()]
    heapq.heapify(heap)

    # Build Huffman tree by combining two lowest frequency characters
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Create Huffman codes for each character
    codes = dict(heapq.heappop(heap)[1:])
    return codes


def encode_text(text, codes):
    encoded_text = ""
    for char in text:
        encoded_text += codes[char]
    return encoded_text


def chunk_text(encoded_text, chunk_size):
    chunks = [encoded_text[i:i+chunk_size] for i in range(0, len(encoded_text), chunk_size)]
    return chunks


def main():
    st.title("Huffman Encoder")

    # Take user input
    input_text = st.text_input("Enter text to encode:", value="", max_chars=None, key=None, type='default')

    # Encode text with Huffman coding
    if input_text:
        codes = huffman_encoding(input_text)
        encoded_text = encode_text(input_text, codes)

        # Output encoded text in chunks of 2000 characters
        encoded_chunks = chunk_text(encoded_text, 2000)
        for i, chunk in enumerate(encoded_chunks):
            st.write(f"Chunk {i+1}: {chunk}")


if __name__ == "__main__":
    main()
