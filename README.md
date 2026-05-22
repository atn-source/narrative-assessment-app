# Narrative Competency Assessment App

Rule-based assessment tool that analyzes narratives against Indonesian government competency framework.

## Features

- ✅ Analyzes narratives against 9 competencies (8 managerial + 1 socio-cultural)
- 📄 Supports DOCX and PDF file uploads
- 📊 Provides narrative-based scoring (Level 1-5)
- 📋 Generates detailed feedback per competency
- 📈 Overall summary and progress tracking
- ⬇️ Download reports as Markdown

## Quick Start

### Local Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
streamlit run app.py
```

3. **Access:** Open http://localhost:8501 in your browser

### Deployment to Streamlit Cloud

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: Competency assessment app"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo, branch, and `app.py` as the main file
   - Click "Deploy"

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
├── app.py                    # Main Streamlit app
├── scorer.py                 # Scoring logic
├── feedback_generator.py      # Feedback formatting
├── file_processor.py         # File handling (DOCX/PDF)
├── scoring-criteria.json     # Competency framework
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore file
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

- **Framework:** Streamlit
- **File Processing:** python-docx, pypdf
- **Language:** Python 3.8+

## Notes

- All competencies have equal weight (1x)
- Scoring is rule-based (keyword matching + indicator coverage)
- No percentage scores; narrative-level based (1-5)
- Reports downloadable as Markdown
