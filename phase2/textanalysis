# Text Analysis Program
# This program reads a text file, analyzes it, and creates a data point


import sys
import os
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
from textblob import TextBlob

# Download the VADER lexicon if not already downloaded
#nltk.download('vader_lexicon', quiet=True)

# Initialize the sentiment analyzer and AI pipelines
analyzer = SentimentIntensityAnalyzer()
sentiment_pipeline = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

# Read text from a .txt file in the current directory
if len(sys.argv) < 2:
    print("Error: Please provide a .txt file as an argument.")
    print("Usage: python textanalysis.py <filename.txt>")
    sys.exit(1)

filename = sys.argv[1]
filepath = os.path.join(os.getcwd(), filename)

try:
    with open(filepath, 'r', encoding='utf-8') as file:
        text_block = file.read()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found in current directory: {os.getcwd()}")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

# Split text into blocks separated by blank lines (gaps)
text_blocks = [block.strip() for block in text_block.split('\n\n') if block.strip()]

# List to store all data points
all_data_points = []

# Process each text block
for block in text_blocks:
    # Count the number of words in the text block
    word_count = len(block.split())
    
    # Count emotional words using VADER lexicon (words that have sentiment scores)
    emotional_count = sum(1 for word in block.lower().split() if word.strip('.,!?;:"') in analyzer.lexicon)
    
    # Use AI-based sentiment analysis for the third data dimension
    sentiment_result = sentiment_pipeline(block)[0]
    if sentiment_result['label'] == 'POSITIVE':
        sentiment_diff = sentiment_result['score']
    else:
        sentiment_diff = -sentiment_result['score']
    
    # Extract important keywords using TextBlob noun phrases
    blob = TextBlob(block)
    keywords = list(blob.noun_phrases)[:5]  # limit to top 5 noun phrases
    
    # Create a data point as a column vector (list) with word count, emotional count, sentiment difference, and keywords
    data_point = [word_count, emotional_count, sentiment_diff, keywords]
    all_data_points.append(data_point)

# Create a matrix with numeric columns (word count, emotional count, sentiment difference)
data_matrix = np.array([[dp[0], dp[1], dp[2]] for dp in all_data_points])

# Print all data points stacked
print(f"Data points: {all_data_points}")
print(f"\nData matrix (rows = text blocks, columns = [word_count, emotional_count, sentiment_score]):")
print(data_matrix)
