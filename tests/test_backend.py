import os
import sys
from fpdf import FPDF

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.loader import DocumentLoader
from modules.preprocessor import TextPreprocessor

def test_backend():
    print("=== Starting Backend Verification ===")
    
    loader = DocumentLoader()
    preprocessor = TextPreprocessor()
    
    # 1. Test Text File
    txt_path = "test_sample.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("This is a sample text file.\n   It has   erratic   spacing.  ")
    
    try:
        print(f"[TEST] Loading {txt_path}...")
        raw_text = loader.load_file(txt_path)
        print(f"  -> Loaded {len(raw_text)} chars.")
        
        cleaned = preprocessor.clean_text(raw_text)
        print(f"  -> Cleaned: '{cleaned}'")
        assert cleaned == "This is a sample text file. It has erratic spacing.", "Cleaning failed!"
        print("[PASS] Text loading and cleaning.")
    except Exception as e:
        print(f"[FAIL] Text test failed: {e}")

    # 2. Test PDF File
    pdf_path = "test_sample.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    long_text = "This is a sentence. " * 50
    pdf.multi_cell(0, 10, txt=long_text)
    pdf.output(pdf_path)
    
    try:
        print(f"[TEST] Loading {pdf_path}...")
        pdf_text = loader.load_file(pdf_path)
        print(f"  -> Loaded {len(pdf_text)} chars.")
        
        chunks = preprocessor.chunk_text(pdf_text, chunk_size=20)
        print(f"  -> Generated {len(chunks)} chunks with chunk_size=20 (words).")
        # Just check if we got chunks
        assert len(chunks) > 1, "Chunking failed to split text!"
        print("[PASS] PDF loading and chunking.")
        
    except Exception as e:
        print(f"[FAIL] PDF test failed: {e}")

    # Cleanup
    if os.path.exists(txt_path): os.remove(txt_path)
    if os.path.exists(pdf_path): os.remove(pdf_path)
    
    print("=== Verification Complete ===")

if __name__ == "__main__":
    test_backend()
