param(
    [string]$Branch = "main",
    [string]$CommitMessage = "Publish site updates"
)

# Ensure Git is available before attempting push.
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Error "Git CLI was not found in PATH. Install Git and try again."
    exit 1
}

# Ensure we are inside a git repository.
& git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Current directory is not a git repository."
    exit 1
}

# Stage all changes.
& git add -A
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to stage changes."
    exit $LASTEXITCODE
}

# Check whether there is anything to commit.
& git diff --cached --quiet
$hasStagedChanges = ($LASTEXITCODE -ne 0)

if (-not $hasStagedChanges) {
    Write-Host "No staged changes found. Nothing to push." -ForegroundColor Yellow
    exit 0
}

# Temporarily allow commit to main during the commit/push operation.
$env:GIT_ALLOW_MAIN_COMMIT = 1
Write-Host "Committing and pushing to branch '$Branch'..." -ForegroundColor Cyan

try {
    & git commit -m $CommitMessage
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Commit failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }

    & git push origin $Branch
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Push failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }

    Write-Host "Push completed successfully. GitHub Actions will publish the site." -ForegroundColor Green
}
finally {
    # Leave the variable in the requested state.
    $env:GIT_ALLOW_MAIN_COMMIT = 0
}
