from typing import List


def get_article_text(blocks: List) -> str:
    texts = []
    last_label = None
    for block in blocks:
        for textract_block in sorted(block["ocr_blocks"], key=lambda s: s["Geometry"]["BoundingBox"]["Top"]):
            if textract_block["BlockType"] != "LINE":
                continue
            if block["label"] != last_label:
                texts.append("")
                last_label = block["label"]
            text = textract_block["Text"].rstrip()
            if text[-1] in "-\xad":
                text = text[:-1]
            elif text[-1] != " ":
                text += " "
            texts[-1] += text
    return "\n\n".join(texts)
