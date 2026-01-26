#!/usr/bin/env python3
"""
Step 2: Volume Preparation - Body masking and air enforcement
"""
import json, ants, numpy as np
from scipy import ndimage as ndi
from pathlib import Path

print("="*70)
print("STEP 2: VOLUME PREPARATION")
print("="*70)

M = json.load(open("results/cbct/manifest.json"))
outd = Path("results/cbct/volumes_prep")
outd.mkdir(parents=True, exist_ok=True)

def body_mask(hu):
    """Create body mask including lung (HU > -950)"""
    b = (hu > -950.0).astype(np.uint8)
    # Keep largest connected component
    lbl, n = ndi.label(b)
    if n > 1:
        sizes = ndi.sum(b, lbl, index=np.arange(1, n+1))
        keep = 1 + int(sizes.argmax())
        b = (lbl == keep).astype(np.uint8)
    # Morphological closing to fill small gaps
    b = ndi.binary_closing(b, iterations=2).astype(np.uint8)
    return b

print("\nProcessing volumes...")
for lab, paths in M["cases"].items():
    img = ants.image_read(paths["gt_hu"])
    hu = img.numpy().astype(np.float32)
    
    # Create body mask
    b = body_mask(hu)
    body_frac = float(b.mean())
    
    # Force air outside body to -1000 HU
    hu[b == 0] = -1000.0
    
    # Save prepared volume
    out_path = str(outd / f"{lab}_HU_prep.nii.gz")
    ants.image_write(
        ants.from_numpy(hu, origin=img.origin, spacing=img.spacing, direction=img.direction),
        out_path
    )
    
    print(f"  {lab}: body fraction = {body_frac*100:.1f}% [{'PASS' if 55 <= body_frac*100 <= 85 else 'CHECK'}]")

print("\n" + "="*70)
print("[OK] Step 2 complete - prepared volumes saved")
print("="*70)
