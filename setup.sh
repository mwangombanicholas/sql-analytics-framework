#!/bin/bash
# Setup script for the SQL Analytics Framework

echo "🚀 Setting up SQL Analytics Framework..."

# Install dependencies
pip install -r requirements.txt

# Check if database exists
if [ -f "analytics_framework.db" ]; then
    echo "✅ Database found"
else
    echo "⚠️ Database not found. Please ensure analytics_framework.db is in the current directory"
fi

echo ""
echo "📊 To run the dashboard:"
echo "streamlit run streamlit_app.py"
echo ""
echo "✨ Setup complete!"
