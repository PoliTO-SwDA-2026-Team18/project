import sys
import csv

def filter_coupling(input_file, output_file, threshold=40):
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        if "degree" not in fieldnames:
            raise ValueError("Column 'degree' not found in CSV")

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                degree = float(row["degree"])
            except ValueError:
                continue

            if degree >= threshold:
                writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python co_dependencies_filter.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    filter_coupling(input_file, output_file)