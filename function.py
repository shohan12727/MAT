import numpy as np
import matplotlib.pyplot as plt

# Define domain: x >= 3/2
x = np.linspace(1.5, 100, 500)

# Define function
y = 1 - np.sqrt(2 * x - 3)

# Plot function
plt.figure(figsize=(8, 5))
plt.plot(x, y, label=r"$y = 1 - \sqrt{2x - 3}$")

# Domain boundary
plt.axvline(1.5, linestyle="--", linewidth=1, label="Domain start (x = 1.5)")

# Range boundary
plt.axhline(1, linestyle="--", linewidth=1, label="Maximum y = 1")

# Labels and grid
plt.xlabel("x")
plt.ylabel("y")
plt.title("Graph of y = 1 - √(2x - 3)")
plt.legend()
plt.grid(True)

plt.show()
