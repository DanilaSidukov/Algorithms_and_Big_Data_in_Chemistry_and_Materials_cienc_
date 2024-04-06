# -*- coding: utf-8 -*-
import pandas as pd

# Load dataset qm9.csv
df = pd.read_csv('qm9.csv')

# state is 21
sampled_df = df.sample(n=20000, random_state=21)

# Save new dataset
sampled_df.to_csv('sampled_dataset.csv', index=False)

print("success sampled_dataset.csv")