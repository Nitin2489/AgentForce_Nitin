"""
Test Generator Agent for CodeForge AI
Generates comprehensive test suites using AI
"""

import os
import ast
import re
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# LLMChain is no longer used, using RunnableSequence instead
import json


class TestGeneratorAgent:
    """AI-powered test generator agent"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Get model from environment or default to gpt-3.5-turbo
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=self.api_key
        )
        
        self.system_prompt = """You are an expert software testing engineer with deep knowledge of unit testing, integration testing, and test-driven development. Your role is to:

1. Analyze code and generate comprehensive test suites
2. Create unit tests that cover all code paths and edge cases
3. Generate integration tests for complex interactions
4. Identify boundary conditions and error scenarios
5. Ensure high test coverage and quality
6. Follow testing best practices and patterns
7. Create readable and maintainable test code

Generate tests that are:
- Comprehensive and thorough
- Well-documented with clear test names
- Include edge cases and error conditions
- Follow the testing framework conventions
- Easy to understand and maintain"""

        self.test_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """
Please generate comprehensive tests for the following code:

**Code to Test:**
{code}

**Context:**
- File: {file_path}
- Language: {language}
- Test Framework: {test_framework}
- Functions/Classes: {functions_classes}

**Requirements:**
1. Generate unit tests for each function/class
2. Include edge cases and boundary conditions
3. Test error scenarios and exceptions
4. Ensure good test coverage
5. Use descriptive test names
6. Include setup and teardown if needed
7. Mock external dependencies appropriately

Please provide:
1. **Unit Tests** - Individual function/class tests
2. **Integration Tests** - End-to-end functionality tests
3. **Edge Case Tests** - Boundary conditions and error scenarios
4. **Test Setup** - Any necessary fixtures or mocks

Format the response as complete, runnable test code with clear documentation.
""")
        ])
        
        # Use the new RunnableSequence pattern instead of deprecated LLMChain
        self.chain = self.test_prompt | self.llm
    
    def generate_tests(self, code: str, file_path: str = None, language: str = "python",
                      test_framework: str = "pytest") -> Dict[str, Any]:
        """Generate comprehensive test suite"""
        try:
            # Analyze code structure
            functions_classes = self._analyze_code_structure(code, language)
            
            # Generate tests using the new invoke method
            response = self.chain.invoke({
                "code": code,
                "file_path": file_path or "unknown",
                "language": language,
                "test_framework": test_framework,
                "functions_classes": functions_classes
            })
            
            # Parse and structure the response
            structured_tests = self._parse_test_response(response, test_framework, language)
            
            return {
                "success": True,
                "tests": structured_tests,
                "raw_response": response,
                "coverage_estimate": self._estimate_test_coverage(code, structured_tests, language)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tests": None
            }
    
    def _analyze_code_structure(self, code: str, language: str = "python") -> str:
        """Analyze code to identify functions and classes with multi-language support"""
        try:
            if language == "python":
                return self._analyze_python_structure(code)
            else:
                return self._analyze_generic_structure(code, language)
        except Exception as e:
            return f"Code analysis error: {str(e)}"
    
    def _analyze_python_structure(self, code: str) -> str:
        """Analyze Python code structure using AST"""
        try:
            tree = ast.parse(code)
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'args': len(node.args.args),
                        'line': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        'name': node.name,
                        'methods': len(methods),
                        'line': node.lineno
                    })
            
            # Format for prompt
            structure = []
            if functions:
                func_list = [f"{f['name']}({f['args']} args)" for f in functions]
                structure.append(f"Functions: {', '.join(func_list)}")
            
            if classes:
                class_list = [f"{c['name']}({c['methods']} methods)" for c in classes]
                structure.append(f"Classes: {', '.join(class_list)}")
            
            return "\n".join(structure) if structure else "No functions or classes found"
            
        except SyntaxError:
            return "Code has syntax errors"
    
    def _analyze_generic_structure(self, code: str, language: str) -> str:
        """Analyze non-Python code structure using regex patterns"""
        # Language-specific patterns
        patterns = {
            'javascript': {
                'function_def': r'function\s+(\w+)\s*\([^)]*\)',
                'class_def': r'class\s+(\w+)',
                'method_def': r'(\w+)\s*\([^)]*\)\s*{',
            },
            'java': {
                'function_def': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(?:abstract\s+)?(?:strictfp\s+)?(?:<[^>]+>\s+)?(?:[\w\[\]]+\s+)+(\w+)\s*\([^)]*\)',
                'class_def': r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)',
                'method_def': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(?:abstract\s+)?(?:strictfp\s+)?(?:<[^>]+>\s+)?(?:[\w\[\]]+\s+)+(\w+)\s*\([^)]*\)',
            }
        }
        
        lang_patterns = patterns.get(language, patterns['javascript'])
        functions = []
        classes = []
        
        # Find functions
        func_matches = re.finditer(lang_patterns['function_def'], code, re.MULTILINE)
        for match in func_matches:
            functions.append({
                'name': match.group(1),
                'args': len(re.findall(r'[^,]+', match.group(0).split('(')[1].split(')')[0])) if '(' in match.group(0) else 0,
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Find classes
        class_matches = re.finditer(lang_patterns['class_def'], code, re.MULTILINE)
        for match in class_matches:
            classes.append({
                'name': match.group(1),
                'methods': len([f for f in functions if f['line'] > match.start()]),
                'line': code[:match.start()].count('\n') + 1
            })
        
        # Format for prompt
        structure = []
        if functions:
            func_list = [f"{f['name']}({f['args']} args)" for f in functions]
            structure.append(f"Functions: {', '.join(func_list)}")
        
        if classes:
            class_list = [f"{c['name']}({c['methods']} methods)" for c in classes]
            structure.append(f"Classes: {', '.join(class_list)}")
        
        return "\n".join(structure) if structure else "No functions or classes found"
    
    def _parse_test_response(self, response: str, framework: str, language: str = "python") -> Dict[str, Any]:
        """Parse the AI response into structured test format with multi-language support"""
        tests = {
            "unit_tests": "",
            "integration_tests": "",
            "edge_case_tests": "",
            "test_setup": "",
            "imports": "",
            "fixtures": ""
        }
        
        # Language-specific patterns
        patterns = {
            "python": {
                "import_pattern": r'import\s+.*|from\s+.*\s+import\s+.*',
                "test_pattern": r'def\s+test_.*?:.*?(?=def\s+test_|def\s+def_|$)',
                "fixture_pattern": r'@pytest\.fixture.*?def\s+.*?:.*?(?=def\s+test_|def\s+def_|$)',
            },
            "javascript": {
                "import_pattern": r'import\s+.*|require\s*\([^)]+\)|const\s+.*=.*require\s*\([^)]+\)',
                "test_pattern": r'(?:function\s+)?(?:test|it|describe)\s*\([^)]*\).*?{.*?}(?=\s*(?:test|it|describe)\s*\(|$)',
                "fixture_pattern": r'(?:beforeEach|afterEach|beforeAll|afterAll)\s*\([^)]*\).*?{.*?}',
            },
            "java": {
                "import_pattern": r'import\s+.*;',
                "test_pattern": r'@Test.*?public\s+void\s+.*?{.*?}(?=\s*@Test|$)',
                "fixture_pattern": r'(?:@Before|@After|@BeforeClass|@AfterClass).*?public\s+void\s+.*?{.*?}',
            }
        }
        
        lang_patterns = patterns.get(language, patterns["python"])
        
        # Extract imports
        import_pattern = lang_patterns["import_pattern"]
        imports = re.findall(import_pattern, response, re.MULTILINE)
        tests["imports"] = "\n".join(imports)
        
        # Extract test functions
        test_pattern = lang_patterns["test_pattern"]
        test_functions = re.findall(test_pattern, response, re.DOTALL)
        
        # Categorize tests
        for test in test_functions:
            if any(keyword in test.lower() for keyword in ['edge', 'boundary', 'error', 'exception']):
                tests["edge_case_tests"] += test + "\n\n"
            elif any(keyword in test.lower() for keyword in ['integration', 'end_to_end', 'e2e']):
                tests["integration_tests"] += test + "\n\n"
            else:
                tests["unit_tests"] += test + "\n\n"
        
        # Extract fixtures
        fixture_pattern = lang_patterns["fixture_pattern"]
        fixtures = re.findall(fixture_pattern, response, re.DOTALL)
        tests["fixtures"] = "\n\n".join(fixtures)
        
        return tests
    
    def _estimate_test_coverage(self, code: str, tests: Dict, language: str = "python") -> Dict[str, Any]:
        """Estimate test coverage based on generated tests with multi-language support"""
        try:
            if language == "python":
                return self._estimate_python_coverage(code, tests)
            else:
                return self._estimate_generic_coverage(code, tests, language)
        except Exception:
            return {
                "estimated_coverage": 0,
                "total_functions": 0,
                "total_classes": 0,
                "test_functions": 0,
                "coverage_level": "unknown"
            }
    
    def _estimate_python_coverage(self, code: str, tests: Dict) -> Dict[str, Any]:
        """Estimate test coverage for Python code"""
        try:
            tree = ast.parse(code)
            total_functions = 0
            total_classes = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_functions += 1
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
            
            # Count test functions
            test_functions = len(re.findall(r'def\s+test_', tests.get("unit_tests", "") + 
                                          tests.get("integration_tests", "") + 
                                          tests.get("edge_case_tests", "")))
            
            # Estimate coverage
            estimated_coverage = min(95, (test_functions / max(1, total_functions)) * 100)
            
            return {
                "estimated_coverage": estimated_coverage,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "test_functions": test_functions,
                "coverage_level": "high" if estimated_coverage > 80 else "medium" if estimated_coverage > 60 else "low"
            }
        except Exception:
            return {
                "estimated_coverage": 0,
                "total_functions": 0,
                "total_classes": 0,
                "test_functions": 0,
                "coverage_level": "unknown"
            }
    
    def _estimate_generic_coverage(self, code: str, tests: Dict, language: str) -> Dict[str, Any]:
        """Estimate test coverage for non-Python code"""
        # Language-specific patterns
        patterns = {
            'javascript': {
                'function_def': r'function\s+(\w+)\s*\([^)]*\)',
                'class_def': r'class\s+(\w+)',
            },
            'java': {
                'function_def': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(?:abstract\s+)?(?:strictfp\s+)?(?:<[^>]+>\s+)?(?:[\w\[\]]+\s+)+(\w+)\s*\([^)]*\)',
                'class_def': r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)',
            }
        }
        
        lang_patterns = patterns.get(language, patterns['javascript'])
        
        # Count functions and classes
        total_functions = len(re.findall(lang_patterns['function_def'], code, re.MULTILINE))
        total_classes = len(re.findall(lang_patterns['class_def'], code, re.MULTILINE))
        
        # Count test functions (language-specific patterns)
        test_patterns = {
            'javascript': r'function\s+test_|it\s*\(|describe\s*\(',
            'java': r'@Test|public\s+void\s+test_',
        }
        
        test_pattern = test_patterns.get(language, r'def\s+test_')
        test_functions = len(re.findall(test_pattern, tests.get("unit_tests", "") + 
                                      tests.get("integration_tests", "") + 
                                      tests.get("edge_case_tests", ""), re.IGNORECASE))
        
        # Estimate coverage
        estimated_coverage = min(95, (test_functions / max(1, total_functions)) * 100)
        
        return {
            "estimated_coverage": estimated_coverage,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "test_functions": test_functions,
            "coverage_level": "high" if estimated_coverage > 80 else "medium" if estimated_coverage > 60 else "low"
        }
    
    def generate_test_summary(self, tests: Dict) -> str:
        """Generate a summary of the generated tests"""
        summary_parts = []
        
        # Count different types of tests
        unit_count = len(re.findall(r'def\s+test_', tests.get("unit_tests", "")))
        integration_count = len(re.findall(r'def\s+test_', tests.get("integration_tests", "")))
        edge_count = len(re.findall(r'def\s+test_', tests.get("edge_case_tests", "")))
        fixture_count = len(re.findall(r'@pytest\.fixture', tests.get("fixtures", "")))
        
        if unit_count > 0:
            summary_parts.append(f"Unit Tests: {unit_count}")
        if integration_count > 0:
            summary_parts.append(f"Integration Tests: {integration_count}")
        if edge_count > 0:
            summary_parts.append(f"Edge Case Tests: {edge_count}")
        if fixture_count > 0:
            summary_parts.append(f"Fixtures: {fixture_count}")
        
        return " | ".join(summary_parts) if summary_parts else "No tests generated"
    
    def suggest_test_improvements(self, code: str, tests: Dict) -> List[str]:
        """Suggest improvements for existing tests"""
        try:
            prompt = f"""
            Analyze the following code and existing tests, then suggest improvements:
            
            **Code:**
            {code}
            
            **Current Tests:**
            {json.dumps(tests, indent=2)}
            
            Provide specific, actionable suggestions for improving test coverage, quality, and maintainability.
            """
            
            response = self.llm.predict(prompt)
            return [s.strip() for s in response.split('\n') if s.strip()]
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"]

    def refine_tests_conversationally(self, code: str, tests: Dict, user_feedback: str) -> Dict[str, Any]:
        """Refine tests based on conversational user feedback"""
        try:
            refinement_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert test engineer helping to refine test cases based on user feedback. 
                Your goal is to improve the existing tests by addressing the user's concerns and suggestions.
                
                Always maintain test quality and coverage while incorporating user feedback."""),
                ("human", """
                **Original Code:**
                {code}
                
                **Current Tests:**
                {current_tests}
                
                **User Feedback:**
                {user_feedback}
                
                Please refine the tests based on the user's feedback. Provide:
                1. **Refined Tests** - Updated test code addressing the feedback
                2. **Changes Made** - Summary of what was changed and why
                3. **Additional Suggestions** - Any other improvements you noticed
                
                Format the response as complete, runnable test code with clear documentation.
                """)
            ])
            
            chain = refinement_prompt | self.llm
            
            response = chain.invoke({
                "code": code,
                "current_tests": json.dumps(tests, indent=2),
                "user_feedback": user_feedback
            })
            
            # Parse the refined tests
            refined_tests = self._parse_test_response(response, "pytest")
            
            return {
                "success": True,
                "refined_tests": refined_tests,
                "original_tests": tests,
                "feedback_addressed": user_feedback,
                "changes_summary": self._extract_changes_summary(response)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to refine tests: {str(e)}"
            }

    def _extract_changes_summary(self, response: str) -> List[str]:
        """Extract a summary of changes made during refinement"""
        try:
            # Look for sections that describe changes
            lines = response.split('\n')
            changes = []
            in_changes_section = False
            
            for line in lines:
                if 'changes' in line.lower() or 'improvements' in line.lower():
                    in_changes_section = True
                    continue
                elif in_changes_section and line.strip().startswith('-'):
                    changes.append(line.strip())
                elif in_changes_section and not line.strip():
                    break
            
            return changes if changes else ["Tests refined based on user feedback"]
        except Exception:
            return ["Tests refined based on user feedback"]

    def generate_mock_code(self, code: str) -> str:
        """Generate mock code for external dependencies"""
        try:
            tree = ast.parse(code)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(ast.unparse(node))
            
            # Generate mock setup
            mock_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a testing expert. Generate mock setup code for the given imports."),
                ("human", f"""
Generate mock setup code for these imports:
{chr(10).join(imports)}

Provide:
1. Mock decorators and patches
2. Mock return values
3. Side effects if needed
4. Cleanup code
""")
            ])
            
            mock_chain = mock_prompt | self.llm
            response = mock_chain.invoke({"imports": chr(10).join(imports)})
            
            return response
            
        except Exception:
            return "# Mock setup could not be generated"
