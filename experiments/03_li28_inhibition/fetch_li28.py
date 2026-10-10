"""Pull the real Li28 neurons and their real edges to/from Tm3 (its main
real driver) and LC4 (its main real target), correctly signed from the
start: positive for real acetylcholine (excitatory) connections, negative
for real GABA or glutamate (inhibitory) connections, inferred from each
neuron's predicted neurotransmitter.

Li28 is a real, 13-neuron GABAergic population wired directly onto LC4,
the escape circuit's looming detector. Scoped to Tm3->Li28 and Li28->LC4
specifically (its two dominant real connections, by far) rather than every
minor connection to the rest of the circuit, matching the experiment as
actually run for the blog post."""
import os
import pandas as pd
from neuprint import Client, fetch_neurons, fetch_simple_connections, NeuronCriteria as NC

token = os.environ["NEUPRINT_APPLICATION_CREDENTIALS"]
client = Client("https://neuprint.janelia.org", dataset="male-cns:v1.0", token=token)

existing = pd.read_csv("../../core/data/connectome_flight_escape_neurons.csv")
tm3_ids = existing.loc[existing["type"] == "Tm3", "bodyId"].tolist()
lc4_ids = existing.loc[existing["type"] == "LC4", "bodyId"].tolist()

li28_neurons, _ = fetch_neurons(NC(type="Li28"), client=client)
li28_ids = li28_neurons["bodyId"].tolist()
print(f"Li28: {len(li28_ids)} real neurons")

in_conns = fetch_simple_connections(
    upstream_criteria=NC(bodyId=tm3_ids), downstream_criteria=NC(bodyId=li28_ids), client=client
)
out_conns = fetch_simple_connections(
    upstream_criteria=NC(bodyId=li28_ids), downstream_criteria=NC(bodyId=lc4_ids), client=client
)
print(f"Tm3 -> Li28: {len(in_conns)} edges, weight {in_conns['weight'].sum()}")
print(f"Li28 -> LC4: {len(out_conns)} edges, weight {out_conns['weight'].sum()}")

edges = pd.concat([in_conns, out_conns], ignore_index=True)

li28_nt = li28_neurons.set_index("bodyId")["predictedNt"]
existing_nt = existing.set_index("bodyId")["predictedNt"]
INHIBITORY = {"gaba", "glutamate"}

def sign_for(body_id):
    nt = li28_nt.get(body_id, existing_nt.get(body_id))
    return -1.0 if nt in INHIBITORY else 1.0

edges["weight"] = edges["weight"].abs() * edges["bodyId_pre"].map(sign_for)

edges_out = pd.DataFrame({
    "bodyId_pre": edges["bodyId_pre"], "bodyId_post": edges["bodyId_post"],
    "weight": edges["weight"], "type_pre": edges["type_pre"], "type_post": edges["type_post"],
    "roi": edges.get("roi", ""),
})
li28_neurons_out = pd.DataFrame({
    "bodyId": li28_neurons["bodyId"], "type": li28_neurons["type"],
    "instance": li28_neurons.get("instance", ""), "region": None,
    "predictedNt": li28_neurons.get("predictedNt", "gaba"),
})

edges_out.to_csv("data/li28_edges.csv", index=False)
li28_neurons_out.to_csv("data/li28_neurons.csv", index=False)
print("saved data/li28_edges.csv, data/li28_neurons.csv")
print("sign check -- negative edges:", (edges_out["weight"] < 0).sum(), "/", len(edges_out))
