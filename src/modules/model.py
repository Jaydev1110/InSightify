from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class Summarizer:
    """
    AI-based summarization using the T5 transformer model.
    """

    def __init__(self, model_name: str = "t5-small"):
        """
        Initializes the Summarizer with a pre-trained T5 model.
        
        Args:
            model_name (str): HuggingFace model identifier. Defaults to "t5-small" for CPU efficiency.
        """
        print(f"Loading {model_name} model on CPU...")
        self.device = torch.device("cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
        print("Model loaded successfully.")

    def summarize_chunks(self, chunks: list[str], max_length: int = 150, min_length: int = 40) -> list[str]:
        """
        Generates summaries for a list of text chunks.

        Args:
            chunks (list[str]): List of text chunks to summarize.
            max_length (int): Maximum length of the generated summary.
            min_length (int): Minimum length of the generated summary.

        Returns:
            list[str]: List of individual chunk summaries.
        """
        summaries = []
        for chunk in chunks:
            if not chunk or not chunk.strip():
                continue

            # T5 requires the prefix "summarize: " for this task
            input_text = "summarize: " + chunk
            
            # Tokenize input
            inputs = self.tokenizer(
                input_text, 
                return_tensors="pt", 
                max_length=1024, 
                truncation=True,
                padding=True
            ).to(self.device)

            # Generate summary
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )

            # Decode output
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            # Basic cleanup
            summary = summary.strip()
            summaries.append(summary)

        return summaries

    def generate_concise_summary(self, chunks: list[str]) -> str:
        """
        Generates a concise summary from the input chunks.

        Args:
            chunks (list[str]): Preprocessed text chunks.

        Returns:
            str: A single combined concise summary.
        """
        # Generate summaries for each chunk
        chunk_summaries = self.summarize_chunks(chunks, max_length=100, min_length=40)
        
        # Combine them (potentially could re-summarize if too long, but for now simple concatenation)
        combined_summary = " ".join(chunk_summaries)
        
        # Cleanup extra spaces
        return " ".join(combined_summary.split())

    def generate_detailed_summary(self, chunks: list[str]) -> str:
        """
        Generates a detailed summary from the input chunks.

        Args:
            chunks (list[str]): Preprocessed text chunks.

        Returns:
            str: A single combined detailed summary.
        """
        # Generate longer summaries for each chunk
        chunk_summaries = self.summarize_chunks(chunks, max_length=200, min_length=80)
        
        combined_summary = " ".join(chunk_summaries)
        return " ".join(combined_summary.split())

if __name__ == "__main__":
    # Internal Verification
    try:
        from loader import DocumentLoader
        from preprocessor import TextPreprocessor
    except ImportError:
        # If running as script from root or modules
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from modules.loader import DocumentLoader
        from modules.preprocessor import TextPreprocessor

    # Simple mock test if files exist, else use dummy text
    print("--- Running Summarizer Test ---")
    summarizer = Summarizer()
    
    dummy_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals. 
    Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. 
    Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. 
    A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." 
    For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    """
    
    pre = TextPreprocessor()
    clean_text = pre.clean_text(dummy_text)
    chunks = pre.chunk_text(clean_text, chunk_size=50) # Small chunk size for testing split
    
    print(f"Generated {len(chunks)} chunks.")
    
    concise = summarizer.generate_concise_summary(chunks)
    print("\n[Concise Summary]:")
    print(concise)
    
    detailed = summarizer.generate_detailed_summary(chunks)
    print("\n[Detailed Summary]:")
    print(detailed)
    
    print("\n--- Test Complete ---")
