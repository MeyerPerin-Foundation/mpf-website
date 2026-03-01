---
applyTo: "posts/**/*.qmd"
---
# Post authoring standards for this Quarto website

Use this file for writing or editing blog posts in `posts/`.

## Front matter

- Match existing post front matter patterns unless a post explicitly needs different metadata.
- Keep these common keys for new posts: `title`, `author`, `date`, `draft`, `image`, `include-in-header`, `page-layout`, `toc`, and `toc-expand`.
- Preserve wrappers and instrumentation used by existing posts (for example `<article data-clarity-region="article">`).

## Voice and structure

- Prefer first-person voice with practical examples and concrete anecdotes.
- Open with a clear hook in the first 1-3 paragraphs before deep background.
- Use short, descriptive section headings (`## ...`) to break long posts into readable chunks.
- Prefer direct, plain language over academic or overly formal prose.

## Content conventions

- Include links to prior related posts when context exists.
- Keep conclusions actionable: summarize the takeaway and what the reader should do or consider.
- Preserve existing callout style (`::: {.callout-note}`, `::: {.callout-important}`) when caution/disclaimer text is needed.
- Avoid broad rewrites of existing voice unless explicitly requested.
