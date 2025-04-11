"""
Abstractive summarization methods for the Financial Text Summarizer.
"""

import torch
from transformers import pipeline


class AbstractiveSummarizer:
    """
    A class that implements various abstractive text summarization methods.
    """
    
    def __init__(self):
        """
        Initialize the summarizer with models lazily loaded when needed.
        """
        self._bart_summarizer = None
        self._t5_summarizer = None
    
    def _get_bart_summarizer(self):
        """
        Lazily load the BART summarization model.
        
        Returns:
            pipeline: The BART summarization pipeline
        """
        if self._bart_summarizer is None:
            self._bart_summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                device=0 if torch.cuda.is_available() else -1
            )
        return self._bart_summarizer
    
    def _get_t5_summarizer(self):
        """
        Lazily load the T5 summarization model.
        
        Returns:
            pipeline: The T5 summarization pipeline
        """
        if self._t5_summarizer is None:
            self._t5_summarizer = pipeline(
                "summarization", 
                model="t5-small",
                device=0 if torch.cuda.is_available() else -1
            )
        return self._t5_summarizer
    
    def bart(self, text, max_length=150, min_length=50):
        """
        Summarize text using the BART model.
        
        Args:
            text (str): The text to summarize
            max_length (int): Maximum length of the summary in tokens
            min_length (int): Minimum length of the summary in tokens
            
        Returns:
            str: The summarized text
        """
        summarizer = self._get_bart_summarizer()
        
        # BART has a maximum input length, so truncate if necessary
        max_input_length = 1024
        if len(text.split()) > max_input_length:
            words = text.split()
            text = " ".join(words[:max_input_length])
        
        summary = summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=False
        )
        
        return summary[0]['summary_text']
    
    def t5(self, text, max_length=150, min_length=50):
        """
        Summarize text using the T5 model.
        
        Args:
            text (str): The text to summarize
            max_length (int): Maximum length of the summary in tokens
            min_length (int): Minimum length of the summary in tokens
            
        Returns:
            str: The summarized text
        """
        summarizer = self._get_t5_summarizer()
        
        # T5 also has a maximum input length
        max_input_length = 512
        if len(text.split()) > max_input_length:
            words = text.split()
            text = " ".join(words[:max_input_length])
        
        # T5 requires a "summarize: " prefix
        prefixed_text = "summarize: " + text
        
        summary = summarizer(
            prefixed_text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=False
        )
        
        return summary[0]['summary_text']
    
    def summarize(self, text, method='bart', max_length=150, min_length=50):
        """
        Summarize text using the specified method.
        
        Args:
            text (str): The text to summarize
            method (str): The summarization method to use ('bart' or 't5')
            max_length (int): Maximum length of the summary in tokens
            min_length (int): Minimum length of the summary in tokens
            
        Returns:
            str: The summarized text
        """
        methods = {
            'bart': self.bart,
            't5': self.t5
        }
        
        if method not in methods:
            raise ValueError(f"Method '{method}' not supported. Choose from: {', '.join(methods.keys())}")
        
        return methods[method](text, max_length, min_length)