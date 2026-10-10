"""Merge the real, correctly-signed Li28 neurons and edges into the
existing escape-circuit connectome from experiments 01/02."""
import pandas as pd

neurons = pd.read_csv("../../core/data/connectome_flight_escape_neurons.csv")
edges = pd.read_csv("../../core/data/connectome_flight_escape.csv")
li28_neurons = pd.read_csv("data/li28_neurons.csv")
li28_edges = pd.read_csv("data/li28_edges.csv")

merged_neurons = pd.concat([neurons, li28_neurons], ignore_index=True).drop_duplicates(subset="bodyId")
merged_edges = pd.concat([edges, li28_edges], ignore_index=True)

merged_neurons.to_csv("data/connectome_li28_intact_neurons.csv", index=False)
merged_edges.to_csv("data/connectome_li28_intact.csv", index=False)
print(f"{len(merged_neurons)} neurons, {len(merged_edges)} edges")
