import pandas as pd
import csv


def process_csv_with_discounts(file_path):
    """
    Reads the provided CSV file, extracts SKUs, and returns a dictionary with SKUs grouped by discount.
    """
    df = pd.read_csv(file_path, sep=";", encoding="ISO-8859-1", dtype={"SKU ": str})
    
    # Grouping SKUs by the "DESCUENTO" column
    grouped = df.groupby("DESCUENTO")["SKU "].apply(list).to_dict()
    
    return grouped


def save_to_csv_formatted_corrected(discount_lists, output_path):
    """
    Saves the processed SKU data to a formatted CSV file.
    """
    rows = []
    for discount, skus in discount_lists.items():
        sku_list_str = ",".join([f'"{sku}"' for sku in skus])
        formatted_string = f'{{"1":{{"type":"product_sku","method":"in_list","value":[{sku_list_str}],"product_variants":[]}}}}'
        # formatted_string = f'{{{"type":"product_sku","method":"in_list","value":[{sku_list_str}],"product_variants":[]}}}'
        rows.append({"Formatted": formatted_string})
    df_output = pd.DataFrame(rows)
    df_output.to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="ISO-8859-1",
        quoting=csv.QUOTE_NONE,
        escapechar="\\",
    )


if __name__ == "__main__":
    # Paths for input and output CSV files
    input_path = "./listado_sku.csv"
    output_path = "./resultado2_sku.csv"
    
    # Process the input file and save the results to the output file
    discount_data = process_csv_with_discounts(input_path)
    # Print the discounts and their associated SKUs
    for discount in discount_data.keys():
        print(f"Discount: {discount}")
    save_to_csv_formatted_corrected(discount_data, output_path)
