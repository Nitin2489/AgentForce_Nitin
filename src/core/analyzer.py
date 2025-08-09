"""
Core code analyzer for CodeForge AI
Provides multi-modal code analysis capabilities
"""

import ast
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import astunparse


@dataclass
class CodeMetrics:
    """Code quality metrics"""
    lines_of_code: int
    cyclomatic_complexity: int
    maintainability_index: float
    security_score: float
    performance_score: float
    test_coverage: float


@dataclass
class CodeIssue:
    """Represents a code issue found during analysis"""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'security', 'performance', 'style', 'complexity'
    message: str
    line_number: int
    suggestion: str


class CodeAnalyzer:
    """Multi-modal code analyzer for CodeForge AI"""
    
    def __init__(self):
        self.security_patterns = {
            'sql_injection': r'execute\(.*\+.*\)',
            'xss': r'innerHTML\s*=',
            'hardcoded_password': r'password\s*=\s*["\'][^"\']+["\']',
            'unsafe_eval': r'eval\(',
            'weak_random': r'random\.randint\(',
        }
        
        self.performance_patterns = {
            'nested_loops': r'for.*:\s*\n.*for.*:',
            'inefficient_string': r'\+.*\+.*\+',
            'large_list_comp': r'\[.*for.*in.*if.*\]',
        }
        
        # Language-specific patterns
        self.language_patterns = {
            'javascript': {
                'function_def': r'function\s+(\w+)\s*\([^)]*\)',
                'class_def': r'class\s+(\w+)',
                'import_stmt': r'import\s+.*|from\s+.*\s+import\s+.*|require\s*\([^)]+\)',
                'variable_decl': r'(?:var|let|const)\s+(\w+)',
                'method_def': r'(\w+)\s*\([^)]*\)\s*{',
            },
            'java': {
                'function_def': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(?:abstract\s+)?(?:strictfp\s+)?(?:<[^>]+>\s+)?(?:[\w\[\]]+\s+)+(\w+)\s*\([^)]*\)',
                'class_def': r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)',
                'import_stmt': r'import\s+.*;',
                'variable_decl': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:transient\s+)?(?:volatile\s+)?(?:[\w\[\]]+\s+)+(\w+)\s*[=;]',
                'method_def': r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:native\s+)?(?:abstract\s+)?(?:strictfp\s+)?(?:<[^>]+>\s+)?(?:[\w\[\]]+\s+)+(\w+)\s*\([^)]*\)',
            },
            'python': {
                'function_def': r'def\s+(\w+)\s*\([^)]*\)',
                'class_def': r'class\s+(\w+)',
                'import_stmt': r'import\s+.*|from\s+.*\s+import\s+.*',
                'variable_decl': r'(\w+)\s*=',
                'method_def': r'def\s+(\w+)\s*\([^)]*\)',
            }
        }
    
    def analyze_code(self, code: str, file_path: str = None, language: str = "python") -> Dict[str, Any]:
        """Comprehensive code analysis with multi-language support"""
        try:
            if language == "python":
                return self._analyze_python_code(code, file_path)
            else:
                return self._analyze_generic_code(code, file_path, language)
        except Exception as e:
            return {
                'error': f'Analysis error: {str(e)}',
                'language': language
            }
    
    def _analyze_python_code(self, code: str, file_path: str = None) -> Dict[str, Any]:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(code)
            
            analysis = {
                'metrics': self._calculate_metrics(tree, code),
                'issues': self._find_issues(tree, code),
                'structure': self._analyze_structure(tree),
                'complexity': self._analyze_complexity(tree),
                'security': self._security_analysis(code),
                'performance': self._performance_analysis(code),
                'suggestions': self._generate_suggestions(tree, code)
            }
            
            return analysis
        except SyntaxError as e:
            return {
                'error': f'Syntax error: {str(e)}',
                'line': e.lineno,
                'offset': e.offset
            }
    
    def _analyze_generic_code(self, code: str, file_path: str = None, language: str = "javascript") -> Dict[str, Any]:
        """Analyze non-Python code using regex patterns"""
        patterns = self.language_patterns.get(language, self.language_patterns['javascript'])
        
        # Basic metrics
        lines = len(code.split('\n'))
        complexity = self._calculate_generic_complexity(code, patterns)
        maintainability = max(0, 100 - complexity * 2 - lines * 0.1)
        
        # Structure analysis
        structure = self._analyze_generic_structure(code, patterns)
        
        # Security and performance analysis
        security = self._security_analysis(code)
        performance = self._performance_analysis(code)
        
        # Generate issues
        issues = self._find_generic_issues(code, patterns, language)
        
        # Generate suggestions
        suggestions = self._generate_generic_suggestions(code, language)
        
        metrics = CodeMetrics(
            lines_of_code=lines,
            cyclomatic_complexity=complexity,
            maintainability_index=maintainability,
            security_score=security['score'],
            performance_score=performance['score'],
            test_coverage=0.0
        )
        
        return {
            'metrics': metrics,
            'issues': issues,
            'structure': structure,
            'complexity': {
                'cyclomatic_complexity': complexity,
                'complexity_level': 'high' if complexity > 10 else 'medium' if complexity > 5 else 'low',
                'nesting_depth': self._calculate_generic_nesting_depth(code)
            },
            'security': security,
            'performance': performance,
            'suggestions': suggestions
        }
    
    def _calculate_metrics(self, tree: ast.AST, code: str) -> CodeMetrics:
        """Calculate code quality metrics"""
        lines = len(code.split('\n'))
        
        # Calculate cyclomatic complexity
        complexity = self._calculate_cyclomatic_complexity(tree)
        
        # Calculate maintainability index (simplified)
        maintainability = max(0, 100 - complexity * 2 - lines * 0.1)
        
        # Security score based on security issues found
        security_score = self._calculate_security_score(code)
        
        # Performance score
        performance_score = self._calculate_performance_score(code)
        
        return CodeMetrics(
            lines_of_code=lines,
            cyclomatic_complexity=complexity,
            maintainability_index=maintainability,
            security_score=security_score,
            performance_score=performance_score,
            test_coverage=0.0  # Would be calculated separately
        )
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _find_issues(self, tree: ast.AST, code: str) -> List[CodeIssue]:
        """Find code issues and problems"""
        issues = []
        
        # Find unused imports
        issues.extend(self._find_unused_imports(tree))
        
        # Find long functions
        issues.extend(self._find_long_functions(tree))
        
        # Find complex expressions
        issues.extend(self._find_complex_expressions(tree))
        
        # Find naming issues
        issues.extend(self._find_naming_issues(tree))
        
        return issues
    
    def _find_unused_imports(self, tree: ast.AST) -> List[CodeIssue]:
        """Find unused imports"""
        issues = []
        imports = []
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
            elif isinstance(node, ast.Name):
                used_names.add(node.id)
        
        for imp in imports:
            if imp not in used_names:
                issues.append(CodeIssue(
                    severity='warning',
                    category='style',
                    message=f'Unused import: {imp}',
                    line_number=1,
                    suggestion=f'Remove unused import: {imp}'
                ))
        
        return issues
    
    def _find_long_functions(self, tree: ast.AST) -> List[CodeIssue]:
        """Find functions that are too long"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = len(node.body)
                if lines > 20:
                    issues.append(CodeIssue(
                        severity='warning',
                        category='complexity',
                        message=f'Function {node.name} is too long ({lines} lines)',
                        line_number=node.lineno,
                        suggestion=f'Consider breaking down {node.name} into smaller functions'
                    ))
        
        return issues
    
    def _find_complex_expressions(self, tree: ast.AST) -> List[CodeIssue]:
        """Find overly complex expressions"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.BoolOp) and len(node.values) > 3:
                issues.append(CodeIssue(
                    severity='info',
                    category='complexity',
                    message='Complex boolean expression',
                    line_number=node.lineno,
                    suggestion='Consider breaking down complex boolean expression'
                ))
        
        return issues
    
    def _find_naming_issues(self, tree: ast.AST) -> List[CodeIssue]:
        """Find naming convention issues"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    issues.append(CodeIssue(
                        severity='warning',
                        category='style',
                        message=f'Function name {node.name} should be snake_case',
                        line_number=node.lineno,
                        suggestion=f'Rename function to follow snake_case convention'
                    ))
        
        return issues
    
    def _analyze_structure(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze code structure"""
        classes = []
        functions = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                })
            elif isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': len(node.args.args)
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append({
                    'line': node.lineno,
                    'type': type(node).__name__
                })
        
        return {
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'total_classes': len(classes),
            'total_functions': len(functions),
            'total_imports': len(imports)
        }
    
    def _analyze_complexity(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze code complexity"""
        complexity = self._calculate_cyclomatic_complexity(tree)
        
        return {
            'cyclomatic_complexity': complexity,
            'complexity_level': 'high' if complexity > 10 else 'medium' if complexity > 5 else 'low',
            'nesting_depth': self._calculate_nesting_depth(tree)
        }
    
    def _calculate_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif isinstance(node, ast.FunctionDef):
                current_depth = 0
        
        return max_depth
    
    def _security_analysis(self, code: str) -> Dict[str, Any]:
        """Analyze code for security issues"""
        issues = []
        score = 100
        
        for pattern_name, pattern in self.security_patterns.items():
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'type': pattern_name,
                    'line': code[:match.start()].count('\n') + 1,
                    'description': f'Potential {pattern_name.replace("_", " ")}'
                })
                score -= 20
        
        return {
            'score': max(0, score),
            'issues': issues,
            'risk_level': 'high' if score < 50 else 'medium' if score < 80 else 'low'
        }
    
    def _performance_analysis(self, code: str) -> Dict[str, Any]:
        """Analyze code for performance issues"""
        issues = []
        score = 100
        
        for pattern_name, pattern in self.performance_patterns.items():
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'type': pattern_name,
                    'line': code[:match.start()].count('\n') + 1,
                    'description': f'Potential {pattern_name.replace("_", " ")}'
                })
                score -= 15
        
        return {
            'score': max(0, score),
            'issues': issues,
            'optimization_level': 'high' if score < 60 else 'medium' if score < 80 else 'low'
        }
    
    def _calculate_security_score(self, code: str) -> float:
        """Calculate security score"""
        score = 100
        for pattern in self.security_patterns.values():
            if re.search(pattern, code, re.IGNORECASE):
                score -= 20
        return max(0, score)
    
    def _calculate_performance_score(self, code: str) -> float:
        """Calculate performance score"""
        score = 100
        for pattern in self.performance_patterns.values():
            if re.search(pattern, code, re.IGNORECASE):
                score -= 15
        return max(0, score)
    
    def _generate_suggestions(self, tree: ast.AST, code: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Check for magic numbers
        if re.search(r'\b\d{3,}\b', code):
            suggestions.append("Consider replacing magic numbers with named constants")
        
        # Check for long lines
        lines = code.split('\n')
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 80]
        if long_lines:
            suggestions.append(f"Consider breaking long lines at lines: {long_lines[:3]}")
        
        # Check for missing docstrings
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
                suggestions.append(f"Add docstring to function '{node.name}'")
        
        return suggestions
    
    def _calculate_generic_complexity(self, code: str, patterns: Dict) -> int:
        """Calculate cyclomatic complexity for non-Python code"""
        complexity = 1  # Base complexity
        
        # Count control flow statements
        control_patterns = [
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b', r'\bswitch\b',
            r'\bcase\b', r'\bcatch\b', r'\btry\b', r'\bthrow\b', r'\breturn\b'
        ]
        
        for pattern in control_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            complexity += len(matches)
        
        return complexity
    
    def _analyze_generic_structure(self, code: str, patterns: Dict) -> Dict[str, Any]:
        """Analyze code structure for non-Python languages"""
        functions = []
        classes = []
        imports = []
        
        # Find functions
        func_matches = re.finditer(patterns['function_def'], code, re.MULTILINE)
        for match in func_matches:
            functions.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1,
                'args': len(re.findall(r'[^,]+', match.group(0).split('(')[1].split(')')[0])) if '(' in match.group(0) else 0
            })
        
        # Find classes
        class_matches = re.finditer(patterns['class_def'], code, re.MULTILINE)
        for match in class_matches:
            classes.append({
                'name': match.group(1),
                'line': code[:match.start()].count('\n') + 1,
                'methods': len([f for f in functions if f['line'] > match.start()])
            })
        
        # Find imports
        import_matches = re.finditer(patterns['import_stmt'], code, re.MULTILINE)
        for match in import_matches:
            imports.append({
                'line': code[:match.start()].count('\n') + 1,
                'type': 'import'
            })
        
        return {
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'total_classes': len(classes),
            'total_functions': len(functions),
            'total_imports': len(imports)
        }
    
    def _find_generic_issues(self, code: str, patterns: Dict, language: str) -> List[CodeIssue]:
        """Find issues in non-Python code"""
        issues = []
        lines = code.split('\n')
        
        # Check for long functions (simplified)
        for i, line in enumerate(lines):
            if re.search(patterns['function_def'], line):
                # Count lines until next function/class or end
                func_lines = 0
                for j in range(i + 1, len(lines)):
                    if re.search(patterns['function_def'], lines[j]) or re.search(patterns['class_def'], lines[j]):
                        break
                    func_lines += 1
                
                if func_lines > 20:
                    issues.append(CodeIssue(
                        severity='warning',
                        category='complexity',
                        message=f'Function is too long ({func_lines} lines)',
                        line_number=i + 1,
                        suggestion='Consider breaking down into smaller functions'
                    ))
        
        # Check for naming conventions
        if language == "javascript":
            # Check for camelCase functions
            func_matches = re.finditer(patterns['function_def'], code)
            for match in func_matches:
                func_name = match.group(1)
                if not re.match(r'^[a-z][a-zA-Z0-9]*$', func_name):
                    issues.append(CodeIssue(
                        severity='warning',
                        category='style',
                        message=f'Function name {func_name} should be camelCase',
                        line_number=code[:match.start()].count('\n') + 1,
                        suggestion=f'Rename function to follow camelCase convention'
                    ))
        
        return issues
    
    def _generate_generic_suggestions(self, code: str, language: str) -> List[str]:
        """Generate suggestions for non-Python code"""
        suggestions = []
        
        # Check for magic numbers
        if re.search(r'\b\d{3,}\b', code):
            suggestions.append("Consider replacing magic numbers with named constants")
        
        # Check for long lines
        lines = code.split('\n')
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 80]
        if long_lines:
            suggestions.append(f"Consider breaking long lines at lines: {long_lines[:3]}")
        
        # Language-specific suggestions
        if language == "javascript":
            if 'var ' in code:
                suggestions.append("Consider using 'let' or 'const' instead of 'var'")
            if 'console.log' in code:
                suggestions.append("Consider removing console.log statements for production")
        
        elif language == "java":
            if 'System.out.println' in code:
                suggestions.append("Consider using a proper logging framework instead of System.out.println")
        
        return suggestions
    
    def _calculate_generic_nesting_depth(self, code: str) -> int:
        """Calculate maximum nesting depth for non-Python code"""
        max_depth = 0
        current_depth = 0
        
        for char in code:
            if char in '{(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in '})':
                current_depth = max(0, current_depth - 1)
        
        return max_depth
