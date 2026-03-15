This python script was created to do functional data analysis of stable isotope enrichment of metabolomics data. Unlike traditional Area Under the Curve analyses (AUC), metabolomics data for bulk tissue uses endpoint data where each sample is unique. This requires analysis using FDA since there is not continuous data for the same sample. This script uses an excel file containing labeling percentage for samples in two groups, and generates both plots and statistical tests for the timecourse. 

This script generates txt (step 7) and PDF (step 8) files that must be renamed appropriately or stored in separate files or they will overwrite the previous output. 

Samples input files (Test_Metabolite1.xlsx and Test_Metabolite2.xlsx) are available to check the required formatting for this script and compare significant (1) vs non-significant (2) outputs. Outputs for the examples files are also included in the sample files. 
