# Troubleshooting Guide

## Common Installation Issues

### 1. numpy Installation Error (pkgutil.ImpImporter)

**Error**: `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'`

**Solution**: 
- This is a Python 3.12 compatibility issue with older numpy versions
- Use the updated requirements.txt or requirements_minimal.txt
- Or run: `python install.py` for automatic fix

### 2. pip Upgrade Issues

**Error**: Permission denied or pip not found

**Solution**:
```bash
# On Windows
python -m pip install --upgrade pip --user

# On Linux/Mac
python3 -m pip install --upgrade pip --user
```

### 3. Virtual Environment Issues

**Error**: Package conflicts or installation failures

**Solution**:
```bash
# Create fresh virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate

# Install dependencies
python install.py
```

### 4. OpenAI API Key Issues

**Error**: API key not found or invalid

**Solution**:
1. Get API key from https://platform.openai.com/api-keys
2. Edit `.env` file
3. Replace `your_openai_api_key_here` with your actual key

### 5. Streamlit Issues

**Error**: Streamlit not found or port conflicts

**Solution**:
```bash
# Install streamlit separately
pip install streamlit

# Run on different port
streamlit run src/ui/web_interface.py --server.port 8502
```

### 6. Memory Issues

**Error**: Out of memory during installation

**Solution**:
```bash
# Install packages one by one
pip install numpy>=1.26.0
pip install pandas>=2.2.0
pip install langchain>=0.1.0
# ... continue with other packages
```

### 7. Network/Proxy Issues

**Error**: Connection timeout or proxy errors

**Solution**:
```bash
# Use alternative index
pip install -r requirements.txt -i https://pypi.org/simple/

# Or use conda
conda install numpy pandas
pip install -r requirements.txt
```

## Quick Fix Commands

### For Python 3.12 Users:
```bash
python install.py
```

### For Manual Installation:
```bash
pip install 'numpy>=1.26.0'
pip install 'pandas>=2.2.0'
pip install -r requirements_minimal.txt
```

### For Complete Reset:
```bash
# Remove virtual environment
rm -rf venv/  # Linux/Mac
rmdir /s venv  # Windows

# Create new environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install fresh
python install.py
```

## System Requirements

- **Python**: 3.9+ (3.12 recommended)
- **RAM**: 4GB+ recommended
- **Disk**: 2GB+ free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

## Getting Help

If you're still having issues:

1. Check your Python version: `python --version`
2. Check pip version: `pip --version`
3. Try the minimal installation: `python install.py`
4. Check the error logs for specific package names
5. Consider using conda instead of pip for scientific packages

## Alternative Installation Methods

### Using Conda:
```bash
conda create -n codeforge python=3.12
conda activate codeforge
conda install numpy pandas
pip install -r requirements.txt
```

### Using Docker:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "demo.py"]
```
