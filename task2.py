# -*- coding: utf-8 -*-
import pandas as pd
import pubchempy as pcp
import pymatgen.core as pmg
from pymatgen.ext.matproj import MPRester
from pymatgen.analysis.phase_diagram import PDPlotter, PhaseDiagram
from rdkit import Chem
from rdkit.Chem import Descriptors

dataset = pd.read_csv('sample_data_cut.csv')

# creating DataFrame for descriptors
descriptors = pd.DataFrame(columns=[
    'mol_id',
    'radial_electrons',
    'molecular_weight',
    'valence_electrons',
    'iupac_name',
    'atom_stereo_count'
    # 'structure_data'
])

# Iterate dataset sampled_dataset.csv
for i, row in dataset.iterrows():
    smiles = row['smiles']
    mol = Chem.MolFromSmiles(smiles)
    chem_variable = pcp.get_compounds(smiles, 'smiles')[0]
    # mr_prester = MPRester(credits.my_api_key)
    # samp = mr_prester.get(smiles)
    if mol:
        # Get all descriptors for each item (molecule)
        try:
            radial_electrons = Descriptors.NumRadicalElectrons(mol)
            molecular_weight = Descriptors.MolWt(mol)
            valence_electrons = Descriptors.NumValenceElectrons(mol)
            iupac_name = chem_variable.iupac_name
            atom_stereo_count = chem_variable.atom_stereo_count
            descriptor_df = pd.DataFrame([{
                'mol_id': row['mol_id'],
                'radial_electrons': radial_electrons,
                'molecular_weight': molecular_weight,
                'valence_electrons': valence_electrons,
                'iupac_name': iupac_name,
                'atom_stereo_count': atom_stereo_count,
                # 'structure_data': samp
            }])
            descriptors = pd.concat([
                descriptors if not descriptors.empty else None,
                descriptor_df
            ])
        except Exception as e:
            print("Error: ", e)
            # if process is failure then continue
            pass

# Merge source dataset and new with descriptors
merged_dataset = pd.merge(dataset, descriptors, on='mol_id')

# Save as .csv
merged_dataset.to_csv('cut_dataset_merged.csv', index=False)

# print merged dataset
print(merged_dataset)
