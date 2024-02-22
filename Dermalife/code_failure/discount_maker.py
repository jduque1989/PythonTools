import pandas as pd


def create_detailed_discount(title, sku, start_date, end_date):
    # Create the 'filters' column based on the SKU provided
    filter_value = (
        f'{{"1":{{"type":"product_sku","method":"in_list","value":["{sku}"]}}}}'
    )

    # Default/placeholder values for other columns
    default_values = {
        "id": 999,  # Placeholder ID
        "enabled": 1,
        "deleted": 0,
        "exclusive": 0,
        "priority": 1,
        "apply_to": 0,
        "conditions": "",
        "product_adjustments": "",
        "cart_adjustments": "",
        "buy_x_get_x_adjustments": "",
        "buy_x_get_y_adjustments": "",
        "bulk_adjustments": "",
        "set_adjustments": "",
        "other_discounts": "",
        "date_from": start_date,
        "date_to": end_date,
        "usage_limits": "",
        "rule_language": "",
        "used_limits": 0,
        "additional": "",
        "max_discount_sum": 0,
        "advanced_discount_message": "",
        "discount_type": "",
        "used_coupons": "",
        "created_by": 1,
        "created_on": start_date,
        "modified_by": 1,
        "modified_on": end_date,
    }

    # Create a new DataFrame with the necessary columns and values
    new_discount = pd.DataFrame(
        {"title": [title], "filters": [filter_value], **default_values}
    )

    return new_discount


# Provide the required values for title, sku, start_date, and end_date
title = "Sample Discount"
sku = "SKU12345"
start_date = "2023-10-01"
end_date = "2023-10-31"

new_detailed_discount_df = create_detailed_discount(title, sku, start_date, end_date)

# Write the results to discount_result.csv
new_detailed_discount_df.to_csv("./detailed_discount_result.csv", index=False)

new_detailed_discount_df
