import argparse
import pandas as pd

# TO RUN: python "datasets\CleanData\remove_empty.py" "datasets\PCParts\pcpart.csv" "datasets\PCParts\pc_clean.csv" "column_name"

def cleanup_csv(input_path: str, output_path: str, column: str) -> None:
    # Read a CSV, remove rows with empty values in the given column, then output cleaned CSV
    # Load the input CSV file into a pandas DataFrame.
    df = pd.read_csv(input_path)

    # Ensure the requested column exists
    if column not in df.columns:
        raise ValueError(f"Column {column!r} not found in input CSV")

    # Filter rows where the column value is neither NaN nor blank after stripping whitespace.
    cleaned = df[df[column].notna() & df[column].astype(str).str.strip().ne("")]

    # Write the filtered DataFrame back out to a new CSV file.
    cleaned.to_csv(output_path, index=False)


def main() -> None:
    # Parse command-line arguments and run the CSV cleanup process
    parser = argparse.ArgumentParser(
        description="Clean CSV by dropping rows with empty values in a specific column."
    )
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("column", help="Column name to check for empty rows")
    args = parser.parse_args()

    # Call the cleanup function with the parsed arguments.
    cleanup_csv(args.input_csv, args.output_csv, args.column)


if __name__ == "__main__":
    # Only execute the script when run directly, not when imported.
    main()
