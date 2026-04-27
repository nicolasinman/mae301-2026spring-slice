# Text Analysis Program
# This program reads a text file, analyzes it, and creates a data point


import sys
import os
import csv
from datetime import datetime
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

# Read market data from market_data.csv in the current directory
market_filename = "market_data.csv"
market_filepath = os.path.join(os.getcwd(), market_filename)

try:
    with open(market_filepath, 'r', encoding='utf-8', newline='') as market_file:
        market_reader = csv.DictReader(market_file)
        date_column = next((field for field in market_reader.fieldnames or [] if field.strip().lower() == "date"), None)
        direction_column = next((field for field in market_reader.fieldnames or [] if field.strip() == "sp500_direction"), None)

        if date_column is None:
            print(f"Error: Column 'date' not found in '{market_filename}'.")
            sys.exit(1)

        if direction_column is None:
            print(f"Error: Column 'sp500_direction' not found in '{market_filename}'.")
            sys.exit(1)

        sp500_direction_by_date = {}
        for row_number, row in enumerate(market_reader, start=2):
            date_text = row[date_column].strip()
            direction = row[direction_column].strip().lower()

            try:
                market_date = datetime.strptime(date_text, "%m/%d/%Y").date()
            except ValueError:
                print(f"Error: Invalid date value on row {row_number}: {row[date_column]}")
                sys.exit(1)

            if direction == "up":
                sp500_direction_by_date[market_date] = 1
            elif direction == "down":
                sp500_direction_by_date[market_date] = -1
            else:
                print(f"Error: Invalid sp500_direction value on row {row_number}: {row[direction_column]}")
                sys.exit(1)
except FileNotFoundError:
    print(f"Error: File '{market_filename}' not found in current directory: {os.getcwd()}")
    sys.exit(1)
except Exception as e:
    print(f"Error reading market data file: {e}")
    sys.exit(1)

# Split text into blocks separated by blank lines (gaps)
text_blocks = [block.strip() for block in text_block.split('\n\n') if block.strip()]

# List to store all data points
all_data_points = []

# Process each text block
for block in text_blocks:
    words = block.split()
    date_text = words[0].strip('.,!?;:"')
    
    try:
        block_date = datetime.strptime(date_text, "%m/%d/%Y").date()
    except ValueError:
        print(f"Error: Text block must start with a date in mm/dd/yyyy format. Found: {words[0]}")
        sys.exit(1)
    
    # Count the number of words in the text block
    word_count = len(words)
    
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
    
    # Create a data point as a column vector (list) with date, word count, emotional count, sentiment difference, and keywords
    data_point = [block_date, word_count, emotional_count, sentiment_diff, keywords]
    all_data_points.append(data_point)

# Filter data points with keywords contained in "S&P500" (case insensitive)
sp500_target = "s&p500"
sp500_data_points = [dp for dp in all_data_points if any(phrase.lower() in sp500_target for phrase in dp[4])]

# Create a matrix with date, word count, emotional count, and sentiment difference columns
full_data_matrix = np.array([[dp[0], dp[1], dp[2], dp[3]] for dp in all_data_points], dtype=object).reshape(-1, 4)
sp500_data_matrix = np.array([[dp[0], dp[1], dp[2], dp[3]] for dp in sp500_data_points], dtype=object).reshape(-1, 4)

# Create final data matrix with matching date, sentiment score, and S&P500 direction
final_data_rows = []
sp500_direction_values = []

for row in sp500_data_matrix:
    block_date = row[0]

    if block_date in sp500_direction_by_date:
        direction_value = sp500_direction_by_date[block_date]
        sp500_direction_values.append(direction_value)
        final_data_rows.append([block_date, row[3], direction_value])

sp500_direction_vector = np.array(sp500_direction_values).reshape(-1, 1)
final_data_matrix = np.array(final_data_rows, dtype=object).reshape(-1, 3)

# Calculate LSRL values using sentiment score as x and S&P500 direction as y
if final_data_matrix.shape[0] < 2:
    print("Error: At least two matching data points are required to calculate LSRL values.")
    sys.exit(1)

lsrl_data = final_data_matrix[:, 1:3].astype(float)
x_values = lsrl_data[:, 0]
y_values = lsrl_data[:, 1]

x_deviation = x_values - np.mean(x_values)
y_deviation = y_values - np.mean(y_values)
x_sum_squares = np.sum(x_deviation ** 2)
y_sum_squares = np.sum(y_deviation ** 2)

if x_sum_squares == 0 or y_sum_squares == 0:
    print("Error: LSRL values require variation in both sentiment scores and S&P500 directions.")
    sys.exit(1)

slope = np.sum(x_deviation * y_deviation) / x_sum_squares
r_value = np.sum(x_deviation * y_deviation) / np.sqrt(x_sum_squares * y_sum_squares)
r_squared = r_value ** 2

predictor_label = "negative predictor" if slope < 0 else "predictor"

if r_squared < 0.3:
    prediction_statement = f"This person is probably an unreliable {predictor_label} of S&P500"
elif r_squared < 0.7:
    prediction_statement = f"This person may be a good {predictor_label} of S&P500"
else:
    prediction_statement = f"This person is a great {predictor_label} of S&P500"

# Print all data points stacked
#print(f"Data points: {all_data_points}")
#print(f"\nFull Data matrix (rows = text blocks, columns = [word_count, emotional_count, sentiment_score]):")
#print(full_data_matrix)
#print(f"\nS&P500 data points: {sp500_data_points}")
#print(sp500_data_points)

#print(sp500_data_matrix)
#print(sp500_direction_vector)
print(final_data_matrix)
print(f"Slope: {slope}")
print(f"r: {r_value}")
print(f"r^2: {r_squared}")
print(prediction_statement)



