import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import pipeline
import pandas as pd
from rouge_score import rouge_scorer
import time

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

# Sample financial news articles
SAMPLE_ARTICLES = {
    "Fed Rate Decision": """
    The Federal Reserve maintained its benchmark interest rate at current levels during Wednesday's meeting, 
    signaling a continued pause in its monetary tightening cycle. Fed Chair Jerome Powell indicated that 
    while inflation has shown signs of moderating, the committee remains vigilant about potential price pressures. 
    "We are prepared to adjust the stance of monetary policy as appropriate if risks emerge," Powell stated 
    during the press conference. Market participants had widely expected this decision, with futures markets 
    now pricing in a potential rate cut in the next meeting. The Fed's decision comes amid mixed economic data, 
    with strong labor market figures contrasting with slowing retail sales and manufacturing activity. 
    The central bank's updated dot plot showed a slightly more dovish outlook compared to previous projections, 
    with most members now seeing one or two rate cuts this year. Treasury yields declined following the announcement, 
    while equity markets showed modest gains.
    """,
    
    "Tech Earnings Report": """
    Tech giant Quantum Computing Inc. reported quarterly earnings that exceeded Wall Street expectations, 
    driving shares up 8% in after-hours trading. The company posted revenue of $15.7 billion, up 22% year-over-year, 
    while earnings per share came in at $1.28, beating analysts' consensus estimate of $1.15. 
    CEO Sarah Chen attributed the strong performance to robust growth in the company's cloud services division, 
    which saw a 35% increase in revenue. "Our strategic investments in quantum computing applications are 
    beginning to yield significant returns," Chen noted during the earnings call. The company also raised its 
    full-year guidance, now expecting revenue growth of 25-28%, up from its previous forecast of 20-23%. 
    Quantum Computing Inc. announced plans to expand its data center capacity and increase R&D spending by 15% 
    as it faces intensifying competition from established tech firms entering the quantum computing market. 
    Analysts from Morgan Stanley maintained their "overweight" rating on the stock, raising their price target 
    from $280 to $320.
    """,
    
    "Market Volatility": """
    Global financial markets experienced significant volatility today as concerns about economic growth and 
    geopolitical tensions weighed on investor sentiment. Major U.S. indices declined, with the S&P 500 falling 
    2.3% and the Nasdaq Composite dropping 3.1%, marking their worst single-day performances in three months. 
    European markets also retreated, with the Stoxx Europe 600 closing down 1.8%. The sell-off was triggered by 
    disappointing manufacturing data from China and Europe, fueling fears about global economic slowdown. 
    Adding to market anxiety were rising tensions in the Middle East and ongoing trade disputes between major economies. 
    Safe-haven assets saw significant inflows, with gold prices rising 1.5% to reach $2,150 per ounce. 
    The 10-year Treasury yield fell 8 basis points to 3.42% as investors sought safety in government bonds. 
    The VIX index, often referred to as Wall Street's "fear gauge," jumped 40% to its highest level since January. 
    Currency markets were not spared from the turbulence, with the dollar index strengthening against a basket of currencies, 
    while emerging market currencies faced substantial pressure.
    """
}

# Function to add custom CSS for retro gaming aesthetic
def add_retro_css():
    # Retro gaming color palette
    primary_color = "#FF2A6D"  # Vibrant pink
    secondary_color = "#05D9E8"  # Cyan
    tertiary_color = "#D65108"  # Orange
    background_color = "#1A1A2E"  # Dark blue
    text_color = "#FFFFFF"  # White
    highlight_color = "#F9C80E"  # Yellow

    # CSS for retro gaming style
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');
    
    /* Main styles */
    .main {
        background-color: """ + background_color + """;
        color: """ + text_color + """;
        font-family: 'Space Mono', monospace;
        padding: 0;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'VT323', monospace;
        color: """ + primary_color + """;
        text-shadow: 3px 3px 0px """ + secondary_color + """;
        letter-spacing: 2px;
    }
    
    /* Buttons */
    .stButton button {
        background-color: """ + tertiary_color + """;
        color: """ + text_color + """;
        border: 2px solid """ + highlight_color + """;
        border-radius: 0;
        font-family: 'VT323', monospace;
        font-size: 18px;
        padding: 8px 16px;
        box-shadow: 4px 4px 0px """ + highlight_color + """;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    
    .stButton button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px """ + highlight_color + """;
    }
    
    /* Text areas and inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox, div[data-baseweb="select"] div {
        background-color: """ + background_color + """;
        color: """ + text_color + """;
        border: 2px solid """ + secondary_color + """;
        border-radius: 0;
        font-family: 'Space Mono', monospace;
    }
    
    /* Cards for summaries */
    .summary-card {
        background-color: """ + background_color + """;
        border: 2px solid """ + primary_color + """;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 5px 5px 0px """ + highlight_color + """;
    }
    
    .summary-card-title {
        font-family: 'VT323', monospace;
        color: """ + secondary_color + """;
        font-size: 22px;
        margin-bottom: 10px;
        border-bottom: 2px solid """ + secondary_color + """;
        padding-bottom: 5px;
    }
    
    /* Loading animation */
    .stProgress .st-bo {
        background-color: """ + primary_color + """;
    }
    
    /* Tables */
    .dataframe {
        font-family: 'Space Mono', monospace;
        border: 2px solid """ + tertiary_color + """;
    }
    
    .dataframe thead {
        background-color: """ + tertiary_color + """;
        color: """ + text_color + """;
    }
    
    /* Custom pixelated container */
    .pixel-container {
        border: 4px solid """ + primary_color + """;
        background-color: rgba(26, 26, 46, 0.7);
        padding: 20px;
        margin: 10px 0;
        position: relative;
    }
    
    .pixel-container::before {
        content: '';
        position: absolute;
        top: -8px;
        left: -8px;
        right: -8px;
        bottom: -8px;
        border: 2px solid """ + secondary_color + """;
        z-index: -1;
    }
    
    /* For tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: """ + background_color + """;
        border: 2px solid """ + primary_color + """;
        border-radius: 0;
        color: """ + primary_color + """;
        font-family: 'VT323', monospace;
        padding: 5px 15px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: """ + primary_color + """;
        color: """ + text_color + """;
    }
    
    /* Scoreboard style */
    .scoreboard {
        background-color: """ + background_color + """;
        border: 3px solid """ + highlight_color + """;
        padding: 10px;
        font-family: 'VT323', monospace;
        color: """ + highlight_color + """;
        margin: 10px 0;
        text-align: center;
    }
    
    .scoreboard-title {
        font-size: 24px;
        margin-bottom: 5px;
    }
    
    .scoreboard-value {
        font-size: 36px;
        color: """ + secondary_color + """;
    }
    
    /* Pixel animation for loading */
    @keyframes pixel-move {
        0% { transform: translateX(0); }
        100% { transform: translateX(20px); }
    }
    
    .pixel-loading {
        font-family: 'VT323', monospace;
        font-size: 24px;
        color: """ + primary_color + """;
        display: inline-block;
        animation: pixel-move 0.5s infinite alternate;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to display pixelated title
def display_retro_title():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 3.5em; line-height: 1.2; margin: 0;">
            FINANCIAL TEXT<br>SUMMARIZER 3000
        </h1>
        <p style="font-family: 'VT323', monospace; font-size: 1.5em; margin-top: 10px; color: #05D9E8;">
            [PRESS START TO SUMMARIZE]
        </p>
    </div>
    """, unsafe_allow_html=True)

# Function to create styled summary cards
def create_summary_card(title, summary_text, method_color):
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

# Summarization functions
def extractive_summarize_text_rank(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def extractive_summarize_lex_rank(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def extractive_summarize_lsa(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

# Simple TF-IDF based summarization
def extractive_summarize_tfidf(text, num_sentences=5):
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    
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

def abstractive_summarize_bart(text, max_length=150):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def abstractive_summarize_t5(text, max_length=150):
    summarizer = pipeline("summarization", model="t5-small")
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Function to calculate ROUGE scores
def calculate_rouge(reference, summary):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, summary)
    return {
        'ROUGE-1': scores['rouge1'].fmeasure,
        'ROUGE-2': scores['rouge2'].fmeasure,
        'ROUGE-L': scores['rougeL'].fmeasure
    }

# Main application
def main():
    st.set_page_config(page_title="Financial Text Summarizer 3000", layout="wide")
    add_retro_css()
    display_retro_title()
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("<h2>🎮 CONTROL PANEL</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='pixel-container'>", unsafe_allow_html=True)
        
        # Input method selection
        input_method = st.radio(
            "SELECT INPUT MODE",
            ["SAMPLE TEXT", "PASTE YOUR OWN", "UPLOAD FILE"],
            key="input_method"
        )
        
        # Number of sentences for extractive methods
        num_sentences = st.slider(
            "EXTRACTIVE LENGTH",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of sentences for extractive summaries"
        )
        
        # Max length for abstractive methods
        max_length = st.slider(
            "ABSTRACTIVE LENGTH",
            min_value=50,
            max_value=300,
            value=150,
            help="Maximum length for abstractive summaries"
        )
        
        # Add some gaming elements
        st.markdown("<div class='scoreboard'>", unsafe_allow_html=True)
        st.markdown("<div class='scoreboard-title'>DIFFICULTY</div>", unsafe_allow_html=True)
        
        difficulty = st.select_slider(
            "",
            options=["EASY", "NORMAL", "HARD", "EXPERT"],
            value="NORMAL"
        )
        
        if difficulty == "EASY":
            st.markdown("<div class='scoreboard-value'>EASY MODE</div>", unsafe_allow_html=True)
            st.info("Shorter texts, simplified metrics")
        elif difficulty == "NORMAL":
            st.markdown("<div class='scoreboard-value'>NORMAL MODE</div>", unsafe_allow_html=True)
            st.info("Standard text size, all metrics")
        elif difficulty == "HARD":
            st.markdown("<div class='scoreboard-value'>HARD MODE</div>", unsafe_allow_html=True)
            st.warning("Longer texts, detailed metrics")
        else:
            st.markdown("<div class='scoreboard-value'>EXPERT MODE</div>", unsafe_allow_html=True)
            st.error("Full article analysis, comprehensive metrics")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Summarization methods selection
        st.markdown("<h3>SELECT SUMMARIZERS</h3>", unsafe_allow_html=True)
        
        use_textrank = st.checkbox("TextRank", value=True)
        use_lexrank = st.checkbox("LexRank", value=True)
        use_lsa = st.checkbox("LSA", value=True)
        use_tfidf = st.checkbox("TF-IDF", value=True)
        use_bart = st.checkbox("BART", value=False)
        use_t5 = st.checkbox("T5", value=False)
        
        # Calculate ROUGE scores option
        calculate_metrics = st.checkbox("CALCULATE ROUGE SCORES", value=False)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h2>📝 INPUT TEXT</h2>", unsafe_allow_html=True)
        
        # Input text handling
        if input_method == "SAMPLE TEXT":
            sample_selection = st.selectbox(
                "CHOOSE A SAMPLE:",
                list(SAMPLE_ARTICLES.keys())
            )
            input_text = SAMPLE_ARTICLES[sample_selection]
            st.markdown("<div class='pixel-container'>", unsafe_allow_html=True)
            st.write(input_text)
            st.markdown("</div>", unsafe_allow_html=True)
            
        elif input_method == "PASTE YOUR OWN":
            input_text = st.text_area(
                "ENTER YOUR TEXT:",
                height=300,
                help="Paste financial news or article here"
            )
            
        else:  # UPLOAD FILE
            uploaded_file = st.file_uploader(
                "UPLOAD TEXT FILE",
                type=["txt", "md", "rtf"],
                help="Upload a text file containing financial news"
            )
            
            if uploaded_file is not None:
                input_text = uploaded_file.read().decode("utf-8")
                st.markdown("<div class='pixel-container'>", unsafe_allow_html=True)
                st.write(input_text[:500] + ("..." if len(input_text) > 500 else ""))
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                input_text = ""
    
    with col2:
        st.markdown("<h2>🚀 REFERENCE SUMMARY</h2>", unsafe_allow_html=True)
        
        # Reference summary for comparison (optional)
        reference_summary = st.text_area(
            "ENTER A REFERENCE SUMMARY (OPTIONAL):",
            height=300,
            help="If you have a gold-standard summary, paste it here for comparison"
        )

    # Process and generate summaries
    if st.button("🎮 PRESS START TO SUMMARIZE"):
        if not input_text:
            st.error("Please enter some text to summarize!")
        else:
            # Show loading animation
            with st.spinner(""):
                st.markdown(
                    "<div style='text-align: center;'><span class='pixel-loading'>GENERATING SUMMARIES...</span></div>",
                    unsafe_allow_html=True
                )
                
                # Initialize dictionaries for summaries and ROUGE scores
                summaries = {}
                rouge_scores = {}
                
                # Generate summaries using selected methods
                if use_textrank:
                    summaries["TextRank"] = extractive_summarize_text_rank(input_text, num_sentences)
                
                if use_lexrank:
                    summaries["LexRank"] = extractive_summarize_lex_rank(input_text, num_sentences)
                
                if use_lsa:
                    summaries["LSA"] = extractive_summarize_lsa(input_text, num_sentences)
                
                if use_tfidf:
                    summaries["TF-IDF"] = extractive_summarize_tfidf(input_text, num_sentences)
                
                if use_bart:
                    # This takes longer, so we'll add a progress message
                    bart_placeholder = st.empty()
                    bart_placeholder.markdown(
                        "<div style='text-align: center;'><span class='pixel-loading'>LOADING BART MODEL...</span></div>",
                        unsafe_allow_html=True
                    )
                    summaries["BART"] = abstractive_summarize_bart(input_text, max_length)
                    bart_placeholder.empty()
                
                if use_t5:
                    # This takes longer too
                    t5_placeholder = st.empty()
                    t5_placeholder.markdown(
                        "<div style='text-align: center;'><span class='pixel-loading'>LOADING T5 MODEL...</span></div>",
                        unsafe_allow_html=True
                    )
                    summaries["T5"] = abstractive_summarize_t5(input_text, max_length)
                    t5_placeholder.empty()
                
                # Calculate ROUGE scores if requested and reference summary exists
                if calculate_metrics and reference_summary:
                    for method, summary in summaries.items():
                        rouge_scores[method] = calculate_rouge(reference_summary, summary)
            
            # Display summaries
            st.markdown("<h2>📊 SUMMARY COMPARISON</h2>", unsafe_allow_html=True)
            
            # Method colors for visual distinction
            method_colors = {
                "TextRank": "#FF2A6D",  # Pink
                "LexRank": "#05D9E8",   # Cyan
                "LSA": "#F9C80E",       # Yellow
                "TF-IDF": "#D65108",    # Orange
                "BART": "#3A86FF",      # Blue
                "T5": "#8338EC"         # Purple
            }
            
            # Use tabs for the summaries
            tabs = st.tabs([f"{method} SUMMARY" for method in summaries.keys()])
            
            for i, (method, summary) in enumerate(summaries.items()):
                with tabs[i]:
                    st.markdown("<div class='pixel-container'>", unsafe_allow_html=True)
                    st.markdown(
                        create_summary_card(
                            f"{method} SUMMARY",
                            summary,
                            method_colors[method]
                        ),
                        unsafe_allow_html=True
                    )
                    
                    # Display metrics if available
                    if calculate_metrics and reference_summary and method in rouge_scores:
                        st.markdown("<h4>EVALUATION METRICS</h4>", unsafe_allow_html=True)
                        
                        # Create three columns for the three ROUGE metrics
                        m1, m2, m3 = st.columns(3)
                        
                        with m1:
                            st.markdown("<div class='scoreboard'>", unsafe_allow_html=True)
                            st.markdown("<div class='scoreboard-title'>ROUGE-1</div>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='scoreboard-value'>{rouge_scores[method]['ROUGE-1']:.3f}</div>", 
                                unsafe_allow_html=True
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        with m2:
                            st.markdown("<div class='scoreboard'>", unsafe_allow_html=True)
                            st.markdown("<div class='scoreboard-title'>ROUGE-2</div>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='scoreboard-value'>{rouge_scores[method]['ROUGE-2']:.3f}</div>", 
                                unsafe_allow_html=True
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                        with m3:
                            st.markdown("<div class='scoreboard'>", unsafe_allow_html=True)
                            st.markdown("<div class='scoreboard-title'>ROUGE-L</div>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='scoreboard-value'>{rouge_scores[method]['ROUGE-L']:.3f}</div>", 
                                unsafe_allow_html=True
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Show a side-by-side comparison
            st.markdown("<h2>🏆 FINAL COMPARISON</h2>", unsafe_allow_html=True)
            
            # Create columns for side-by-side view
            columns = st.columns(min(3, len(summaries)))
            col_index = 0
            
            for method, summary in summaries.items():
                with columns[col_index % len(columns)]:
                    st.markdown(
                        create_summary_card(
                            f"{method}",
                            summary[:150] + ("..." if len(summary) > 150 else ""),
                            method_colors[method]
                        ),
                        unsafe_allow_html=True
                    )
                col_index += 1
            
            # If we calculated metrics, show a comparison chart
            if calculate_metrics and reference_summary and rouge_scores:
                st.markdown("<h2>📈 PERFORMANCE METRICS</h2>", unsafe_allow_html=True)
                
                # Prepare data for the chart
                metrics_data = {
                    'Method': [],
                    'ROUGE-1': [],
                    'ROUGE-2': [],
                    'ROUGE-L': []
                }
                
                for method, scores in rouge_scores.items():
                    metrics_data['Method'].append(method)
                    metrics_data['ROUGE-1'].append(scores['ROUGE-1'])
                    metrics_data['ROUGE-2'].append(scores['ROUGE-2'])
                    metrics_data['ROUGE-L'].append(scores['ROUGE-L'])
                
                # Convert to DataFrame
                metrics_df = pd.DataFrame(metrics_data)
                
                # Display as a table
                st.dataframe(metrics_df.style.highlight_max(axis=0))
                
                # Create a bar chart
                st.markdown("<div class='pixel-container'>", unsafe_allow_html=True)
                
                # Reshape the data for charting
                chart_data = pd.melt(
                    metrics_df, 
                    id_vars=['Method'], 
                    value_vars=['ROUGE-1', 'ROUGE-2', 'ROUGE-L'],
                    var_name='Metric', 
                    value_name='Score'
                )
                
                # Display the chart
                st.bar_chart(
                    data=chart_data,
                    x='Method',
                    y='Score',
                    color='Metric',
                    use_container_width=True
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Show the winner
                best_method = metrics_df.iloc[:, 1:].mean(axis=1).idxmax()
                
                st.markdown(
                    f"""
                    <div style='text-align: center; margin: 20px 0;'>
                        <h2 style='font-family: "VT323", monospace; color: #F9C80E; text-shadow: 3px 3px 0px #FF2A6D;'>
                            🏆 WINNER: {best_method} 🏆
                        </h2>
                        <p style='font-family: "Space Mono", monospace; font-size: 16px;'>
                            Based on ROUGE scores compared to the reference summary
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Add a retro game-like footer
            st.markdown(
                """
                <div style='text-align: center; margin-top: 30px; padding: 20px; border-top: 2px solid #05D9E8;'>
                    <p style='font-family: "VT323", monospace; font-size: 18px; color: #FF2A6D;'>
                        FINANCIAL TEXT SUMMARIZER 3000 © 2025 - INSERT COIN TO CONTINUE
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()