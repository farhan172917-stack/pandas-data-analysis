
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
df = pd.read_csv("data/sales_data.csv")
print("Original rows:", len(df))

# Clean dataset
df = df.drop_duplicates()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

df = df.dropna(
    subset=["Date", "Product", "Category",
            "Quantity", "Price", "City"]
)
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# Group and summarize
product_sales = df.groupby("Product")["Revenue"].sum()
category_sales = df.groupby("Category")["Revenue"].sum()
city_sales = df.groupby("City")["Revenue"].sum()

# Display insights
print("\nCLEANED DATA")
print(df.to_string(index=False))

print("\nSUMMARY STATISTICS")
print(df[["Quantity", "Price", "Revenue"]].describe())

print("\nPRODUCT REVENUE")
print(product_sales.sort_values(ascending=False))

print("\nCATEGORY REVENUE")
print(category_sales)

print("\nCITY REVENUE")
print(city_sales)

print(f"\nTotal revenue: Rs. {df['Revenue'].sum():,.2f}")
print(f"Units sold: {df['Quantity'].sum():.0f}")
print(f"Top product: {product_sales.idxmax()}")
print(f"Top city: {city_sales.idxmax()}")

# Save results
df.to_csv("cleaned_sales_data.csv", index=False)
product_sales.to_csv("product_sales_summary.csv")

# Create graph
product_sales.sort_values(ascending=False).plot(
    kind="bar", title="Revenue by Product"
)
plt.xlabel("Product")
plt.ylabel("Revenue (INR)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.close()

print("\nAnalysis completed successfully!")
