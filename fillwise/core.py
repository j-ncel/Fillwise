import numpy as np
import pandas as pd
from typing import List, Literal, Tuple, Union
from PIL import Image
from ._utils import (
    normalize_proportions,
    load_mask_image,
    extract_labels_and_counts,
    validate_colors,
    compute_cutoffs,
    array_to_image
)
from ._styles import (
    vertical_fill,
    horizontal_fill,
    radial_fill
)


class Fillwise:
    def __init__(
        self,
        data: Union[pd.DataFrame, List[Tuple[str, Union[int, float]]]],
        colors: List[str] = None,
        mask_path: str = None,
        fill_style: Literal["vertical", "horizontal", "radial"] = "vertical",
        threshold: int = 10
    ):
        self.mask_path = mask_path
        self.threshold = threshold
        self.fill_style = fill_style.lower()

        if self.fill_style not in ["vertical", "horizontal", "radial"]:
            raise ValueError(f"Unsupported fill style: {self.fill_style}")
        if mask_path is None:
            raise ValueError("mask_path must be provided")

        # Extract labels and counts
        self.labels, self.counts = extract_labels_and_counts(data)
        self.percentages = normalize_proportions(self.counts)

        # Assign and validate colors
        self.colors = validate_colors(colors, len(self.labels))

        # Load mask and extract visible pixels
        self.mask_array, self.visible_mask, self.alpha_channel = load_mask_image(
            self.mask_path, self.threshold)
        self.visible_coords = np.argwhere(self.visible_mask)

        # Compute cutoffs if needed
        shape = self.mask_array.shape[:2]
        self.cutoffs = compute_cutoffs(
            self.fill_style, shape, self.percentages)

    def render(self) -> np.ndarray:
        shape = self.mask_array.shape[:2]

        if self.fill_style == "vertical":
            fill_array = vertical_fill(
                shape, self.visible_coords, self.cutoffs, self.colors)
        elif self.fill_style == "horizontal":
            fill_array = horizontal_fill(
                shape, self.visible_coords, self.cutoffs, self.colors)
        elif self.fill_style == "radial":
            fill_array = radial_fill(
                shape, self.visible_coords, self.percentages, self.colors)
        else:
            raise ValueError(f"Unsupported fill style: {self.fill_style}")

        return np.dstack((fill_array, self.alpha_channel))

    def save(self, path: str = "output.png", format: str = "PNG") -> None:
        """
        Saves the rendered image to disk.
        Parameters:
            path: File path to save the image (e.g., 'output.png').
            format: Image format (e.g., 'PNG', 'JPEG'). Defaults to 'PNG'.
        """
        image = array_to_image(self.render())
        image.save(path, format=format)
        print(f"Fillwise Image was saved to {path}")

    def show(self) -> None:
        """
        Displays the rendered image using the default image viewer.
        """
        image = array_to_image(self.render())
        image.show()
        print("Image Displayed")
