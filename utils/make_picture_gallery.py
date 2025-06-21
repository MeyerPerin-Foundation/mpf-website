from collections import defaultdict
from pathlib import Path
from datetime import datetime
import html
import textwrap
from azure.cosmos import CosmosClient
import random
from dotenv import load_dotenv
import os

load_dotenv()


PAGE_DIR = Path("galleries")
PAGE_DIR.mkdir(parents=True, exist_ok=True)

endpoint = os.getenv("MPFU_COSMOS_ENDPOINT")
key = os.getenv("MPFU_COSMOS_KEY")

client = CosmosClient(endpoint, key)
database = client.get_database_client("media")
container = database.get_container_client("photography")

# ──────────── 1. Query the database for all images ───────────────────────────
query = "SELECT * FROM c WHERE IS_DEFINED(c.content_variant.gallery_slug) " \
        "AND IS_DEFINED(c.content_variant.web_quality_url) AND IS_DEFINED(c.content_variant.thumbnail_url) " \
        "AND IS_DEFINED(c.content_variant.gallery_name) AND IS_DEFINED(c.content_variant.short_description) " \
        "AND c.content_variant.type = 'photography'"
records = list(container.query_items(query=query, enable_cross_partition_query=True))

print(f"Found {len(records)} images for galleries in the database.")

groups = defaultdict(list)
for rec in records:
    groups[rec["content_variant"]["gallery_slug"]].append(rec)

CSS_BLOCK = textwrap.dedent("""
    <style>
      .image-row{display:flex;align-items:flex-start;gap:1rem;margin:1rem 0;}
      .image-row img{max-width:300px;height:auto;flex-shrink:0;}
      .image-row .caption{max-width:42rem;}
    </style>
""").strip()

def row_block(thumb, full, caption):
    """
    thumbnail (left) wrapped in a link → lightbox
    short caption (right) in a div
    long caption in the lightbox title
    """
    cap_full = caption.strip()
    cap_full = cap_full.replace('"', '&quot;')  # escape quotes for HTML
    return (
        f"::: {{.image-row}}\n"
        # 1️⃣  .lightbox on the <img>, alt = long caption
        f"[![{cap_full}]({thumb}){{.lightbox title=\"{cap_full}\" alt=\"{cap_full}\"}}]({full})\n"
        #       ^---------- alt ---------------^
        f"<div class=\"caption\">{html.escape(cap_full)}</div>\n"
        f":::\n"
    )

def gallery_page(title, images):
    # find a pattern of the form (YYYY-MM-DD) in the title
    gallery_date = ""
    for part in title.split():
        if part.startswith("(") and part.endswith(")"):
            gallery_date = part
            break

    title = title.split("(")[0].strip()  # remove the date part from the title


    # remove the parenthesis from the date
    gallery_date = gallery_date.replace("(", "").replace(")", "")
    subtitle = gallery_date
    
    # use a random image for the thumbnail between 0 and n_img - 1
    n_img = len(images)
    img_url = images[random.randint(0, n_img - 1)]["content_variant"]["thumbnail_url"]  # select a random image

    # if title has - replace it with a space
    title = title.replace("-", " ")

    """compose the full .qmd string"""
    front_matter = textwrap.dedent(f"""\
        ---
        title: "{title}"
        date: {gallery_date}
        subtitle: "{subtitle}"
        image: {img_url}
        author: "Lucas A. Meyer"
        lightbox: true
        include-in-header:
          - text: |
              {CSS_BLOCK.replace('\n', '\n'+' ' * 14)}
        ---
        """)
    

    body = "\n\n".join(
        row_block(img["content_variant"]["thumbnail_url"], img["content_variant"]["web_quality_url"], img["content_variant"]["short_description"])
        for img in images
    )
    return front_matter + "\n\n" + body + "\n"


for slug, imgs in groups.items():
    page = gallery_page(imgs[0]["content_variant"]["gallery_name"], imgs)
    (PAGE_DIR / f"{slug}.qmd").write_text(page, encoding="utf-8")
    print("wrote", slug + ".qmd")

print(f"✅  Generated {len(groups)} gallery pages in '{PAGE_DIR}/'")

# ──────────── 6. Index page (cards for every gallery) ─────────────────────────
index_md = textwrap.dedent("""\
    ---
    title: "Photo Galleries"
    listing:
      contents: galleries
      type: grid
      grid-columns: 3
      fields: [title, date, author, image]
      sort: date
                           
    ---
    My photography galleries
    """)
(Path("galleries.qmd")).write_text(index_md, encoding="utf-8")

