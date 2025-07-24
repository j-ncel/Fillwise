import numpy as np
from typing import List, Tuple


def enforce_minimum(percentages: List[float], total: int, min_ratio: float = 0.03) -> List[float]:
    min_pixels = int(total * min_ratio)
    adjusted = [max(p * total, min_pixels) for p in percentages]
    total_adjusted = sum(adjusted)
    return [p / total_adjusted for p in adjusted]


def compute_vertical_cutoffs(height: int, percentages: List[float]) -> List[int]:
    adjusted = enforce_minimum(percentages, height)
    scaled = np.array(adjusted) * height
    return np.cumsum(scaled).astype(int).tolist()


def compute_horizontal_cutoffs(width: int, percentages: List[float]) -> List[int]:
    adjusted = enforce_minimum(percentages, width)
    scaled = np.array(adjusted) * width
    return np.cumsum(scaled).astype(int).tolist()


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def vertical_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, cutoffs: List[int], colors: List[str]) -> np.ndarray:
    fill = np.zeros((*mask_shape, 3), dtype=np.uint8)
    rgb_colors = np.array([hex_to_rgb(c) for c in colors], dtype=np.uint8)

    y_coords = visible_coords[:, 0]
    indices = np.searchsorted(cutoffs, y_coords, side="right")
    valid = indices < len(rgb_colors)

    fill[visible_coords[valid, 0], visible_coords[valid, 1]
         ] = rgb_colors[indices[valid]]
    return fill


def horizontal_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, cutoffs: List[int], colors: List[str]) -> np.ndarray:
    fill = np.zeros((*mask_shape, 3), dtype=np.uint8)
    rgb_colors = np.array([hex_to_rgb(c) for c in colors], dtype=np.uint8)

    x_coords = visible_coords[:, 1]
    indices = np.searchsorted(cutoffs, x_coords, side="right")
    valid = indices < len(rgb_colors)

    fill[visible_coords[valid, 0], visible_coords[valid, 1]
         ] = rgb_colors[indices[valid]]
    return fill


def radial_fill(mask_shape: Tuple[int, int], visible_coords: np.ndarray, percentages: List[float], colors: List[str]) -> np.ndarray:
    fill = np.zeros((*mask_shape, 3), dtype=np.uint8)
    center = np.array(mask_shape) // 2
    coords = np.array(visible_coords)
    distances = np.linalg.norm(
        coords - center[::-1], axis=1)  # reverse for (x,y)

    max_distance = distances.max()
    adjusted = enforce_minimum(percentages, total=max_distance)
    cutoffs = np.cumsum(np.array(adjusted) * max_distance)
    rgb_colors = np.array([hex_to_rgb(c) for c in colors], dtype=np.uint8)

    indices = np.searchsorted(cutoffs, distances, side="right")
    valid = indices < len(rgb_colors)
    fill[coords[valid, 0], coords[valid, 1]] = rgb_colors[indices[valid]]
    return fill
