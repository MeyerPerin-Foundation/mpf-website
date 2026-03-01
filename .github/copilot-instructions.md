---
applyTo: "**/*"
---
# Project coding standards for this Quarto website

This repository is a Quarto website, not a Python package-first codebase.

## Core principles

- Prioritize content quality and site stability over tool churn.
- Keep changes minimal and targeted to the user request.
- Preserve existing voice, tone, and structure in posts/pages unless asked to rewrite.
- Do not introduce unrelated refactors.

## Quarto content rules (`.qmd`)

- Preserve valid YAML front matter and existing metadata keys.
- Keep paths and links consistent with the current site structure.
- Prefer relative links for internal content when already used.
- Do not remove existing analytics or header includes unless requested.
- When adding new listing/feed behavior, use Quarto-native options in page front matter.

Post-specific writing guidance is maintained in `.github/copilot-posts-instructions.md`.

## Site configuration (`_quarto.yml`)

- Keep `project.type: website` and existing output structure intact.
- Avoid changing global site metadata (title, site-url, analytics, navbar) unless requested.
- If updating feed behavior, ensure it remains compatible with the homepage/listing setup.

## Generated and build artifacts

- Treat `_site/`, `_freeze/`, and `site_libs/` as generated artifacts.
- Prefer editing source files (`.qmd`, `_quarto.yml`, `styles.css`) rather than generated output.
- Only modify generated files when the user explicitly asks.

## Styling (`styles.css`)

- Follow existing design language and avoid broad visual redesigns unless requested.
- Keep CSS changes scoped to the requested feature or fix.

## Publishing workflow

- Publishing is triggered by pushing to `main` via GitHub Actions (`.github/workflows/publish.yml`).
- Local helper script (`publish.ps1`) should stage/commit/push, not bypass CI behavior unless explicitly requested.
- Preserve `GIT_ALLOW_MAIN_COMMIT` safety behavior in `publish.ps1` when modifying publish logic.

## Python usage in this repo

- Use Python only when needed for project dependencies or tooling.
- Avoid package-structure changes unless explicitly requested.
- If creating temporary analysis scripts, place them in `.local/dev_utils`.
- use `uv` for package management

