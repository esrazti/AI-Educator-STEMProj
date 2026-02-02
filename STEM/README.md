# 🎮 PDF-to-Game Factory

Transform any PDF document into interactive educational games using AI-powered multi-agent workflows!

## ✨ Features

- **5-Agent AI Pipeline**: Extractor → Architect → Reviewer → Refiner → Builder
- **3 Game Types**: Matching, Quiz, and Flashcards
- **Dynamic Theming**: Color schemes adapt to content (medical, tech, history, etc.)
- **Diamond Loop Architecture**: AI agents fact-check and refine content automatically
- **Beautiful UI**: Dark-themed Streamlit interface with animated backgrounds
- **Production-Ready Games**: Standalone HTML files with no dependencies

## 🏗️ Architecture

```
┌─────────────┐
│   AI 1      │  Extract PDF → Markdown Summary
│ Extractor   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   AI 2      │  Design Game Structure (JSON)
│ Architect   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐
│   AI 3      │─NO─→ │   AI 4      │
│ Reviewer    │      │  Refiner    │
└──────┬──────┘      └──────┬──────┘
       │                    │
      YES                   │
       │◄───────────────────┘
       ▼
┌─────────────┐
│   AI 5      │  Generate HTML Game
│  Builder    │
└─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone & Install

```bash
# Clone the repository
git clone <your-repo-url>
cd pdf-game-factory

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Directory Structure

**IMPORTANT:** The app requires a specific folder structure. Create it like this:

```bash
# Create templates directory
mkdir templates

# Move HTML template files into templates/
# You should have these three files:
# - templates/matching_game.html
# - templates/quiz_game.html
# - templates/flashcards_game.html
```

Your project structure should look like:
```
./
├── app.py
├── requirements.txt
├── .env
└── templates/
    ├── matching_game.html
    ├── quiz_game.html
    └── flashcards_game.html
```

### 3. Set Up API Key

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your OpenAI API key to `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Get your API key:** https://platform.openai.com/api-keys

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Creating a Game

1. **Upload PDF**: Click "Browse files" and select your educational PDF
2. **Select Game Type**: Choose from:
   - 🔗 **Matching Game**: Match terms with definitions
   - ❓ **Quiz Game**: Multiple-choice questions with explanations
   - 🗂️ **Flashcards**: Flip cards to study
3. **Generate**: Click "🚀 Generate Game" and watch the AI agents work
4. **Download**: Save the HTML game file or preview it directly

### AI Agent Pipeline

The app uses a sophisticated multi-agent workflow:

1. **Agent 1 (Extractor)**: 
   - Converts PDF to Markdown using PyMuPDF4LLM
   - Extracts key concepts, facts, and learning objectives
   - Uses GPT-4o for intelligent summarization

2. **Agent 2 (Architect)**:
   - Designs game structure based on content
   - Selects appropriate color theme for subject area
   - Creates questions, pairs, or cards

3. **Agent 3 (Reviewer)**:
   - Fact-checks content against original text
   - Ensures educational accuracy
   - Provides specific feedback if issues found

4. **Agent 4 (Refiner)**:
   - Only runs if reviewer rejects content
   - Fixes issues based on feedback
   - Loops back to reviewer (max 3 attempts)

5. **Agent 5 (Builder)**:
   - Injects validated data into HTML templates
   - Applies dynamic theming
   - Generates standalone game file

## 🎨 Game Templates

### Matching Game
- Drag-and-drop interface
- Real-time scoring
- Confetti animation on completion
- Mobile-responsive design

### Quiz Game
- Multiple-choice questions
- Detailed explanations
- Progress tracking
- Accuracy metrics

### Flashcards
- 3D flip animation
- Keyboard navigation (←, →, Space)
- Shuffle functionality
- Progress dots

## 🎨 Theming System

Games automatically adapt their color scheme based on content:

- **Medical/Biology**: Teal (`#00bfa5`)
- **History**: Orange (`#ff6b35`)
- **Technology**: Purple (`#667eea`)
- **Physics**: Blue (`#3b82f6`)
- **Chemistry**: Green (`#10b981`)

The color is determined by AI Agent 2 during game design.

## 📁 Project Structure

```
./
├── app.py                      # Main Streamlit application
├── templates/                  # Game HTML templates (REQUIRED)
│   ├── matching_game.html      # Matching pairs game
│   ├── quiz_game.html          # Multiple-choice quiz
│   └── flashcards_game.html    # Flip-card study tool
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### AI Model Settings

By default, the app uses:
- **Model**: `gpt-4o` (GPT-4 Optimized)
- **Max Retries**: 3 attempts for reviewer loop
- **Temperature**: Varies by agent (0.2-0.7)

You can modify these in `app.py`:
```python
self.model = "gpt-4o"
self.max_retries = 3
```

## 🐛 Troubleshooting

### "Template not found" Error

**Problem:** `FileNotFoundError: Template not found: templates\matching_game.html`

**Solution:**
1. Create a `templates/` directory in your project root
2. Place all three template files inside:
   - `matching_game.html`
   - `quiz_game.html`
   - `flashcards_game.html`

```bash
mkdir templates
# Move or copy your HTML files into templates/
```

### PDF Extraction Issues

**Problem:** Content extraction fails or is incomplete

**Solutions:**
- Ensure PDF is text-based (not scanned images)
- Try PDFs under 50 pages for best results
- Complex formatting may not extract perfectly
- For scanned PDFs, use OCR preprocessing first

### API Errors

**Problem:** OpenAI API errors or authentication failures

**Solutions:**
- Check your OpenAI API key is valid and active
- Verify you have available credits at https://platform.openai.com/usage
- Ensure `.env` file is in the project root directory
- Check the `.env` file has no extra spaces: `OPENAI_API_KEY=sk-...` (no quotes needed)

### "No API key found in .env file"

**Problem:** App can't find your API key

**Solutions:**
1. Ensure `.env` file exists in project root
2. Check file contains: `OPENAI_API_KEY=your-actual-key`
3. Restart the Streamlit app after creating `.env`

### Import Errors

**Problem:** `ModuleNotFoundError` for packages

**Solution:**
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Or install individually
pip install streamlit openai python-dotenv jinja2 PyMuPDF pymupdf4llm
```

### Streamlit Won't Start

**Problem:** `streamlit: command not found`

**Solution:**
```bash
# Install streamlit
pip install streamlit

# Or use python -m
python -m streamlit run app.py
```

## 💡 Tips for Best Results

### PDF Quality
- **Best:** Text-heavy educational PDFs with clear formatting
- **Good:** Textbooks, study guides, lecture notes, research papers
- **Avoid:** Scanned images, image-heavy documents, complex layouts

### Content Length
- **Optimal:** 10-50 pages
- **Works well:** 5-100 pages
- **Too large:** 100+ pages (may timeout or hit token limits)

### Topic Specificity
- Clear, focused topics generate better games
- Single-subject PDFs work best
- Well-structured documents with headers produce better results

### Review Attempts
- The app will retry up to 3 times if content fails review
- If all 3 attempts fail, it proceeds with the best version
- Try simpler or more clearly written PDFs if this happens often

## 📋 Common Use Cases

### For Teachers
- Convert lecture slides into study games
- Create review materials from textbook chapters
- Generate quiz games for test preparation

### For Students
- Turn study notes into flashcards
- Create matching games from vocabulary lists
- Build quiz games from course materials

### For Trainers
- Transform training manuals into interactive content
- Create compliance training games
- Build onboarding materials

## 🎯 Roadmap

Future improvements planned:

- [ ] Support for image-based PDFs (OCR integration)
- [ ] More game types (crossword, word search, timeline)
- [ ] Multi-language support
- [ ] Game analytics and progress tracking
- [ ] Export to SCORM for LMS integration
- [ ] Batch processing multiple PDFs
- [ ] Custom theming options
- [ ] Collaborative game editing

## 📊 System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- Internet connection for API calls

### Recommended
- Python 3.10+
- 8GB RAM
- Fast internet connection

### API Costs
- Uses GPT-4o model
- Typical cost per game: $0.10-0.30 USD
- Depends on PDF length and complexity

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Pull requests are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Templates maintain responsive design
- AI prompts are well-documented
- Add tests for new features

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing issues first
- Provide PDF example and error logs when reporting bugs
- Include your Python version and OS

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT-4o](https://openai.com/)
- PDF extraction via [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF)
- Template rendering with [Jinja2](https://jinja.palletsprojects.com/)

---

**Built with 🧠 by AI Agents | Powered by GPT-4o & Streamlit**

*Made by EeSaRa Dev Team
