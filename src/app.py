import streamlit as st
import os
import time
from modules.loader import DocumentLoader
from modules.preprocessor import TextPreprocessor
from modules.model import Summarizer
from modules.insights import InsightExtractor
from modules.visualizer import InsightVisualizer
from modules.reporter import ReportGenerator

# --- Configuration & Setup ---
st.set_page_config(
    page_title="InSightify",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure temp directories exist
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# --- Lazy Loading Models ---
@st.cache_resource
def load_summarizer():
    return Summarizer()

@st.cache_resource
def load_extractor():
    return InsightExtractor()

# --- Main Application ---
def main():
    # --- Sidebar ---
    st.sidebar.title("InSightify 📊")
    st.sidebar.markdown("### Document Settings")
    
    uploaded_file = st.sidebar.file_uploader("Upload Document (PDF/TXT)", type=["pdf", "txt"])
    
    summary_mode = st.sidebar.radio(
        "Summary Mode",
        options=["Concise", "Detailed"],
        index=0,
        help="Concise: Short & sweet. Detailed: Comprehensive overview."
    )
    
    generate_btn = st.sidebar.button("Generate Analysis", type="primary")

    # --- Main Content ---
    st.title("InSightify: Smart Report Summarizer")
    st.markdown("Upload a document to generate AI-powered summaries, insights, and visual reports.")
    st.divider()

    if generate_btn and uploaded_file:
        try:
            with st.spinner("Processing document... Please wait."):
                # 1. Save uploaded file temporarily
                file_path = os.path.join(TEMP_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 2. Load & Preprocess
                status_text = st.empty()
                status_text.info("Loading and cleaning text...")
                
                loader = DocumentLoader()
                raw_text = loader.load_file(file_path)
                
                preprocessor = TextPreprocessor()
                cleaned_text = preprocessor.clean_text(raw_text)
                chunks = preprocessor.chunk_text(cleaned_text)
                
                # 3. Summarization
                status_text.info("Generating AI summary...")
                summarizer = load_summarizer()
                
                if summary_mode == "Concise":
                    summary_text = summarizer.generate_concise_summary(chunks)
                else:
                    summary_text = summarizer.generate_detailed_summary(chunks)

                # 4. Insight Extraction
                status_text.info("Extracting insights & sentiment...")
                extractor = load_extractor()
                insights = extractor.generate_insights(cleaned_text)
                keywords = insights["keywords"]
                sentiment = insights["sentiment"]

                # 5. Visualization Generation
                status_text.info("Creating visualizations...")
                visualizer = InsightVisualizer()
                
                img_paths = {
                    "wordcloud": os.path.join(TEMP_DIR, "wordcloud.png"),
                    "keyword_chart": os.path.join(TEMP_DIR, "keyword_chart.png"),
                    "sentiment_chart": os.path.join(TEMP_DIR, "sentiment_chart.png"),
                    "compression_chart": os.path.join(TEMP_DIR, "compression_chart.png")
                }
                
                visualizer.generate_wordcloud(keywords, img_paths["wordcloud"])
                visualizer.generate_keyword_bar_chart(keywords, img_paths["keyword_chart"])
                visualizer.generate_sentiment_chart(sentiment, img_paths["sentiment_chart"])
                visualizer.generate_compression_chart(len(cleaned_text), len(summary_text), img_paths["compression_chart"])

                # 6. PDF Report Generation
                status_text.info("Compiling PDF report...")
                reporter = ReportGenerator()
                report_path = os.path.join(TEMP_DIR, "InSightify_Report.pdf")
                reporter.generate_report(
                    output_path=report_path,
                    title=f"Report: {uploaded_file.name}",
                    summary=summary_text,
                    keywords=keywords,
                    sentiment=sentiment,
                    image_paths=img_paths
                )

                status_text.empty() # Clear status
                st.toast("Analysis Complete!", icon="✅")

                # --- Display Results ---
                
                # Summary Section
                st.subheader("📝 Executive Summary")
                st.info(summary_text)
                
                # Insights Section
                st.subheader("🔍 Key Insights")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Top Keywords**")
                    st.write(", ".join([f"`{k}`" for k in keywords[:10]]))
                
                with col2:
                    st.markdown("**Sentiment Analysis**")
                    label = sentiment['label']
                    color = "green" if label == "Positive" else "red" if label == "Negative" else "gray"
                    st.markdown(f":{color}[**{label}**]")
                    st.write(f"Polarity: {sentiment['polarity']}")

                # Visualizations Section
                st.subheader("📊 Visual Data Analysis")
                tab1, tab2, tab3, tab4 = st.tabs(["Word Cloud", "Top Keywords", "Sentiment", "Compression"])
                
                with tab1:
                    st.image(img_paths["wordcloud"], use_container_width=True)
                with tab2:
                    st.image(img_paths["keyword_chart"], use_container_width=True)
                with tab3:
                    st.image(img_paths["sentiment_chart"], use_container_width=True)
                with tab4:
                    st.image(img_paths["compression_chart"], use_container_width=True)

                # Download Section
                st.divider()
                st.subheader("📥 Download Report")
                with open(report_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_file,
                        file_name="InSightify_Report.pdf",
                        mime="application/pdf",
                        type="primary"
                    )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.code(e)
            
    elif generate_btn and not uploaded_file:
        st.warning("Please upload a document first.")

if __name__ == "__main__":
    main()
