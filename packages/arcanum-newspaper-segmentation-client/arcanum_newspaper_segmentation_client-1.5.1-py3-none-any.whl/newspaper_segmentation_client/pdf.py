from typing import Dict, Tuple

import numpy as np
import fitz


def render_pdf_page(page: fitz.Page, dpi: int = 150) -> np.ndarray:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, annots=False, alpha=False)
    image = np.array(bytearray(pix.samples), dtype=np.uint8)
    return np.reshape(image, (pix.height, pix.width, 3))


def bbox_to_textract_bounding_box(bbox: Tuple[float, float, float, float], image_box) -> Dict:
    left = min(max(0.0, (bbox[0] - image_box[0]) / (image_box[2] - image_box[0])), 1.0)
    top = min(max(0.0, (bbox[1] - image_box[1]) / (image_box[3] - image_box[1])), 1.0)
    right = min(max(0.0, (bbox[2] - image_box[0]) / (image_box[2] - image_box[0])), 1.0)
    bottom = min(max(0.0, (bbox[3] - image_box[1]) / (image_box[3] - image_box[1])), 1.0)
    return {'Width': right - left, 'Height': bottom - top, 'Left': left, 'Top': top}


def extract_pdf_text_to_textract_format(page: fitz.Page) -> Dict:
    pdf_text_textract_format = {
        'Rotation': 0.0,
        'Blocks': [{
            'BlockType': 'PAGE',
            'Text': '',
            'Id': '1',
            'Geometry': {
                'BoundingBox': {"Width": 1.0, "Height": 1.0, "Top": 0.0, "Left": 0.0}
            }
        }]
    }
    text_page_flags = fitz.TEXT_INHIBIT_SPACES | fitz.TEXT_PRESERVE_WHITESPACE
    page_text = page.get_text("dict", flags=text_page_flags)
    line_id = 2
    line_ids = []
    for block in page_text["blocks"]:
        for line in block["lines"]:
            line_text = "".join(span["text"] for span in line["spans"])
            if not line_text:
                continue
            image_box = page.bound()
            pdf_text_textract_format["Blocks"].append({
                'BlockType': 'LINE',
                'Text': line_text,
                'Id': str(line_id),
                'Geometry': {
                    'BoundingBox': bbox_to_textract_bounding_box(line["bbox"], image_box)
                }
            })
            line_ids.append(str(line_id))
            line_id += 1

    pdf_text_textract_format["Blocks"][0]["Relationships"] = [
        {"Ids": line_ids, "Type": "CHILD"}
    ]

    return pdf_text_textract_format
