from rake_nltk import Rake
from textblob import TextBlob

class InsightExtractor:
    """
    Extracts insights from text, including keywords (RAKE) and sentiment (TextBlob).
    """

    def __init__(self):
        """
        Initializes the InsightExtractor with RAKE.
        """
        # specialized stopwords/punctuations can be configured here if needed
        self.r = Rake()

    def extract_keywords(self, text: str, top_n: int = 10) -> list[str]:
        """
        Extracts top ranked keywords/phrases from the text using RAKE.

        Args:
            text (str): Input text.
            top_n (int): Number of top keywords to return.

        Returns:
            list[str]: List of keywords.
        """
        if not text or not text.strip():
            return []

        # RAKE analysis
        self.r.extract_keywords_from_text(text)
        
        # Get ranked phrases with scores
        ranked_phrases = self.r.get_ranked_phrases()
        
        # Return top N
        return ranked_phrases[:top_n]

    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyzes the sentiment of the text using TextBlob.

        Args:
            text (str): Input text.

        Returns:
            dict: Dictionary containing polarity, subjectivity, and a descriptive label.
        """
        if not text or not text.strip():
            return {"polarity": 0.0, "subjectivity": 0.0, "label": "Neutral"}

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Determine label based on polarity
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "polarity": round(polarity, 2),
            "subjectivity": round(subjectivity, 2),
            "label": label
        }

    def generate_insights(self, text: str) -> dict:
        """
        Generates combined insights (keywords + sentiment).

        Args:
            text (str): Input text.

        Returns:
            dict: Structured insights.
        """
        return {
            "keywords": self.extract_keywords(text),
            "sentiment": self.analyze_sentiment(text)
        }

if __name__ == "__main__":
    print("--- Running InsightExtractor Test ---")
    
    extractor = InsightExtractor()
    
    dummy_text = """
    InSightify is an amazing tool that saves time by summarizing long documents. 
    However, the installation process can be a bit tricky and frustrating for beginners.
    Overall, it is a very useful project with great potential for future improvements.
    """
    
    print(f"Input Text: {dummy_text.strip()}\n")
    
    # Test Keywords
    keywords = extractor.extract_keywords(dummy_text)
    print(f"[Keywords]: {keywords}")
    
    # Test Sentiment
    sentiment = extractor.analyze_sentiment(dummy_text)
    print(f"[Sentiment]: {sentiment}")
    
    print("\n--- Test Complete ---")
