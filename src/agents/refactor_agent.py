"""
Refactor Agent for CodeForge AI
Suggests and implements code improvements using AI
"""

import os
import ast
import re
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# LLMChain is no longer used, using RunnableSequence instead
import json


class RefactorAgent:
    """AI-powered code refactoring agent"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Get model from environment or default to gpt-3.5-turbo
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.1,
            api_key=self.api_key
        )
        
        self.system_prompt = """You are an expert software engineer specializing in code refactoring and optimization. Your role is to:

1. Analyze code for refactoring opportunities
2. Suggest specific improvements for readability, performance, and maintainability
3. Provide refactored code that follows best practices
4. Maintain functionality while improving code quality
5. Consider SOLID principles, DRY, and clean code practices
6. Optimize for performance where appropriate
7. Improve code structure and organization

When refactoring:
- Preserve existing functionality
- Improve readability and maintainability
- Follow language-specific conventions
- Add appropriate documentation
- Consider performance implications
- Maintain backward compatibility where possible"""

        self.refactor_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """
Please analyze and refactor the following code:

**Original Code:**
{code}

**Context:**
- File: {file_path}
- Language: {language}
- Analysis Results: {analysis_results}

**Refactoring Goals:**
1. Improve code readability and maintainability
2. Reduce complexity where possible
3. Follow best practices and conventions
4. Optimize performance if needed
5. Add appropriate documentation
6. Improve code structure

Please provide:
1. **Refactored Code** - The improved version
2. **Changes Summary** - What was changed and why
3. **Improvements Made** - Specific improvements and their benefits
4. **Additional Suggestions** - Further improvements that could be made

Format the response with clear sections and explanations for each change.
""")
        ])
        
        # Use the new RunnableSequence pattern instead of deprecated LLMChain
        self.chain = self.refactor_prompt | self.llm
    
    def suggest_refactoring(self, code: str, file_path: str = None, language: str = "python",
                          analysis_results: Dict = None) -> Dict[str, Any]:
        """Suggest refactoring improvements"""
        try:
            # Prepare analysis results for the prompt
            analysis_text = self._format_analysis_results(analysis_results) if analysis_results else "No static analysis available"
            
            # Generate refactoring suggestions
            response = self.chain.invoke({
                "code": code,
                "file_path": file_path or "unknown",
                "language": language,
                "analysis_results": analysis_text
            })
            
            # Parse and structure the response
            structured_refactor = self._parse_refactor_response(response)
            
            return {
                "success": True,
                "refactored_code": structured_refactor.get("refactored_code", ""),
                "changes_summary": structured_refactor.get("changes_summary", []),
                "improvements": structured_refactor.get("improvements", []),
                "suggestions": structured_refactor.get("suggestions", []),
                "raw_response": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "refactored_code": None
            }
    
    def _format_analysis_results(self, analysis: Dict) -> str:
        """Format analysis results for the prompt"""
        if not analysis:
            return "No analysis data available"
        
        formatted = []
        
        if 'metrics' in analysis:
            metrics = analysis['metrics']
            formatted.append(f"Lines of Code: {metrics.lines_of_code}")
            formatted.append(f"Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
            formatted.append(f"Maintainability Index: {metrics.maintainability_index:.1f}")
        
        if 'issues' in analysis:
            issues = analysis['issues']
            formatted.append(f"Found {len(issues)} code issues:")
            for issue in issues[:5]:  # Limit to first 5 issues
                formatted.append(f"- {issue.severity.upper()}: {issue.message}")
        
        if 'complexity' in analysis:
            complexity = analysis['complexity']
            formatted.append(f"Complexity Level: {complexity['complexity_level']}")
            formatted.append(f"Nesting Depth: {complexity['nesting_depth']}")
        
        if 'suggestions' in analysis:
            suggestions = analysis['suggestions']
            if suggestions:
                formatted.append("Static Analysis Suggestions:")
                for suggestion in suggestions[:3]:
                    formatted.append(f"- {suggestion}")
        
        return "\n".join(formatted)
    
    def _parse_refactor_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response into structured format"""
        sections = {
            "refactored_code": "",
            "changes_summary": [],
            "improvements": [],
            "suggestions": []
        }
        
        # Simple parsing - look for code blocks and sections
        lines = response.split('\n')
        current_section = None
        in_code_block = False
        code_block = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect code blocks
            if line.startswith('```'):
                if in_code_block:
                    # End of code block
                    sections["refactored_code"] = "\n".join(code_block)
                    in_code_block = False
                    code_block = []
                else:
                    # Start of code block
                    in_code_block = True
                continue
            
            if in_code_block:
                code_block.append(line)
                continue
            
            # Detect section headers
            if any(keyword in line.lower() for keyword in ['changes', 'summary', 'what was changed']):
                current_section = 'changes_summary'
            elif any(keyword in line.lower() for keyword in ['improvements', 'benefits']):
                current_section = 'improvements'
            elif any(keyword in line.lower() for keyword in ['suggestions', 'additional']):
                current_section = 'suggestions'
            
            # Add content to current section
            if current_section and line and not line.startswith('#'):
                if line.startswith('-') or line.startswith('•'):
                    sections[current_section].append(line[1:].strip())
                else:
                    sections[current_section].append(line)
        
        return sections
    
    def generate_refactor_summary(self, refactor_result: Dict) -> str:
        """Generate a summary of the refactoring changes"""
        summary_parts = []
        
        changes_count = len(refactor_result.get("changes_summary", []))
        if changes_count > 0:
            summary_parts.append(f"Changes: {changes_count}")
        
        improvements_count = len(refactor_result.get("improvements", []))
        if improvements_count > 0:
            summary_parts.append(f"Improvements: {improvements_count}")
        
        suggestions_count = len(refactor_result.get("suggestions", []))
        if suggestions_count > 0:
            summary_parts.append(f"Additional Suggestions: {suggestions_count}")
        
        return " | ".join(summary_parts) if summary_parts else "No refactoring suggestions"
    
    def apply_refactoring(self, original_code: str, refactored_code: str) -> Dict[str, Any]:
        """Apply the refactored code and validate changes"""
        try:
            # Basic validation
            original_ast = ast.parse(original_code)
            refactored_ast = ast.parse(refactored_code)
            
            # Compare structure
            original_functions = [n.name for n in ast.walk(original_ast) if isinstance(n, ast.FunctionDef)]
            refactored_functions = [n.name for n in ast.walk(refactored_ast) if isinstance(n, ast.FunctionDef)]
            
            # Check if all original functions are preserved
            missing_functions = set(original_functions) - set(refactored_functions)
            
            return {
                "success": len(missing_functions) == 0,
                "missing_functions": list(missing_functions),
                "preserved_functions": len(original_functions),
                "new_functions": len(set(refactored_functions) - set(original_functions))
            }
            
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"Syntax error in refactored code: {str(e)}"
            }
    
    def suggest_specific_improvements(self, code: str, analysis: Dict) -> List[str]:
        """Generate specific improvement suggestions based on analysis"""
        suggestions = []
        
        if 'metrics' in analysis:
            metrics = analysis['metrics']
            
            if metrics.cyclomatic_complexity > 10:
                suggestions.append("Break down complex functions into smaller, more focused functions")
            
            if metrics.maintainability_index < 50:
                suggestions.append("Improve code organization and reduce complexity")
        
        if 'issues' in analysis:
            issues = analysis['issues']
            
            for issue in issues:
                if issue.category == 'complexity':
                    suggestions.append(f"Simplify complex logic in {issue.message}")
                elif issue.category == 'style':
                    suggestions.append(f"Follow naming conventions: {issue.message}")
        
        if 'complexity' in analysis:
            complexity = analysis['complexity']
            
            if complexity['nesting_depth'] > 3:
                suggestions.append("Reduce nesting depth by extracting helper functions")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def generate_documentation(self, code: str) -> str:
        """Generate documentation for the code"""
        try:
            doc_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a technical writer. Generate clear, comprehensive documentation for the given code."),
                ("human", f"""
Please generate documentation for this code:

{code}

Include:
1. Module/class overview
2. Function documentation with parameters and return values
3. Usage examples
4. Important notes or warnings
5. Dependencies and requirements

Format as clear, well-structured documentation.
""")
            ])
            
            doc_chain = LLMChain(llm=self.llm, prompt=doc_prompt)
            response = doc_chain.run({"code": code})
            
            return response
            
        except Exception:
            return "# Documentation could not be generated"
