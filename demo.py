#!/usr/bin/env python3
"""
CodeForge AI Demo Script
Demonstrates the capabilities of the multi-modal code intelligence agent
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.analyzer import CodeAnalyzer
from src.agents.code_review_agent import CodeReviewAgent
from src.agents.test_generator_agent import TestGeneratorAgent
from src.agents.refactor_agent import RefactorAgent


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


def run_demo():
    """Run the CodeForge AI demo"""
    print("🚀 CodeForge AI Demo")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        print("   You can create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    try:
        # Initialize components
        print("🔧 Initializing CodeForge AI components...")
        analyzer = CodeAnalyzer()
        review_agent = CodeReviewAgent(api_key)
        test_agent = TestGeneratorAgent(api_key)
        refactor_agent = RefactorAgent(api_key)
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
        
        # Step 2: Code Review
        print("\n📝 Step 2: Running AI Code Review...")
        review = review_agent.review_code(code, analysis_results=analysis)
        
        if review['success']:
            print("✅ Code review completed")
            review_data = review['review']
            
            if review_data.get('overall_assessment'):
                print(f"   📋 Overall: {review_data['overall_assessment'][:100]}...")
            
            critical_count = len(review_data.get('critical_issues', []))
            quality_count = len(review_data.get('code_quality', []))
            print(f"   🚨 Critical Issues: {critical_count}")
            print(f"   📝 Quality Issues: {quality_count}")
        else:
            print(f"❌ Code review failed: {review['error']}")
        
        # Step 3: Test Generation
        print("\n🧪 Step 3: Generating Tests...")
        tests = test_agent.generate_tests(code)
        
        if tests['success']:
            print("✅ Test generation completed")
            
            if 'coverage_estimate' in tests:
                coverage = tests['coverage_estimate']
                print(f"   📊 Estimated Coverage: {coverage['estimated_coverage']:.1f}%")
                print(f"   📊 Test Functions: {coverage['test_functions']}")
            
            test_data = tests['tests']
            unit_count = len(test_data.get('unit_tests', '').split('def test_')) - 1
            print(f"   🧪 Unit Tests: {unit_count}")
        else:
            print(f"❌ Test generation failed: {tests['error']}")
        
        # Step 4: Refactoring
        print("\n🔧 Step 4: Analyzing Refactoring Opportunities...")
        refactor = refactor_agent.suggest_refactoring(code, analysis_results=analysis)
        
        if refactor['success']:
            print("✅ Refactoring analysis completed")
            
            changes_count = len(refactor.get('changes_summary', []))
            improvements_count = len(refactor.get('improvements', []))
            print(f"   📝 Suggested Changes: {changes_count}")
            print(f"   ✨ Improvements: {improvements_count}")
            
            if refactor.get('refactored_code'):
                print("   🔧 Refactored code generated")
        else:
            print(f"❌ Refactoring analysis failed: {refactor['error']}")
        
        # Summary
        print("\n" + "=" * 50)
        print("🎯 Demo Summary")
        print("=" * 50)
        print("✅ Static Analysis: Code quality metrics and issue detection")
        print("✅ AI Code Review: Intelligent review with suggestions")
        print("✅ Test Generation: Comprehensive test suite creation")
        print("✅ Refactoring: Code improvement suggestions")
        print("\n🚀 CodeForge AI successfully demonstrated all capabilities!")
        
        # Next steps
        print("\n📋 Next Steps:")
        print("1. Run 'python main.py examples/sample_code.py' for full analysis")
        print("2. Run 'streamlit run src/ui/web_interface.py' for web interface")
        print("3. Check the README.md for detailed usage instructions")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure you have set up your OpenAI API key correctly.")


if __name__ == "__main__":
    run_demo()
