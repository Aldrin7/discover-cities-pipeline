# Preprocessing module
import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


def verify_data_units(data: np.ndarray, dataset_name: str) -> dict:
    """Verify that data plausibility checks pass.
    
    Checks:
    - No negative values (traffic speed should be >= 0)
    - Reasonable max values (METR-LA: ~0-80 mph, PEMS-BAY: ~0-80 mph)
    - No extreme outliers that suggest unit errors
    
    Returns dict with verification results.
    """
    result = {
        "dataset": dataset_name,
        "min": float(data.min()),
        "max": float(data.max()),
        "mean": float(data.mean()),
        "std": float(data.std()),
        "negative_count": int((data < 0).sum()),
        "plausible": True,
        "warnings": [],
    }
    
    # Traffic speed should never be negative
    if result["min"] < 0:
        result["plausible"] = False
        result["warnings"].append(f"Negative values found: min={result['min']}")
    
    # Check reasonable max values per dataset
    if "METR-LA" in dataset_name:
        if result["max"] > 150:
            result["plausible"] = False
            result["warnings"].append(f"METR-LA max speed={result['max']:.1f} exceeds typical 0-80 mph range")
    elif "PEMS-BAY" in dataset_name:
        if result["max"] > 150:
            result["plausible"] = False
            result["warnings"].append(f"PEMS-BAY max speed={result['max']:.1f} exceeds typical 0-80 mph range")
    
    if not result["plausible"]:
        print(f"[WARN] Data unit verification failed for {dataset_name}: {result['warnings']}")
    else:
        print(f"[OK] Data unit verification passed for {dataset_name}")
    
    return result


def add_data_documentation(
    cfg: dict,
    data_dir: str,
    dataset: str,
) -> dict:
    """Add data processing documentation to config.
    
    Records:
    - Raw data min/max/mean/std
    - Normalization stats
    - Any imputation applied
    - KNN parameters if used
    
    Returns updated config with data documentation.
    """
    import os
    
    # Load raw data to verify
    train_path = os.path.join(data_dir, dataset, "train.npz")
    raw = np.load(train_path)
    
    if "data" in raw.files:
        raw_data = raw["data"].astype(np.float32)
    elif "arr_0" in raw.files:
        raw_data = raw["arr_0"].astype(np.float32)
    else:
        raw_data = raw[raw.files[0]].astype(np.float32)
    
    # Ensure shape (n_timesteps, n_sensors)
    if raw_data.shape[0] < raw_data.shape[1]:
        raw_data = raw_data.T
    
    doc = {
        "data_unit_verification": {
            "raw_min": float(raw_data.min()),
            "raw_max": float(raw_data.max()),
            "raw_mean": float(raw_data.mean()),
            "raw_std": float(raw_data.std()),
        },
        "normalization_applied": cfg.get("data", {}).get("normalize", True),
        "normalization_type": "z-score",
    }
    
    # Check if KNN imputation was applied (look for imputation indicators)
    if cfg.get("preprocessing", {}).get("knn_impute", False):
        knn_cfg = cfg["preprocessing"]["knn_impute"]
        doc["knn_imputation"] = {
            "k": knn_cfg.get("k", 5),
            "metric": knn_cfg.get("metric", "euclidean"),
            "applied": True,
        }
    else:
        doc["knn_imputation"] = {"applied": False}
    
    return doc
