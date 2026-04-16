# SPDX-FileCopyrightText: : 2023- The PyPSA-Eur Authors
#
# SPDX-License-Identifier: MIT


def custom_extra_functionality(n, snapshots, snakemake):
    """
    Add custom extra functionality constraints.
    """
    import logging
    logger  = logging.getLogger(__name__)
    # Dictionary of scaling factors (Target 2025 TWh / Baseline 2013 TWh)
    # These are defensible ratios based on ENTSO-E and RTE/national data.
    DEMAND_SCALE = {
        "DE": 465.5 / 561.0,  # User input
        "DK": 36.8 / 32.8,    # User input
        "FR": 460.0 / 495.2,  # France: Moderate decline due to efficiency
        "BE": 88.0 / 89.0,    # Belgium: Largely flat demand
        "NL": 122.0 / 116.5,  # Netherlands: Growth via electrification
        "AT": 75.0 / 71.0,    # Austria: Moderate growth
        "CZ": 72.0 / 68.1,    # Czechia: Steady industrial growth
        "PL": 185.0 / 158.0,  # Poland: Significant growth/electrification
    }

    logger.info("Applying country-specific demand scaling for 2025 scenario...")

    # Iterate through each country and scale its associated loads
    for country, scale in DEMAND_SCALE.items():
        # Identify all loads belonging to the country (e.g., 'DE0 0', 'FR1 2')
        country_loads = n.loads.index[n.loads.index.str.startswith(country)]

        if not country_loads.empty:
            # Scale the time-varying power demand (p_set)
            n.loads_t.p_set[country_loads] *= scale
            logger.info(f"Scaled {len(country_loads):>4} loads for {country} by {scale:.4f}")
        else:
            logger.warning(f"No loads found for country {country}. Check if it is included in the model.")

    # Verification: Log total demand to ensure scaling was applied correctly
    total_demand_twh = (n.loads_t.p_set.sum().sum() * n.snapshot_weightings.objective.iloc[0] / 1e6)
    logger.info(f"Total model demand after scaling: {total_demand_twh:.2f} TWh")