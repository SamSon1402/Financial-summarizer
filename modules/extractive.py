"""
Extractive summarization methods for the Financial Text Summarizer.
"""

import nltk
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Make sure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')


class ExtractiveSummarizer:
    """
    A class that implements various extractive text summarization methods.
    """
    
    @staticmethod
    def text_rank(text, num_sentences=5):
        """
        Summarize text using the TextRank algorithm.
        
        Args:
            text (str): The text to summarize
            num_sentences (int): Number of sentences to include in the summary
            
        Returns:
            str: The summarized text
        """
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, num_sentences)
        return " ".join([str(sentence) for sentence in summary])
    
    @staticmethod
    def lex_rank(text, num_sentences=5):
        """
        Summarize text using the LexRank algorithm.
        
        Args:
            text (str): The text to summarize
            num_sentences (int): Number of sentences to include in the summary
            
        Returns:
            str: The summarized text
        """
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, num_sentences)
        return " ".join([str(sentence) for sentence in summary])
    
    @staticmethod
    def lsa(text, num_sentences=5):
        """
        Summarize text using Latent Semantic Analysis.
        
        Args:
            text (str): The text to summarize
            num_sentences (int): Number of sentences to include in the summary
            
        Returns:
            str: The summarized text
        """
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, num_sentences)
        return " ".join([str(sentence) for sentence in summary])
    
    @staticmethod
    def tfidf(text, num_sentences=5):
        """
        Summarize text using TF-IDF scoring.
        
        Args:
            text (str): The text to summarize
            num_sentences (int): Number of sentences to include in the summary
            
        Returns:
            str: The summarized text
        """
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # If there are fewer sentences than requested, return all sentences
        if len(sentences) <= num_sentences:
            return text
        
        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # Fit and transform the sentences
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Calculate sentence scores based on TF-IDF values
        sentence_scores = np.array([tfidf_matrix[i].sum() for i in range(len(sentences))])
        
        # Get the indices of the top N sentences
        top_indices = sentence_scores.argsort()[-num_sentences:]
        
        # Sort indices to maintain original order
        top_indices = sorted(top_indices)
        
        # Combine the top sentences
        summary = ' '.join([sentences[i] for i in top_indices])
        
        return summary
    
    def summarize(self, text, method='text_rank', num_sentences=5):
        """
        Summarize text using the specified method.
        
        Args:
            text (str): The text to summarize
            method (str): The summarization method to use
                ('text_rank', 'lex_rank', 'lsa', or 'tfidf')
            num_sentences (int): Number of sentences to include in the summary
            
        Returns:
            str: The summarized text
        """
        methods = {
            'text_rank': self.text_rank,
            'lex_rank': self.lex_rank,
            'lsa': self.lsa,
            'tfidf': self.tfidf
        }
        
        if method not in methods:
            raise ValueError(f"Method '{method}' not supported. Choose from: {', '.join(methods.keys())}")
        
        return methods[method](text, num_sentences)