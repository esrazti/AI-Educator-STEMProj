# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
pip install streamlit openai pymupdf4llm python-dotenv jinja2
```

### Step 2: Set API Key (1 minute)
Create a file named `.env` in the project folder:
```env
OPENAI_API_KEY=sk-proj-your-key-here
```

Get your key from: https://platform.openai.com/api-keys

### Step 3: Run! (30 seconds)
```bash
streamlit run app.py
```

That's it! The app will open in your browser.

## First Time Use

1. **Upload a PDF** - Any educational document (textbook chapter, notes, article)
2. **Choose Game Type** - Matching, Quiz, or Flashcards
3. **Click Generate** - Wait 30-60 seconds while AI agents work
4. **Download Game** - Get standalone HTML file you can share anywhere!

## Pro Tips

✅ **Best PDFs**: 
- Educational content (textbooks, study guides)
- 10-50 pages
- Clear text (not scanned images)
- Well-formatted

❌ **Avoid**:
- Scanned PDFs without OCR
- Image-heavy documents
- Very long books (100+ pages)

## What Happens Behind the Scenes?

```
Your PDF → AI extracts content → AI designs game → 
AI fact-checks → AI refines (if needed) → 
AI builds beautiful HTML → You get game!
```

The "diamond loop" ensures quality - if AI Agent 3 finds issues, Agent 4 fixes them automatically (up to 3 tries).

## Game Examples

**Matching Game**: Perfect for vocabulary, definitions, concepts
- Example: Medical terms ↔ Definitions

**Quiz Game**: Best for testing comprehension
- Example: 10 multiple-choice questions about history

**Flashcards**: Ideal for memorization
- Example: Chemical formulas and names

## Need Help?

- **Error with API key?** Check it's correctly set in `.env`
- **Game looks weird?** Try a different PDF with clearer formatting
- **Taking too long?** Shorter PDFs (10-20 pages) work fastest

## Share Your Games!

The HTML files are completely standalone - no server needed!
- Email them
- Upload to your website
- Share via Google Drive
- Use in your LMS

Enjoy! 🎮
