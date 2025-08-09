#!/usr/bin/env python3
"""
Test script to verify OpenAI API key setup
"""

import os
from dotenv import load_dotenv
import openai

def test_openai_connection():
    """Test if OpenAI API key is working"""
    print("🔑 Testing OpenAI API Key...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OpenAI API key not set!")
        print("   Please edit .env file and add your API key")
        return False
    
    try:
        # Test the API key
        client = openai.OpenAI(api_key=api_key)
        
        # Make a simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! Just testing the API connection."}],
            max_tokens=10
        )
        
        print("✅ OpenAI API key is working!")
        print(f"   Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print("   Please check your API key and internet connection")
        return False

if __name__ == "__main__":
    test_openai_connection()
