#!/usr/bin/env python
# coding: utf-8

# In[68]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.stats import permutation_test
import statsmodels.api as sm
from patsy import dmatrix
from pathlib import Path
import statsmodels.formula.api as smf
from datetime import datetime

np.random.seed(42)  # For data reproducibility


# In[116]:


# ----------------------------------------------------------
# 1. Load Excel File
# ----------------------------------------------------------

file_path = r"C:/Users/file_path.xlsx"
df = pd.read_excel(file_path)

# Rename first column to Time if needed
df = df.rename(columns={df.columns[0]: "Time"})


# In[117]:


# ----------------------------------------------------------
# 2. Convert Wide Format → Long Format (Preserve Replicates)
# ----------------------------------------------------------

long_list = []

for col in df.columns:
    if col == "Time":
        continue
    
    group = "Group1" if col.startswith("Group1") else "Group2"
    
    temp = pd.DataFrame({
        "Time": df["Time"],
        "Value": df[col],
        "Group": group
    })
    
    long_list.append(temp)

long_df = pd.concat(long_list, ignore_index=True)
long_df = long_df.dropna()

# Binary group variable
long_df["GroupBinary"] = (long_df["Group"] == "Group2").astype(int)


# In[118]:


# ----------------------------------------------------------
# 3. Confirm Replicates
# ----------------------------------------------------------

print("\nReplicates per group per timepoint:")
print(long_df.groupby(["Group", "Time"]).size())


# In[119]:


# ----------------------------------------------------------
# 4. Fit Quadratic Functional Model
# ----------------------------------------------------------

model = smf.ols(
    "Value ~ Time + I(Time**2) + GroupBinary + Time:GroupBinary + I(Time**2):GroupBinary",
    data=long_df
).fit()

print("\nModel Summary:")
print(model.summary())


# In[120]:


# ----------------------------------------------------------
# 5. Extract Functional Difference p-value
# ----------------------------------------------------------

# Joint test: do time-related group interaction terms differ?
hypothesis = "Time:GroupBinary = 0, I(Time ** 2):GroupBinary = 0"
result = model.f_test(hypothesis)

p_value = float(result.pvalue)

print(f"\nExact functional comparison p-value: {p_value:.10f}")


# In[121]:


# ----------------------------------------------------------
# 6. Interpretation
# ----------------------------------------------------------

if p_value < 0.05:
    interpretation = "The enrichment time-course functions differ significantly between groups."
else:
    interpretation = "No statistically significant functional difference detected."

print("\nResult:", interpretation)


# In[122]:


# ----------------------------------------------------------
# 7. Save Statistical Report
# ----------------------------------------------------------

report_path = r"C:/Users/file_path.txt"

with open(report_path, "w") as f:
    f.write("Functional Time-Course Comparison Report\n")
    f.write("Generated: " + str(datetime.now()) + "\n\n")
    f.write("Replicates per group per timepoint:\n")
    f.write(str(long_df.groupby(["Group", "Time"]).size()))
    f.write("\n\n")
    f.write("Model Summary:\n")
    f.write(model.summary().as_text())
    f.write("\n\n")
    f.write(f"Exact Functional Comparison p-value: {p_value:.10f}\n\n")
    f.write("Interpretation:\n")
    f.write(interpretation)

print(f"\nReport saved to: {report_path}")


# In[123]:


# ----------------------------------------------------------
# 8. Publication-Quality Plot (Save as PDF)
# ----------------------------------------------------------

time_grid = np.linspace(long_df["Time"].min(),
                        long_df["Time"].max(), 200)

# Create prediction data
pred_ref = pd.DataFrame({
    "Time": time_grid,
    "GroupBinary": 0
})

pred_comp = pd.DataFrame({
    "Time": time_grid,
    "GroupBinary": 1
})

curve_ref = model.predict(pred_ref)
curve_comp = model.predict(pred_comp)

plt.figure(figsize=(7,5))

plt.plot(time_grid, curve_ref, linewidth=3, label="Group1")
plt.plot(time_grid, curve_comp, linewidth=3, label="Group2")

plt.scatter(
    long_df[long_df["GroupBinary"]==0]["Time"],
    long_df[long_df["GroupBinary"]==0]["Value"],
    alpha=0.5
)

plt.scatter(
    long_df[long_df["GroupBinary"]==1]["Time"],
    long_df[long_df["GroupBinary"]==1]["Value"],
    alpha=0.5
)

plt.xlabel("Time")
plt.ylabel("Isotope Enrichment")
plt.title("Functional Time-Course Comparison")
plt.legend()
plt.tight_layout()

# Save as PDF
plot_path = r"C:/Users/file_path.pdf"
plt.savefig(plot_path, format="pdf")

plt.show()

print(f"\nPlot saved to: {plot_path}")


# In[106]:


# 9. Interpretation & Report (Saved to Documents)
# ----------------------------------------------------------

report_text = f"""
Functional Time-Course Analysis Report
======================================
Reference group: {reference_group}
Comparison group: {comparison_group}

Observed L2 functional difference: {observed_stat:.6f}
Global permutation p-value: {p_value:.5f}

Interpretation:
"""

if p_value < 0.05:
    report_text += "The enrichment time-course functions differ significantly between groups.\n"
else:
    report_text += "No statistically significant functional difference detected.\n"

# Print report
print(report_text)

# Save report to C:/Users/Kayla/Documents/
report_file = Path(r"C:/Users/filepath_2.txt")
with open(report_file, "w") as f:
    f.write(report_text)

print(f"Report saved to {report_file.resolve()}")


# In[ ]:




