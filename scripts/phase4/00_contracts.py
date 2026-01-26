#!/usr/bin/env python3
"""Step 0: Contracts and Reset - Freeze geometry and establish manifests"""
import json, ants, numpy as np
from pathlib import Path

# Load geometry from config file
geom = json.load(open("configs/cbct_geom.json"))["geometry"]

MAN = {
  "geometry": geom,
  "grid": {"spacing_mm": [1.75,1.75,1.75], "shape": [162,162,162]},
  "cases": {}
}

# Populate from Phase 3 outputs
base_dir = Path("results/cbct/volumes")
base_dir.mkdir(parents=True, exist_ok=True)

# Copy Phase 3 outputs to cbct/volumes if they don't exist
from shutil import copy2
pca_dir = Path("results/pca")
if pca_dir.exists():
    # Find all HU volumes from PCA output
    for hu_file in pca_dir.glob("*_HU.nii.gz"):
        dest = base_dir / hu_file.name
        if not dest.exists():
            copy2(hu_file, dest)
            print(f"Copied {hu_file.name} to cbct/volumes/")

labels = ["exhale_strong","exhale_moderate","mean","mixed_1","mixed_2"]
for lab in labels:
    gt_hu = f"results/cbct/volumes_cubic/{lab}_HU.nii.gz"  # Use cubic grid volumes
    if Path(gt_hu).exists():
        MAN["cases"][lab] = {"gt_hu": gt_hu}
    else:
        print(f"WARNING: {gt_hu} not found!")

Path("results/cbct").mkdir(parents=True, exist_ok=True)
json.dump(MAN, open("results/cbct/manifest.json","w"), indent=2)
print(f"\nManifest created with {len(MAN['cases'])} cases")

# Quick HU sanity check
for lab in MAN["cases"]:
    a = ants.image_read(MAN["cases"][lab]["gt_hu"]).numpy().astype(np.float32)
    print(f"{lab}: HU min={a.min():.1f}, p1={np.percentile(a,1):.1f}, median={np.median(a):.1f}, p99={np.percentile(a,99):.1f}, max={a.max():.1f}")

print("\n[OK] Step 0 complete - manifest saved")
