import os
import zipfile
import argparse
import pandas as pd


def extract_csv_from_zip(zip_path: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(zip_folder):
        if filename.endswith(".zip"):
            zip_path = os.path.join(zip_folder, filename)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_folder)


def concatenate_csv_files(folder_path: str, output_file: str):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    dataframes = []

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)

        # Filter to only retrieve energy hub data (SettlementPoint contains "HB_")
        df = df[df["SettlementPoint"].str.contains("HB_")]
        dataframes.append(df)

    if dataframes:
        concatenated_df = pd.concat(dataframes, ignore_index=True)
        concatenated_df.to_csv(output_file, index=False)
        print(f"Concatenated CSV saved to: {output_file}")
    else:
        print("No CSV files found to concatenate.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract CSVs from ZIP files in a folder and concatenates when --concatenate is used.")
    parser.add_argument("--zip_folder", required=True, help="Path to the folder containing ZIP files.")
    parser.add_argument("--raw_csv_folder", default=None, help="Path to the output folder for extracted CSVs.")
    parser.add_argument("--concatenate", action="store_true", help="Concatenate extracted CSV files into a single file.")
    parser.add_argument("--output_file", help="Path for the concatenated CSV file (if --concatenate is used).")
    args = parser.parse_args()

    zip_folder = args.zip_folder
    if not os.path.isdir(zip_folder):
        print(f"Error: The specified zip_folder '{zip_folder}' does not exist or is not a directory.")
        exit(1)
    
    if not args.raw_csv_folder:
        raw_csv_folder = os.path.join(args.zip_folder, "extracted_csvs")
    else:
        raw_csv_folder = args.raw_csv_folder

    print(f"Extracting ZIP files from: {zip_folder}")

    extract_csv_from_zip(zip_folder, raw_csv_folder)

    print(f"Extracted CSV files are saved in: {raw_csv_folder}")
    print("\nExtraction complete.")

    if args.concatenate:
        print(f"Concatenating CSV files in: {raw_csv_folder}")
        if args.output_file is None:
            print("Error: --output_file is required when using --concatenate.")
        else:
            print(f"Output file for concatenated CSV: {args.output_file}")
            concatenate_csv_files(raw_csv_folder, args.output_file)