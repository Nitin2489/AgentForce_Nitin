#!/usr/bin/env python3
"""
Test Runner for CodeForge AI Generated Tests
Demonstrates how to use the generated test cases
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents.mock_test_generator import MockTestGeneratorAgent


def load_sample_code():
    """Load sample code for testing"""
    return '''
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

def process_numbers(numbers):
    """Process a list of numbers"""
    if not numbers:
        return []
    
    result = []
    for num in numbers:
        if isinstance(num, (int, float)):
            result.append(num * 2)
        else:
            raise ValueError(f"Invalid number: {num}")
    
    return result

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
    
    def get_history(self):
        return self.history
'''


def run_test_demo():
    """Run the test generation and execution demo"""
    print("🧪 CodeForge AI Test Generation Demo")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize test generator
        print("🔧 Initializing Mock Test Generator...")
        test_agent = MockTestGeneratorAgent()
        print("✅ Test generator initialized!")
        
        # Load sample code
        print("\n📝 Loading sample code...")
        code = load_sample_code()
        print("✅ Sample code loaded")
        
        # Generate tests
        print("\n🧪 Generating test cases...")
        result = test_agent.generate_tests(code, test_framework="pytest")
        
        if result['success']:
            print("✅ Tests generated successfully!")
            
            # Display test information
            tests = result['tests']
            coverage = result['coverage']
            
            print(f"\n📊 Test Statistics:")
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
            
            # Show test summary
            print(f"\n📝 Test Summary:")
            print(f"   {result['summary']}")
            
            # Show suggestions
            print(f"\n💡 Improvement Suggestions:")
            for i, suggestion in enumerate(result['suggestions'][:5], 1):
                print(f"   {i}. {suggestion}")
            
            # Save generated tests to file
            test_file = "generated_tests.py"
            with open(test_file, 'w') as f:
                f.write(result['raw_response'])
            
            print(f"\n💾 Generated tests saved to: {test_file}")
            
            # Show sample of generated test code
            print(f"\n📄 Sample Generated Test Code:")
            test_code = result['raw_response']
            lines = test_code.split('\n')[:30]  # Show first 30 lines
            for line in lines:
                print(f"   {line}")
            print("   ... (see generated_tests.py for full code)")
            
            # Demonstrate how to customize tests
            print(f"\n🔧 Customizing Tests:")
            print("   1. Open generated_tests.py")
            print("   2. Replace placeholder assertions with actual logic")
            print("   3. Add your specific test cases")
            print("   4. Run with: pytest generated_tests.py")
            
            # Show example of customized test
            print(f"\n📝 Example Customized Test:")
            customized_test = '''
def test_calculate_fibonacci_custom():
    """Custom test for calculate_fibonacci function"""
    # Test basic cases
    assert calculate_fibonacci(0) == 0
    assert calculate_fibonacci(1) == 1
    assert calculate_fibonacci(5) == 5
    assert calculate_fibonacci(10) == 55
    
    # Test edge cases
    assert calculate_fibonacci(-1) == 0  # Assuming negative returns 0
    
    # Test performance (large number)
    # Note: This might be slow due to recursive implementation
    # assert calculate_fibonacci(20) == 6765
'''
            for line in customized_test.strip().split('\n'):
                print(f"   {line}")
            
        else:
            print(f"❌ Test generation failed: {result['error']}")
        
        print(f"\n🎯 Demo completed successfully!")
        print(f"💡 The mock test generator works without API calls!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure all dependencies are installed correctly.")


if __name__ == "__main__":
    run_test_demo()
