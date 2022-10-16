import pandas as pd
import os

# with open(os.path.join("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/MGI-RNASeq/excel-merged-cells-pandas-tests.xlsx"), "r") as input:
# df = pd.ExcelFile("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/MGI-RNASeq/excel-merged-cells-pandas-tests.xlsx")
# print(df.sheet_names)

qc_df = pd.read_excel(open("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/QC&libprep&Sequecing_Report_13.09_full to 3 prime sample information copy.xlsx", 'rb'), sheet_name='QC', skiprows=1)

rt_cdna_df = pd.read_excel(open("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/QC&libprep&Sequecing_Report_13.09_full to 3 prime sample information copy.xlsx", 'rb'), sheet_name='RT&cDNA')
rt_cdna_df = rt_cdna_df.fillna(method='ffill')

qc_rt_cdna_df = pd.merge(qc_df, rt_cdna_df, how='inner', on='MGI Sample ID')

qc_rt_cdna_df.to_excel("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/mgi-rna-seq-batch-1-qc-rtcdna.xlsx", sheet_name='MGI-RNA-Seq-Batch-1-qc-rtcdna')
# new_qc_df = qc_df.set_index('MGI Sample ID').join(rt_cdna_df.set_index('MGI Sample ID'))
# qc_df.join(rt_cdna_df.set_index('MGI Sample ID'), on='MGI Sample ID')

lib_prep_df = pd.read_excel(open("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/QC&libprep&Sequecing_Report_13.09_full to 3 prime sample information copy.xlsx", 'rb'), sheet_name='LibPrep&Circ&DNB', skiprows=1)
lib_prep_df = lib_prep_df.fillna(method='ffill')

# rt_cdna_df.join(lib_prep_df.set_index('MGI Sample ID'), on='MGI Sample ID')
qc_rt_cdna_lib_prep_df = pd.merge(qc_rt_cdna_df, lib_prep_df, how='inner', on='MGI Sample ID')

qc_rt_cdna_lib_prep_df.to_excel("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/mgi-rna-seq-batch-1-qc-rtcdna-libprep.xlsx", sheet_name='MGI-RNA-Seq-Batch-1-qc-rtcdna-libprep')

seq_df = pd.read_excel(open("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/QC&libprep&Sequecing_Report_13.09_full to 3 prime sample information copy.xlsx", 'rb'), sheet_name='Sequencing',skiprows=1)
seq_df = seq_df.fillna(method='ffill')

all_df = pd.merge(qc_rt_cdna_lib_prep_df, seq_df, how='inner', on='Sample Name')
all_df.to_excel("/Users/philippe/Documents/H2020-PRECISIONTOX/Data-Management-WG/mgi-rna-seq-batch-1.xlsx", sheet_name='MGI-RNA-Seq-Batch-1')


