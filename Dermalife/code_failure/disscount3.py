import pandas as pd
import csv

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


def save_to_csv_formatted(discount_lists, output_path):
    # Convert the dictionary to a formatted DataFrame
    rows = []
    for discount, skus in discount_lists.items():
        # Convert SKUs to string and format with "SKU"
        sku_list_str = ", ".join([f'"{sku}"' for sku in map(str, skus)])
        rows.append({"Discount": f"{discount*100:.1f}%;", "SKUs": f"[{sku_list_str}]"})
    df_output = pd.DataFrame(rows)

    # Save the DataFrame to CSV without additional quoting
    df_output.to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="ISO-8859-1",
        quoting=csv.QUOTE_NONE,
        escapechar="\\",
    )


# Execute the function and store results
discount_lists = process_csv(file_path)

# Save results to result.csv in the desired format
save_to_csv_formatted(discount_lists, "result.csv")

# Print the results
for discount, skus in discount_lists.items():
    print(f"Discount: {discount*100}%")
    print(f"SKUs: {skus}\n")
