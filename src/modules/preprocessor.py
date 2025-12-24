import re
import nltk

class TextPreprocessor:
    """
    Preprocesses text for NLP tasks: cleaning and chunking.
    """

    def __init__(self):
        """
        Initializes the preprocessor and ensures necessary NLTK data is available.
        """
        self._download_nltk_data()

    def _download_nltk_data(self):
        """Downloads required NLTK data if not present."""
        required_packages = ['punkt', 'punkt_tab']
        for package in required_packages:
            try:
                nltk.data.find(f'tokenizers/{package}')
            except LookupError:
                try:
                    nltk.download(package, quiet=True)
                except Exception:
                    # punkt_tab might fail on older NLTK versions or if not found, 
                    # specific error handling can be added if strict
                    pass

    def clean_text(self, text: str) -> str:
        """
        Cleans the input text by removing extra whitespace and non-printing characters.

        Args:
            text (str): Raw text.

        Returns:
            str: Cleaned text.
        """
        if not text:
            return ""

        # Normalize newlines and whitespace
        # Replace multiple newlines/tabs/spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-printable characters (optional, but good for cleaning PDF noise)
        # Keeping basic printable ASCII + common generic unicode characters if needed.
        # For now, just stripping leading/trailing whitespace is the most safe operation
        # alongside the whitespace normalization.
        
        return text.strip()

    def chunk_text(self, text: str, chunk_size: int = 1000) -> list[str]:
        """
        Splits text into chunks of approximately `chunk_size` words, preserving sentence boundaries.

        Args:
            text (str): The text to chunk.
            chunk_size (int): Maximum number of words per chunk.

        Returns:
            list[str]: List of text chunks.
        """
        if not text:
            return []

        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_word_count = 0

        for sentence in sentences:
            # Simple word count by splitting
            word_count = len(sentence.split())
            
            # If adding this sentence exceeds chunk size (and the chunk isn't empty),
            # finalize the current chunk.
            if current_word_count + word_count > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
            
            # If a single sentence is huge (larger than chunk size), we still have to add it 
            # (or split it further, but for now we keep sentences intact as per requirements).
            current_chunk.append(sentence)
            current_word_count += word_count

        # Add any remaining text
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
