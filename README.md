# Reproducible Data Preprocessing Pipeline for Spatio-Temporal Urban Accessibility Analysis

Code accompanying the manuscript:

> "A Reproducible Data Preprocessing Pipeline for Spatio-Temporal Urban Accessibility Analysis"

This repository implements the preprocessing pipeline described in the paper, including:

1. **Automatic unit verification** — plausibility checks for sensor readings (non-negative, plausible maxima).
2. **K-Nearest Neighbors imputation** — formally specified neighbor selection based on Pearson correlation, Euclidean distance metric, and an explicit fill order (forward-backward fill → KNN → constant fill).
3. **Z-score normalization** — with documented statistical invariance properties (skewness and kurtosis preserved).
4. **Automatic data documentation** — startup logging of normalization statistics for full reproducibility.

## Files

- `preprocessing.py` — unit verification and data documentation functions.
- `train.py` — startup logging of normalization statistics.

## Requirements

- Python 3.9+
- numpy
- pandas (optional, for full pipeline)

Install with:

```bash
pip install -r requirements.txt
```

## Usage

```python
from preprocessing import verify_data_units, add_data_documentation

result = verify_data_units(data, "METR-LA")
print(result)
```

## Citation

If you use this code, please cite the manuscript.


## Data

This repository contains code only. Datasets are not redistributed due to licensing restrictions:

- METR-LA: https://github.com/zhenggy92/STL
- PEMS-BAY: https://github.com/ieee-dsp/pems-bay
- Synthetic Portland network: generated using parameters in Section 3.1 of the manuscript.
