import pypsa
n = pypsa.Network("resources/kupferzell_2024/networks/base_s_256_elec_.nc")

# Check for infinite bounds
print("Lines with s_nom > 100000:")
print(n.lines[n.lines.s_nom > 100000][['s_nom','s_nom_extendable']])

print("\nStorage units e_nom:")
print(n.storage_units[['p_nom','e_nom','e_nom_extendable','e_nom_max']])

# Flag any inf values
import numpy as np
for comp in ['lines','links','storage_units','generators']:
    df = getattr(n, comp).select_dtypes('number')
    inf_cols = (df == np.inf).any()
    if inf_cols.any():
        print(f"\nINF values in {comp}:", inf_cols[inf_cols].index.tolist())