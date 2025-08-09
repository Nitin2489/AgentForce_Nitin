#!/usr/bin/env python3
"""
Quick Demo - CodeForge AI Mock Test Generator
Shows how test generation works without API calls
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents.mock_test_generator import MockTestGeneratorAgent


def main():
    """Quick demo of mock test generation"""
    print("🚀 CodeForge AI - Quick Demo (No API Required)")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Sample code for testing
    sample_code = '''
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
'''
    
    print("📝 Sample Code:")
    print(sample_code)
    print("\n" + "=" * 50)
    
    try:
        # Initialize mock test generator (no API key needed)
        print("🔧 Initializing Mock Test Generator...")
        test_agent = MockTestGeneratorAgent()
        print("✅ Mock Test Generator ready!")
        
        # Generate tests
        print("\n🧪 Generating test cases...")
        result = test_agent.generate_tests(sample_code, test_framework="pytest")
        
        if result['success']:
            print("✅ Test generation successful!")
            
            # Show results
            tests = result['tests']
            coverage = result['coverage']
            
            print(f"\n📊 Results:")
            print(f"   Total Tests: {tests['test_count']}")
            print(f"   Estimated Coverage: {coverage['coverage_percentage']}%")
            print(f"   Functions Covered: {coverage['functions_covered']}")
            print(f"   Classes Covered: {coverage['classes_covered']}")
            
            # Show test categories
            categories = tests['categories']
            print(f"\n📋 Test Categories:")
            print(f"   Unit Tests: {categories['unit_tests']}")
            print(f"   Integration Tests: {categories['integration_tests']}")
            print(f"   Edge Case Tests: {categories['edge_case_tests']}")
            print(f"   Error Tests: {categories['error_tests']}")
            
            # Show summary
            print(f"\n📝 Summary:")
            print(f"   {result['summary']}")
            
            # Show suggestions
            print(f"\n💡 Suggestions:")
            for suggestion in result['suggestions'][:3]:
                print(f"   - {suggestion}")
            
            # Save generated tests
            with open("quick_demo_tests.py", "w") as f:
                f.write(result['raw_response'])
            
            print(f"\n💾 Generated tests saved to: quick_demo_tests.py")
            
            # Show sample of generated code
            print(f"\n📄 Sample Generated Test Code:")
            test_code = result['raw_response']
            lines = test_code.split('\n')[:15]  # Show first 15 lines
            for line in lines:
                print(f"   {line}")
            print("   ... (see quick_demo_tests.py for full code)")
            
        else:
            print(f"❌ Test generation failed: {result['error']}")
        
        print(f"\n🎯 Demo completed!")
        print(f"💡 This works without any API calls or costs!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")


if __name__ == "__main__":
    main()
