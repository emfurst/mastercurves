import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
from mastercurves import MasterCurve
from mastercurves.transforms import Multiply, PowerLawAge
from sklearn.gaussian_process.kernels import WhiteKernel

# Read the files
ts = [[],[],[],[],[]]
Js = [[],[],[],[],[]]
with open("data/joshi_compliance_55.csv") as file:
    reader = csv.reader(file)
    next(reader)
    next(reader)
    for row in reader:
        for k in range(5):
            if not row[8 - 2*k] == "":
                ts[k] += [float(row[8 - 2*k])]
                Js[k] += [float(row[9 - 2*k])]

for k in range(5):
    ts[k].reverse()
    Js[k].reverse()
    ts[k] = np.log(np.array(ts[k]))
    Js[k] = np.log(np.array(Js[k]))

tws = [15000, 9600, 6000, 3600, 1500]

# Develop a master curve
mc = MasterCurve()
mc.add_data(ts, Js, tws)
mc.set_gp_kernel(mc.kernel + WhiteKernel(0.02**2, "fixed"))

# Add transformations
mc.add_htransform(PowerLawAge(15000))
mc.add_vtransform(Multiply())

# Superpose
mc.superpose()
print(mc.hparams[0])

# Plot
fig1, ax1, fig2, ax2, fig3, ax3 = mc.plot()
plt.show()
