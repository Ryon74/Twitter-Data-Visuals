Twitter Data Visualization
Overview
This project analyzes and visualizes Twitter data to explore user activity, sentiment, and word usage patterns. It focuses on the top 10 most active users, providing insights through sentiment analysis, word clouds, and n-gram visualizations. The dataset is processed to extract meaningful information from English tweets, with an emphasis on clean text preprocessing and effective data visualization.
Features

Dataset: Processes AE1_vishing_data_zipped.csv.zip, containing Twitter data with tweet text, author IDs, and timestamps.
Text Preprocessing: Cleans tweets by removing URLs, special characters, and stopwords, and filters for valid English words.
Analysis:
Identifies the top 10 most active users by tweet count.
Analyzes word frequency and vocabulary richness for these users.
Detects common words used across multiple users.


Visualizations:
Sentiment scores over time for top users.
Word clouds for each of the top 10 users.
Normalized time-series of bi-grams, tri-grams, and quad-grams.


Sentiment Analysis: Uses TextBlob to calculate sentiment polarity of tweets.
N-gram Analysis: Generates and visualizes 2- to 4-word phrases to show usage trends over time.

Installation

Clone the repository:git clone https://github.com/your-username/twitter-data-visualization.git


Navigate to the project directory:cd twitter-data-visualization


Install the required dependencies:pip install -r requirements.txt



Dependencies

Python 3.8+
pandas
numpy
nltk
textblob
matplotlib
seaborn
wordcloud
scikit-learn

Install dependencies using:
pip install pandas numpy nltk textblob matplotlib seaborn wordcloud scikit-learn

You also need to download NLTK data:
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('words')
nltk.download('stopwords')

Usage

Place the AE1_vishing_data_zipped.csv.zip file in the project directory.
Run the Jupyter notebook Twitter_Data_Visuals.ipynb:jupyter notebook Twitter_Data_Visuals.ipynb


Follow the notebook to:
Load and preprocess the Twitter dataset.
Analyze the top 10 users' tweets.
Generate visualizations (sentiment plots, word clouds, n-gram time-series).


Review the output, including printed word frequencies, vocabulary richness scores, and visualizations.

Dataset
The dataset (AE1_vishing_data_zipped.csv.zip) includes:

Columns: Tweet text, author ID, creation timestamp, language, and more.
Preprocessing: Filters for English tweets, cleans text, and converts timestamps to a year-month format.

Analysis and Visualizations

Top 10 Users:
Identifies the most active users and analyzes their word usage.
Outputs top 5 words per user, vocabulary richness, and common words across users.


Sentiment Analysis:
Calculates sentiment polarity for each tweet.
Plots average sentiment scores over time for top users, grouped by year-month.


Word Clouds:
Generates a word cloud for each top user, visualizing their most frequent words.


N-gram Analysis:
Creates bi-grams, tri-grams, and quad-grams from cleaned text.
Normalizes and standardizes n-gram frequencies for a time-series plot, showing trends over time.



Challenges and Lessons Learned

Processing Time: Initial long execution times (3-4 minutes) were a bottleneck. Future optimizations include avoiding loops, using multiprocessing, and preferring dictionaries/sets over lists.
Sentiment Visualization: Early graphs were cluttered; compressing timestamps to year-month format improved readability.
Normalized Time-Series: Learning to use StandardScaler from scikit-learn was key to creating effective n-gram visualizations.
Common Words: Displaying words shared by all top users (instead of any overlap) would provide more meaningful insights.

