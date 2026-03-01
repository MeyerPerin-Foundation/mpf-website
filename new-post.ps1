# new-post.ps1
# Creates a new blog post with the proper template and naming convention

param(
    [string]$Title,
    [datetime]$Date = (Get-Date)
)

# If no title provided, prompt for it
if (-not $Title) {
    $Title = Read-Host "Enter the post title"
    if (-not $Title) {
        Write-Error "Title is required"
        exit 1
    }
}

# Format the date as YYYY-MM-DD
$dateStr = $Date.ToString("yyyy-MM-dd")

# Create a slug from the title (lowercase, replace spaces with hyphens, remove special chars)
$slug = $Title.ToLower() `
    -replace '[^a-z0-9\s-]', '' `
    -replace '\s+', '-' `
    -replace '-+', '-' `
    -replace '^-|-$', ''

# Create the filename
$filename = "$dateStr-$slug.qmd"
$filepath = Join-Path "posts" $filename

# Check if file already exists
if (Test-Path $filepath) {
    Write-Error "File already exists: $filepath"
    exit 1
}

# Create the post content with template
$content = @"
---
author: Lucas A. Meyer
date: $dateStr
draft: true
image: /images/
include-in-header: _msft-clarity.html
page-layout: full
title: $Title
toc: true
toc-expand: true
---
<article data-clarity-region="article">

Write your post content here...

</article>
"@

# Write the file
$content | Out-File -FilePath $filepath -Encoding utf8

Write-Host "✓ Created new post: $filepath" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Add an image to /images/ and update the 'image:' field"
Write-Host "  2. Write your content"
Write-Host "  3. Change 'draft: true' to 'draft: false' when ready to publish"

# Open the file in the default editor (optional - uncomment if desired)
# code $filepath
