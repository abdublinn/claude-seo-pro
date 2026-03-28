#!/bin/bash
# claude-seo-pro v2.1.0 installer

set -e

SKILL_DIR="$HOME/.claude/skills"
AGENT_DIR="$HOME/.claude/agents"
SCRIPT_DIR="$HOME/.claude/skills/seo/scripts"

echo "Installing claude-seo-pro v2.1.0..."

# Create directories
mkdir -p "$SKILL_DIR/seo/references"
mkdir -p "$SKILL_DIR/seo-audit"
mkdir -p "$SKILL_DIR/seo-crawl"
mkdir -p "$SKILL_DIR/seo-page"
mkdir -p "$SKILL_DIR/seo-technical"
mkdir -p "$SKILL_DIR/seo-content"
mkdir -p "$SKILL_DIR/seo-schema"
mkdir -p "$SKILL_DIR/seo-sitemap"
mkdir -p "$SKILL_DIR/seo-images"
mkdir -p "$SKILL_DIR/seo-geo"
mkdir -p "$SKILL_DIR/seo-local"
mkdir -p "$SKILL_DIR/seo-plan/assets"
mkdir -p "$SKILL_DIR/seo-programmatic"
mkdir -p "$SKILL_DIR/seo-competitor-pages"
mkdir -p "$SKILL_DIR/seo-hreflang"
mkdir -p "$AGENT_DIR"
mkdir -p "$SCRIPT_DIR"

# Copy skills
cp seo/SKILL.md "$SKILL_DIR/seo/"
cp seo/references/*.md "$SKILL_DIR/seo/references/"
cp skills/seo-audit/SKILL.md "$SKILL_DIR/seo-audit/"
cp skills/seo-crawl/SKILL.md "$SKILL_DIR/seo-crawl/"
cp skills/seo-page/SKILL.md "$SKILL_DIR/seo-page/"
cp skills/seo-technical/SKILL.md "$SKILL_DIR/seo-technical/"
cp skills/seo-content/SKILL.md "$SKILL_DIR/seo-content/"
cp skills/seo-schema/SKILL.md "$SKILL_DIR/seo-schema/"
cp skills/seo-sitemap/SKILL.md "$SKILL_DIR/seo-sitemap/"
cp skills/seo-images/SKILL.md "$SKILL_DIR/seo-images/"
cp skills/seo-geo/SKILL.md "$SKILL_DIR/seo-geo/"
cp skills/seo-local/SKILL.md "$SKILL_DIR/seo-local/"
cp skills/seo-plan/SKILL.md "$SKILL_DIR/seo-plan/"
cp skills/seo-plan/assets/*.md "$SKILL_DIR/seo-plan/assets/"
cp skills/seo-programmatic/SKILL.md "$SKILL_DIR/seo-programmatic/"
cp skills/seo-competitor-pages/SKILL.md "$SKILL_DIR/seo-competitor-pages/"
cp skills/seo-hreflang/SKILL.md "$SKILL_DIR/seo-hreflang/"

# Copy agents
cp agents/*.md "$AGENT_DIR/"

# Copy scripts
cp scripts/*.py "$SCRIPT_DIR/"

# Copy schema templates
mkdir -p "$SKILL_DIR/seo/schema"
cp schema/templates.json "$SKILL_DIR/seo/schema/"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --quiet requests beautifulsoup4 lxml 2>/dev/null || {
    echo "Warning: Could not install Python deps. Install manually: pip install requests beautifulsoup4 lxml"
}

echo ""
echo "claude-seo-pro v2.1.0 installed successfully!"
echo ""
echo "Usage:"
echo "  /seo audit https://example.com"
echo "  /seo crawl https://example.com"
echo "  /seo page https://example.com/page"
echo ""
echo "For full command list: see README.md"
