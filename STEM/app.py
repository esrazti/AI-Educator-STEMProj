"""
PDF-to-Game Factory
A multi-agent system that transforms PDFs into interactive educational games
"""

import streamlit as st
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import pymupdf4llm
from jinja2 import Template

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page config
st.set_page_config(
    page_title="PDF Game Factory",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme vibe
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00f5ff !important;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #00f5ff;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(0, 245, 255, 0.1);
        border: 2px dashed #00f5ff;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f5ff 0%, #0080ff 100%);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 245, 255, 0.6);
    }
    
    /* Progress indicators */
    .agent-status {
        background: rgba(0, 245, 255, 0.1);
        border-left: 4px solid #00f5ff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)


class PDFGameFactory:
    """Multi-agent system to convert PDFs into interactive games"""
    
    def __init__(self):
        self.model = "gpt-4o"
        self.max_retries = 3
        # Initialize template directory
        self._setup_templates()
        
    def _setup_templates(self):
        """Ensure templates directory exists and locate template files"""
        self.template_dir = Path('templates')
        
        # If templates directory doesn't exist, try to find templates in current directory
        if not self.template_dir.exists():
            # Check if template files are in current directory
            current_dir = Path('.')
            if (current_dir / 'matching_game.html').exists():
                st.info("📁 Templates found in current directory. Creating templates/ folder...")
                self.template_dir.mkdir(exist_ok=True)
                # Move templates to proper directory
                for game_type in ['matching', 'quiz', 'flashcards']:
                    src = current_dir / f'{game_type}_game.html'
                    if src.exists():
                        import shutil
                        shutil.copy(src, self.template_dir / f'{game_type}_game.html')
            else:
                # Create empty templates directory
                self.template_dir.mkdir(exist_ok=True)
                st.warning(f"⚠️ Templates directory created at {self.template_dir.absolute()}")
                st.info("Please add the template HTML files to the templates/ directory")
        
    def agent_1_extractor(self, pdf_path: str) -> dict:
        """AI Agent 1: Extract PDF content and create Markdown summary"""
        st.markdown('<div class="agent-status">🤖 Agent 1 (Extractor): Processing PDF...</div>', 
                   unsafe_allow_html=True)
        
        try:
            # Extract markdown from PDF
            markdown_text = pymupdf4llm.to_markdown(pdf_path)
        except Exception as e:
            st.error(f"Failed to extract PDF content: {str(e)}")
            raise
        
        # Use AI to create a concise summary
        prompt = f"""You are an expert content analyzer. 
        
Given this document content, create a comprehensive summary that captures:
1. Main topic and subject area
2. Key concepts and terminology (at least 10-15 items)
3. Important facts and relationships
4. Learning objectives

Document content:
{markdown_text[:8000]}

Provide a structured summary in JSON format with these keys:
- topic: main subject
- subject_area: (e.g., "biology", "history", "programming", "physics")
- key_concepts: list of important terms/concepts
- facts: list of key facts or relationships
- learning_objectives: what students should learn

Return ONLY valid JSON, no markdown formatting."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        summary_json = self._extract_json(response.choices[0].message.content)
        summary_json['full_markdown'] = markdown_text
        
        return summary_json
    
    def agent_2_architect(self, summary: dict, game_type: str) -> dict:
        """AI Agent 2: Design game logic structure"""
        st.markdown('<div class="agent-status">🏗️ Agent 2 (Architect): Designing game structure...</div>', 
                   unsafe_allow_html=True)
        
        prompt = f"""You are a game design architect specializing in educational games.

Content Summary:
{json.dumps(summary, indent=2)}

Design a {game_type} game with the following structure:

For MATCHING game:
{{
  "game_type": "matching",
  "title": "creative title",
  "theme_color": "CSS color based on subject (e.g., medical=#00bfa5, history=#ff6b35, tech=#667eea)",
  "pairs": [
    {{"term": "concept name", "definition": "clear definition"}},
    ... (minimum 8 pairs)
  ]
}}

For QUIZ game:
{{
  "game_type": "quiz",
  "title": "creative title",
  "theme_color": "CSS color",
  "questions": [
    {{
      "question": "question text",
      "options": ["A", "B", "C", "D"],
      "correct": 0,
      "explanation": "why this is correct"
    }},
    ... (minimum 10 questions)
  ]
}}

For FLASHCARDS game:
{{
  "game_type": "flashcards",
  "title": "creative title",
  "theme_color": "CSS color",
  "cards": [
    {{"front": "term or question", "back": "definition or answer"}},
    ... (minimum 12 cards)
  ]
}}

Use content from the summary. Make it educational and engaging.
Return ONLY valid JSON."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        game_structure = self._extract_json(response.choices[0].message.content)
        return game_structure
    
    def agent_3_reviewer(self, game_structure: dict, original_summary: dict) -> tuple[bool, str]:
        """AI Agent 3: Fact-check game content against original text"""
        st.markdown('<div class="agent-status">🔍 Agent 3 (Reviewer): Fact-checking content...</div>', 
                   unsafe_allow_html=True)
        
        prompt = f"""You are a strict educational content reviewer.

Original Content Summary:
{json.dumps(original_summary, indent=2)}

Proposed Game Structure:
{json.dumps(game_structure, indent=2)}

Review the game content for:
1. Factual accuracy (do terms/definitions match the source?)
2. Completeness (are key concepts included?)
3. Clarity (are explanations clear and correct?)

Respond in JSON format:
{{
  "approved": true/false,
  "feedback": "specific issues found or 'Content approved'"
}}

Be strict but fair. Approve only if content is accurate and educational.
Return ONLY valid JSON."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        review = self._extract_json(response.choices[0].message.content)
        return review.get('approved', False), review.get('feedback', 'No feedback provided')
    
    def agent_4_refiner(self, game_structure: dict, feedback: str, original_summary: dict) -> dict:
        """AI Agent 4: Refine game based on reviewer feedback"""
        st.markdown('<div class="agent-status">✨ Agent 4 (Refiner): Improving game based on feedback...</div>', 
                   unsafe_allow_html=True)
        
        prompt = f"""You are a game content refiner.

Original Summary:
{json.dumps(original_summary, indent=2)}

Current Game Structure:
{json.dumps(game_structure, indent=2)}

Reviewer Feedback:
{feedback}

Fix the issues mentioned in the feedback while maintaining the same JSON structure.
Ensure all content is factually accurate and educationally sound.
Return ONLY the corrected JSON in the same format."""

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        refined_structure = self._extract_json(response.choices[0].message.content)
        return refined_structure
    
    def agent_5_builder(self, game_structure: dict) -> str:
        """AI Agent 5: Generate final HTML game from template"""
        st.markdown('<div class="agent-status">🎨 Agent 5 (Builder): Building game interface...</div>', 
                   unsafe_allow_html=True)
        
        game_type = game_structure.get('game_type', 'matching')
        template_path = self.template_dir / f'{game_type}_game.html'
        
        # Check if template exists
        if not template_path.exists():
            # Provide helpful error message
            available_templates = list(self.template_dir.glob('*.html'))
            error_msg = f"Template not found: {template_path}\n\n"
            
            if available_templates:
                error_msg += f"Available templates: {[t.name for t in available_templates]}"
            else:
                error_msg += "No templates found in templates/ directory.\n"
                error_msg += "Please ensure matching_game.html, quiz_game.html, and flashcards_game.html are in the templates/ folder."
            
            raise FileNotFoundError(error_msg)
        
        # Read and render template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        html_output = template.render(**game_structure)
        
        return html_output
    
    def _extract_json(self, text: str) -> dict:
        """Extract JSON from AI response (handles markdown code blocks)"""
        # Remove markdown code blocks
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {e}")
            st.code(text)
            return {}
    
    def run_diamond_workflow(self, pdf_path: str, game_type: str) -> str:
        """Execute the complete diamond workflow with retry loop"""
        
        # Agent 1: Extract and summarize
        summary = self.agent_1_extractor(pdf_path)
        if not summary:
            raise ValueError("Failed to extract PDF content")
        
        # Diamond loop: Architect → Reviewer → (Refiner) → repeat until approved
        attempt = 0
        game_structure = None
        feedback = ""
        
        while attempt < self.max_retries:
            attempt += 1
            st.info(f"🔄 Attempt {attempt}/{self.max_retries}")
            
            # Agent 2: Design game structure
            if attempt == 1:
                game_structure = self.agent_2_architect(summary, game_type)
            else:
                # Agent 4: Refine based on previous feedback
                game_structure = self.agent_4_refiner(game_structure, feedback, summary)
            
            if not game_structure:
                st.warning(f"Attempt {attempt} failed to generate structure")
                continue
            
            # Agent 3: Review
            approved, feedback = self.agent_3_reviewer(game_structure, summary)
            
            if approved:
                st.success(f"✅ Content approved on attempt {attempt}!")
                break
            else:
                st.warning(f"⚠️ Reviewer feedback (attempt {attempt}): {feedback}")
                if attempt == self.max_retries:
                    st.error("Max retries reached. Proceeding with best version...")
        
        # Agent 5: Build final game
        html_game = self.agent_5_builder(game_structure)
        
        return html_game


def main():
    """Main Streamlit application"""
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # API Key status
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("✅ OpenAI API Key loaded")
        else:
            st.error("❌ No API key found in .env file")
            st.info("Create a .env file with: OPENAI_API_KEY=your-key-here")
            st.stop()
        
        st.divider()
        
        # Game type selector
        game_type = st.selectbox(
            "🎮 Select Game Type",
            ["matching", "quiz", "flashcards"],
            format_func=lambda x: {
                "matching": "🔗 Matching Game",
                "quiz": "❓ Quiz Game",
                "flashcards": "🗂️ Flashcards"
            }[x]
        )
        
        st.divider()
        
        st.markdown("""
        ### 🤖 Agent Pipeline
        1. **Extractor** - PDF → Markdown
        2. **Architect** - Design game logic
        3. **Reviewer** - Fact-check (Diamond Loop)
        4. **Refiner** - Fix issues
        5. **Builder** - Generate HTML
        """)
    
    # Main content
    st.title("🎮 PDF-to-Game Factory")
    st.markdown("### Transform any PDF into an interactive learning game")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📄 Upload your PDF document",
        type=['pdf'],
        help="Upload any educational PDF to convert into a game"
    )
    
    if uploaded_file:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        # Generate button
        if st.button("🚀 Generate Game", type="primary"):
            try:
                factory = PDFGameFactory()
                
                with st.spinner("🔮 Running multi-agent workflow..."):
                    html_game = factory.run_diamond_workflow(temp_path, game_type)
                
                # Save game
                output_path = f"game_{game_type}_{uploaded_file.name.replace('.pdf', '')}.html"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_game)
                
                # Success message
                st.markdown(f"""
                <div class="success-box">
                    <h2>🎉 Game Generated Successfully!</h2>
                    <p>Your {game_type} game is ready to play.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Game (HTML)",
                    data=html_game,
                    file_name=output_path,
                    mime="text/html"
                )
                
                # Preview
                with st.expander("👀 Preview Game", expanded=True):
                    st.components.v1.html(html_game, height=800, scrolling=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
            
            finally:
                # Cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #00f5ff; font-family: monospace;'>
        Built with 🧠 AI Agents | Powered by GPT-4o & Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
