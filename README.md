# Growfinix Internship — Task 1
## Real Estate Market Data Cleaning and Sales Integration

### Project Overview
This project demonstrates real estate data cleaning and integration using Python. The objective is to improve data consistency, identify potential duplicate property listings, handle missing ZIP codes, and combine property listing data with historical sales records.

### Tools Used
- Python
- Visual Studio Code
- CSV files
- Python standard library

### Tasks Performed
1. Standardized text fields by removing extra spaces and applying consistent capitalization.
2. Preserved ZIP codes as text and retained missing ZIP codes for verification.
3. Identified repeated property addresses for manual review.
4. Combined property listing records with historical sales using `PropertyID`.
5. Generated output files and a cleaning report.

### Project Structure
- `data/` — Input property and historical sales CSV files.
- `output/` — Generated cleaned data, merged data, report, and duplicate-review file.
- `clean_data.py` — Python cleaning and merging script.
- `README.md` — Project documentation.

### Output Files
- `cleaned_property_listings.csv`
- `merged_property_sales.csv`
- `cleaning_report.txt`
- `duplicate_address_review.csv`

### How to Run
1. Install Python 3.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run:

   `python clean_data.py`

### Important Note
The supplied starter CSV files are practice data. Repeated addresses are flagged for review rather than automatically deleted, and missing ZIP codes are not guessed. Results depend on the input data.

### Conclusion
This project demonstrates basic data-cleaning, data-quality review, and data-integration techniques that can support real estate market analysis.
