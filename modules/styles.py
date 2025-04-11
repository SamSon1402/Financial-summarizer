"""
Custom CSS styles for the retro gaming aesthetic in the Financial Text Summarizer.
"""

import streamlit as st


class RetroStyles:
    """
    Class for managing custom CSS styles with a retro gaming aesthetic.
    """
    
    # Retro gaming color palette
    PRIMARY_COLOR = "#FF2A6D"     # Vibrant pink
    SECONDARY_COLOR = "#05D9E8"   # Cyan
    TERTIARY_COLOR = "#D65108"    # Orange
    BACKGROUND_COLOR = "#1A1A2E"  # Dark blue
    TEXT_COLOR = "#FFFFFF"        # White
    HIGHLIGHT_COLOR = "#F9C80E"   # Yellow
    
    # Method-specific colors for visual distinction
    METHOD_COLORS = {
        "TextRank": "#FF2A6D",  # Pink
        "LexRank": "#05D9E8",   # Cyan
        "LSA": "#F9C80E",       # Yellow
        "TF-IDF": "#D65108",    # Orange
        "BART": "#3A86FF",      # Blue
        "T5": "#8338EC"         # Purple
    }
    
    @classmethod
    def apply_styles(cls):
        """
        Apply the retro gaming CSS styles to the Streamlit app.
        """
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');
        
        /* Main styles */
        .main {{
            background-color: {cls.BACKGROUND_COLOR};
            color: {cls.TEXT_COLOR};
            font-family: 'Space Mono', monospace;
            padding: 0;
        }}
        
        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'VT323', monospace;
            color: {cls.PRIMARY_COLOR};
            text-shadow: 3px 3px 0px {cls.SECONDARY_COLOR};
            letter-spacing: 2px;
        }}
        
        /* Buttons */
        .stButton button {{
            background-color: {cls.TERTIARY_COLOR};
            color: {cls.TEXT_COLOR};
            border: 2px solid {cls.HIGHLIGHT_COLOR};
            border-radius: 0;
            font-family: 'VT323', monospace;
            font-size: 18px;
            padding: 8px 16px;
            box-shadow: 4px 4px 0px {cls.HIGHLIGHT_COLOR};
            transition: transform 0.1s, box-shadow 0.1s;
        }}
        
        .stButton button:hover {{
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px {cls.HIGHLIGHT_COLOR};
        }}
        
        /* Text areas and inputs */
        .stTextInput input, .stTextArea textarea, .stSelectbox, div[data-baseweb="select"] div {{
            background-color: {cls.BACKGROUND_COLOR};
            color: {cls.TEXT_COLOR};
            border: 2px solid {cls.SECONDARY_COLOR};
            border-radius: 0;
            font-family: 'Space Mono', monospace;
        }}
        
        /* Cards for summaries */
        .summary-card {{
            background-color: {cls.BACKGROUND_COLOR};
            border: 2px solid {cls.PRIMARY_COLOR};
            padding: 10px;
            margin: 10px 0;
            box-shadow: 5px 5px 0px {cls.HIGHLIGHT_COLOR};
        }}
        
        .summary-card-title {{
            font-family: 'VT323', monospace;
            color: {cls.SECONDARY_COLOR};
            font-size: 22px;
            margin-bottom: 10px;
            border-bottom: 2px solid {cls.SECONDARY_COLOR};
            padding-bottom: 5px;
        }}
        
        /* Loading animation */
        .stProgress .st-bo {{
            background-color: {cls.PRIMARY_COLOR};
        }}
        
        /* Tables */
        .dataframe {{
            font-family: 'Space Mono', monospace;
            border: 2px solid {cls.TERTIARY_COLOR};
        }}
        
        .dataframe thead {{
            background-color: {cls.TERTIARY_COLOR};
            color: {cls.TEXT_COLOR};
        }}
        
        /* Custom pixelated container */
        .pixel-container {{
            border: 4px solid {cls.PRIMARY_COLOR};
            background-color: rgba(26, 26, 46, 0.7);
            padding: 20px;
            margin: 10px 0;
            position: relative;
        }}
        
        .pixel-container::before {{
            content: '';
            position: absolute;
            top: -8px;
            left: -8px;
            right: -8px;
            bottom: -8px;
            border: 2px solid {cls.SECONDARY_COLOR};
            z-index: -1;
        }}
        
        /* For tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {cls.BACKGROUND_COLOR};
            border: 2px solid {cls.PRIMARY_COLOR};
            border-radius: 0;
            color: {cls.PRIMARY_COLOR};
            font-family: 'VT323', monospace;
            padding: 5px 15px;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {cls.PRIMARY_COLOR};
            color: {cls.TEXT_COLOR};
        }}
        
        /* Scoreboard style */
        .scoreboard {{
            background-color: {cls.BACKGROUND_COLOR};
            border: 3px solid {cls.HIGHLIGHT_COLOR};
            padding: 10px;
            font-family: 'VT323', monospace;
            color: {cls.HIGHLIGHT_COLOR};
            margin: 10px 0;
            text-align: center;
        }}
        
        .scoreboard-title {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        
        .scoreboard-value {{
            font-size: 36px;
            color: {cls.SECONDARY_COLOR};
        }}
        
        /* Pixel animation for loading */
        @keyframes pixel-move {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(20px); }}
        }}
        
        .pixel-loading {{
            font-family: 'VT323', monospace;
            font-size: 24px;
            color: {cls.PRIMARY_COLOR};
            display: inline-block;
            animation: pixel-move 0.5s infinite alternate;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @classmethod
    def create_title(cls):
        """
        Create a pixelated retro gaming title for the app.
        
        Returns:
            None: Displays the title directly using st.markdown
        """
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3.5em; line-height: 1.2; margin: 0;">
                FINANCIAL TEXT<br>SUMMARIZER 3000
            </h1>
            <p style="font-family: 'VT323', monospace; font-size: 1.5em; margin-top: 10px; color: {cls.SECONDARY_COLOR};">
                [PRESS START TO SUMMARIZE]
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @classmethod
    def create_summary_card(cls, title, summary_text, method):
        """
        Create a styled summary card for displaying results.
        
        Args:
            title (str): Title of the summary card
            summary_text (str): Summary text to display
            method (str): Summarization method (determines color)
            
        Returns:
            str: HTML for the styled summary card
        """
        method_color = cls.METHOD_COLORS.get(method, cls.PRIMARY_COLOR)
        
        return f"""
        <div class="summary-card" style="border-color: {method_color};">
            <div class="summary-card-title" style="color: {method_color};">
                {title}
            </div>
            <div style="font-family: 'Space Mono', monospace; font-size: 14px;">
                {summary_text}
            </div>
        </div>
        """
    
    @classmethod
    def create_scoreboard(cls, title, value):
        """
        Create a retro gaming scoreboard for displaying metrics.
        
        Args:
            title (str): Title of the scoreboard
            value (float or str): Value to display
            
        Returns:
            str: HTML for the styled scoreboard
        """
        return f"""
        <div class="scoreboard">
            <div class="scoreboard-title">{title}</div>
            <div class="scoreboard-value">{value}</div>
        </div>
        """
    
    @classmethod
    def create_winner_announcement(cls, method, score=None):
        """
        Create a winner announcement banner.
        
        Args:
            method (str): Name of the winning method
            score (float, optional): Score of the winning method
            
        Returns:
            str: HTML for the winner announcement
        """
        score_text = f" (Score: {score:.3f})" if score is not None else ""
        
        return f"""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="font-family: 'VT323', monospace; color: {cls.HIGHLIGHT_COLOR}; 
                       text-shadow: 3px 3px 0px {cls.PRIMARY_COLOR};">
                🏆 WINNER: {method}{score_text} 🏆
            </h2>
            <p style="font-family: 'Space Mono', monospace; font-size: 16px;">
                Based on ROUGE scores compared to the reference summary
            </p>
        </div>
        """
    
    @classmethod
    def create_loading_animation(cls, text="LOADING..."):
        """
        Create a retro pixel-style loading animation.
        
        Args:
            text (str): Text to display during loading
            
        Returns:
            str: HTML for the loading animation
        """
        return f"""
        <div style="text-align: center;">
            <span class="pixel-loading">{text}</span>
        </div>
        """
    
    @classmethod
    def create_footer(cls):
        """
        Create a retro gaming footer.
        
        Returns:
            str: HTML for the styled footer
        """
        return f"""
        <div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 2px solid {cls.SECONDARY_COLOR};">
            <p style="font-family: 'VT323', monospace; font-size: 18px; color: {cls.PRIMARY_COLOR};">
                FINANCIAL TEXT SUMMARIZER 3000 © 2025 - INSERT COIN TO CONTINUE
            </p>
        </div>
        """