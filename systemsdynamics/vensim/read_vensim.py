import pysd
import pandas as pd

model = pysd.read_vensim("M-01.mdl")
results = model.run()
print(results)
results.to_csv("M-01_vensim.csv")