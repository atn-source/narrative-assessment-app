import streamlit as st
import tempfile
from pathlib import Path
from file_processor import extract_text, get_file_size_mb
from scorer import score_narrative, format_score_summary
from feedback_generator import generate_feedback, generate_summary_feedback

st.set_page_config(page_title="Narrative Assessment", layout="wide")

st.title("📝 Narrative Competency Assessment")
st.markdown("Analyze narratives against competency rubric framework")

uploaded_file = st.file_uploader(
    "Upload narrative file (DOCX or PDF)",
    type=["docx", "pdf"],
    help="Supported formats: Microsoft Word (.docx) and PDF (.pdf)"
)

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        file_size = get_file_size_mb(tmp_path)
        st.info(f"📄 File: {uploaded_file.name} ({file_size:.2f} MB)")

        with st.spinner("Extracting text..."):
            narrative_text = extract_text(tmp_path)

        Path(tmp_path).unlink()

        if len(narrative_text.strip()) == 0:
            st.error("The uploaded file appears to be empty. Please upload a file with content.")
        else:
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown("### File Preview")
                preview_length = min(500, len(narrative_text))
                st.text(narrative_text[:preview_length] + "...")
                st.caption(f"Total characters: {len(narrative_text)}")

            with col2:
                st.markdown("### Assessment Results")

                if st.button("🔍 Analyze Narrative", type="primary"):
                    with st.spinner("Analyzing against competency rubric..."):
                        scores = score_narrative(narrative_text)

                    st.success("✅ Analysis Complete!")

                    with st.expander("📊 Score Summary", expanded=True):
                        st.markdown(format_score_summary(scores))

                    with st.expander("📋 Detailed Feedback"):
                        st.markdown(generate_feedback(scores, narrative_text))

                    with st.expander("📈 Overall Summary"):
                        st.markdown(generate_summary_feedback(scores))

                    st.divider()

                    st.markdown("### Download Results")

                    full_report = f"""# Laporan Penilaian Kompetensi

## Informasi File
- **Nama File:** {uploaded_file.name}
- **Ukuran:** {file_size:.2f} MB
- **Jumlah Karakter:** {len(narrative_text)}

---

{format_score_summary(scores)}

---

{generate_feedback(scores, narrative_text)}

---

{generate_summary_feedback(scores)}
"""

                    st.download_button(
                        label="⬇️ Download Full Report (Markdown)",
                        data=full_report.encode('utf-8'),
                        file_name=f"assessment_report_{uploaded_file.name.split('.')[0]}.md",
                        mime="text/markdown"
                    )

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
else:
    st.info("👆 Upload a DOCX or PDF file to begin assessment")
