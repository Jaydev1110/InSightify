import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

class InsightVisualizer:
    """
    Generates static visualizations for insights and metrics.
    """

    def generate_wordcloud(self, keywords: list[str], output_path: str):
        """
        Generates a word cloud from a list of keywords.

        Args:
            keywords (list[str]): List of keywords/phrases.
            output_path (str): Path to save the image.
        """
        if not keywords:
            return

        text = " ".join(keywords)
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white'
        ).generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(output_path)
        plt.close()

    def generate_keyword_bar_chart(self, keywords: list[str], output_path: str, top_n: int = 10):
        """
        Generates a horizontal bar chart for top keywords.
        Note: Since RAKE provides ranked phrases, we treat rank as implicit importance.
        We will plot them in reverse order (top rank at top).

        Args:
            keywords (list[str]): List of ranked keywords.
            output_path (str): Path to save the image.
            top_n (int): Number of top keywords to plot.
        """
        if not keywords:
            return

        # Take top N and reverse for horizontal bar plotting (so #1 is at top)
        top_keywords = keywords[:top_n][::-1]
        
        plt.figure(figsize=(10, 6))
        # Create a simple range for y-axis
        y_pos = range(len(top_keywords))
        
        # We can assign an arbitrary score or just 1 for presence if we don't have scores passed down.
        # Assuming keywords are ranked, we can visualize rank via order.
        # For visual effect, let's give them growing bars based on rank order.
        scores = [i+1 for i in range(len(top_keywords))]

        plt.barh(y_pos, scores, align='center', color='skyblue')
        plt.yticks(y_pos, top_keywords)
        plt.xlabel('Relevance Rank')
        plt.title('Top Keywords')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def generate_sentiment_chart(self, sentiment: dict, output_path: str):
        """
        Generates a visualization for sentiment.

        Args:
            sentiment (dict): Dictionary with 'label' (Positive/Negative/Neutral).
            output_path (str): Path to save the image.
        """
        label = sentiment.get('label', 'Neutral')
        
        # Define colors and values for a pie chart
        # We accentuate the detected sentiment
        labels = ['Positive', 'Neutral', 'Negative']
        colors = ['#66b3ff', '#99ff99', '#ff9999'] # Light blue, Light green, Light red
        
        # Dummy distribution to highlight the detected one
        if label == 'Positive':
            sizes = [70, 20, 10]
            explode = (0.1, 0, 0)
        elif label == 'Negative':
            sizes = [10, 20, 70]
            explode = (0, 0, 0.1)
        else: # Neutral
            sizes = [20, 60, 20]
            explode = (0, 0.1, 0)

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title(f"Detected Sentiment: {label}")
        plt.axis('equal')
        plt.savefig(output_path)
        plt.close()

    def generate_compression_chart(self, original_len: int, summary_len: int, output_path: str):
        """
        Generates a bar chart comparing original vs summary text length.

        Args:
            original_len (int): Length of original text.
            summary_len (int): Length of summary text.
            output_path (str): Path to save the image.
        """
        labels = ['Original', 'Summary']
        values = [original_len, summary_len]
        colors = ['lightgray', 'lightgreen']

        plt.figure(figsize=(6, 6))
        bars = plt.bar(labels, values, color=colors)
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + (max(values)*0.01), int(yval), ha='center', va='bottom')

        plt.ylabel('Character Count')
        plt.title('Content Compression')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

if __name__ == "__main__":
    print("--- Running InsightVisualizer Test ---")
    
    viz = InsightVisualizer()
    
    # Create a dummy output directory
    output_dir = "tests/viz_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Dummy Data
    dummy_keywords = ["artificial intelligence", "machine learning", "neural networks", "deep learning", "data science", "python programming", "automation", "future tech"]
    dummy_sentiment = {"label": "Positive", "polarity": 0.8}
    dummy_orig_len = 5000
    dummy_summ_len = 500
    
    print("Generating WordCloud...")
    viz.generate_wordcloud(dummy_keywords, os.path.join(output_dir, "wordcloud.png"))
    
    print("Generating Keyword Bar Chart...")
    viz.generate_keyword_bar_chart(dummy_keywords, os.path.join(output_dir, "keywords_bar.png"))
    
    print("Generating Sentiment Chart...")
    viz.generate_sentiment_chart(dummy_sentiment, os.path.join(output_dir, "sentiment.png"))
    
    print("Generating Compression Chart...")
    viz.generate_compression_chart(dummy_orig_len, dummy_summ_len, os.path.join(output_dir, "compression.png"))
    
    print(f"--- Test Complete. Check {output_dir} ---")
