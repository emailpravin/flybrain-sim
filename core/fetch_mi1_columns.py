"""
Fetch the Mi1 neurons for one eye (one per visual column, hex-grid coordinates
assignedOlHex1/2) -- this is our simulated "retina surface": the real fly
neurons whose activity is organized retinotopically, ~2 synapses downstream
of the actual photoreceptors.

Usage:
  python fetch_mi1_columns.py --side R --out mi1_columns.csv
"""
import argparse
import os
import sys

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", default="R", choices=["L", "R"])
    parser.add_argument("--out", default="mi1_columns.csv")
    args = parser.parse_args()

    token = os.environ.get("NEUPRINT_APPLICATION_CREDENTIALS")
    if not token:
        print("No NEUPRINT_APPLICATION_CREDENTIALS found.", file=sys.stderr)
        sys.exit(1)

    from neuprint import Client, fetch_neurons, NeuronCriteria as NC

    client = Client("https://neuprint.janelia.org", dataset="male-cns:v1.0", token=token)
    print(f"Connected to neuprint: {client.fetch_version()}")

    df, _ = fetch_neurons(NC(type="Mi1"))
    df = df.dropna(subset=["assignedOlHex1", "assignedOlHex2"])
    df = df[df["somaSide"] == args.side]

    out = df[["bodyId", "assignedOlHex1", "assignedOlHex2"]].rename(
        columns={"assignedOlHex1": "hex1", "assignedOlHex2": "hex2"}
    )
    out.to_csv(args.out, index=False)
    print(f"Saved {len(out)} Mi1 columns (side {args.side}) to {args.out}")
    print(f"hex1 range: {out['hex1'].min()}-{out['hex1'].max()}, hex2 range: {out['hex2'].min()}-{out['hex2'].max()}")


if __name__ == "__main__":
    main()
