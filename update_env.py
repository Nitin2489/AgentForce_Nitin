#!/usr/bin/env python3
"""
Simple script to update the .env file with your API key
"""

import os

def update_env_file():
    """Update the .env file with the API key"""
    print("🔧 Updating .env file...")
    
    # Read current .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ .env file not found!")
        return
    
    # Check if API key is already set
    if 'your_openai_api_key_here' in content:
        print("📝 Current .env file contains placeholder API key")
        print("Please enter your OpenAI API key (it should start with 'sk-'):")
        
        api_key = input().strip()
        
        if not api_key.startswith('sk-'):
            print("❌ Invalid API key format. API key should start with 'sk-'")
            return
        
        # Replace the placeholder
        new_content = content.replace('your_openai_api_key_here', api_key)
        
        # Write back to file
        with open('.env', 'w') as f:
            f.write(new_content)
        
        print("✅ .env file updated successfully!")
        print("🔒 API key is now securely stored in .env file")
        
    else:
        print("✅ .env file already contains a custom API key")
    
    # Test the API key
    print("\n🧪 Testing API key...")
    os.environ.clear()  # Clear any existing env vars
    from dotenv import load_dotenv
    load_dotenv()
    
    key = os.getenv('OPENAI_API_KEY', '')
    if key and key.startswith('sk-'):
        print("✅ API key loaded successfully!")
        print(f"   Key starts with: {key[:10]}...")
    else:
        print("❌ API key not loaded correctly")

if __name__ == "__main__":
    update_env_file()
