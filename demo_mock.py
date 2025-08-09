#!/usr/bin/env python3
"""
CodeForge AI Demo Script (Mock Version)
Demonstrates the capabilities without requiring API calls
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.analyzer import CodeAnalyzer
from src.agents.mock_test_generator import MockTestGeneratorAgent


def load_sample_code():
    """Load sample code for demonstration"""
    sample_code = '''
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_user_data(user_data):
    """Process user data with some issues for demonstration"""
    # Security issue: no input validation
    username = user_data.get('username')
    password = user_data.get('password')  # Should be hashed!
    
    # Performance issue: inefficient string concatenation
    result = ""
    for key, value in user_data.items():
        result += key + ":" + str(value) + ","
    
    # Complexity issue: deeply nested logic
    if user_data.get('age', 0) > 18:
        if user_data.get('verified', False):
            if user_data.get('status') == 'active':
                return {"status": "success", "data": result}
            else:
                return {"status": "error", "message": "inactive"}
        else:
            return {"status": "error", "message": "unverified"}
    else:
        return {"status": "error", "message": "underage"}

def fetch_data(url):
    """Fetch data from URL"""
    import requests
    # Security issue: no timeout
    response = requests.get(url)
    return response.json()

class DataManager:
    def __init__(self):
        self.data = []
    
    def add_item(self, item):
        self.data.append(item)
    
    def get_items(self):
        return self.data
    
    def process_items(self):
        # Performance issue: nested loops
        processed = []
        for item in self.data:
            for key, value in item.items():
                if key == 'value':
                    processed.append(value * 2)
        return processed
'''
    return sample_code


def run_mock_demo():
    """Run the CodeForge AI demo with mock components"""
    print("🚀 CodeForge AI Demo (Mock Version - No API Required)")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize components
        print("🔧 Initializing CodeForge AI components...")
        analyzer = CodeAnalyzer()
        test_agent = MockTestGeneratorAgent()  # No API key needed
        print("✅ Components initialized successfully!")
        
        # Load sample code
        print("\n📝 Loading sample code...")
        code = load_sample_code()
        print("✅ Sample code loaded")
        
        # Step 1: Static Analysis
        print("\n🔍 Step 1: Running Static Analysis...")
        analysis = analyzer.analyze_code(code)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return
        
        print("✅ Static analysis completed")
        
        # Display analysis results
        if 'metrics' in analysis:
            metrics = analysis['metrics']
            print(f"   📊 Lines of Code: {metrics.lines_of_code}")
            print(f"   📊 Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
            print(f"   📊 Security Score: {metrics.security_score:.1f}/100")
            print(f"   📊 Performance Score: {metrics.performance_score:.1f}/100")
        
        if 'issues' in analysis:
            print(f"   🔍 Issues Found: {len(analysis['issues'])}")
            for issue in analysis['issues'][:3]:  # Show first 3 issues
                print(f"      - {issue.severity.upper()}: {issue.message}")
        
        # Step 2: Mock Code Review
        print("\n📝 Step 2: Running Mock Code Review...")
        print("✅ Mock code review completed")
        print("   📋 Overall: Code analysis shows several areas for improvement")
        print("   🚨 Critical Issues: 3 (Security vulnerabilities detected)")
        print("   📝 Quality Issues: 5 (Performance and maintainability concerns)")
        
        # Step 3: Test Generation (Mock)
        print("\n🧪 Step 3: Generating Tests (Mock)...")
        tests = test_agent.generate_tests(code)
        
        if tests['success']:
            print("✅ Test generation completed")
            
            test_data = tests['tests']
            coverage = tests['coverage']
            
            print(f"   📊 Estimated Coverage: {coverage.get('coverage_percentage', 0)}%")
            print(f"   🧪 Total Tests Generated: {test_data.get('test_count', 0)}")
            print(f"   📊 Test Categories:")
            categories = test_data.get('categories', {})
            print(f"      - Unit Tests: {categories.get('unit_tests', 0)}")
            print(f"      - Integration Tests: {categories.get('integration_tests', 0)}")
            print(f"      - Edge Case Tests: {categories.get('edge_case_tests', 0)}")
            print(f"      - Error Tests: {categories.get('error_tests', 0)}")
            
            # Show test summary
            print(f"\n   📋 Test Summary:")
            print(f"      {tests['summary']}")
            
            # Show suggestions
            print(f"\n   💡 Suggestions:")
            for suggestion in tests['suggestions'][:3]:
                print(f"      - {suggestion}")
        else:
            print(f"❌ Test generation failed: {tests['error']}")
        
        # Step 4: Mock Refactoring
        print("\n🔧 Step 4: Analyzing Refactoring Opportunities (Mock)...")
        print("✅ Refactoring analysis completed")
        print("   📝 Suggested Changes: 4")
        print("   ✨ Improvements: 6")
        print("   🔧 Refactored code generated")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 Demo Summary (Mock Version)")
        print("=" * 60)
        print("✅ Static Analysis: Code quality metrics and issue detection")
        print("✅ Mock Code Review: Intelligent review with suggestions")
        print("✅ Test Generation: Comprehensive test suite creation (MOCK)")
        print("✅ Refactoring: Code improvement suggestions (MOCK)")
        print("\n🚀 CodeForge AI successfully demonstrated all capabilities!")
        print("💡 This version works without API calls - perfect for hackathons!")
        
        # Next steps
        print("\n📋 Next Steps:")
        print("1. Run 'python demo_mock.py' for this offline demo")
        print("2. Run 'streamlit run src/ui/web_interface.py' for web interface")
        print("3. Check the generated test code and customize it for your needs")
        print("4. Use the static analysis for code quality assessment")
        
        # Show sample test code
        if tests['success']:
            print(f"\n📄 Sample Generated Test Code:")
            test_code = tests['raw_response']
            lines = test_code.split('\n')[:20]  # Show first 20 lines
            for line in lines:
                print(f"   {line}")
            print("   ... (truncated)")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure all dependencies are installed correctly.")


if __name__ == "__main__":
    run_mock_demo()
