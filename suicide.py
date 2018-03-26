#General

import pandas as pd     # To handle data
import numpy as np      # For number computing

# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns


df1=pd.read_csv("suicide.csv")

data=df1


#total length of csv file
no_df1=len(df1)

#display the total data available
display(df1.head(no_df1))

