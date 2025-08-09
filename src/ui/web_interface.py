"""
Web Interface for CodeForge AI - Test Case Generator
Modern Streamlit-based web application
"""

import streamlit as st
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.analyzer import CodeAnalyzer
from src.agents.code_review_agent import CodeReviewAgent
from src.agents.test_generator_agent import TestGeneratorAgent
from src.agents.refactor_agent import RefactorAgent
from src.agents.ci_integration_agent import CIIntegrationAgent


def init_session_state():
    """Initialize session state variables"""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'current_code' not in st.session_state:
        st.session_state.current_code = ""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""


def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Load API key from environment
        env_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # API Key input - read-only if loaded from environment
        if env_api_key and env_api_key != "your_openai_api_key_here":
            st.success("✅ API Key loaded from environment")
            api_key = env_api_key
            st.session_state.api_key = api_key
        else:
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=st.session_state.api_key,
                help="Enter your OpenAI API key or set OPENAI_API_KEY in .env file"
            )
            st.session_state.api_key = api_key
        
        # Add manual API key override option
        if st.checkbox("🔑 Use different API key"):
            api_key = st.text_input(
                "Alternative OpenAI API Key",
                type="password",
                help="Enter a different OpenAI API key if current one has quota issues"
            )
        
        # Demo mode for testing without API
        if st.checkbox("🎭 Demo Mode (No API Required)"):
            st.info("Demo mode will show sample test cases without using OpenAI API")
            api_key = "demo_mode"
        
        # Security note
        if env_api_key and env_api_key != "your_openai_api_key_here":
            st.info("🔒 API Key is loaded from environment variables (secure)")
        else:
            st.warning("⚠️ For security, consider setting OPENAI_API_KEY in .env file")
        
        return api_key


def display_test_results(test_results, analysis_results):
    """Display test generation results"""
    st.success("✅ Test cases generated successfully!")
    
    # Coverage information
    coverage = test_results.get("coverage_estimate", {})
    if coverage:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Estimated Coverage", f"{coverage.get('estimated_coverage', 0):.1f}%")
        with col2:
            st.metric("Total Functions", coverage.get('total_functions', 0))
        with col3:
            st.metric("Test Functions", coverage.get('test_functions', 0))
        with col4:
            st.metric("Coverage Level", coverage.get('coverage_level', 'unknown').title())
    
    # Test tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧪 Unit Tests", "🔗 Integration Tests", "⚠️ Edge Cases", "🔧 Fixtures", "📋 Raw Response"])
    
    with tab1:
        if test_results["tests"]["unit_tests"]:
            st.code(test_results["tests"]["unit_tests"], language="python")
        else:
            st.info("No unit tests generated")
    
    with tab2:
        if test_results["tests"]["integration_tests"]:
            st.code(test_results["tests"]["integration_tests"], language="python")
        else:
            st.info("No integration tests generated")
    
    with tab3:
        if test_results["tests"]["edge_case_tests"]:
            st.code(test_results["tests"]["edge_case_tests"], language="python")
        else:
            st.info("No edge case tests generated")
    
    with tab4:
        if test_results["tests"]["fixtures"]:
            st.code(test_results["tests"]["fixtures"], language="python")
        else:
            st.info("No fixtures generated")
    
    with tab5:
        st.text(test_results.get("raw_response", "No raw response available"))


def display_review_results(review_results, analysis_results):
    """Display code review results"""
    st.success("✅ Code review completed!")
    
    review = review_results.get("review", {})
    
    # Review summary
    if review.get("overall_assessment"):
        st.subheader("📋 Overall Assessment")
        st.write(review["overall_assessment"])
    
    # Review sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚨 Critical Issues", "📊 Code Quality", "🔒 Security", "⚡ Performance", "💡 Suggestions"])
    
    with tab1:
        issues = review.get("critical_issues", [])
        if issues:
            for issue in issues:
                st.error(f"• {issue}")
        else:
            st.success("No critical issues found!")
    
    with tab2:
        quality = review.get("code_quality", [])
        if quality:
            for item in quality:
                st.warning(f"• {item}")
        else:
            st.success("No code quality issues found!")
    
    with tab3:
        security = review.get("security", [])
        if security:
            for item in security:
                st.error(f"• {item}")
        else:
            st.success("No security issues found!")
    
    with tab4:
        performance = review.get("performance", [])
        if performance:
            for item in performance:
                st.info(f"• {item}")
        else:
            st.success("No performance issues found!")
    
    with tab5:
        suggestions = review.get("refactoring_opportunities", [])
        if suggestions:
            for suggestion in suggestions:
                st.info(f"• {suggestion}")
        else:
            st.info("No refactoring suggestions")


def display_refactor_results(refactor_results, analysis_results):
    """Display refactoring results"""
    st.success("✅ Refactoring analysis completed!")
    
    # Refactored code
    if refactor_results.get("refactored_code"):
        st.subheader("🔄 Refactored Code")
        st.code(refactor_results["refactored_code"], language="python")
    
    # Changes summary
    changes = refactor_results.get("changes_summary", [])
    if changes:
        st.subheader("📝 Changes Made")
        for change in changes:
            st.info(f"• {change}")
    
    # Improvements
    improvements = refactor_results.get("improvements", [])
    if improvements:
        st.subheader("✨ Improvements")
        for improvement in improvements:
            st.success(f"• {improvement}")


def display_ci_results(ci_results):
    """Display CI integration results"""
    st.success("✅ CI workflow generated!")
    
    # Workflow YAML
    if ci_results.get("workflow_yaml"):
        st.subheader("⚙️ GitHub Actions Workflow")
        st.code(ci_results["workflow_yaml"], language="yaml")
    
    # Setup instructions
    instructions = ci_results.get("setup_instructions", [])
    if instructions:
        st.subheader("📋 Setup Instructions")
        for instruction in instructions:
            st.info(f"• {instruction}")


def display_quick_stats(analysis_results):
    """Display quick statistics"""
    if not analysis_results:
        st.info("No analysis data available")
        return
    
    metrics = analysis_results.get("metrics")
    if metrics:
        # Handle CodeMetrics object (has attributes, not dict methods)
        if hasattr(metrics, 'lines_of_code'):
            st.metric("Lines of Code", metrics.lines_of_code)
        if hasattr(metrics, 'cyclomatic_complexity'):
            st.metric("Complexity", metrics.cyclomatic_complexity)
        if hasattr(metrics, 'maintainability_index'):
            st.metric("Maintainability", f"{metrics.maintainability_index:.1f}")
    
    issues = analysis_results.get("issues", [])
    if issues:
        st.metric("Issues Found", len(issues))
    
    security = analysis_results.get("security", {})
    if security and isinstance(security, dict):
        st.metric("Security Score", f"{security.get('score', 0):.1f}")


def main():
    st.set_page_config(
        page_title="CodeForge AI - Test Case Generator",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧪 CodeForge AI - Test Case Generator")
    st.markdown("**AI-Powered Test Case Generation for Multiple Programming Languages**")
    
    # Initialize session state
    init_session_state()
    
    # Sidebar configuration
    api_key = render_sidebar()
    
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        return
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Code Input")
        
        # Language selection
        language = st.selectbox(
            "Programming Language",
            ["python", "javascript", "java", "cpp", "csharp", "go", "rust"],
            help="Select the programming language of your code"
        )
        
        # Test framework selection (language-specific)
        test_frameworks = {
            "python": ["pytest", "unittest", "nose"],
            "javascript": ["jest", "mocha", "jasmine"],
            "java": ["junit", "testng", "mockito"],
            "cpp": ["gtest", "catch2", "boost.test"],
            "csharp": ["nunit", "xunit", "mstest"],
            "go": ["testing", "testify", "ginkgo"],
            "rust": ["cargo test", "mockall", "criterion"]
        }
        
        available_frameworks = test_frameworks.get(language, ["pytest"])
        test_framework = st.selectbox(
            "Test Framework",
            available_frameworks,
            help="Select the test framework for test generation"
        )
        
        # Code input with language-specific examples
        language_examples = {
            "python": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
            "javascript": "function calculateFactorial(n) {\n    if (n <= 1) return 1;\n    return n * calculateFactorial(n - 1);\n}",
            "java": "public class Calculator {\n    public int add(int a, int b) {\n        return a + b;\n    }\n}",
            "cpp": "class Calculator {\npublic:\n    int add(int a, int b) { return a + b; }\n    int multiply(int a, int b) { return a * b; }\n};",
            "csharp": "public class Calculator\n{\n    public int Add(int a, int b) => a + b;\n    public int Multiply(int a, int b) => a * b;\n}",
            "go": "func Add(a, b int) int {\n    return a + b\n}\n\nfunc Multiply(a, b int) int {\n    return a * b\n}",
            "rust": "fn add(a: i32, b: i32) -> i32 {\n    a + b\n}\n\nfn multiply(a: i32, b: i32) -> i32 {\n    a * b\n}"
        }
        
        example_code = language_examples.get(language, language_examples["python"])
        
        code = st.text_area(
            "Enter your code here:",
            height=300,
            placeholder=f"Paste your {language.upper()} code here...\n\nExample:\n{example_code}"
        )
        
        # Analysis mode selection
        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["Test Generation", "Code Review", "Refactoring", "CI Integration"],
            help="Select what type of analysis you want to perform"
        )
        
        if st.button("🚀 Generate Analysis", type="primary"):
            if not code.strip():
                st.error("Please enter some code to analyze.")
                return
            
            with st.spinner("Analyzing code and generating results..."):
                try:
                    # Initialize agents
                    analyzer = CodeAnalyzer()
                    test_agent = TestGeneratorAgent(api_key)
                    review_agent = CodeReviewAgent(api_key)
                    refactor_agent = RefactorAgent(api_key)
                    ci_agent = CIIntegrationAgent(api_key)
                    
                    # Perform code analysis
                    analysis_results = analyzer.analyze_code(code, language=language)
                    
                    # Store analysis results in session state for display
                    st.session_state.analysis_results = analysis_results
                    
                    if analysis_mode == "Test Generation":
                        # Check for demo mode
                        if api_key == "demo_mode":
                            # Generate demo test results
                            demo_tests = {
                                "success": True,
                                "tests": {
                                    "unit_tests": f"""# Demo Unit Tests for {language.upper()}
import {test_framework}

def test_basic_functionality():
    \"\"\"Test basic functionality\"\"\"
    # This is a demo test case
    assert True

def test_edge_cases():
    \"\"\"Test edge cases\"\"\"
    # Demo edge case testing
    assert True

def test_error_handling():
    \"\"\"Test error handling\"\"\"
    # Demo error handling tests
    assert True""",
                                    "integration_tests": f"""# Demo Integration Tests for {language.upper()}
import {test_framework}

def test_integration():
    \"\"\"Test integration scenarios\"\"\"
    # Demo integration test
    assert True""",
                                    "edge_case_tests": f"""# Demo Edge Case Tests for {language.upper()}
import {test_framework}

def test_edge_cases():
    \"\"\"Test edge cases\"\"\"
    # Demo edge case tests
    assert True""",
                                    "fixtures": f"""# Demo Test Fixtures for {language.upper()}
import {test_framework}

@pytest.fixture
def sample_data():
    \"\"\"Sample test data\"\"\"
    return {{"test": "data"}}"""
                                },
                                "coverage_estimate": {
                                    "estimated_coverage": 85.0,
                                    "total_functions": 3,
                                    "test_functions": 3,
                                    "coverage_level": "good"
                                }
                            }
                            display_test_results(demo_tests, analysis_results)
                        else:
                            # Generate tests with real API
                            test_results = test_agent.generate_tests(
                                code, language=language, test_framework=test_framework
                            )
                        
                        if test_results["success"]:
                            display_test_results(test_results, analysis_results)
                        else:
                            error_msg = test_results['error']
                            if "quota" in error_msg.lower() or "429" in error_msg:
                                st.error("❌ OpenAI API Quota Exceeded!")
                                st.warning("""
                                **Solutions:**
                                1. **Check your OpenAI billing** at https://platform.openai.com/account/billing
                                2. **Add payment method** or upgrade your plan
                                3. **Use a different API key** (check the sidebar option)
                                4. **Wait for quota reset** (usually monthly)
                                """)
                            else:
                                st.error(f"Test generation failed: {error_msg}")
                    
                    elif analysis_mode == "Code Review":
                        # Perform code review
                        review_results = review_agent.review_code(
                            code, language=language, analysis_results=analysis_results
                        )
                        
                        if review_results["success"]:
                            display_review_results(review_results, analysis_results)
                        else:
                            st.error(f"Code review failed: {review_results['error']}")
                    
                    elif analysis_mode == "Refactoring":
                        # Suggest refactoring
                        refactor_results = refactor_agent.suggest_refactoring(
                            code, language=language, analysis_results=analysis_results
                        )
                        
                        if refactor_results["success"]:
                            display_refactor_results(refactor_results, analysis_results)
                        else:
                            st.error(f"Refactoring analysis failed: {refactor_results['error']}")
                    
                    elif analysis_mode == "CI Integration":
                        # Generate CI workflow
                        ci_results = ci_agent.generate_github_actions_workflow(
                            project_type=language, features=["test_generation", "code_review"]
                        )
                        
                        if ci_results["success"]:
                            display_ci_results(ci_results)
                        else:
                            st.error(f"CI integration failed: {ci_results['error']}")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.exception(e)
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        # Display analysis results if available
        if hasattr(st.session_state, 'analysis_results') and st.session_state.analysis_results:
            display_quick_stats(st.session_state.analysis_results)
        else:
            st.info("Run analysis to see statistics")
        
        st.subheader("💡 Tips")
        st.markdown("""
        **For Best Results:**
        - Include complete functions/classes
        - Add comments for complex logic
        - Specify input/output expectations
        - Include error handling scenarios
        
        **Supported Languages:**
        - Python, JavaScript, Java
        - C++, C#, Go, Rust
        
        **Test Frameworks:**
        - pytest, unittest, nose (Python)
        - jest, mocha, jasmine (JavaScript)
        - junit, testng, mockito (Java)
        - gtest, catch2, boost.test (C++)
        """)


if __name__ == "__main__":
    main()
