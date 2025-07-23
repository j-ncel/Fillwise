import numpy as np
from PIL import Image
from typing import List, Tuple


def compute_vertical_cutoffs(height: int, percentages: List[float]) -> List[int]:
    return [int(height * sum(percentages[:i + 1])) for i in range(len(percentages))]


def vertical_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, cutoffs: List[int], colors: List[str]) -> np.ndarray:
    fill = np.zeros((mask_shape[0], mask_shape[1], 3), dtype=np.uint8)
    for y, x in visible_coords:
        for i, cutoff in enumerate(cutoffs):
            if y < cutoff:
                fill[y, x] = Image.new(
                    "RGB", (1, 1), colors[i]).getpixel((0, 0))
                break
    return fill


def compute_horizontal_cutoffs(width: int, percentages: List[float]) -> List[int]:
    return [int(width * sum(percentages[:i + 1])) for i in range(len(percentages))]


def horizontal_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, cutoffs: List[int], colors: List[str]) -> np.ndarray:
    fill = np.zeros((mask_shape[0], mask_shape[1], 3), dtype=np.uint8)
    for y, x in visible_coords:
        for i, cutoff in enumerate(cutoffs):
            if x < cutoff:
                fill[y, x] = Image.new(
                    "RGB", (1, 1), colors[i]).getpixel((0, 0))
                break
    return fill


def radial_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, percentages: List[float], colors: List[str]) -> np.ndarray:
    fill = np.zeros((mask_shape[0], mask_shape[1], 3), dtype=np.uint8)
    center_y, center_x = mask_shape[0] // 2, mask_shape[1] // 2

    distances = np.array([
        np.sqrt((y - center_y) ** 2 + (x - center_x) ** 2)
        for y, x in visible_coords
    ])
    max_distance = distances.max()

    cutoffs = [max_distance * sum(percentages[:i + 1])
               for i in range(len(percentages))]

    for idx, (y, x) in enumerate(visible_coords):
        d = distances[idx]
        for i, cutoff in enumerate(cutoffs):
            if d < cutoff:
                fill[y, x] = Image.new(
                    "RGB", (1, 1), colors[i]).getpixel((0, 0))
                break
    return fill
