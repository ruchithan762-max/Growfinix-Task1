"""
Growfinix Task 1: Real Estate Market Data Cleaning
Practice project using fictional CSV files and Python's standard library.
Run from the project folder: python clean_data.py
"""
import csv
import os
import re
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

PROPERTY_FILE = os.path.join(DATA_DIR, "property_listings.csv")
SALES_FILE = os.path.join(DATA_DIR, "historical_sales.csv")


def read_csv(path):
    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean_text(value):
    """Trim extra spaces and use consistent title case for text."""
    value = (value or "").strip()
    value = re.sub(r"\s+", " ", value)
    return value.title()


def clean_property_rows(rows):
    cleaned = []
    seen = set()
    duplicate_count = 0
    duplicate_rows = []

    for row in rows:
        # Keep IDs and ZIP codes as text so leading zeroes are preserved.
        property_id = (row.get("PropertyID") or "").strip().upper()
        address = clean_text(row.get("Address"))
        city = clean_text(row.get("City"))
        zip_code = (row.get("ZipCode") or "").strip()
        property_type = clean_text(row.get("PropertyType"))

        # Flag exact repeated listing details for review.
        key = (
            address.casefold(),
            city.casefold(),
            zip_code,
            property_type.casefold(),
            (row.get("ListingPrice") or "").strip(),
            (row.get("Bedrooms") or "").strip(),
            (row.get("Bathrooms") or "").strip(),
        )

        if key in seen:
            duplicate_count += 1
            duplicate_rows.append(row.copy())
            continue
        seen.add(key)


        row["PropertyID"] = property_id
        row["Address"] = address
        row["City"] = city
        row["ZipCode"] = zip_code
        row["PropertyType"] = property_type
        row["ListingPrice"] = (row.get("ListingPrice") or "").strip()
        row["Bedrooms"] = (row.get("Bedrooms") or "").strip()
        row["Bathrooms"] = (row.get("Bathrooms") or "").strip()
        cleaned.append(row)

    return cleaned, duplicate_count, duplicate_rows


def main():
    if not os.path.exists(PROPERTY_FILE) or not os.path.exists(SALES_FILE):
        print("ERROR: Could not find the CSV files in the data folder.")
        print("Check that data/property_listings.csv and data/historical_sales.csv exist.")
        return

    property_rows = read_csv(PROPERTY_FILE)
    sales_rows = read_csv(SALES_FILE)

    cleaned_properties, duplicates_found, duplicate_rows = clean_property_rows(property_rows)
    review_fields = [
        "PropertyID",
        "Address",
        "City",
        "ZipCode",
        "PropertyType",
        "ListingPrice",
        "Bedrooms",
        "Bathrooms",
    ]

    write_csv(
        os.path.join(OUTPUT_DIR, "duplicate_address_review.csv"),
        duplicate_rows,
        review_fields,
    )

    # Do not guess missing ZIP codes. Keep them blank unless a reliable
    # reference dataset is supplied.
    missing_zip_count = sum(
        1 for row in cleaned_properties if not row["ZipCode"]
    )

    # Create a one-to-many merge: a property can have multiple historical sales.
    sales_by_property = {}

    for sale in sales_rows:
        pid = (sale.get("PropertyID") or "").strip().upper()
        sale["PropertyID"] = pid
        sales_by_property.setdefault(pid, []).append(sale)

    merged_rows = []
    for prop in cleaned_properties:
        matching_sales = sales_by_property.get(prop["PropertyID"], [])
        if matching_sales:
            for sale in matching_sales:
                merged_rows.append({
                    **prop,
                    "SaleID": (sale.get("SaleID") or "").strip(),
                    "SaleDate": (sale.get("SaleDate") or "").strip(),
                    "SalePrice": (sale.get("SalePrice") or "").strip(),
                })
        else:
            merged_rows.append({
                **prop,
                "SaleID": "",
                "SaleDate": "",
                "SalePrice": "",
            })

    property_fields = [
        "PropertyID", "Address", "City", "ZipCode", "PropertyType",
        "ListingPrice", "Bedrooms", "Bathrooms"
    ]
    merged_fields = property_fields + ["SaleID", "SaleDate", "SalePrice"]

    write_csv(
        os.path.join(OUTPUT_DIR, "cleaned_property_listings.csv"),
        cleaned_properties,
        property_fields
    )
    write_csv(
        os.path.join(OUTPUT_DIR, "merged_property_sales.csv"),
        merged_rows,
        merged_fields
    )

    report_path = os.path.join(OUTPUT_DIR, "cleaning_report.txt")
    with open(report_path, "w", encoding="utf-8") as report:
        report.write("GROWFINIX TASK 1 — CLEANING REPORT\n")
        report.write("Dataset type: Fictional practice data (not supplied by Growfinix)\n")
        report.write(f"Property rows before cleaning: {len(property_rows)}\n")
        report.write(f"Duplicate listing rows found for review: {duplicates_found}\n")
        report.write(f"Property rows after cleaning: {len(cleaned_properties)}\n")
        report.write(f"Rows still missing ZIP codes: {missing_zip_count}\n")
        report.write(f"Historical sales rows read: {len(sales_rows)}\n")
        report.write(f"Rows in merged output: {len(merged_rows)}\n")
        report.write("Missing ZIP codes were not guessed; they remain blank pending a trusted lookup.\n")

    print("SUCCESS! Task 1 practice cleaning finished.")
    print(f"Property rows before cleaning: {len(property_rows)}")
    print(f"Duplicate listing rows removed: {duplicates_found}")
    print(f"Property rows after cleaning: {len(cleaned_properties)}")
    print(f"Rows with missing ZIP codes: {missing_zip_count}")
    print(f"Historical sales rows: {len(sales_rows)}")
    print("\nCheck the output folder for:")
    print("- cleaned_property_listings.csv")
    print("- merged_property_sales.csv")
    print("- cleaning_report.txt")


if __name__ == "__main__":
    main()
