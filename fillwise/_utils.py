import colorsys
import numpy as np
from PIL import Image
from typing import List, Tuple, Union

import pandas as pd

from fillwise._styles import compute_horizontal_cutoffs, compute_vertical_cutoffs


def normalize_proportions(counts: List[int]) -> List[float]:
    total = sum(counts)
    return [count / total for count in counts]


def load_mask_image(path: str, threshold: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    image = Image.open(path).convert("RGBA")
    array = np.array(image)
    alpha = array[..., 3]
    visible = alpha > threshold
    return array, visible, alpha


def generate_default_colors(n: int) -> List[str]:
    base_colors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
        "#F67019", "#C9CBCF", "#8B0000", "#228B22", "#DAA520"
    ]

    if n <= len(base_colors):
        return base_colors[:n]

    hues = np.linspace(0, 1, n, endpoint=False)
    saturation = 0.6
    value = 0.9

    generated = [
        f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        for h in hues
        for r, g, b in [colorsys.hsv_to_rgb(h, saturation, value)]
    ]

    return generated[:n]


def extract_labels_and_counts(data: Union[pd.DataFrame, List[Tuple[str, Union[int, float]]]]) -> Tuple[List[str], List[Union[int, float]]]:
    if data is None:
        raise ValueError(
            "Data must be provided as a list of (label, count) tuples or a DataFrame")

    if hasattr(data, "iloc"):
        labels = data.iloc[:, 0].tolist()
        counts = data.iloc[:, 1].tolist()
    else:
        labels, counts = zip(*data)

    return list(labels), list(counts)


def validate_colors(colors: List[str], num_labels: int) -> List[str]:
    if colors is None:
        colors = generate_default_colors(num_labels)

    if len(colors) < num_labels:
        raise ValueError(
            f"Not enough colors provided for {num_labels} groups.")

    return colors


def compute_cutoffs(fill_style: str, shape: Tuple[int, int], percentages: List[float]) -> Union[List[int], None]:
    if fill_style == "vertical":
        return compute_vertical_cutoffs(shape[0], percentages)
    elif fill_style == "horizontal":
        return compute_horizontal_cutoffs(shape[1], percentages)
    return None


def array_to_image(image_array: np.ndarray) -> Image.Image:
    if image_array.dtype != np.uint8:
        image_array = (image_array * 255).astype(
            np.uint8) if image_array.max() <= 1 else image_array.astype(np.uint8)

    return Image.fromarray(image_array)
