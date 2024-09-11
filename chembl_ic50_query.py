import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to retrieve bioactivity for a single molecule
def fetch_bioactivity(chembl_id):
    base_url = "https://www.ebi.ac.uk/chembl/api/data"
    bioactivity_url = f"{base_url}/activity?molecule_chembl_id={chembl_id}&format=json&limit=10"
    bio_response = requests.get(bioactivity_url)

    if bio_response.status_code != 200:
        return None

    bio_data = bio_response.json()
    ic50_value, ic50_units = 'N/A', 'N/A'
    ki_value, ki_units = 'N/A', 'N/A'
    ec50_value, ec50_units = 'N/A', 'N/A'
    target_name = 'N/A'

    for bio in bio_data['activities']:
        activity_type = bio.get('standard_type', 'N/A')
        target = bio.get('target_chembl_id', 'N/A')
        value = bio.get('standard_value', 'N/A')
        units = bio.get('standard_units', 'N/A')

        if target != 'N/A':
            # Retrieve target name (only once per compound)
            target_name = target

        # Assign values based on activity type
        if activity_type == 'IC50' and value != 'N/A':
            ic50_value = f"{value} {units}"
        elif activity_type == 'Ki' and value != 'N/A':
            ki_value = f"{value} {units}"
        elif activity_type == 'EC50' and value != 'N/A':
            ec50_value = f"{value} {units}"

    return {
        "chembl_id": chembl_id,
        "ic50": ic50_value,
        "ki": ki_value,
        "ec50": ec50_value,
        "target": target_name
    }

# Function to search for molecules and retrieve their bioactivity in parallel
def search_chembl_with_all_activity(substructure_name, max_results=100):
    base_url = "https://www.ebi.ac.uk/chembl/api/data"
    results = []
    offset = 0
    limit = 20  # Number of results per page (ChEMBL API default)
    total_retrieved = 0
    retrieved_chembl_ids = set()  # Set to track unique ChEMBL IDs

    # Prepare thread pool for parallel fetching
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_chembl = {}

        while total_retrieved < max_results:
            # Search for compounds containing the substructure, handling pagination
            compound_url = f"{base_url}/molecule?format=json&smiles_contains={substructure_name}&limit={limit}&offset={offset}"
            response = requests.get(compound_url)

            if response.status_code != 200:
                print(f"Failed to retrieve data from ChEMBL API: {response.status_code}")
                break

            compounds = response.json()
            if not compounds['molecules']:
                print("No more results found.")
                break  # Exit loop if no more results

            for compound in compounds['molecules']:
                chembl_id = compound['molecule_chembl_id']

                # Skip if already retrieved
                if chembl_id in retrieved_chembl_ids:
                    continue

                retrieved_chembl_ids.add(chembl_id)  # Track unique ChEMBL ID
                smiles = compound.get('molecule_structures', {}).get('canonical_smiles', 'N/A')

                # Submit bioactivity retrieval task
                future = executor.submit(fetch_bioactivity, chembl_id)
                future_to_chembl[future] = {
                    "compound_name": compound.get('pref_name', 'N/A'),
                    "chembl_id": chembl_id,
                    "smiles": smiles
                }

                total_retrieved += 1
                if total_retrieved >= max_results:
                    break

            offset += limit

        # Collect results as tasks complete
        for future in as_completed(future_to_chembl):
            compound_info = future_to_chembl[future]
            bioactivity = future.result()

            if bioactivity:
                results.append([
                    compound_info['compound_name'],
                    bioactivity['chembl_id'],
                    compound_info['smiles'],
                    bioactivity['target'],
                    bioactivity['ic50'],
                    bioactivity['ki'],
                    bioactivity['ec50']
                ])

    # Save results to Excel
    if results:
        df = pd.DataFrame(results, columns=['Compound Name', 'ChEMBL ID', 'SMILES', 'Target', 'IC50 (with units)', 'Ki (with units)', 'EC50 (with units)'])
        df.to_excel(f'{substructure_name}_activity_results.xlsx', index=False)
        print(f"Results saved to {substructure_name}_activity_results.xlsx")
    else:
        print("No results found.")

# Example usage: limit to 100 unique molecules with IC50, Ki, EC50
search_chembl_with_all_activity("catechol", max_results=100)

