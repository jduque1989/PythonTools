import pandas as pd

file_path = "./ARCHIVO_PRUEBA.csv"


def process_csv(file_path):
    # Read the CSV file with the correct encoding
    df = pd.read_csv(file_path, delimiter=";", encoding="ISO-8859-1")

    # Remove any spaces from column names
    df.columns = df.columns.str.strip()

    # Convert the discount values to numeric form
    df["DESCUENTO"] = df["DESCUENTO"].str.rstrip("%").astype("float") / 100.0

    # Group by discount and collect SKUs for each discount
    discount_skus = {}
    for discount, group in df.groupby("DESCUENTO"):
        discount_skus[discount] = group["SKU"].tolist()

    return discount_skus


# Execute the function and store results
discount_lists = process_csv(file_path)

# Print the results
for discount, skus in discount_lists.items():
    print(f"Discount: {discount*100}%")
    print(f"SKUs: {skus}\n")
