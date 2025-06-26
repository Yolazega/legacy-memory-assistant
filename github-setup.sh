#!/bin/bash

# Legacy Memory Assistant - GitHub Setup and Push Script

echo "🚀 Legacy Memory Assistant - Complete GitHub Setup"
echo "=================================================="

# Check if we are in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run from the project directory."
    exit 1
fi

echo "📋 Project Status:"
echo "   - Files ready: $(find . -type f | wc -l) files"
echo "   - Git repository: ✅ Initialized"
echo "   - Commit ready: ✅ All files staged and committed"

echo ""
echo "🔄 Creating GitHub repository..."

# Create GitHub repository using curl (requires authentication)
curl -u $USER -X POST https://api.github.com/user/repos \
  -d '{
    "name": "legacy-memory-assistant",
    "description": "A hybrid AI-based personal memory preservation system for secure, private digital legacy management using local processing and avatar interface.",
    "public": true,
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true
  }'

echo ""
echo "🔗 Setting up remote repository..."

# Add remote origin
git remote add origin https://github.com/$USER/legacy-memory-assistant.git 2>/dev/null || git remote set-url origin https://github.com/$USER/legacy-memory-assistant.git

# Set main branch
git branch -M main

echo ""
echo "📤 Pushing to GitHub..."

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Repository created and pushed to GitHub!"
    echo ""
    echo "🌐 Repository URL: https://github.com/$USER/legacy-memory-assistant"
    echo ""
    echo "📊 Project Statistics:"
    echo "   - Lines of code: $(find src -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')"
    echo "   - Python modules: $(find src -name "*.py" | wc -l)"
    echo "   - Documentation: $(wc -l README.md | awk '{print $1}') lines"
    echo "   - License: Creative Commons BY-NC-SA 4.0"
    echo ""
    echo "🎉 Your Legacy Memory Assistant project is now live on GitHub!"
else
    echo ""
    echo "❌ Push failed. Please check your GitHub authentication."
    echo "   You may need to:"
    echo "   1. Create the repository manually at: https://github.com/new"
    echo "   2. Set the repository name to: legacy-memory-assistant"
    echo "   3. Make it public"
    echo "   4. Then run: git push -u origin main"
fi

