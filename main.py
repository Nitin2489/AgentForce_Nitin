#!/usr/bin/env python3
"""
CodeForge AI - Multi-Modal Code Intelligence Agent
Main application entry point

Built for AgentForce Hackathon 2025
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.analyzer import CodeAnalyzer
from src.agents.code_review_agent import CodeReviewAgent
from src.agents.test_generator_agent import TestGeneratorAgent
from src.agents.refactor_agent import RefactorAgent


class CodeForgeAI:
    """Main CodeForge AI application"""
    
    def __init__(self, api_key: str = None):
        """Initialize the CodeForge AI system"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize components
        self.analyzer = CodeAnalyzer()
        self.review_agent = CodeReviewAgent(self.api_key)
        self.test_agent = TestGeneratorAgent(self.api_key)
        self.refactor_agent = RefactorAgent(self.api_key)
        
        print("🚀 CodeForge AI initialized successfully!")
    
    def analyze_code(self, code: str, file_path: str = None) -> dict:
        """Perform comprehensive code analysis"""
        print("🔍 Analyzing code...")
        
        # Static analysis
        analysis = self.analyzer.analyze_code(code, file_path)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return analysis
        
        print("✅ Static analysis completed")
        return analysis
    
    def review_code(self, code: str, file_path: str = None, analysis: dict = None) -> dict:
        """Perform AI-powered code review"""
        print("📝 Performing code review...")
        
        if not analysis:
            analysis = self.analyze_code(code, file_path)
        
        review = self.review_agent.review_code(code, file_path, analysis_results=analysis)
        
        if review['success']:
            print("✅ Code review completed")
        else:
            print(f"❌ Code review failed: {review['error']}")
        
        return review
    
    def generate_tests(self, code: str, file_path: str = None) -> dict:
        """Generate comprehensive test suite"""
        print("🧪 Generating tests...")
        
        tests = self.test_agent.generate_tests(code, file_path)
        
        if tests['success']:
            print("✅ Test generation completed")
        else:
            print(f"❌ Test generation failed: {tests['error']}")
        
        return tests
    
    def refactor_code(self, code: str, file_path: str = None, analysis: dict = None) -> dict:
        """Suggest and implement code refactoring"""
        print("🔧 Analyzing refactoring opportunities...")
        
        if not analysis:
            analysis = self.analyze_code(code, file_path)
        
        refactor = self.refactor_agent.suggest_refactoring(code, file_path, analysis_results=analysis)
        
        if refactor['success']:
            print("✅ Refactoring analysis completed")
        else:
            print(f"❌ Refactoring analysis failed: {refactor['error']}")
        
        return refactor
    
    def comprehensive_analysis(self, code: str, file_path: str = None) -> dict:
        """Perform comprehensive analysis with all agents"""
        print("🎯 Starting comprehensive analysis...")
        
        # Step 1: Static analysis
        analysis = self.analyze_code(code, file_path)
        if 'error' in analysis:
            return analysis
        
        # Step 2: Code review
        review = self.review_code(code, file_path, analysis)
        
        # Step 3: Test generation
        tests = self.generate_tests(code, file_path)
        
        # Step 4: Refactoring suggestions
        refactor = self.refactor_code(code, file_path, analysis)
        
        # Compile results
        results = {
            "static_analysis": analysis,
            "code_review": review,
            "test_generation": tests,
            "refactoring": refactor,
            "summary": self._generate_summary(analysis, review, tests, refactor)
        }
        
        print("✅ Comprehensive analysis completed!")
        return results
    
    def _generate_summary(self, analysis: dict, review: dict, tests: dict, refactor: dict) -> dict:
        """Generate a summary of all analysis results"""
        summary = {
            "overall_score": 0,
            "issues_found": 0,
            "recommendations": [],
            "test_coverage": 0,
            "security_score": 0,
            "performance_score": 0
        }
        
        # Calculate overall score
        if 'metrics' in analysis:
            metrics = analysis['metrics']
            summary['security_score'] = metrics.security_score
            summary['performance_score'] = metrics.performance_score
            
            # Calculate overall score based on various metrics
            scores = [
                metrics.security_score,
                metrics.performance_score,
                metrics.maintainability_index
            ]
            summary['overall_score'] = sum(scores) / len(scores)
        
        # Count issues
        if 'issues' in analysis:
            summary['issues_found'] = len(analysis['issues'])
        
        # Test coverage
        if tests.get('success') and 'coverage_estimate' in tests:
            summary['test_coverage'] = tests['coverage_estimate'].get('estimated_coverage', 0)
        
        # Collect recommendations
        if review.get('success') and 'review' in review:
            review_data = review['review']
            for section in ['critical_issues', 'code_quality', 'security', 'performance']:
                if section in review_data:
                    summary['recommendations'].extend(review_data[section][:3])
        
        return summary
    
    def print_results(self, results: dict):
        """Print formatted results"""
        print("\n" + "="*60)
        print("🎯 CODEFORGE AI ANALYSIS RESULTS")
        print("="*60)
        
        if 'summary' in results:
            summary = results['summary']
            print(f"\n📊 Overall Score: {summary['overall_score']:.1f}/100")
            print(f"🔍 Issues Found: {summary['issues_found']}")
            print(f"🧪 Test Coverage: {summary['test_coverage']:.1f}%")
            print(f"🔒 Security Score: {summary['security_score']:.1f}/100")
            print(f"⚡ Performance Score: {summary['performance_score']:.1f}/100")
        
        if 'code_review' in results and results['code_review'].get('success'):
            review = results['code_review']['review']
            print(f"\n📝 Code Review Summary:")
            print(f"   {self.review_agent.generate_review_summary(review)}")
        
        if 'test_generation' in results and results['test_generation'].get('success'):
            tests = results['test_generation']['tests']
            print(f"\n🧪 Test Generation Summary:")
            print(f"   {self.test_agent.generate_test_summary(tests)}")
        
        if 'refactoring' in results and results['refactoring'].get('success'):
            refactor = results['refactoring']
            print(f"\n🔧 Refactoring Summary:")
            print(f"   {self.refactor_agent.generate_refactor_summary(refactor)}")
        
        print("\n" + "="*60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="CodeForge AI - Multi-Modal Code Intelligence Agent")
    parser.add_argument("file", nargs="?", help="File to analyze")
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--mode", choices=["analyze", "review", "test", "refactor", "comprehensive"], 
                       default="comprehensive", help="Analysis mode")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize CodeForge AI
        codeforge = CodeForgeAI(args.api_key)
        
        # Get code to analyze
        if args.file:
            with open(args.file, 'r') as f:
                code = f.read()
            file_path = args.file
        else:
            # Interactive mode
            print("Enter your code (press Ctrl+D when done):")
            code = sys.stdin.read()
            file_path = "input.py"
        
        if not code.strip():
            print("❌ No code provided")
            return
        
        # Perform analysis based on mode
        if args.mode == "analyze":
            results = codeforge.analyze_code(code, file_path)
        elif args.mode == "review":
            results = codeforge.review_code(code, file_path)
        elif args.mode == "test":
            results = codeforge.generate_tests(code, file_path)
        elif args.mode == "refactor":
            results = codeforge.refactor_code(code, file_path)
        else:  # comprehensive
            results = codeforge.comprehensive_analysis(code, file_path)
        
        # Print results
        codeforge.print_results(results)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
