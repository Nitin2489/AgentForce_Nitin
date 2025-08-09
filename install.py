#!/usr/bin/env python3
"""
Simple installation script for CodeForge AI
Handles common dependency issues
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🚀 CodeForge AI - Installation Script")
    print("=" * 50)
    
    # Check Python version
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        return
    
    # Upgrade pip
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")
    
    # Try to install numpy first (most common issue)
    print("\n📦 Installing core dependencies...")
    
    # Install numpy with specific version for Python 3.12
    if version.major == 3 and version.minor >= 12:
        numpy_cmd = [sys.executable, "-m", "pip", "install", "numpy>=1.26.0"]
    else:
        numpy_cmd = [sys.executable, "-m", "pip", "install", "numpy>=1.24.0"]
    
    if run_command(numpy_cmd, "Installing numpy"):
        # Install pandas
        run_command([sys.executable, "-m", "pip", "install", "pandas>=2.2.0"], "Installing pandas")
        
        # Install core AI packages
        run_command([sys.executable, "-m", "pip", "install", "langchain>=0.1.0"], "Installing langchain")
        run_command([sys.executable, "-m", "pip", "install", "openai>=1.12.0"], "Installing openai")
        run_command([sys.executable, "-m", "pip", "install", "fastapi>=0.109.0"], "Installing fastapi")
        run_command([sys.executable, "-m", "pip", "install", "streamlit>=1.29.0"], "Installing streamlit")
        
        # Install remaining packages
        print("\n📦 Installing remaining packages...")
        if Path("requirements_minimal.txt").exists():
            run_command([sys.executable, "-m", "pip", "install", "-r", "requirements_minimal.txt"], "Installing remaining dependencies")
        else:
            run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], "Installing remaining dependencies")
    
    # Create .env file
    print("\n🔧 Setting up environment...")
    if not Path(".env").exists() and Path("env_example.txt").exists():
        with open("env_example.txt", "r") as f:
            content = f.read()
        with open(".env", "w") as f:
            f.write(content)
        print("✅ Created .env file")
    
    print("\n🎉 Installation completed!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python demo.py")
    print("3. Or run: streamlit run src/ui/web_interface.py")

if __name__ == "__main__":
    main()
