import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned datasets
gym_csv_path = "clean_gym_locations.csv"
supplement_csv_path = "clean_supplement_store_locations.csv"

gym_df = pd.read_csv(gym_csv_path)
supplement_df = pd.read_csv(supplement_csv_path)

### **1. Scatter Map: Gyms vs Supplement Stores**
plt.figure(figsize=(10, 6))
plt.scatter(gym_df["Longitude"], gym_df["Latitude"], color="blue", label="Gyms", alpha=0.5)
plt.scatter(supplement_df["Longitude"], supplement_df["Latitude"], color="red", label="Supplement Stores", alpha=0.5)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Scatter Map of Gyms and Supplement Stores")
plt.legend()
plt.grid(True)
plt.show()

### **2. Heatmap: Gym & Supplement Store Density**
plt.figure(figsize=(10, 6))
sns.kdeplot(x=gym_df["Longitude"], y=gym_df["Latitude"], cmap="Blues", fill=True, alpha=0.5, label="Gym Density")
sns.kdeplot(x=supplement_df["Longitude"], y=supplement_df["Latitude"], cmap="Reds", fill=True, alpha=0.5, label="Supplement Store Density")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Heatmap of Gyms and Supplement Stores Density")
plt.legend()
plt.show()

