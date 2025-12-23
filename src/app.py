import streamlit as st
import config

def main():
    st.set_page_config(
        page_title="InSightify",
        page_icon="📊",
        layout="wide"
    )

    st.title("InSightify 📊")
    st.markdown("### Smart Report Summarizer & Visualizer")
    
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF or Text file", type=["pdf", "txt"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        # TODO: Add processing logic here
    else:
        st.info("Please upload a document to get started.")

    st.markdown("---")
    st.markdown("Powered by **InSightify AI**")

if __name__ == "__main__":
    main()
