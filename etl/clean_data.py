import pandas as pd

def clean_data(input_path, output_path):
    """
    Cleans the data from the input CSV file and saves the cleaned data to the output CSV file.

    Parameters:
    input_path (str): The path to the input CSV file.
    output_path (str): The path to save the cleaned CSV file.
    """
    # Read the data from the input CSV file
    df = pd.read_csv(input_path, encoding='latin-1')  # Specify encoding to handle special characters

    # Perform data cleaning operations
    df = df.dropna()  # Remove rows with missing values
    df = df.drop_duplicates()  # Remove duplicate rows

    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]  # Strip whitespace from column names and replace spaces with underscores

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')  # Convert order_date to datetime
    df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')  # Convert ship_date to datetime


    df=df.dropna(subset=['customer_name', 'product_name'])  # Drop rows where customer_name or product_name is null

    # Save the cleaned data to the output CSV file
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {df.shape}")
    return df

if __name__ == "__main__":
    clean_data("D:/retail-sales-analytics/data/raw/Sample - Superstore.csv", "data/processed/cleaned_data.csv")