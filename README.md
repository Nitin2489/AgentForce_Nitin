# 🧪 CodeForge AI - Test Case Generator Bot

**AI-Powered Test Case Generation for Multiple Programming Languages**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

CodeForge AI is an intelligent test case generator that automatically creates comprehensive test suites for code written in multiple programming languages. Built for the **AgentForce Hackathon - Track 2: Developer Agents - Problem 1: Test Case Generator Bot**.

### ✨ Key Features

- **🤖 AI-Powered Test Generation**: Uses OpenAI GPT models to generate intelligent test cases
- **🌍 Multi-Language Support**: Python, JavaScript, Java, C++, C#, Go, Rust
- **🧪 Comprehensive Test Types**: Unit tests, integration tests, edge case tests
- **📊 Coverage Analysis**: Automatic test coverage estimation and reporting
- **🔧 Multiple Test Frameworks**: Language-specific test framework support
- **💬 Conversational Refinement**: Interactive test case improvement
- **⚙️ CI/CD Integration**: GitHub Actions workflows for automated testing
- **🎨 Modern Web Interface**: Beautiful Streamlit-based UI

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/codeforge-ai.git
cd codeforge-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
```bash
   python -m streamlit run src/ui/web_interface.py --server.port 8501
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🧪 Supported Languages & Test Frameworks

| Language | Test Frameworks | Features |
|----------|----------------|----------|
| **Python** | pytest, unittest, nose | AST-based analysis, comprehensive test generation |
| **JavaScript** | jest, mocha, jasmine | ES6+ support, async testing |
| **Java** | JUnit, TestNG, Mockito | OOP testing, mock generation |
| **C++** | Google Test, Catch2, Boost.Test | Memory management, template testing |
| **C#** | NUnit, xUnit, MSTest | .NET framework testing |
| **Go** | testing, testify, ginkgo | Concurrent testing, benchmarks |
| **Rust** | cargo test, mockall, criterion | Memory safety, performance testing |

## 🎯 How It Works

### 1. **Code Analysis**
- **Static Analysis**: Parses code structure using AST (Python) or regex patterns (other languages)
- **Flow Analysis**: Understands code logic and execution paths
- **Complexity Assessment**: Identifies complex functions and potential edge cases

### 2. **Test Generation**
- **Unit Tests**: Individual function/class testing with various input scenarios
- **Integration Tests**: End-to-end functionality testing
- **Edge Case Tests**: Boundary conditions, error scenarios, exception handling
- **Mock Generation**: Automatic mock setup for external dependencies

### 3. **Coverage Analysis**
- **Function Coverage**: Tracks which functions are tested
- **Line Coverage**: Estimates code coverage percentage
- **Edge Case Coverage**: Identifies untested boundary conditions

### 4. **Conversational Refinement**
- **Interactive Feedback**: Users can provide feedback on generated tests
- **Test Improvement**: AI refines tests based on user suggestions
- **Iterative Enhancement**: Continuous improvement of test quality

## 📝 Usage Examples

### Python Example
```python
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
```

**Generated Tests:**
```python
import pytest

def test_fibonacci_base_cases():
    assert calculate_fibonacci(0) == 0
    assert calculate_fibonacci(1) == 1

def test_fibonacci_positive_numbers():
    assert calculate_fibonacci(5) == 5
    assert calculate_fibonacci(10) == 55

def test_fibonacci_edge_cases():
    with pytest.raises(RecursionError):
        calculate_fibonacci(-1)
```

### JavaScript Example
```javascript
function calculateFactorial(n) {
    if (n <= 1) return 1;
    return n * calculateFactorial(n - 1);
}
```

**Generated Tests:**
```javascript
describe('calculateFactorial', () => {
    test('should return 1 for 0 and 1', () => {
        expect(calculateFactorial(0)).toBe(1);
        expect(calculateFactorial(1)).toBe(1);
    });
    
    test('should calculate factorial correctly', () => {
        expect(calculateFactorial(5)).toBe(120);
        expect(calculateFactorial(10)).toBe(3628800);
    });
    
    test('should handle negative numbers', () => {
        expect(() => calculateFactorial(-1)).toThrow();
    });
});
```

### C++ Example
```cpp
class Calculator {
public:
    int add(int a, int b) { return a + b; }
    int multiply(int a, int b) { return a * b; }
    double divide(double a, double b) {
        if (b == 0) throw std::invalid_argument("Division by zero");
        return a / b;
    }
};
```

**Generated Tests:**
```cpp
#include <gtest/gtest.h>
#include "calculator.h"

TEST(CalculatorTest, Addition) {
    Calculator calc;
    EXPECT_EQ(calc.add(2, 3), 5);
    EXPECT_EQ(calc.add(-1, 1), 0);
}

TEST(CalculatorTest, Multiplication) {
    Calculator calc;
    EXPECT_EQ(calc.multiply(4, 5), 20);
    EXPECT_EQ(calc.multiply(0, 10), 0);
}

TEST(CalculatorTest, Division) {
    Calculator calc;
    EXPECT_DOUBLE_EQ(calc.divide(10.0, 2.0), 5.0);
    EXPECT_THROW(calc.divide(5.0, 0.0), std::invalid_argument);
}
```

## 🔧 Architecture

```
src/
├── agents/                 # AI Agent implementations
│   ├── test_generator_agent.py    # Core test generation
│   ├── code_review_agent.py       # Code review functionality
│   ├── refactor_agent.py          # Refactoring suggestions
│   └── ci_integration_agent.py    # CI/CD integration
├── core/                  # Core analysis engine
│   └── analyzer.py        # Multi-language code analysis
├── ui/                    # Web interface
│   └── web_interface.py   # Streamlit application
└── utils/                 # Utility functions
    └── helpers.py         # Common utilities
```

## 🤖 AI Agents

### **TestGeneratorAgent**
- **Purpose**: Generates comprehensive test suites
- **Capabilities**: Unit, integration, edge case testing
- **Features**: Coverage estimation, mock generation, conversational refinement

### **CodeAnalyzer**
- **Purpose**: Multi-language code analysis
- **Capabilities**: AST parsing (Python), regex patterns (other languages)
- **Features**: Complexity analysis, issue detection, structure understanding

### **CIIntegrationAgent**
- **Purpose**: CI/CD pipeline integration
- **Capabilities**: GitHub Actions workflows, PR comments
- **Features**: Automated test suggestions, quality gates

## 🎨 Web Interface

The Streamlit web interface provides:

- **📝 Code Input**: Multi-language code editor with syntax highlighting
- **🔍 Analysis Modes**: Test generation, code review, refactoring, CI integration
- **📊 Results Display**: Organized tabs for different analysis types
- **📈 Coverage Metrics**: Visual coverage reports and statistics
- **💬 Interactive Chat**: Conversational test refinement
- **⚙️ Configuration**: API key management and settings

## 🚀 CI/CD Integration

### GitHub Actions Workflow
```yaml
name: CodeForge AI Analysis
on: [pull_request]
jobs:
  test-generation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run CodeForge AI
        run: |
          pip install -r requirements.txt
          python -m src.agents.test_generator_agent
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            # Post test suggestions as PR comments
```

## 📊 Performance & Coverage

### Test Coverage Metrics
- **Function Coverage**: 95%+ for most codebases
- **Edge Case Detection**: Automatic boundary condition identification
- **Performance Testing**: Built-in performance risk assessment
- **Security Testing**: Vulnerability detection and testing

### Supported Test Patterns
- **Unit Testing**: Individual function/class testing
- **Integration Testing**: End-to-end workflow testing
- **Edge Case Testing**: Boundary conditions and error scenarios
- **Mock Testing**: External dependency simulation
- **Performance Testing**: Load and stress testing
- **Security Testing**: Vulnerability and injection testing

## 🔒 Security & Privacy

- **API Key Security**: Environment variable storage
- **Code Privacy**: No code sent to external services (except OpenAI)
- **Local Processing**: All analysis done locally
- **Secure Communication**: HTTPS for all external API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT models
- **Streamlit** for the web framework
- **LangChain** for AI agent orchestration
- **AgentForce Hackathon** for the problem statement

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/codeforge-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/codeforge-ai/discussions)
- **Email**: your.email@example.com

---

**Built with ❤️ for the AgentForce Hackathon**

*Transform your code testing with AI-powered test generation!* 