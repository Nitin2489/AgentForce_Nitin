"""
Code Review Agent for CodeForge AI
Provides intelligent code review using AI
"""

import os
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
# LLMChain is no longer used, using RunnableSequence instead
import json


class CodeReviewAgent:
    """AI-powered code review agent"""
    
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
        
        self.system_prompt = """You are an expert code reviewer with deep knowledge of software engineering best practices, security, performance, and code quality. Your role is to:

1. Analyze code for potential issues, bugs, and improvements
2. Provide constructive feedback with specific suggestions
3. Identify security vulnerabilities and performance issues
4. Suggest refactoring opportunities
5. Ensure code follows best practices and standards
6. Consider maintainability, readability, and scalability

Provide your review in a structured format with clear categories and actionable recommendations."""

        self.review_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", """
Please review the following code and provide a comprehensive analysis:

**Code to Review:**
{code}

**Context:**
- File: {file_path}
- Language: {language}
- Analysis Results: {analysis_results}

Please provide your review covering:
1. **Overall Assessment** - Brief summary of code quality
2. **Critical Issues** - Any bugs, security vulnerabilities, or major problems
3. **Code Quality** - Style, readability, and maintainability issues
4. **Performance** - Performance optimization opportunities
5. **Security** - Security concerns and recommendations
6. **Best Practices** - Suggestions for following industry standards
7. **Refactoring Opportunities** - Specific improvements that could be made
8. **Positive Aspects** - What the code does well

Format your response as a structured analysis with clear sections and actionable recommendations.
""")
        ])
        
        # Use the new RunnableSequence pattern instead of deprecated LLMChain
        self.chain = self.review_prompt | self.llm
    
    def review_code(self, code: str, file_path: str = None, language: str = "python", 
                   analysis_results: Dict = None) -> Dict[str, Any]:
        """Perform comprehensive code review"""
        try:
            # Prepare analysis results for the prompt
            analysis_text = self._format_analysis_results(analysis_results) if analysis_results else "No static analysis available"
            
            # Generate review
            response = self.chain.invoke({
                "code": code,
                "file_path": file_path or "unknown",
                "language": language,
                "analysis_results": analysis_text
            })
            
            # Parse and structure the response
            structured_review = self._parse_review_response(response)
            
            return {
                "success": True,
                "review": structured_review,
                "raw_response": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "review": None
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
            formatted.append(f"Security Score: {metrics.security_score:.1f}")
            formatted.append(f"Performance Score: {metrics.performance_score:.1f}")
        
        if 'issues' in analysis:
            issues = analysis['issues']
            formatted.append(f"Found {len(issues)} code issues:")
            for issue in issues[:5]:  # Limit to first 5 issues
                formatted.append(f"- {issue.severity.upper()}: {issue.message}")
        
        if 'security' in analysis:
            security = analysis['security']
            formatted.append(f"Security Risk Level: {security['risk_level']}")
            formatted.append(f"Security Score: {security['score']}")
        
        if 'performance' in analysis:
            performance = analysis['performance']
            formatted.append(f"Performance Optimization Level: {performance['optimization_level']}")
            formatted.append(f"Performance Score: {performance['score']}")
        
        return "\n".join(formatted)
    
    def _parse_review_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response into structured format"""
        # Try to extract sections from the response
        sections = {
            "overall_assessment": "",
            "critical_issues": [],
            "code_quality": [],
            "performance": [],
            "security": [],
            "best_practices": [],
            "refactoring_opportunities": [],
            "positive_aspects": []
        }
        
        # Simple parsing - look for section headers
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect section headers
            if any(keyword in line.lower() for keyword in ['overall', 'assessment', 'summary']):
                current_section = 'overall_assessment'
            elif any(keyword in line.lower() for keyword in ['critical', 'issues', 'bugs', 'problems']):
                current_section = 'critical_issues'
            elif any(keyword in line.lower() for keyword in ['quality', 'readability', 'maintainability']):
                current_section = 'code_quality'
            elif 'performance' in line.lower():
                current_section = 'performance'
            elif 'security' in line.lower():
                current_section = 'security'
            elif any(keyword in line.lower() for keyword in ['best practices', 'standards']):
                current_section = 'best_practices'
            elif any(keyword in line.lower() for keyword in ['refactor', 'improvement']):
                current_section = 'refactoring_opportunities'
            elif any(keyword in line.lower() for keyword in ['positive', 'good', 'well']):
                current_section = 'positive_aspects'
            
            # Add content to current section
            if current_section and line and not line.startswith('#'):
                if current_section == 'overall_assessment':
                    sections[current_section] += line + " "
                else:
                    if line.startswith('-') or line.startswith('•'):
                        sections[current_section].append(line[1:].strip())
                    else:
                        sections[current_section].append(line)
        
        return sections
    
    def generate_review_summary(self, review: Dict) -> str:
        """Generate a concise summary of the review"""
        summary_parts = []
        
        if review.get('overall_assessment'):
            summary_parts.append(f"Overall: {review['overall_assessment']}")
        
        critical_count = len(review.get('critical_issues', []))
        if critical_count > 0:
            summary_parts.append(f"Critical Issues: {critical_count}")
        
        quality_count = len(review.get('code_quality', []))
        if quality_count > 0:
            summary_parts.append(f"Quality Issues: {quality_count}")
        
        security_count = len(review.get('security', []))
        if security_count > 0:
            summary_parts.append(f"Security Issues: {security_count}")
        
        return " | ".join(summary_parts) if summary_parts else "No issues found"
    
    def suggest_improvements(self, code: str, review: Dict) -> List[str]:
        """Extract specific improvement suggestions from review"""
        suggestions = []
        
        # Collect suggestions from different sections
        for section in ['critical_issues', 'code_quality', 'performance', 'security', 'refactoring_opportunities']:
            if section in review:
                suggestions.extend(review[section])
        
        return suggestions[:10]  # Limit to top 10 suggestions
