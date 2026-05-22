# Deployment Guide - Narrative Competency Assessment App

This guide explains how to deploy the Claude AI-powered narrative assessment app to Streamlit Cloud.

## Prerequisites

- GitHub account with the narrative-assessment-app repository
- Anthropic API key (from https://console.anthropic.com/)
- Streamlit Cloud account (free tier available at https://streamlit.io/cloud)

## Local Testing (Optional)

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### 3. Run locally:
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Deployment to Streamlit Cloud

### Step 1: Verify GitHub Repository
Ensure your code is committed and pushed to GitHub:
```bash
git status
git push origin main
```

### Step 2: Connect to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select:
   - GitHub repo: `atn-source/narrative-assessment-app`
   - Branch: `main`
   - File: `app.py`
4. Click "Deploy"

### Step 3: Add API Key as Secret
1. Your app will start deploying
2. Once it appears in the dashboard, click on your app
3. Click the "⚙️" menu → "Settings"
4. Go to "Secrets" section
5. Add your API key:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-..."
   ```
6. Click "Save"

### Step 4: Wait for Rerun
The app will automatically rerun with the new secret loaded. Once it completes, your app is ready!

## Accessing Your App

Your app will be available at: `https://<your-username>-narrative-assessment-app.streamlit.app`

## Monitoring & Troubleshooting

### View Logs
- Click on your app in Streamlit Cloud dashboard
- Logs show in the app details panel

### Common Issues

**"API key not configured" error:**
- Check Settings → Secrets
- Ensure `ANTHROPIC_API_KEY` is set correctly
- Wait a few seconds for the app to reload

**Assessment takes too long:**
- Claude is processing the narrative
- Each competency requires 1 API call
- 9 competencies = 9 API calls (typically 30-60 seconds)

**File upload fails:**
- Ensure file is DOCX or PDF
- Check file isn't corrupted
- Maximum file size: 200MB (Streamlit default)

## Cost Considerations

**Anthropic API Usage:**
- Each assessment = 9 API calls (one per competency)
- Cost varies based on prompt and response tokens
- For a ~23,000 character narrative: approximately $0.10-0.20 per assessment
- See https://www.anthropic.com/pricing for current rates

**Streamlit Cloud:**
- Free tier: 1 app, 1GB RAM, limited resources
- Pro tier: $10/month for additional apps
- See https://streamlit.io/pricing for details

## Updates & Maintenance

To update your deployed app:
```bash
git add .
git commit -m "Update features/fixes"
git push origin main
```

The app on Streamlit Cloud will automatically redeploy within minutes.

## Support

For issues with:
- **Streamlit**: https://discuss.streamlit.io/
- **Anthropic API**: https://support.anthropic.com/
- **This app**: Check GitHub Issues or contact the development team
