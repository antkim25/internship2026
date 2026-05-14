import pysd
import pandas     as pd
import subprocess
import sys

mdl_file = "M-01.mdl"
py_file = "M-01.py"

# Translate
subprocess.run([sys.executable, "-c", f"import pysd; pysd.read_vensim('{mdl_file}')"],
               capture_output=True)

# Fix 1: add xarray import
with open(py_file, "r") as f:
    content = f.read()

content = content.replace(
    "import numpy as np",
    "import numpy as np\nimport xarray as xr"
)

# Fix 2: replace broken result() body
old_func = """    value = xr.DataArray(np.nan, {}, [])
    value.loc[None] = incomplete(result())
    value.loc[None] = float(np.minimum(a(), b()))
    return value"""

new_func = """    return float(np.minimum(a(), b()))"""

content = content.replace(old_func, new_func)

with open(py_file, "w") as f:
    f.write(content)

# Load and run
model = pysd.load(py_file)
results = model.run()
print(results)
results.to_csv("M-01_vensim.csv", index=False)
print("Saved to M-01_vensim.csv")