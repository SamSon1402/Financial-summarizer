"""
Text processing utilities for the Financial Text Summarizer.
"""

import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Make sure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextProcessor:
    """
    Utility class for processing and analyzing text.
    """
    
    def __init__(self):
        """
        Initialize with English stopwords.
        """
        self.stopwords = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """
        Clean text by removing special characters and extra whitespace.
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Cleaned text
        """
        # Remove special characters and digits
        text = re.sub(r'[^\w\s\.\,\?\!]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text):
        """
        Remove common stopwords from text.
        
        Args:
            text (str): Text to process
            
        Returns:
            str: Text with stopwords removed
        """
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in self.stopwords]
        
        return ' '.join(filtered_words)
    
    def count_words(self, text):
        """
        Count the number of words in a text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            int: Number of words
        """
        words = word_tokenize(text)
        return len(words)
    
    def count_sentences(self, text):
        """
        Count the number of sentences in a text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            int: Number of sentences
        """
        sentences = sent_tokenize(text)
        return len(sentences)
    
    def calculate_compression_ratio(self, original_text, summary):
        """
        Calculate the compression ratio of a summary.
        
        Args:
            original_text (str): Original text
            summary (str): Summarized text
            
        Returns:
            float: Compression ratio (lower is more compressed)
        """
        original_word_count = self.count_words(original_text)
        summary_word_count = self.count_words(summary)
        
        if original_word_count == 0:
            return 0
        
        return summary_word_count / original_word_count
    
    def analyze_text(self, text):
        """
        Perform basic text analysis.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Analysis results
        """
        word_count = self.count_words(text)
        sentence_count = self.count_sentences(text)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        words = word_tokenize(text.lower())
        word_freq = {}
        for word in words:
            if word.isalnum() and word not in self.stopwords:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 10 words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': avg_sentence_length,
            'top_words': dict(top_words)
        }
    
    @staticmethod
    def load_sample_articles(file_path='assets/samples.json'):
        """
        Load sample articles from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing sample articles
            
        Returns:
            dict: Dictionary of sample articles
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                samples = json.load(f)
            
            # Convert to simpler format if needed
            if isinstance(samples, dict) and all(isinstance(v, dict) for v in samples.values()):
                return {k: v['text'] for k, v in samples.items()}
            
            return samples
        except Exception as e:
            print(f"Error loading sample articles: {e}")
            # Fallback sample
            return {
                "Default Sample": "This is a fallback sample text since the sample file could not be loaded."
            }