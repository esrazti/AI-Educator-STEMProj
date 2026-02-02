#!/usr/bin/env python3
"""
Setup script for PDF-to-Game Factory
Automatically organizes project structure and validates setup
"""

import os
import sys
from pathlib import Path
import shutil

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🎮 PDF-to-Game Factory - Setup Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: Python {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def create_templates_directory():
    """Create templates directory if it doesn't exist"""
    templates_dir = Path('templates')
    
    if templates_dir.exists():
        print(f"✅ Templates directory already exists: {templates_dir.absolute()}")
        return templates_dir
    
    templates_dir.mkdir(exist_ok=True)
    print(f"✅ Created templates directory: {templates_dir.absolute()}")
    return templates_dir

def find_and_move_templates():
    """Find template HTML files and move them to templates/ directory"""
    templates_dir = Path('templates')
    current_dir = Path('.')
    
    template_files = ['matching_game.html', 'quiz_game.html', 'flashcards_game.html']
    found_files = []
    moved_files = []
    
    for template_file in template_files:
        # Check if file exists in current directory
        src = current_dir / template_file
        dest = templates_dir / template_file
        
        if dest.exists():
            print(f"✅ Template already in place: {template_file}")
            found_files.append(template_file)
        elif src.exists():
            shutil.copy(src, dest)
            print(f"✅ Moved template: {template_file} → templates/")
            moved_files.append(template_file)
        else:
            print(f"⚠️  Template not found: {template_file}")
    
    return found_files, moved_files

def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("   Creating .env template...")
        
        with open('.env', 'w') as f:
            f.write("OPENAI_API_KEY=your-api-key-here\n")
        
        print("✅ Created .env file")
        print("   ⚠️  IMPORTANT: Edit .env and add your OpenAI API key!")
        print("   Get your key from: https://platform.openai.com/api-keys")
        return False
    
    # Check if API key is set
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'your-api-key-here' in content or 'OPENAI_API_KEY=' not in content:
        print("⚠️  .env file exists but API key not configured")
        print("   Please edit .env and add your OpenAI API key")
        return False
    
    print("✅ .env file configured")
    return True

def check_requirements():
    """Check if requirements.txt exists"""
    req_path = Path('requirements.txt')
    
    if not req_path.exists():
        print("⚠️  requirements.txt not found")
        print("   Creating requirements.txt...")
        
        requirements = """streamlit>=1.31.0
openai>=1.12.0
python-dotenv>=1.0.0
jinja2>=3.1.0
PyMuPDF>=1.24.0
pymupdf4llm>=0.0.10
"""
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        
        print("✅ Created requirements.txt")
        return False
    
    print("✅ requirements.txt found")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'openai',
        'dotenv',
        'jinja2',
        'pymupdf4llm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ Package installed: {package}")
        except ImportError:
            print(f"❌ Package missing: {package}")
            missing_packages.append(package)
    
    return missing_packages

def print_summary(template_status, env_status, missing_packages):
    """Print setup summary"""
    print()
    print("=" * 60)
    print("📋 Setup Summary")
    print("=" * 60)
    print()
    
    # Check overall status
    all_good = True
    
    # Templates
    if template_status['found'] == 3:
        print("✅ All templates are in place")
    elif template_status['found'] > 0:
        print(f"⚠️  {template_status['found']}/3 templates found")
        print("   Missing templates:")
        for missing in template_status['missing']:
            print(f"   - {missing}")
        all_good = False
    else:
        print("❌ No templates found")
        print("   Please add template HTML files to templates/ directory")
        all_good = False
    
    # Environment
    if env_status:
        print("✅ API key configured")
    else:
        print("❌ API key not configured")
        print("   Edit .env and add your OpenAI API key")
        all_good = False
    
    # Dependencies
    if not missing_packages:
        print("✅ All dependencies installed")
    else:
        print("❌ Missing dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print()
        print("   Run: pip install -r requirements.txt")
        all_good = False
    
    print()
    if all_good:
        print("🎉 Setup complete! You're ready to go!")
        print()
        print("To start the app, run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Setup incomplete. Please fix the issues above.")
    
    print()
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Create templates directory
    create_templates_directory()
    
    # Find and move templates
    found_files, moved_files = find_and_move_templates()
    
    print()
    
    # Check .env file
    env_status = check_env_file()
    
    print()
    
    # Check requirements.txt
    check_requirements()
    
    print()
    
    # Check dependencies
    missing_packages = check_dependencies()
    
    # Calculate template status
    all_templates = ['matching_game.html', 'quiz_game.html', 'flashcards_game.html']
    templates_in_place = list(Path('templates').glob('*.html'))
    template_names = [t.name for t in templates_in_place]
    missing_templates = [t for t in all_templates if t not in template_names]
    
    template_status = {
        'found': len(templates_in_place),
        'missing': missing_templates
    }
    
    # Print summary
    print_summary(template_status, env_status, missing_packages)

if __name__ == "__main__":
    main()
