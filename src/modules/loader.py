import os
import pdfplumber
import PyPDF2

class DocumentLoader:
    """
    Handles loading of documents from various file formats (PDF, TXT).
    """

    def load_file(self, file_path: str) -> str:
        """
        Loads a file based on its extension and returns the extracted text.

        Args:
            file_path (str): The path to the file to be loaded.

        Returns:
            str: The extracted text content.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported or file is empty.
            Exception: For other loading errors.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        try:
            if ext == '.pdf':
                return self._load_pdf(file_path)
            elif ext == '.txt':
                return self._load_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except Exception as e:
            raise Exception(f"Error loading file {file_path}: {str(e)}")

    def _load_pdf(self, file_path: str) -> str:
        """
        Extracts text from a PDF file using pdfplumber for better accuracy.
        
        Args:
            file_path (str): Path to the PDF file.
            
        Returns:
            str: Extracted text.
        """
        text_content = []
        
        try:
            # First try with pdfplumber (better for text extraction)
            with pdfplumber.open(file_path) as pdf:
                if not pdf.pages:
                    raise ValueError("PDF file is empty (no pages found).")
                
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                        
            full_text = "\n".join(text_content)
            
            if not full_text.strip():
                # Fallback to PyPDF2 if pdfplumber yields empty text (scanned or weird encoding)
                return self._load_pdf_fallback(file_path)

            return full_text

        except Exception as e:
            # If pdfplumber fails completely, try fallback
            try:
                return self._load_pdf_fallback(file_path)
            except Exception as fallback_error:
                raise Exception(f"Failed to extract PDF text: {str(e)} | Fallback error: {str(fallback_error)}")

    def _load_pdf_fallback(self, file_path: str) -> str:
        """
        Fallback PDF extraction using PyPDF2.
        """
        text_content = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) == 0:
                raise ValueError("PDF file is empty.")
                
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        full_text = "\n".join(text_content)
        if not full_text.strip():
            raise ValueError("Could not extract text from PDF. File might be empty or contain only images.")
            
        return full_text

    def _load_txt(self, file_path: str) -> str:
        """
        Reads text from a text file.
        
        Args:
            file_path (str): Path to the text file.
            
        Returns:
            str: File content.
        """
        if os.path.getsize(file_path) == 0:
            raise ValueError("Text file is empty.")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
