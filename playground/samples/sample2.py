import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from fillwise import Fillwise

# Sample data
df = pd.DataFrame({
    "Genre": ["RPG", "Shooter", "Puzzle", "Sports", "Adventure"],
    "Votes": [40, 25, 20, 15, 10]
})


image_path = os.path.join(os.path.dirname(__file__), "images/gamepad.png")

# Usage of Fillwise
fw = Fillwise(df, image_path=image_path, fill_style="radial")
image = fw.render()

# Sample Plotting
fig, ax = plt.subplots()
ax.imshow(image)
ax.axis("off")

patches = [mpatches.Patch(color=color, label=label)
           for color, label in zip(fw.colors, fw.labels)]
ax.set_title("Game Genre Preferences",
             fontweight='bold', fontsize=16)
ax.legend(handles=patches, loc="center left", bbox_to_anchor=(1, 0.5),
          frameon=True)

plt.tight_layout()
plt.show()
