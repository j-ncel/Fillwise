# Fillwise <img src="assets/icon.png" width="50" alt="Fillwise Icon">

**Visualize group data by filling images with color proportions.**

Fillwise is a Python module for visualizing group data by filling images with color proportions. It can be used for custom charts, data art, and creative data storytelling.

---

## Usage

```bash
pip install fillwise
```

```python
import pandas as pd
from fillwise import Fillwise

# Sample data
df = pd.DataFrame({
    "Fruits": ["Apple", "Banana", "Cherry"],
    "Counts": [20, 35, 45]
})

# Usage of Fillwise
fw = Fillwise(df, mask_path="cart.png", fill_style="horizontal")

# Save
fw.save("output.png")

# Display using system default image viewer
fw.show()
```

| Before                                                                  | After                                                                         |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| <img src="playground/samples/images/cart.png" width="250" alt="Before"> | <img src="playground/samples/images/cart_output.png" width="250" alt="After"> |

_Sample image credit from [UXWing](https://uxwing.com/cart-black-icon/)_.
_The data presented here are made-up only._

## Fillwise Output with Matplotlib

```python
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
```

<img src="playground/samples/images/gamepad_output.png" width="500" alt="Matplotlib Sample">

_Sample image credit from [UXWing](https://uxwing.com/gamepad-icon/)_.
_The data presented here are made-up only._

## Fill Styles

Fillwise supports multiple fill styles to suit different image shapes and storytelling needs:

| Style        | Description                   | Best For               |
| ------------ | ----------------------------- | ---------------------- |
| `horizontal` | Fills left to right           | Wide images like carts |
| `vertical`   | Fills top to bottom           | Tall silhouettes       |
| `radial`     | Fills outward from the center | Symmetrical shapes     |

You can switch styles by setting `fill_style="..."` when creating a Fillwise instance.

## Image Masks

You can use any transparent PNG image as a mask. Fillwise fills only the visible (non-transparent) pixels.

```python
fw = Fillwise(df, image_path="your_mask.png", fill_style="horizontal")
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Attribution

Images used in examples are credited to [UXWing](https://uxwing.com).
