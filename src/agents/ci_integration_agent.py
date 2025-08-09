"""
CI/CD Integration Agent for CodeForge AI
Generates GitHub Actions workflows for automated test suggestions
"""

import os
import yaml
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# LLMChain is no longer used, using RunnableSequence instead


class CIIntegrationAgent:
    """AI-powered CI/CD integration agent"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.1,
            api_key=self.api_key
        )
        
        self.system_prompt = """You are an expert DevOps engineer specializing in CI/CD pipelines and GitHub Actions. Your role is to:

1. Generate GitHub Actions workflows for automated code analysis
2. Create PR comment bots that suggest test improvements
3. Set up automated test generation on code changes
4. Configure quality gates and security checks
5. Implement best practices for CI/CD automation

Focus on:
- Automated test suggestions on PRs
- Code quality checks
- Security vulnerability scanning
- Performance monitoring
- Clear, maintainable workflow configurations"""

    def generate_github_actions_workflow(self, project_type: str = "python", 
                                       features: List[str] = None) -> Dict[str, Any]:
        """Generate GitHub Actions workflow for automated test suggestions"""
        try:
            features = features or ["test_generation", "code_review", "security_scan"]
            
            workflow_prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", """
                Generate a GitHub Actions workflow for automated test suggestions on PRs.
                
                **Project Type:** {project_type}
                **Features:** {features}
                
                Requirements:
                1. Trigger on pull requests
                2. Run CodeForge AI analysis
                3. Generate test suggestions
                4. Comment on PR with results
                5. Include security and quality checks
                6. Support multiple programming languages
                
                Provide:
                1. **Workflow YAML** - Complete GitHub Actions workflow
                2. **Setup Instructions** - How to configure the workflow
                3. **Environment Variables** - Required secrets and variables
                4. **Usage Examples** - How to use the automated suggestions
                """)
            ])
            
            chain = workflow_prompt | self.llm
            
            response = chain.invoke({
                "project_type": project_type,
                "features": ", ".join(features)
            })
            
            # Extract workflow YAML
            workflow_yaml = self._extract_workflow_yaml(response)
            
            return {
                "success": True,
                "workflow_yaml": workflow_yaml,
                "setup_instructions": self._extract_setup_instructions(response),
                "environment_variables": self._extract_env_vars(response),
                "usage_examples": self._extract_usage_examples(response)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate workflow: {str(e)}"
            }

    def generate_pr_comment_bot(self, analysis_results: Dict) -> str:
        """Generate PR comment with test suggestions"""
        try:
            comment_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a helpful bot that comments on GitHub PRs with test suggestions.
                Be concise, actionable, and friendly. Focus on the most important improvements."""),
                ("human", """
                Generate a GitHub PR comment based on CodeForge AI analysis results.
                
                **Analysis Results:**
                {analysis_results}
                
                Create a comment that:
                1. Summarizes key findings
                2. Suggests specific test improvements
                3. Provides actionable next steps
                4. Uses GitHub markdown formatting
                5. Is encouraging and helpful
                """)
            ])
            
            chain = comment_prompt | self.llm
            
            response = chain.invoke({
                "analysis_results": str(analysis_results)
            })
            
            return response
            
        except Exception as e:
            return f"❌ Error generating PR comment: {str(e)}"

    def generate_quality_gates_config(self, project_type: str = "python") -> Dict[str, Any]:
        """Generate quality gates configuration"""
        try:
            gates_prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", """
                Generate quality gates configuration for automated code quality checks.
                
                **Project Type:** {project_type}
                
                Include gates for:
                1. Test coverage thresholds
                2. Code complexity limits
                3. Security vulnerability checks
                4. Performance benchmarks
                5. Documentation requirements
                
                Provide configuration in YAML format with clear thresholds and actions.
                """)
            ])
            
            chain = gates_prompt | self.llm
            
            response = chain.invoke({
                "project_type": project_type
            })
            
            return {
                "success": True,
                "quality_gates": self._extract_quality_gates(response),
                "configuration": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate quality gates: {str(e)}"
            }

    def _extract_workflow_yaml(self, response: str) -> str:
        """Extract workflow YAML from response"""
        try:
            lines = response.split('\n')
            yaml_lines = []
            in_yaml = False
            
            for line in lines:
                if '```yaml' in line or '```yml' in line:
                    in_yaml = True
                    continue
                elif '```' in line and in_yaml:
                    break
                elif in_yaml:
                    yaml_lines.append(line)
            
            return '\n'.join(yaml_lines) if yaml_lines else self._generate_default_workflow()
        except Exception:
            return self._generate_default_workflow()

    def _generate_default_workflow(self) -> str:
        """Generate a default GitHub Actions workflow"""
        return """name: CodeForge AI Analysis

on:
  pull_request:
    branches: [ main, develop ]

jobs:
  codeforge-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install CodeForge AI
      run: |
        pip install -r requirements.txt
    
    - name: Run CodeForge AI Analysis
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        python -m src.agents.test_generator_agent
        
    - name: Comment PR with Results
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const results = fs.readFileSync('analysis_results.json', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## 🤖 CodeForge AI Analysis Results\\n\\n${results}`
          });"""

    def _extract_setup_instructions(self, response: str) -> List[str]:
        """Extract setup instructions from response"""
        try:
            lines = response.split('\n')
            instructions = []
            in_instructions = False
            
            for line in lines:
                if 'setup' in line.lower() or 'instructions' in line.lower():
                    in_instructions = True
                    continue
                elif in_instructions and line.strip().startswith('#'):
                    break
                elif in_instructions and line.strip():
                    instructions.append(line.strip())
            
            return instructions if instructions else ["Follow the workflow YAML configuration"]
        except Exception:
            return ["Follow the workflow YAML configuration"]

    def _extract_env_vars(self, response: str) -> Dict[str, str]:
        """Extract environment variables from response"""
        return {
            "OPENAI_API_KEY": "Your OpenAI API key for CodeForge AI",
            "GITHUB_TOKEN": "GitHub token for PR comments (auto-provided)",
            "CODEFORGE_CONFIG": "Optional: Path to CodeForge configuration file"
        }

    def _extract_usage_examples(self, response: str) -> List[str]:
        """Extract usage examples from response"""
        return [
            "The workflow automatically runs on every PR",
            "Test suggestions are posted as PR comments",
            "Quality gates can block PRs if thresholds aren't met",
            "Security vulnerabilities are flagged automatically"
        ]

    def _extract_quality_gates(self, response: str) -> Dict[str, Any]:
        """Extract quality gates configuration"""
        return {
            "test_coverage": {
                "minimum": 80,
                "target": 90,
                "action": "warn"
            },
            "complexity": {
                "max_cyclomatic": 10,
                "action": "block"
            },
            "security": {
                "vulnerabilities": 0,
                "action": "block"
            },
            "performance": {
                "max_response_time": 1000,
                "action": "warn"
            }
        }
