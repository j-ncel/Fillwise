# Fillwise <img src="assets/icon.png" width="50" height="" alt="jncel identimorph">

**Visualize group data by filling images with color proportions.**

Fillwise is a data visualization module that fills images with color proportions based on group data. It supports vertical, horizontal, and radial fill styles, making it useful for custom charts, data art, and creative data storytelling.

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
    "Food": ["Berries", "Apples", "Thunder Candy"],
    "Votes": [20, 35, 45]
})

# Create visualization
viz = Fillwise(df, mask_path="pika.png", fill_style="horizontal")
viz.save("output.png")
viz.show()
```
