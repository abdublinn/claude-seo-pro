# claude-seo-pro v2.1.0 installer (Windows PowerShell)

$ErrorActionPreference = "Stop"

$SKILL_DIR = "$env:USERPROFILE\.claude\skills"
$AGENT_DIR = "$env:USERPROFILE\.claude\agents"
$SCRIPT_DIR = "$SKILL_DIR\seo\scripts"

Write-Host "Installing claude-seo-pro v2.1.0..." -ForegroundColor Cyan

# Create directories
$dirs = @(
    "$SKILL_DIR\seo\references",
    "$SKILL_DIR\seo-audit",
    "$SKILL_DIR\seo-crawl",
    "$SKILL_DIR\seo-page",
    "$SKILL_DIR\seo-technical",
    "$SKILL_DIR\seo-content",
    "$SKILL_DIR\seo-schema",
    "$SKILL_DIR\seo-sitemap",
    "$SKILL_DIR\seo-images",
    "$SKILL_DIR\seo-geo",
    "$SKILL_DIR\seo-local",
    "$SKILL_DIR\seo-plan\assets",
    "$SKILL_DIR\seo-programmatic",
    "$SKILL_DIR\seo-competitor-pages",
    "$SKILL_DIR\seo-hreflang",
    "$AGENT_DIR",
    "$SCRIPT_DIR",
    "$SKILL_DIR\seo\schema"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# Copy skills
Copy-Item "seo\SKILL.md" "$SKILL_DIR\seo\" -Force
Copy-Item "seo\references\*.md" "$SKILL_DIR\seo\references\" -Force
Copy-Item "skills\seo-audit\SKILL.md" "$SKILL_DIR\seo-audit\" -Force
Copy-Item "skills\seo-crawl\SKILL.md" "$SKILL_DIR\seo-crawl\" -Force
Copy-Item "skills\seo-page\SKILL.md" "$SKILL_DIR\seo-page\" -Force
Copy-Item "skills\seo-technical\SKILL.md" "$SKILL_DIR\seo-technical\" -Force
Copy-Item "skills\seo-content\SKILL.md" "$SKILL_DIR\seo-content\" -Force
Copy-Item "skills\seo-schema\SKILL.md" "$SKILL_DIR\seo-schema\" -Force
Copy-Item "skills\seo-sitemap\SKILL.md" "$SKILL_DIR\seo-sitemap\" -Force
Copy-Item "skills\seo-images\SKILL.md" "$SKILL_DIR\seo-images\" -Force
Copy-Item "skills\seo-geo\SKILL.md" "$SKILL_DIR\seo-geo\" -Force
Copy-Item "skills\seo-local\SKILL.md" "$SKILL_DIR\seo-local\" -Force
Copy-Item "skills\seo-plan\SKILL.md" "$SKILL_DIR\seo-plan\" -Force
Copy-Item "skills\seo-plan\assets\*.md" "$SKILL_DIR\seo-plan\assets\" -Force
Copy-Item "skills\seo-programmatic\SKILL.md" "$SKILL_DIR\seo-programmatic\" -Force
Copy-Item "skills\seo-competitor-pages\SKILL.md" "$SKILL_DIR\seo-competitor-pages\" -Force
Copy-Item "skills\seo-hreflang\SKILL.md" "$SKILL_DIR\seo-hreflang\" -Force

# Copy agents
Copy-Item "agents\*.md" "$AGENT_DIR\" -Force

# Copy scripts
Copy-Item "scripts\*.py" "$SCRIPT_DIR\" -Force

# Copy schema templates
Copy-Item "schema\templates.json" "$SKILL_DIR\seo\schema\" -Force

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install --quiet requests beautifulsoup4 lxml 2>$null
} catch {
    Write-Host "Warning: Could not install Python deps. Install manually: pip install requests beautifulsoup4 lxml" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "claude-seo-pro v2.1.0 installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage:"
Write-Host "  /seo audit https://example.com"
Write-Host "  /seo crawl https://example.com"
Write-Host "  /seo page https://example.com/page"
Write-Host ""
Write-Host "For full command list: see README.md"
