import pandas as pd
import re
import numpy as np
from scipy.stats import entropy
from joblib import Parallel,delayed

eng_dict = pd.read_table("ejdict-hand-utf8.txt",header=None).rename(columns={0:"key",1:"value"})
eng_dict = eng_dict[[len(str(key))==5 for key in eng_dict["key"]]]
eng_dict = eng_dict[[True if re.match(r'[a-zA-Z]{5}', str(key)) else False for key in eng_dict["key"]]]
eng_dict["key"] = eng_dict["key"].str.upper()
eng_dict.drop_duplicates(subset="key",inplace=True)
eng_dict.set_index("key",inplace=True)
eng_dict
f = open ('list.txt','w')
for key in eng_dict.index:
    f.write(key+"\n")
f.close()
