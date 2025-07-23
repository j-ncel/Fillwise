import os
import pandas as pd
from fillwise import Fillwise

# Sample data
df = pd.DataFrame({
    "Fruits": ["Apple", "Banana", "Cherry"],
    "Counts": [20, 35, 45]
})
image_path = os.path.join(os.path.dirname(__file__), "images/cart.png")

# Usage of Fillwise
fw = Fillwise(df, image_path=image_path, fill_style="horizontal")

# Save
fw.save("cart_output.png")

# Display using system default image viewer
fw.show()
