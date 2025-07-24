import timeit
import os

image_path = os.path.abspath("playground/samples/images/cart.png")

setup = f"""
import numpy as np
import pandas as pd
from fillwise import Fillwise
from fillwise._utils import (
    load_mask_image,
    extract_labels_and_counts,
    normalize_proportions,
    generate_default_colors,
    validate_colors,
    compute_cutoffs,
    array_to_image
)

image_path = r'{image_path}'
data = pd.DataFrame({{"Fruit": ["Apple", "Banana", "Cherry"], "Count": [20, 35, 45]}})
"""


def run_test(label, stmt, setup, number=5):
    time_taken = timeit.timeit(stmt=stmt, setup=setup, number=number)
    print(f"{label}: {time_taken / number:.6f}s")


# --- Individual Function Benchmarks ---
print("\n--- Function Benchmarks ---")

run_test("load_mask_image", "load_mask_image(image_path)", setup)
run_test("extract_labels_and_counts", "extract_labels_and_counts(data)", setup)
run_test("normalize_proportions", "normalize_proportions([20, 35, 45])", setup)
run_test("generate_default_colors", "generate_default_colors(3)", setup)
run_test("validate_colors",
         "validate_colors(['#FF0000', '#00FF00', '#0000FF'], 3)", setup)
run_test("compute_cutoffs",
         "compute_cutoffs('horizontal', (500, 500), [0.2, 0.3, 0.5])", setup)
run_test("Fillwise instantiation",
         "Fillwise(data, image_path=image_path, fill_style='horizontal')", setup)
run_test("Fillwise render",
         "Fillwise(data, image_path=image_path, fill_style='horizontal').render()", setup)
