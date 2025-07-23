import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from fillwise import Fillwise


# Create DataFrame
df = pd.DataFrame({
    "Food": ["Berries", "Apples", "Thunder Candy"],
    "Votes": [20, 35, 45]
})

# Initialize Fillwise
viz = Fillwise(df, mask_path="a.png", fill_style="vertical")

# Render the image
image_array = viz.render()

# Prepare legend entries
legend_elements = [
    Patch(facecolor=color, label=f"{label}: {round(p * 100)}%")
    for label, p, color in zip(viz.labels, viz.percentages, viz.colors)
]

# Display using matplotlib
plt.figure(figsize=(6, 6))
plt.imshow(image_array)
plt.title("Food Popularity Fillwise Visualization", fontsize=14)
plt.legend(handles=legend_elements, loc="upper right", frameon=True)
plt.show()
