from collections import defaultdict
from pathlib import Path
from datetime import datetime
import html
import textwrap
from mpfutils.cosmosdb import CosmosDBContainer
import random

PAGE_DIR = Path("galleries")
PAGE_DIR.mkdir(parents=True, exist_ok=True)

cdb = CosmosDBContainer("content", "themed_folders")
records = cdb.run_query("SELECT * FROM c WHERE c.folder_name = 'photography'")

for r in records:
    # path element 7 = "YYYY_MM_DD_folder_name"
    tokens = r["blob_url"].split("/")[7].split("_")
    yyyy, mm, dd, *name_parts = tokens
    date_iso  = f"{yyyy}-{mm}-{dd}"
    date_text = datetime.strptime(date_iso, "%Y-%m-%d").strftime("%B %d, %Y")

    folder_raw  = " ".join(name_parts)
    slug_root   = "ccr" if folder_raw == "Fulshear" else folder_raw.lower().replace(" ", "-")
    r["slug"]   = f"{slug_root}-{date_iso}"
    r["title"]  = f"{'Cross Creek Ranch — Fulshear, TX' if folder_raw=='Fulshear' else folder_raw} — ({date_text})"

groups = defaultdict(list)
for rec in records:
    groups[rec["slug"]].append(rec)

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
    cap_full   = html.escape(" ".join(caption.split()))    # no  newlines/quotes

    return (
        f"::: {{.image-row}}\n"
        # 1️⃣  .lightbox on the <img>, alt = long caption
        f"[![{cap_full}]({thumb}){{.lightbox title=\"{cap_full}\" alt=\"{cap_full}\"}}]({full})\n"
        #       ^---------- alt ---------------^
        f"<div class=\"caption\">{html.escape(cap_full)}</div>\n"
        f":::\n"
    )

def gallery_page(title, images):
    # break off the date from the title, it will be the last part of the title
    gallery_date = title.split(" — ")[-1]

    # remove the date from the title, it will be in the front matter
    title = title.replace(" — " + gallery_date, "")

    # remove the parenthesis from the date
    gallery_date = gallery_date.replace("(", "").replace(")", "")

    # date is in the format "Month Day, Year"
    # convert to ISO format YYYY-MM-DD
    gallery_date = datetime.strptime(gallery_date, "%B %d, %Y").strftime("%Y-%m-%d")
    
    # if the title still has a —, break off a subtitle
    if " — " in title:
        title, subtitle = title.split(" — ", 1)
        title = f"{title}"
    else:
        subtitle = ""

    # use a random image for the thumbnail between 0 and n_img - 1
    n_img = len(images)
    img_url = images[random.randint(0, n_img - 1)]["thumbnail_blob_url"]  # select a random image

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
        row_block(img["thumbnail_blob_url"], img["blob_url"], img.get("text", ""))
        for img in images
    )
    return front_matter + "\n\n" + body + "\n"


for slug, imgs in groups.items():
    page = gallery_page(imgs[0]["title"], imgs)
    (PAGE_DIR / f"{slug}.qmd").write_text(page, encoding="utf-8")
    print("wrote", slug + ".qmd")
    for img in imgs:
        # add a field to the image with the gallery url
        img["gallery_url"] = f"https://www.meyerperin.org/galleries/{slug}.html"
        img["urls"]=[f"https://www.meyerperin.org/galleries/{slug}.html"]
        img["url_titles"]=["🖼️: Gallery"]
        # update the database
        cdb.upsert_item(img)

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

