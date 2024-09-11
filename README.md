# ChEMBL IC50 Query Script

## Description

This Python script retrieves bioactivity data for compounds containing a specified substructure from the ChEMBL database. It fetches **IC50**, **Ki**, and **EC50** values, along with their units, and outputs the results to an Excel file. The script is optimized for performance with parallel fetching of data and limiting the number of results.

## Features

- Retrieves compounds containing a specified substructure from ChEMBL.
- Fetches **IC50**, **Ki**, and **EC50** values with their units.
- Includes target information associated with each compound.
- Saves the results in an Excel file for easy access and analysis.
- Optimized for performance with parallel data fetching.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `openpyxl` library (for Excel file handling)

You can install the required libraries using pip:

```bash
pip install requests pandas openpyxl

## **Usage**

# Clone the Repository
First, clone the repository to your local machine:
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Navigate to the Repository Directory
Change into the directory of the cloned repository:
cd YOUR-REPO-NAME

# Run the Script
Execute the script using Python. Replace "catechol" with the substructure you want to search for:
python chembl_ic50_query.py

# The script will generate an Excel file named catechol_activity_results.xlsx (or another name based on your substructure) with the results.

# Check the Results
Open the generated Excel file to review the retrieved data, including IC50, Ki, EC50 values, and target information.

## **Contributing**
If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request. Contributions are welcome!

## **License**
This project is licensed under the MIT License - see the LICENSE file for details.

## **Contact**
For any questions or issues, please contact precision.stalin@gmail.com
