"""
StructCrew Lead Generation - Automated Setup Script
Checks dependencies, creates directories, and configures environment
Author: StructCrew Development Team
Updated: Nov 27, 2025
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

# ANSI colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{text.center(60)}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def check_python_version():
    """Check Python version (need 3.11+)"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python 3.11+ required. You have {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run(['pip', '--version'], capture_output=True, check=True)
        print_success("pip is installed")
        return True
    except:
        print_error("pip not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'data/raw_images',
        'data/extracted_text',
        'logs',
        'templates',
        '.agent/workflows'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success(f"Created {len(directories)} directories")

def create_env_file():
    """Create .env from template if not exists"""
    env_file = Path('.env')
    template_file = Path('.env.template')
    
    if env_file.exists():
        print_warning(".env file already exists (skipping)")
        return
    
    if template_file.exists():
        shutil.copy(template_file, env_file)
        print_success("Created .env file from template")
        print_info("  → Edit .env file with your credentials!")
    else:
        print_error(".env.template not found")

def install_requirements():
    """Install Python dependencies"""
    print_info("Installing Python dependencies...")
    
    try:
        subprocess.run(
            ['pip', 'install', '-r', 'requirements.txt'],
            check=True
        )
        print_success("Python dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        return False

def install_playwright():
    """Install Playwright browsers"""
    print_info("Installing Playwright browsers (this may take a few minutes)...")
    
    try:
        subprocess.run(['playwright', 'install', 'chromium'], check=True)
        print_success("Playwright chromium browser installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install Playwright browsers")
        print_info("  → Run manually: playwright install chromium")
        return False

def install_spacy_model():
    """Install spaCy language model"""
    print_info("Installing spaCy English language model...")
    
    try:
        subprocess.run(
            ['python', '-m', 'spacy', 'download', 'en_core_web_sm'],
            check=True
        )
        print_success("spaCy language model installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install spaCy model")
        print_info("  → Run manually: python -m spacy download en_core_web_sm")
        return False

def check_optional_dependencies():
    """Check for optional dependencies"""
    optional = {
        'tesseract': 'Tesseract OCR (fallback if Claude API unavailable)',
        'git': 'Git (for version control)'
    }
    
    print_info("Checking optional dependencies...")
    
    for cmd, description in optional.items():
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            print_success(f"{cmd}: {description}")
        except:
            print_warning(f"{cmd} not found: {description}")

def show_next_steps():
    """Display next steps"""
    print_header("SETUP COMPLETE!")
    
    print(f"{BOLD}Next Steps:{RESET}\n")
    
    steps = [
        ("1. Configure .env file", "Edit .env with your API keys and credentials"),
        ("2. Get Claude API key", "Visit: https://console.anthropic.com/"),
        ("3. Set up Gmail API", "Visit: https://console.cloud.google.com/"),
        ("4. Test the scraper", "python 1_scraper/instagram_scraper_pro.py"),
        ("5. Read the docs", "See README.md and COMPLIANCE_CHECKLIST.md"),
        ("6. Run workflow", "Follow .agent/workflows/lead-gen-pipeline.md")
    ]
    
    for step, description in steps:
        print(f"{GREEN}✓{RESET} {BOLD}{step}{RESET}")
        print(f"  → {description}\n")
    
    print(f"\n{YELLOW}⚠ IMPORTANT:{RESET}")
    print("  • Review COMPLIANCE_CHECKLIST.md before sending emails")
    print("  • Test with small batches first (10-50 emails)")
    print("  • Monitor logs daily")
    print("  • Respect unsubscribe requests immediately\n")
    
    print(f"{BLUE}📚 Documentation:{RESET}")
    print("  • README.md - Complete project overview")
    print("  • COMPLIANCE_CHECKLIST.md - Legal requirements")
    print("  • .agent/workflows/lead-gen-pipeline.md - Step-by-step guide\n")

def main():
    """Main setup function"""
    print_header("StructCrew Lead Gen - Automated Setup")
    
    print(f"{BOLD}Checking system requirements...{RESET}\n")
    
    # Check Python version
    if not check_python_version():
        print_error("Setup aborted. Please install Python 3.11 or higher.")
        sys.exit(1)
    
    # Check pip
    if not check_pip():
        print_error("Setup aborted. Please install pip.")
        sys.exit(1)
    
    print()
    
    # Create directories
    print(f"{BOLD}Creating project directories...{RESET}\n")
    create_directories()
    
    print()
    
    # Create .env file
    print(f"{BOLD}Setting up configuration...{RESET}\n")
    create_env_file()
    
    print()
    
    # Ask user if they want to install dependencies
    print(f"{BOLD}Install dependencies?{RESET}")
    print("This will:")
    print("  • Install Python packages (playwright, anthropic, etc.)")
    print("  • Install Playwright browsers (~300MB download)")
    print("  • Install spaCy language model (~20MB)\n")
    
    response = input(f"{YELLOW}Continue? (y/n):{RESET} ").lower().strip()
    
    if response == 'y':
        print()
        
        # Install requirements
        if not install_requirements():
            print_warning("Some dependencies failed to install. Check logs above.")
        
        print()
        
        # Install Playwright
        install_playwright()
        
        print()
        
        # Install spaCy model
        install_spacy_model()
        
        print()
    else:
        print_warning("Skipped dependency installation")
        print_info("  → Run manually: pip install -r requirements.txt")
    
    # Check optional dependencies
    print()
    check_optional_dependencies()
    
    # Show next steps
    print()
    show_next_steps()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Setup interrupted by user.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)
