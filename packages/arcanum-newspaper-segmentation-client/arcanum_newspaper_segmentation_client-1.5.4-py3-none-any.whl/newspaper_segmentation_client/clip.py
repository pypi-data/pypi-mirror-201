from typing import Dict, List, Tuple

from PIL import Image, ImageDraw


def scale_boundary(boundary: List[List[List[Tuple[float, float]]]], scale: Tuple[float, float]) -> None:
    for polygon in boundary:
        for linestring in polygon:
            for point_idx, point in enumerate(linestring):
                linestring[point_idx] = (point[0] * scale[0], point[1] * scale[1])


def clip_article(image: Image, article: Dict, margin: int = 10):
    alpha_mask = Image.new('L', image.size, 0)
    alpha_mask_draw = ImageDraw.Draw(alpha_mask)
    scale_boundary(article["boundary"], (image.width, image.height))
    for polygon in article["boundary"]:
        alpha_mask_draw.polygon(polygon[0], fill=255)
        for point_idx in range(len(polygon[0])):
            point0, point1 = (polygon[0][point_idx], polygon[0][(point_idx + 1) % len(polygon[0])])
            x_min = min(int(point0[0]), int(point1[0])) - margin
            x_max = max(int(point0[0]), int(point1[0])) + margin
            y_min = min(int(point0[1]), int(point1[1])) - margin
            y_max = max(int(point0[1]), int(point1[1])) + margin
            alpha_mask_draw.rectangle((x_min, y_min, x_max, y_max), fill=255)
        for hole in polygon[1:]:
            alpha_mask_draw.polygon(hole, fill=0)
    article_image = image.copy()
    article_image.putalpha(alpha_mask)
    return article_image.crop(alpha_mask.getbbox())
