# Narrative Competency Assessment App

AI-powered assessment tool using Claude to analyze narratives against Indonesian government competency framework (Permenpan 38/2017).

## Features

- ✅ **Claude AI Analysis** - Uses Claude Sonnet 4.6 for intelligent narrative understanding
- 🎯 Analyzes narratives against 9 competencies (8 managerial + 1 socio-cultural)
- 📄 Supports DOCX and PDF file uploads
- 📊 Provides semantic scoring with evidence extraction (Level 1-5)
- 📋 Generates comprehensive feedback with behavioral indicators
- 📈 Overall summary with competency distribution analysis
- ⬇️ Download reports as Markdown

## Quick Start

### Local Setup

1. **Get an API key:**
   - Create account at https://console.anthropic.com/
   - Generate new API key
   - Save it securely

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment:**
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key: `ANTHROPIC_API_KEY=sk-ant-...`

4. **Run the app:**
```bash
streamlit run app.py
```

5. **Access:** Open http://localhost:8501 in your browser

### Deployment to Streamlit Cloud

1. **Push to GitHub:**
```bash
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo, branch, and `app.py` as the main file
   - Click "Deploy"

3. **Add API Key to Streamlit Cloud:**
   - Go to your app dashboard on Streamlit Cloud
   - Click ⚙️ Settings → Secrets
   - Add your API key:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
   - Click "Save"

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## How It Works

1. **Upload** a narrative document (DOCX or PDF)
2. **Click** "Analyze Narrative"
3. **View** scores, detailed feedback, and summary
4. **Download** the full report

## Competencies Assessed

### Managerial (8):
1. **Integritas** - Integrity and ethical behavior
2. **Kerjasama** - Collaboration and teamwork
3. **Komunikasi** - Communication skills
4. **Orientasi pada Hasil** - Results orientation
5. **Pelayanan Publik** - Public service
6. **Pengembangan Diri dan Orang Lain** - Self and others development
7. **Mengelola Perubahan** - Change management
8. **Pengambilan Keputusan** - Decision making

### Socio-Cultural (1):
9. **Perekat Bangsa** - National unity and cultural diversity

Each competency is scored on **Level 1-5** based on:
- Presence of behavioral indicators in the narrative
- Keyword and phrase matching
- Contextual relevance

## Scoring Levels

- **Level 1:** Basic competency
- **Level 2:** Team-oriented approach
- **Level 3:** Leadership capability
- **Level 4:** Organizational impact
- **Level 5:** National/strategic level

## Project Structure

```
.
├── app.py                      # Main Streamlit app
├── claude_assessor.py          # Claude AI assessment module
├── scorer.py                   # Legacy scoring logic
├── feedback_generator.py        # Feedback formatting
├── file_processor.py           # File handling (DOCX/PDF)
├── scoring-criteria.json       # Competency framework
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .streamlit/secrets.toml.example  # Streamlit Cloud secrets template
├── README.md                   # This file
└── .gitignore                  # Git ignore file
```

## Customization

### Edit Competencies
Edit `scoring-criteria.json` to:
- Add/remove competencies
- Change behavioral indicators
- Adjust level descriptions

### Modify Feedback Template
Edit `feedback_generator.py` to customize:
- Feedback format
- Development recommendations
- Report structure

## Technical Stack

- **Framework:** Streamlit 1.28+
- **AI:** Anthropic Claude Sonnet 4.6
- **File Processing:** python-docx, pypdf
- **Language:** Python 3.11+

## How It Works

1. **Upload** a narrative document (DOCX or PDF)
2. **Claude analyzes** the narrative by:
   - Parsing narrative for behavioral examples
   - Evaluating against competency level indicators
   - Extracting relevant evidence and quotes
   - Assigning achievement level (1-5) with reasoning
3. **View** comprehensive feedback including:
   - Achieved level with full description
   - Behavioral indicators identified
   - Evidence quotes from narrative
   - Guidance for next level progression
4. **Download** the complete assessment report

## Notes

- Uses Claude Sonnet 4.6 for semantic analysis
- AI-powered extraction of behavioral indicators
- Evidence-based scoring with quote attribution
- Competency levels range 1-5 with detailed descriptions
- Reports downloadable as Markdown with full details
