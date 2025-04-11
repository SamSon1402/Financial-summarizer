"""
Evaluation metrics for summarization in the Financial Text Summarizer.
"""

from rouge_score import rouge_scorer
import pandas as pd


class SummaryEvaluator:
    """
    A class for evaluating summarization quality using various metrics.
    """
    
    def __init__(self):
        """
        Initialize the evaluator with the ROUGE scorer.
        """
        self.scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=True
        )
    
    def calculate_rouge(self, reference, summary):
        """
        Calculate ROUGE scores between a reference summary and a generated summary.
        
        Args:
            reference (str): The reference (gold standard) summary
            summary (str): The generated summary to evaluate
            
        Returns:
            dict: Dictionary containing ROUGE-1, ROUGE-2, and ROUGE-L F1 scores
        """
        scores = self.scorer.score(reference, summary)
        
        return {
            'ROUGE-1': scores['rouge1'].fmeasure,
            'ROUGE-2': scores['rouge2'].fmeasure,
            'ROUGE-L': scores['rougeL'].fmeasure
        }
    
    def evaluate_summaries(self, reference, summaries):
        """
        Evaluate multiple summaries against a reference summary.
        
        Args:
            reference (str): The reference (gold standard) summary
            summaries (dict): Dictionary mapping method names to generated summaries
            
        Returns:
            pd.DataFrame: DataFrame containing ROUGE scores for each method
        """
        results = {
            'Method': [],
            'ROUGE-1': [],
            'ROUGE-2': [],
            'ROUGE-L': [],
            'Average': []
        }
        
        for method, summary in summaries.items():
            scores = self.calculate_rouge(reference, summary)
            average = sum(scores.values()) / len(scores)
            
            results['Method'].append(method)
            results['ROUGE-1'].append(scores['ROUGE-1'])
            results['ROUGE-2'].append(scores['ROUGE-2'])
            results['ROUGE-L'].append(scores['ROUGE-L'])
            results['Average'].append(average)
        
        return pd.DataFrame(results)
    
    def find_best_method(self, evaluation_df):
        """
        Find the best summarization method based on average ROUGE scores.
        
        Args:
            evaluation_df (pd.DataFrame): DataFrame with evaluation results
            
        Returns:
            str: Name of the best method
            float: Average score of the best method
        """
        if 'Average' not in evaluation_df.columns:
            evaluation_df['Average'] = evaluation_df[
                ['ROUGE-1', 'ROUGE-2', 'ROUGE-L']
            ].mean(axis=1)
        
        best_idx = evaluation_df['Average'].idxmax()
        best_method = evaluation_df.loc[best_idx, 'Method']
        best_score = evaluation_df.loc[best_idx, 'Average']
        
        return best_method, best_score