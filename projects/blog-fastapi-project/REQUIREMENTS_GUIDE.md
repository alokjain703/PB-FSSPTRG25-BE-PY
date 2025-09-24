# 📦 Requirements Management Guide

## 🗂️ **File Structure:**
```
requirements/
├── base.txt     # Core dependencies (common to all environments)
├── dev.txt      # Development dependencies (includes base + dev tools)
├── prod.txt     # Production dependencies (includes base + production tools)
└── test.txt     # Testing dependencies (includes base + testing tools)
requirements.txt # Default pointer to dev.txt
```

## 🚀 **Installation Commands:**

### **Development Environment** (Recommended for local development):
```bash
pip install -r requirements/dev.txt
# OR
pip install -r requirements.txt  # (defaults to dev)
```

### **Production Environment**:
```bash
pip install -r requirements/prod.txt
```

### **Testing Only**:
```bash
pip install -r requirements/test.txt
```

### **Base Only** (minimal installation):
```bash
pip install -r requirements/base.txt
```

## 🎯 **Usage Examples:**

### **Fresh Development Setup:**
```bash
# Clone your project
git clone <your-repo>
cd blog-fastapi-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements/dev.txt

# Start development server
uvicorn src.main:app --reload
```

### **Production Deployment:**
```bash
# In production environment
pip install -r requirements/prod.txt

# Start with gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### **Running Tests:**
```bash
# Install test dependencies
pip install -r requirements/test.txt

# Run tests
pytest
```

## 📝 **Adding New Dependencies:**

### **Add to Base** (needed in all environments):
```bash
# Add to requirements/base.txt
echo "new-package>=1.0.0" >> requirements/base.txt
```

### **Add to Development Only**:
```bash
# Add to requirements/dev.txt
echo "dev-only-package>=1.0.0" >> requirements/dev.txt
```

### **Add to Production Only**:
```bash
# Add to requirements/prod.txt
echo "prod-only-package>=1.0.0" >> requirements/prod.txt
```

## 🔄 **Updating Dependencies:**

### **Check for Updates:**
```bash
pip list --outdated
```

### **Update Specific Package:**
```bash
# Update in the appropriate requirements file
# Then reinstall
pip install -r requirements/dev.txt --upgrade
```

## 🐳 **Docker Integration:**

### **Development Dockerfile:**
```dockerfile
COPY requirements/dev.txt .
RUN pip install -r dev.txt
```

### **Production Dockerfile:**
```dockerfile
COPY requirements/prod.txt .
RUN pip install -r prod.txt
```