import pandas as pd
import matplotlib.pyplot as plt 
import glob,os

os.chdir("csv/")
for file in glob.glob("*.csv"):
  df = pd.read_csv(file)
  plt.plot(df['timestamp'], df['value'])   
  plt.xlabel('timestamp') 
  plt.ylabel('value') 
  plt.title(file) 
  plt.show() 
