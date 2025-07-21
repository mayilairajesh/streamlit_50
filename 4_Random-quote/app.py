import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Inspirational Quote Generator",
    page_icon="✨",
    layout="centered"
)

# Styling
st.markdown("""
    <style>
        .quote-box {
            padding: 2rem;
            font-size: 1.5rem;
            font-style: italic;
            color: #2C3E50;
            background-color: #F8F9FA;
            border-left: 5px solid #4CAF50;
            border-radius: 8px;
            margin: 2rem 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .author {
            text-align: right;
            font-weight: bold;
            color: #1A5276;
            margin-top: 1rem;
        }
        .refresh-btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        .refresh-btn:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found. Please set it in .env or environment.")
        st.stop()
    return Groq(api_key=api_key)

client = get_client()

# Predefined fallback quotes (in case of API failure)
fallback_quotes = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("It always seems impossible until it’s done.", "Nelson Mandela"),
    ("Success is not final, failure is not fatal: It is the courage to continue that counts.", "Winston Churchill"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson")
]

# Function to generate quote using Groq
def generate_inspiration_quote():
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Fast & efficient for short creative tasks
            messages=[
                {
                    "role": "system",
                    "content": "You are an inspirational quote generator. "
                               "Respond with exactly one quote in the format: "
                               "\"[quote]\" — [author]"
                },
                {
                    "role": "user",
                    "content": "Generate a unique and uplifting inspirational quote."
                }
            ],
            temperature=0.9,
            max_tokens=100,
            stream=False,
        )
        quote_text = response.choices[0].message.content.strip()

        # Basic parsing
        if "—" in quote_text:
            quote, author = quote_text.split("—", 1)
            quote = quote.strip().strip('"')
            author = author.strip()
        else:
            # Fallback parsing
            parts = quote_text.split(" - ")
            if len(parts) == 2:
                quote, author = parts
            else:
                quote, author = quote_text, "Unknown"

        return quote, author

    except Exception as e:
        st.warning("Could not reach Groq API. Showing a classic quote.")
        return random.choice(fallback_quotes)

# App title
st.title("✨ Inspirational Quote Generator")

# Session state for current quote
if 'quote' not in st.session_state:
    st.session_state.quote = ""
    st.session_state.author = ""

# Button logic
if st.button("🎯 Refresh Quote", key="refresh"):
    with st.spinner("Generating inspiration..."):
        quote, author = generate_inspiration_quote()
        st.session_state.quote = quote
        st.session_state.author = author

# Initial load
if not st.session_state.quote:
    with st.spinner("Loading your first quote..."):
        quote, author = generate_inspiration_quote()
        st.session_state.quote = quote
        st.session_state.author = author

# Display quote
st.markdown('<div class="quote-box">', unsafe_allow_html=True)
st.write(st.session_state.quote)
st.markdown(f'<div class="author">— {st.session_state.author}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Powered by Groq & Llama3 • Stay inspired every day 💡")