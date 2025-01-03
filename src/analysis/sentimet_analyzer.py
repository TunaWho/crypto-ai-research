from textblob import TextBlob
import pandas as pd
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_scores = []

    def analyze_text(self, texts):
        sentiments = []
        for text in texts:
            analysis = TextBlob(text)
            sentiments.append({
                'text': text,
                'polarity': analysis.sentiment.polarity,
                'subjectivity': analysis.sentiment.subjectivity
            })
        return sentiments

    def get_overall_sentiment(self):
        if not self.sentiment_scores:
            return 0
        return np.mean([score['polarity'] for score in self.sentiment_scores])