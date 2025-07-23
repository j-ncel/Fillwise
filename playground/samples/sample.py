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
