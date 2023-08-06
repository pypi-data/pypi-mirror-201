from typing import Dict, List, Tuple

from PIL import Image, ImageDraw


def scale_boundary(boundary: List[List[List[Tuple[float, float]]]], scale: Tuple[float, float]) -> None:
    for polygon in boundary:
        for linestring in polygon:
            for point_idx, point in enumerate(linestring):
                linestring[point_idx] = (point[0] * scale[0], point[1] * scale[1])


def clip_article(image: Image, article: Dict):
    alpha_mask = Image.new('L', image.size, 0)
    alpha_mask_draw = ImageDraw.Draw(alpha_mask)
    scale_boundary(article["boundary"], (image.width, image.height))
    for polygon in article["boundary"]:
        alpha_mask_draw.polygon(polygon[0], fill=255, outline=255, width=10)
        for hole in polygon[1:]:
            alpha_mask_draw.polygon(hole, fill=0)
    article_image = image.copy()
    article_image.putalpha(alpha_mask)
    return article_image.crop(alpha_mask.getbbox())
