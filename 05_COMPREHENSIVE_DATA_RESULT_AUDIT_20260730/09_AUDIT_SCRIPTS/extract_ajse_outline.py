import hashlib
import json
import sys
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


def iter_block_items(parent):
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = Document(src)

    blocks = []
    heading_rows = []
    table_rows = []
    paragraph_index = 0
    table_index = 0

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            paragraph_index += 1
            text = block.text.strip()
            style = block.style.name if block.style else ""
            item = {
                "block_type": "paragraph",
                "paragraph_index": paragraph_index,
                "style": style,
                "text": text,
                "has_runs": bool(block.runs),
            }
            blocks.append(item)
            if text and (style.lower().startswith("heading") or style.startswith("标题")):
                heading_rows.append(item)
        else:
            table_index += 1
            rows = []
            for r_idx, row in enumerate(block.rows, start=1):
                values = [cell.text.strip() for cell in row.cells]
                rows.append(values)
                table_rows.append({
                    "table_index": table_index,
                    "row_index": r_idx,
                    "values": values,
                })
            blocks.append({
                "block_type": "table",
                "table_index": table_index,
                "row_count": len(rows),
                "column_count": max((len(r) for r in rows), default=0),
                "rows": rows,
            })

    images = []
    for rel_id, rel in doc.part.rels.items():
        if "image" in rel.reltype:
            part = rel.target_part
            images.append({
                "relationship_id": rel_id,
                "partname": str(part.partname),
                "content_type": part.content_type,
                "size_bytes": len(part.blob),
                "sha256": hashlib.sha256(part.blob).hexdigest(),
            })

    core = doc.core_properties
    result = {
        "source_file": str(src),
        "source_size_bytes": src.stat().st_size,
        "source_sha256": sha256(src),
        "core_properties": {
            "title": core.title,
            "subject": core.subject,
            "author": core.author,
            "keywords": core.keywords,
            "comments": core.comments,
            "created": core.created.isoformat() if core.created else None,
            "modified": core.modified.isoformat() if core.modified else None,
            "last_modified_by": core.last_modified_by,
            "revision": core.revision,
        },
        "section_count": len(doc.sections),
        "paragraph_count": paragraph_index,
        "table_count": table_index,
        "inline_shape_count": len(doc.inline_shapes),
        "image_relationship_count": len(images),
        "headings": heading_rows,
        "tables_flat": table_rows,
        "images": images,
        "blocks": blocks,
    }

    (out_dir / "outline_structure.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = [
        "# Extracted AJSE Phase 2A outline",
        "",
        f"Source: `{src}`",
        f"SHA-256: `{result['source_sha256']}`",
        f"Paragraphs: {paragraph_index}; tables: {table_index}; images: {len(images)}",
        "",
    ]
    for item in blocks:
        if item["block_type"] == "paragraph":
            if not item["text"]:
                continue
            style = item["style"]
            text = item["text"]
            lower = style.lower()
            if lower.startswith("heading"):
                try:
                    level = int(style.split()[-1])
                except Exception:
                    level = 2
                md.append("#" * min(max(level, 1), 6) + " " + text)
            elif style.startswith("标题"):
                md.append("## " + text)
            else:
                md.append(text)
            md.append("")
        else:
            md.append(f"### Table {item['table_index']}")
            md.append("")
            for row in item["rows"]:
                md.append(" | ".join(cell.replace("\n", " / ") for cell in row))
            md.append("")
    (out_dir / "outline_extracted.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps({
        "source_sha256": result["source_sha256"],
        "paragraph_count": paragraph_index,
        "table_count": table_index,
        "image_count": len(images),
        "heading_count": len(heading_rows),
        "output_dir": str(out_dir),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
