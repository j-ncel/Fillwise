import numpy as np
from typing import List, Tuple


def enforce_minimum(percentages: List[float], total: int, min_ratio: float = 0.03) -> List[float]:
    min_pixels = int(total * min_ratio)
    adjusted = [max(p * total, min_pixels) for p in percentages]
    total_adjusted = sum(adjusted)
    return [p / total_adjusted for p in adjusted]


def compute_vertical_cutoffs(height: int, percentages: List[float]) -> List[int]:
    adjusted = enforce_minimum(percentages, height)
    return [int(height * sum(adjusted[:i + 1])) for i in range(len(adjusted))]


def compute_horizontal_cutoffs(width: int, percentages: List[float]) -> List[int]:
    adjusted = enforce_minimum(percentages, width)
    return [int(width * sum(adjusted[:i + 1])) for i in range(len(adjusted))]


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def vertical_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, cutoffs: List[int], colors: List[str]) -> np.ndarray:
    fill = np.zeros((*mask_shape, 3), dtype=np.uint8)
    rgb_colors = [hex_to_rgb(c) for c in colors]
    for y, x in visible_coords:
        for i, cutoff in enumerate(cutoffs):
            if y < cutoff:
                fill[y, x] = rgb_colors[i]
                break
    return fill


def horizontal_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, cutoffs: List[int], colors: List[str]) -> np.ndarray:
    fill = np.zeros((*mask_shape, 3), dtype=np.uint8)
    rgb_colors = [hex_to_rgb(c) for c in colors]
    for y, x in visible_coords:
        for i, cutoff in enumerate(cutoffs):
            if x < cutoff:
                fill[y, x] = rgb_colors[i]
                break
    return fill


def radial_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, percentages: List[float], colors: List[str]) -> np.ndarray:
    fill = np.zeros((*mask_shape, 3), dtype=np.uint8)
    center_y, center_x = mask_shape[0] // 2, mask_shape[1] // 2
    coords = np.array(visible_coords)
    dy = coords[:, 0] - center_y
    dx = coords[:, 1] - center_x
    distances = np.sqrt(dy**2 + dx**2)
    max_distance = distances.max()
    adjusted = enforce_minimum(percentages, total=max_distance)
    cutoffs = [max_distance * sum(adjusted[:i + 1])
               for i in range(len(adjusted))]
    rgb_colors = [hex_to_rgb(c) for c in colors]
    for idx, (y, x) in enumerate(visible_coords):
        d = distances[idx]
        for i, cutoff in enumerate(cutoffs):
            if d < cutoff:
                fill[y, x] = rgb_colors[i]
                break
    return fill
