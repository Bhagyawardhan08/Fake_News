import streamlit as st
import numpy as np
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Debug print statement to ensure Streamlit is working
st.write("Streamlit is working")

# Example text processing (for testing purposes)
text = "This is an example sentence."
words = word_tokenize(text)
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word.lower() not in stop_words]
print(filtered_words)

# Load data
try:
    news_df = pd.read_csv('train.csv')
    st.write("Data loaded successfully")
except Exception as e:
    st.write(f"Error loading data: {e}")

# Check if the dataframe is loaded
if 'news_df' in locals():
    news_df = news_df.fillna(' ')
    news_df['content'] = news_df['author'] + ' ' + news_df['title']
    X = news_df.drop('label', axis=1)
    y = news_df['label']

    # Define stemming function
    ps = PorterStemmer()
    def stemming(content):
        stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
        stemmed_content = stemmed_content.lower()
        stemmed_content = stemmed_content.split()
        stemmed_content = [ps.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
        stemmed_content = ' '.join(stemmed_content)
        return stemmed_content

    # Apply stemming function to content column
    news_df['content'] = news_df['content'].apply(stemming)

    # Vectorize data
    X = news_df['content'].values
    y = news_df['label'].values
    vector = TfidfVectorizer()
    vector.fit(X)
    X = vector.transform(X)

    # Split data into train and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

    # Fit logistic regression model
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    # Website
    st.title('Fake News Detector')
    input_text = st.text_input('Enter news Article')

    def prediction(input_text):
        input_data = vector.transform([input_text])
        prediction = model.predict(input_data)
        return prediction[0]

    if input_text:
        pred = prediction(input_text)
        if pred == 0:
            st.write('The News is Fake')
        else:
            st.write('The News Is Real')
else:
    st.write("Dataframe not loaded")
