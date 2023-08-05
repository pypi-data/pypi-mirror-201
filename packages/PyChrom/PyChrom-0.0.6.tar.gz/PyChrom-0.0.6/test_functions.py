import numpy as np
import app as pc
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('CAF-ISOMER1_11542.arw', sep='\t', skiprows=2)
data = np.asarray(df)
y_data = data[:,1]

plt.plot(y_data)

noise = pc.calculate_noise(y_data)
print(noise)

print()