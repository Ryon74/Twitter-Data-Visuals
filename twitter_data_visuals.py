# -*- coding: utf-8 -*-
"""Twitter_Data_Visuals.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FVfgdYiphAVfldc-dsT1TlRmt5XEolgh
"""



"""# Twitter Data Visualization"""

# Loading and Preprocessing Text
import re
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from collections import Counter
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
nltk.download('punkt')
nltk.download('punkt_tab')
# Download word list
nltk.download('words')
#Download stop-words
nltk.download('stopwords')

# Load English words into a set
english_vocab = set(words.words())
# Load stopwords for filtering meaningless words
stop_words = set(stopwords.words('english'))

# Load dataset
df = pd.read_csv('AE1_vishing_data_zipped.csv.zip', engine='python')

# Filter only English tweets
df = df[df['lang'] == 'en']

# Function to clean text
def clean_text(text):
    text = str(text).lower()  # Convert to lowercase
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|t\.co/\S+", "", text)
    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", '', text)  # Keep only letters and spaces
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # Tokenize words
    tokens = word_tokenize(text)
    # Remove stopwords and meaningless words
    tokens = [word for word in tokens if word not in stop_words and word in english_vocab]
    return tokens


# Apply cleaning function to the dataset
df['clean_text'] = df['text'].apply(clean_text)

"""# **Analyzing the Tweets of The Top 10 Most Active Users**"""

# Analysing Text

# Get top 10 most active users by tweet count
top_ten_users = df['author_id'].value_counts().head(10)

# Filter dataset to only include tweets from the top 10 users
df_top_users = df[df['author_id'].isin(top_ten_users.index)]

# Dictionary to store processed tweets per user
user_tweets = {user: [] for user in top_ten_users.index}

# Populate dictionary with already preprocessed tweets
for _, row in df_top_users.iterrows():
    user_tweets[row['author_id']].extend(row['clean_text'])  # Use already preprocessed words

#Store words and their usage rates
word_counts = {}

#Store users and their corresponding vocabulary richness scores
vocabulary_richness = {}

# Store all words used by top 10 users
all_words = []

# Process each user's tweets
for user, words in user_tweets.items():

    # Store word frequency count
    word_counts[user] = Counter(words)

    # Calculate vocabulary richness
    vocabulary_richness[user] = len(set(words)) / len(words)

    # Get unique words per user
    all_words.extend(set(words))

# Identify common words appearing in multiple users' tweets 5 or more times
word_freq = Counter(all_words)
common_words = {word for word, count in word_freq.items() if count >= 5}

# Display top 5 words used by each user and their usage rate
print("\n=== Word Frequency for Top 10 Users ===")
for user, freq in word_counts.items():
    top_words = freq.most_common(5)  # Get top 5 words
    print(f"\nTop words for user {user}:")
    for word, count in top_words:
        print(f"  {word}: {count}")
# Display each user's vocabulary richness
print("\n=== Vocabulary Richness per User ===")
for user, richness in vocabulary_richness.items():
    print(f"User {user}: {richness:.4f}")
# Display all words used 5 or more times by multiple users
print("\n=== Common Words Among Users ===")
print(", ".join(common_words))

"""# **Visualizing Data Through Sentiment Scores and Word Clouds**"""

# Visualing Data
import seaborn as sns
from wordcloud import WordCloud

# Convert to datetime format
df['created_at'] = pd.to_datetime(df['created_at'])

# Create date column(only showing year and month)
df['date'] = df['created_at'].dt.strftime('%Y-%m')

# Function to calculate sentiment scores
def sentiment_scores(text):
    text_str = ' '.join(text)  # Join tokenized words into a string
    return TextBlob(text_str).sentiment.polarity  # Calculate sentiment polarity

# Apply sentiment score function
df['sentiment_score'] = df['clean_text'].apply(sentiment_scores)

# Filter for the top 10 users
df_top_10_users = df[df['author_id'].isin(top_ten_users.index)]

# Group by author_id and date
grouped = df_top_10_users.groupby(['author_id', 'date'])['sentiment_score'].mean().reset_index()

# Plot Sentiment Scores Over Time
plt.figure(figsize=(12,6))
sns.lineplot(data=grouped, x='date', y='sentiment_score', hue='author_id')
plt.title('Sentiment Scores Over Time')
plt.xlabel('Date')
plt.ylabel('Sentiment Score')
plt.xticks(rotation=45)
plt.legend(title="User ID")
plt.show()

#create a for loop to create 10 world clouds for top 10 users
for i in range(10):
    # Get the 'clean_text' for the current user
    word = df_top_users.iloc[i]['clean_text']
    #generate the word cloud for user
    wc = WordCloud().generate(' '.join(word))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    print(f"User {top_ten_users.index[i]}")

"""# **Creating a n-gram Visualization of the Data**"""

from sklearn.preprocessing import StandardScaler

  def n_grams(text, n):
      ngrams = []
      for tokens in text:
        # combine all text into a single string
          combined_text = ' '.join(tokens)
        #tokenize the text: split by whitespace
          words = combined_text.split()
        #generate n-grams using zip
          ngrams.extend(zip(*[words[i:] for i in range(n)]))
      #concatenate tokens in each n-gram to form a string
      return [" ".join(ngram) for ngram in ngrams]
  # Sort data by time
  df.sort_values('date', inplace=True)

  def count_ngrams_by_time(ngrams, df):
      # Store n-grams and their counts
      ngram_counts = Counter(ngrams)
      # creates a data frame that has two columns: n-grams and their counts
      ngram_df = pd.DataFrame(ngram_counts.items(), columns=['n-gram', 'count'])
      # Merge with 'date' column and group by date
      ngram_df['date'] = df['date'].values[:len(ngram_df)]
      #Group the n-gram occurrences by date and sum the occurrences for each month
      return ngram_df.groupby('date', as_index=False).sum()

  # Generate n-grams(2-4)
  bi_gram = n_grams(df['clean_text'], 2)
  tri_gram = n_grams(df['clean_text'], 3)
  quad_gram = n_grams(df['clean_text'], 4)

  # Count top 5 word occurences per n-gram
  top_5_bi_grams = count_ngrams_by_time(bi_gram, df['date']).nlargest(5, 'count')
  top_5_tri_grams = count_ngrams_by_time(tri_gram, df['date']).nlargest(5, 'count')
  top_5_quad_grams = count_ngrams_by_time(quad_gram, df['date']).nlargest(5, 'count')

  # Normalize values by dividing count by number of users
  num_users = df['user_id'].nunique()
  top_5_bi_grams['normalized'] = top_5_bi_grams['count'] / num_users
  top_5_tri_grams['normalized'] = top_5_tri_grams['count'] / num_users
  top_5_quad_grams['normalized'] = top_5_quad_grams['count'] / num_users

  # Standardize the normalized values
  scaler = StandardScaler()
  top_5_bi_grams['standardized'] = scaler.fit_transform(top_5_bi_grams[['normalized']])
  top_5_tri_grams['standardized'] = scaler.fit_transform(top_5_tri_grams[['normalized']])
  top_5_quad_grams['standardized'] = scaler.fit_transform(top_5_quad_grams[['normalized']])

  # Plot the normalized time-series
  plt.figure(figsize=(12, 6))
  plt.plot(top_5_bi_grams['date'], top_5_bi_grams['standardized'], label='Bi-grams', marker='o')
  plt.plot(top_5_tri_grams['date'], top_5_tri_grams['standardized'], label='Tri-grams', marker='s')
  plt.plot(top_5_quad_grams['date'], top_5_quad_grams['standardized'], label='Quad-grams', marker='^')

  plt.xlabel('Time(monthly)')
  plt.ylabel('Standardized Frequency')
  plt.title('Normalized Time-Series of N-grams Over Time')
  plt.legend()
  plt.xticks(rotation=45)
  plt.show()

"""Intially, I thought that the project did not seem too hard but I soon ran into many issues. The first and most consistent being that the executing time was far too long. Between each test run to troubleshoot my code, I had to wait 3-4 minutes just for the loading and preprocessing text cell. I often worked on other parts of the project while waiting for the cells to execute, but in the future, I can optimize the processing time by: avoid loops and object creation, use multiprocessing for larger operations, and replacing lists with dictionaries/sets. Another problem I faced was attempting to make an effective visual for the sentiment scores over time for the top 10 users. My first graph was far too confusing, not conveying any information. However, I found out if I created the date column to only show year/month I can compress the data by 30 times, making the graph easier to read. Finally, the last problem I had was understanding how to create a normalised time-series visual. Prior to this project I didn't fully understand what a normalised time-series visual was, making the process a lot harder. I was able to look into the sklearn module and find the Standard Scaler function. From here I found out how to implement the function into my code to create a normalised time-series visual. Overall, I learned, next time, I need to ensure that my code is able to execute and process fast to make trouble-shooting less tedious. Additionally, I believe that only words used by all 10 of the top 10 users should be shown instead of all simply identifying any common words between users as showing all common words is very useless."""