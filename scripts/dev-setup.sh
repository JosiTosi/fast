#!/bin/bash
# Development setup script

set -e

echo "🚀 Setting up Fast API development environment..."

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Install dependencies
echo "📥 Installing dependencies..."
uv sync --all-extras --dev

# Set up environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env file. Please review and update as needed."
fi

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
uv run pre-commit install

# Run initial tests to make sure everything works
echo "🧪 Running tests..."
uv run pytest

echo "✅ Development environment setup complete!"
echo ""
echo "🚀 To start the development server:"
echo "   uv run uvicorn src.fast_api.main:app --reload"
echo ""
echo "📖 API Documentation will be available at:"
echo "   http://localhost:8000/docs"
