import os
os.chdir("/faststorage/project/jsp_student_projects/miRNA_DGD_DE_F2024/DGD/bulkDGD_git")

import sys
sys.path.append("/faststorage/project/jsp_student_projects/miRNA_DGD_DE_F2024/DGD/bulkDGD_git")


# Import the 'logging' module
import logging as log
# Import the 'model' module
from bulkDGD.core import model
# Import the 'ioutil' module 
from bulkDGD import ioutil


import numpy as np
import pandas as pd

import os
print (os.getcwd())



#------------------------------ Logging ------------------------------#


# Set the logging options so that every message
# above and including the INFO level is reported
log.basicConfig(level = "INFO")

logger = log.getLogger(__name__)


#---------------------- Preprocess the samples -----------------------#



# Load the samples into a data frame
df_samples = \
    ioutil.load_samples(# The CSV file where the samples are stored
                        csv_file = "/faststorage/project/jsp_student_projects/miRNA_DGD_DE_F2024/DGD/data/full_TCGA_(scaled)/TCGA_mrna_scaled_match.csv",
                        # The field separator used in the CSV file
                        sep = ",",
                        # Whether to keep the original samples' names/
                        # indexes (if True, they are assumed to be in
                        # the first column of the data frame 
                        keep_samples_names = True,
                        # Whether to split the input data frame into
                        # two data frames, one containing only gene
                        # expression data and the other containing
                        # additional information about the samples                  
                        split = False)
                        

infostr = f"Dimensions = {df_samples.shape}"
other = f"{df_samples.head()}"

log.info(infostr)
log.info(other)


# Preprocess the samples
df_preproc, genes_excluded, genes_missing = \
    ioutil.preprocess_samples(df_samples = df_samples)


#---------------------- Load the configurations ----------------------#



# Load the model's configuration
config_model = ioutil.load_config_model("bulkDGD/ioutil/configs/model/model.yaml")

# Load the configuration with the options to configure
# the search for the best representations
config_rep = ioutil.load_config_rep("bulkDGD/ioutil/configs/representations/two_opt.yaml")


#----------------------- Get the trained model -----------------------#


# Get the trained DGD model (Gaussian mixture model
# and decoder)
dgd_model = model.DGDModel(**config_model)


#---------------------- Get the representations ----------------------#

'''
# Get the representations, the corresponding decoder outputs, and
# the time spent in finding the representations
df_rep, df_dec_out, df_time_opt = \
    dgd_model.get_representations(\
        # The data frame with the samples
        df_samples = df_preproc,
        # The method to use to get the representation
        method = "two_opt",
        # The configuration for the optimization                         
        config_opt = config_rep["optimization"],
        # The number of new representations per component
        # per sample                         
        n_rep_per_comp = config_rep["n_rep_per_comp"])

'''

restacked_rep = []
restacked_dec_out = []
restacked_time_opt = []
i = 1
k = len(df_preproc) // 200

for section in np.array_split(df_preproc,k,axis=0):
    infostr = f"processing batch {i}/{k}, size = {len(section)}"
    log.info(infostr)
    # Get the representations, the corresponding decoder outputs, and
    # the time spent in finding the representations
    df_rep, df_dec_out, df_time_opt = \
        dgd_model.get_representations(\
            # The data frame with the samples
            df_samples = section,
            # The method to use to get the representation
            method = "two_opt",
            # The configuration for the optimization                         
            config_opt = config_rep["optimization"],
            # The number of new representations per component
            # per sample                         
            n_rep_per_comp = config_rep["n_rep_per_comp"])
    
    restacked_rep += [df_rep]
    restacked_dec_out += [df_dec_out]
    restacked_time_opt += [df_time_opt]
    
    i += 1


df_rep = pd.concat(restacked_rep)
df_dec_out = pd.concat(restacked_dec_out)
df_time_opt = pd.concat(restacked_time_opt)




#------------------------- Save the outputs --------------------------#

os.chdir("/faststorage/project/jsp_student_projects/miRNA_DGD_DE_F2024/DGD/data/full_TCGA_(scaled)/")

# Save the preprocessed samples
ioutil.save_samples(\
   # The data frame containing the samples
   df = df_preproc,
   # The output CSV file
   csv_file = "samples_preprocessed.csv",
   # The field separator in the output CSV file
   sep = ",")

# Save the representations
ioutil.save_representations(\
    # The data frame containing the representations
    df = df_rep,
    # The output CSV file
    csv_file = "representations.csv",
    # The field separator in the output CSV file
    sep = ",")

# Save the decoder outputs
ioutil.save_decoder_outputs(\
    # The data frame containing the decoder outputs
    df = df_dec_out,
    # The output CSV file
    csv_file = "decoder_outputs.csv",
    # The field separator in the output CSV file
    sep = ",")

# Save the time data
ioutil.save_time(\
    # The data frame containing the time data
    df = df_time_opt,
    # The output CSV file
    csv_file = "time_opt.csv",
    # The field separator in the output CSV file
    sep = ",")