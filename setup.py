#!/usr/bin/env python3
"""
CodeForge AI Setup Script
Helps users set up the CodeForge AI development environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_banner():
    """Print the CodeForge AI banner"""
    print("=" * 60)
    print("🚀 CodeForge AI - Multi-Modal Code Intelligence Agent")
    print("Built for AgentForce Hackathon 2025")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.9+ is required.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def check_pip():
    """Check if pip is available"""
    print("📦 Checking pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # First, upgrade pip to latest version
        print("   Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      capture_output=True, check=True)
        
        # Install dependencies with verbose output
        print("   Installing packages from requirements.txt...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("   Trying minimal requirements...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_minimal.txt"], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies:")
            print(result.stderr)
            
            # Try alternative approach for problematic packages
            print("🔄 Trying alternative installation approach...")
            try:
                # Install core packages first
                core_packages = [
                    "numpy>=1.26.0",
                    "pandas>=2.2.0", 
                    "langchain>=0.1.0",
                    "openai>=1.12.0",
                    "fastapi>=0.109.0",
                    "streamlit>=1.29.0"
                ]
                
                for package in core_packages:
                    print(f"   Installing {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                 capture_output=True, check=True)
                
                print("✅ Core dependencies installed successfully")
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Alternative installation also failed: {e}")
                return False
                
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    print("🔧 Setting up environment file...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    # Read the example file
    example_file = Path("env_example.txt")
    if not example_file.exists():
        print("❌ env_example.txt not found")
        return False
    
    # Copy example to .env
    with open(example_file, 'r') as f:
        content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ Created .env file")
    print("   Please edit .env and add your OpenAI API key")
    return True


def check_openai_key():
    """Check if OpenAI API key is set"""
    print("🔑 Checking OpenAI API key...")
    
    # Load from .env if it exists
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OpenAI API key is set")
        return True
    else:
        print("⚠️  OpenAI API key not set")
        print("   Please edit .env file and add your OpenAI API key")
        return False


def run_tests():
    """Run basic tests to verify installation"""
    print("🧪 Running basic tests...")
    
    try:
        # Test imports
        sys.path.append(str(Path(__file__).parent / "src"))
        
        from src.core.analyzer import CodeAnalyzer
        print("✅ Core analyzer imported successfully")
        
        # Test basic functionality
        analyzer = CodeAnalyzer()
        test_code = "def hello(): return 'world'"
        result = analyzer.analyze_code(test_code)
        
        if 'error' not in result:
            print("✅ Basic analysis test passed")
            return True
        else:
            print(f"❌ Basic analysis test failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎯 Setup Complete! Next Steps:")
    print("=" * 60)
    
    print("\n1. 🔑 Set up OpenAI API Key:")
    print("   - Edit the .env file")
    print("   - Replace 'your_openai_api_key_here' with your actual API key")
    print("   - Get your API key from: https://platform.openai.com/api-keys")
    
    print("\n2. 🚀 Run the demo:")
    print("   python demo.py")
    
    print("\n3. 📝 Analyze your code:")
    print("   python main.py your_file.py")
    
    print("\n4. 🌐 Use the web interface:")
    print("   streamlit run src/ui/web_interface.py")
    
    print("\n5. 📚 Read the documentation:")
    print("   - README.md for detailed usage")
    print("   - examples/ for sample code")
    
    print("\n6. 🏆 Hackathon Submission:")
    print("   - Create a 2-minute demo video")
    print("   - Prepare 8-slide presentation")
    print("   - Document your agent architecture")
    
    print("\n" + "=" * 60)
    print("🚀 Good luck with AgentForce Hackathon 2025!")
    print("=" * 60)


def main():
    """Main setup function"""
    print_banner()
    
    # Check system requirements
    if not check_python_version():
        return
    
    if not check_pip():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Setup environment
    if not create_env_file():
        return
    
    # Check API key
    check_openai_key()
    
    # Run tests
    if run_tests():
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed, but setup can continue")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
