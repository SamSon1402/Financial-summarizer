"""
Data visualization utilities for the Financial Text Summarizer.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class DataVisualizer:
    """
    Utility class for visualizing text summarization results.
    """
    
    @staticmethod
    def plot_rouge_scores(scores_df):
        """
        Create a bar chart of ROUGE scores.
        
        Args:
            scores_df (pd.DataFrame): DataFrame with ROUGE scores
            
        Returns:
            None: Displays the chart directly using Streamlit
        """
        # Make a copy to avoid modifying the original
        df = scores_df.copy()
        
        # Melt the dataframe for easier plotting
        plot_data = pd.melt(
            df,
            id_vars=['Method'],
            value_vars=['ROUGE-1', 'ROUGE-2', 'ROUGE-L'],
            var_name='Metric',
            value_name='Score'
        )
        
        # Use Streamlit's native bar chart
        st.bar_chart(
            data=plot_data,
            x='Method',
            y='Score',
            color='Metric',
            use_container_width=True
        )
    
    @staticmethod
    def plot_text_stats(summaries, original_text=None):
        """
        Create visualizations comparing statistics of different summaries.
        
        Args:
            summaries (dict): Dictionary mapping method names to summaries
            original_text (str, optional): Original text for comparison
            
        Returns:
            None: Displays the chart directly using Streamlit
        """
        # Calculate word counts
        word_counts = {}
        
        if original_text:
            word_counts['Original'] = len(original_text.split())
        
        for method, summary in summaries.items():
            word_counts[method] = len(summary.split())
        
        # Create a DataFrame
        stats_df = pd.DataFrame({
            'Method': list(word_counts.keys()),
            'Word Count': list(word_counts.values())
        })
        
        # Sort by word count descending
        stats_df = stats_df.sort_values('Word Count', ascending=False)
        
        # Calculate compression ratios if original text is available
        if original_text:
            original_word_count = word_counts['Original']
            compression_ratios = {}
            
            for method, summary in summaries.items():
                summary_word_count = word_counts[method]
                compression_ratios[method] = summary_word_count / original_word_count
            
            # Add to DataFrame
            compression_df = pd.DataFrame({
                'Method': list(compression_ratios.keys()),
                'Compression Ratio': list(compression_ratios.values())
            })
            
            # Display compression ratios
            st.subheader("Compression Ratios")
            st.bar_chart(
                data=compression_df,
                x='Method',
                y='Compression Ratio',
                use_container_width=True
            )
        
        # Display word counts
        st.subheader("Word Counts")
        st.bar_chart(
            data=stats_df,
            x='Method',
            y='Word Count',
            use_container_width=True
        )
    
    @staticmethod
    def create_heatmap(scores_df):
        """
        Create a heatmap of ROUGE scores for different methods.
        
        Args:
            scores_df (pd.DataFrame): DataFrame with ROUGE scores
            
        Returns:
            None: Displays the chart directly using Streamlit
        """
        # Prepare the data
        methods = scores_df['Method'].tolist()
        metrics = ['ROUGE-1', 'ROUGE-2', 'ROUGE-L']
        
        # Create a matrix from the scores
        data = scores_df[metrics].values
        
        # Create the figure
        fig, ax = plt.subplots(figsize=(10, len(methods) * 0.5 + 1))
        
        # Create the heatmap
        im = ax.imshow(data, cmap='viridis')
        
        # Set up the axes
        ax.set_xticks(np.arange(len(metrics)))
        ax.set_yticks(np.arange(len(methods)))
        ax.set_xticklabels(metrics)
        ax.set_yticklabels(methods)
        
        # Rotate the x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Score", rotation=-90, va="bottom")
        
        # Add text annotations
        for i in range(len(methods)):
            for j in range(len(metrics)):
                text = ax.text(j, i, f"{data[i, j]:.3f}",
                               ha="center", va="center", color="w")
        
        # Add title
        ax.set_title("ROUGE Scores Comparison")
        
        # Adjust layout
        fig.tight_layout()
        
        # Display the plot
        st.pyplot(fig)
    
    @staticmethod
    def create_radar_chart(scores_df):
        """
        Create a radar chart comparing different summarization methods.
        
        Args:
            scores_df (pd.DataFrame): DataFrame with ROUGE scores
            
        Returns:
            None: Displays the chart directly using Streamlit
        """
        # Get methods and metrics
        methods = scores_df['Method'].tolist()
        metrics = ['ROUGE-1', 'ROUGE-2', 'ROUGE-L']
        
        # Number of variables
        num_vars = len(metrics)
        
        # Calculate angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # Make the plot circular
        angles += angles[:1]
        
        # Create the figure
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Add extra metric to close the loop
        metrics_loop = metrics + [metrics[0]]
        
        # Plot each method
        for i, method in enumerate(methods):
            values = scores_df.loc[scores_df['Method'] == method, metrics].values.flatten().tolist()
            values += values[:1]  # Close the loop
            
            # Plot the method
            ax.plot(angles, values, linewidth=2, label=method)
            ax.fill(angles, values, alpha=0.1)
        
        # Set the labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        
        # Add legend
        plt.legend(loc='upper right')
        
        # Add title
        plt.title('Summarization Methods Comparison', size=15)
        
        # Display the plot
        st.pyplot(fig)
    
    @staticmethod
    def create_retro_scoreboard(scores_dict, title="SCORES"):
        """
        Create a retro gaming-style scoreboard for displaying metrics.
        
        Args:
            scores_dict (dict): Dictionary mapping score names to values
            title (str): Title for the scoreboard
            
        Returns:
            str: HTML for the styled scoreboard
        """
        # Define retro colors
        background_color = "#1A1A2E"
        border_color = "#F9C80E"
        title_color = "#F9C80E"
        value_color = "#05D9E8"
        
        # Create HTML for the scoreboard
        html = f"""
        <div style="background-color: {background_color}; border: 3px solid {border_color}; 
                    padding: 10px; font-family: 'VT323', monospace; color: {title_color}; 
                    margin: 10px 0; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 5px;">{title}</div>
        """
        
        # Add each score
        for name, value in scores_dict.items():
            # Format the value as needed
            if isinstance(value, float):
                formatted_value = f"{value:.3f}"
            else:
                formatted_value = str(value)
            
            html += f"""
            <div style="margin: 5px 0;">
                <span style="font-size: 16px;">{name}</span>
                <div style="font-size: 28px; color: {value_color};">{formatted_value}</div>
            </div>
            """
        
        html += "</div>"
        
        return html