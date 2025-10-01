import pandas as pd

# Load results
df_results = pd.read_pickle("ACIT4610---Mandatory-2/results_incremental.pkl")

#write to csv
df_results.to_csv("ACIT4610---Mandatory-2/results_incremental.csv", index=False)