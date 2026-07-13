import argparse
import pandas as pd


# TO RUN:
# python "datasets\CleanData\remove_duplicates.py" "input.csv" "output.csv" "Column Name"

# Removes duplicate rows based on specified column while preserving the first occurrence.
def remove_duplicates(input_csv, output_csv, column):
    df = pd.read_csv(input_csv)

    # Verify the column exists
    if column not in df.columns:
        print(f"Error: Column '{column}' not found.")
        print("Available columns:")
        for col in df.columns:
            print(f"  - {col}")
        return

    before = len(df)

    df = df.drop_duplicates(
        subset=[column],
        keep="first"
    )

    after = len(df)

    print(f"Removed {before - after} duplicate rows.")
    print(f"Remaining rows: {after}")

    df.to_csv(output_csv, index=False)

    print(f"Saved cleaned CSV to '{output_csv}'.")


def main():

    parser = argparse.ArgumentParser(
        description="Remove duplicate rows from a CSV based on a specified column."
    )

    parser.add_argument(
        "input_csv",
        help="Path to the input CSV file"
    )

    parser.add_argument(
        "output_csv",
        help="Path to the output CSV file"
    )

    parser.add_argument(
        "column",
        help="Column name to remove duplicates on"
    )

    args = parser.parse_args()

    remove_duplicates(
        args.input_csv,
        args.output_csv,
        args.column
    )


if __name__ == "__main__":
    main()