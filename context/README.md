# Context Files

Drop PDF or DOCX reference files here. They will be automatically loaded and used by the AI assessor to provide better, more informed assessments.

## What to put here

- Assessment methodology guides
- Competency framework documentation (e.g., Permenpan 38/2017 full text)
- Scoring calibration examples
- Example narratives with expected assessment levels
- Any reference material that helps the AI understand context

## How it works

- All files are loaded once at app startup
- Content is injected into every competency assessment prompt
- Uses Anthropic prompt caching — loaded once, reused across all parallel calls (faster + cheaper)
- Supports: `.pdf` and `.docx`
- Files are read in alphabetical order

## Tips

- Keep files focused and relevant — unnecessary content adds noise
- Avoid duplicate content across files
- Shorter, clear reference material works better than large unstructured documents
