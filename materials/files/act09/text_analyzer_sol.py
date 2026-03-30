"""
Tutorial 3: Text Analysis Tool
Author: Student
Date: 03/27/2026

This program performs text analysis including word frequency, sentiment analysis,
and visualization. Complete the TODO items below to build a text analyzer.
"""

import streamlit as st

#
#
#
#
# MUST be the first Streamlit command to set page configuration before any other Streamlit commands. On some versions of Streamlit, this may cause an error if not placed at the top. If you encounter an error, move this line to the very top of the file.

st.set_page_config(
    page_title="Text Analysis Tool",
    page_icon="📝",
    layout="wide"
)
#
#
#
#
#

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import nltk
from collections import Counter
import re


# Download required NLTK data (only needs to run once)
@st.cache_resource
def download_nltk_data():
    """Download required NLTK data packages."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

download_nltk_data()

st.title("📝 Text Analysis Tool")
st.write("""
This application analyzes text to provide insights including word frequencies, 
sentiment analysis, and visualizations. You can type or paste text directly, 
or upload a text file for analysis.
""")

st.sidebar.header("📥 Text Input Options")

input_method = st.sidebar.radio(
    "Choose input method:",
    ["Type/Paste Text", "Upload Text File", "Use Sample Text"]
)

text = ""

if input_method == "Type/Paste Text":
    text = st.text_area("Enter your text here:", height=200, 
                        placeholder="Type or paste your text...")

elif input_method == "Upload Text File":
    uploaded_file = st.file_uploader("Choose a .txt file", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.success(f"File '{uploaded_file.name}' loaded successfully!")
        with st.expander("View loaded text"):
            st.text(text[:500] + "..." if len(text) > 500 else text)

else:  # Use Sample Text
    sample_choice = st.selectbox(
        "Choose a sample text:",
        ["Sample 1: Product Review", "Sample 2: News Article", "Sample 3: Story Excerpt"]
    )
    
    # Load sample texts from the data folder
    sample_files = {
        "Sample 1: Product Review": "data/sample_review.txt",
        "Sample 2: News Article": "data/sample_article.txt",
        "Sample 3: Story Excerpt": "data/sample_story.txt"
    }
    
    try:
        with open(sample_files[sample_choice], 'r') as f:
            text = f.read()
        st.success(f"{sample_choice} loaded!")
    except FileNotFoundError:
        st.warning(f"Sample file not found. Please create {sample_files[sample_choice]}")

def clean_text(text):
    """Remove special characters and extra whitespace."""
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

def get_word_frequencies(text, num_words=20):
    """Get the most common words and their frequencies."""
    words = text.lower().split()
    # Remove stopwords
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = [word for word in words if word not in stop_words and len(word) > 2]
    return Counter(words).most_common(num_words)

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
    
    if polarity > 0.1:
        sentiment = "Positive 😊"
    elif polarity < -0.1:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"
    
    return sentiment, polarity, subjectivity

def get_text_statistics(text):
    """Calculate various text statistics."""
    words = text.split()
    sentences = nltk.sent_tokenize(text)
    
    stats = {
        "Total Characters": len(text),
        "Total Characters (no spaces)": len(text.replace(" ", "")),
        "Total Words": len(words),
        "Total Sentences": len(sentences),
        "Unique Words": len(set(words)),
        "Average Word Length": sum(len(word) for word in words) / len(words) if words else 0,
        "Average Sentence Length": len(words) / len(sentences) if sentences else 0,
        "Longest Word": max(words, key=len) if words else "",
        "Shortest Word": min(words, key=len) if words else ""
    }
    
    return stats

if text:
    st.header("📊 Text Analysis Results")
    
    # Basic Text Statistics
    st.subheader("1. Basic Text Statistics")
    stats = get_text_statistics(text)
    
    # Display in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Words", stats["Total Words"])
        st.metric("Unique Words", stats["Unique Words"])
    
    with col2:
        st.metric("Total Sentences", stats["Total Sentences"])
        st.metric("Total Characters", stats["Total Characters"])
    
    with col3:
        st.metric("Avg Word Length", f"{stats['Average Word Length']:.1f}")
        st.metric("Avg Sentence Length", f"{stats['Average Sentence Length']:.1f}")
    
    with col4:
        st.metric("Longest Word", stats["Longest Word"][:15] + "..." if len(stats["Longest Word"]) > 15 else stats["Longest Word"])
        st.metric("Shortest Word", stats["Shortest Word"])

else:
    st.info("👈 Please enter or upload text to begin analysis.")
    st.stop()  # Stop execution here if no text

st.subheader("2. Sentiment Analysis")

sentiment, polarity, subjectivity = analyze_sentiment(text)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Overall Sentiment", sentiment)

with col2:
    st.metric("Polarity Score", f"{polarity:.3f}")
    st.caption("(-1: negative, 0: neutral, +1: positive)")

with col3:
    st.metric("Subjectivity Score", f"{subjectivity:.3f}")
    st.caption("(0: objective, 1: subjective)")

# Visualize polarity
fig, ax = plt.subplots(figsize=(10, 2))
ax.barh(['Polarity'], [polarity], color='green' if polarity > 0 else 'red' if polarity < 0 else 'gray')
ax.set_xlim(-1, 1)
ax.set_xlabel('Sentiment Polarity')
ax.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
st.pyplot(fig)

st.subheader("3. Word Frequency Analysis")

# Get word frequencies
num_words = st.slider("Number of top words to display:", 5, 50, 20)
cleaned_text = clean_text(text)
word_freq = get_word_frequencies(cleaned_text, num_words)

if word_freq:
    # Create DataFrame for display
    df_freq = pd.DataFrame(word_freq, columns=["Word", "Frequency"])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(df_freq, use_container_width=True, height=400)
    
    with col2:
        # Bar chart of word frequencies
        fig, ax = plt.subplots(figsize=(10, 8))
        words = [item[0] for item in word_freq]
        freqs = [item[1] for item in word_freq]
        ax.barh(words[::-1], freqs[::-1], color='skyblue')
        ax.set_xlabel('Frequency')
        ax.set_title(f'Top {num_words} Most Common Words')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
else:
    st.warning("No meaningful words found for frequency analysis.")

st.subheader("4. Word Cloud Visualization")

if cleaned_text:
    # Generate word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(cleaned_text)
    
    # Display word cloud
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Word Cloud - Larger words appear more frequently', fontsize=16)
    st.pyplot(fig)
    
    st.info("💡 Tip: Larger words appear more frequently in the text.")
else:
    st.warning("Not enough text to generate a word cloud.")

st.header("🔄 Compare Two Texts")

with st.expander("Click to compare two texts"):
    st.write("Enter two texts to compare their statistics and sentiment:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Text A")
        text_a = st.text_area("Enter first text:", height=150, key="text_a")
    
    with col2:
        st.subheader("Text B")
        text_b = st.text_area("Enter second text:", height=150, key="text_b")
    
    if st.button("Compare Texts") and text_a and text_b:
        st.subheader("Comparison Results")
        
        # Get statistics for both texts
        stats_a = get_text_statistics(text_a)
        stats_b = get_text_statistics(text_b)
        
        # Create comparison DataFrame
        comparison_data = {
            "Metric": ["Total Words", "Unique Words", "Total Sentences", 
                      "Avg Word Length", "Avg Sentence Length"],
            "Text A": [
                stats_a["Total Words"],
                stats_a["Unique Words"],
                stats_a["Total Sentences"],
                f"{stats_a['Average Word Length']:.1f}",
                f"{stats_a['Average Sentence Length']:.1f}"
            ],
            "Text B": [
                stats_b["Total Words"],
                stats_b["Unique Words"],
                stats_b["Total Sentences"],
                f"{stats_b['Average Word Length']:.1f}",
                f"{stats_b['Average Sentence Length']:.1f}"
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
        
        # Compare sentiments
        sentiment_a, polarity_a, _ = analyze_sentiment(text_a)
        sentiment_b, polarity_b, _ = analyze_sentiment(text_b)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Text A Sentiment", sentiment_a, delta=f"{polarity_a:.3f}")
        with col2:
            st.metric("Text B Sentiment", sentiment_b, delta=f"{polarity_b:.3f}")

st.header("🔬 Advanced Analysis")

col1, col2 = st.columns(2)

with col1:
    if st.checkbox("Show Sentence Breakdown"):
        st.subheader("Sentence Analysis")
        sentences = nltk.sent_tokenize(text)
        for i, sentence in enumerate(sentences[:10], 1):  # Show first 10
            st.write(f"**Sentence {i}:** {sentence}")
        if len(sentences) > 10:
            st.info(f"... and {len(sentences) - 10} more sentences")

with col2:
    if st.checkbox("Show Word Length Distribution"):
        st.subheader("Word Length Distribution")
        words = text.split()
        word_lengths = [len(word) for word in words]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(word_lengths, bins=20, color='lightcoral', edgecolor='black')
        ax.set_xlabel('Word Length (characters)')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Word Lengths')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

st.header("💾 Export Results")

if text:
    # Prepare results for export
    stats = get_text_statistics(text)
    sentiment, polarity, subjectivity = analyze_sentiment(text)
    
    results_text = f"""
TEXT ANALYSIS RESULTS
=====================

BASIC STATISTICS:
- Total Words: {stats['Total Words']}
- Unique Words: {stats['Unique Words']}
- Total Sentences: {stats['Total Sentences']}
- Average Word Length: {stats['Average Word Length']:.2f}
- Average Sentence Length: {stats['Average Sentence Length']:.2f}

SENTIMENT ANALYSIS:
- Overall Sentiment: {sentiment}
- Polarity: {polarity:.3f}
- Subjectivity: {subjectivity:.3f}

MOST COMMON WORDS:
"""
    
    cleaned_text = clean_text(text)
    word_freq = get_word_frequencies(cleaned_text, 10)
    for word, freq in word_freq:
        results_text += f"- {word}: {freq}\n"
    
    st.download_button(
        label="Download Analysis Report",
        data=results_text,
        file_name="text_analysis_report.txt",
        mime="text/plain"
    )

# Sidebar tips
st.sidebar.write("---")
st.sidebar.header("💡 Tips & Information")
st.sidebar.write("""
**How to use this tool:**
1. Choose your input method
2. Enter or upload text
3. Explore the analysis results
4. Download your report

**What is Sentiment Analysis?**
Determines whether text is positive, negative, or neutral based on word choice and context.

**What are Stopwords?**
Common words like "the", "and", "is" that are filtered out to focus on meaningful words.

**Bring Your Own Text:**
Try analyzing:
- Book excerpts
- News articles
- Social media posts
- Your own writing
""")

# Footer
st.write("---")
st.success("✅ Tutorial 3 Complete! You've learned text analysis, sentiment analysis, and NLP basics.")
