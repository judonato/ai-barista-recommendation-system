import pandas as pd

def load_sales_data():

    df = pd.read_csv("data/coffee_sales_clean.csv")

    return df


def top_products_by_period(df):

    sales = (
        df.groupby(["period","product_type"])["transaction_qty"]
        .sum()
        .reset_index()
    )

    top10 = (
        sales
        .sort_values(["period","transaction_qty"], ascending=[True, False])
        .groupby("period")
        .head(10)
    )

    return top10
