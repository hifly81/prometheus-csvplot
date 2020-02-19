import pandas as pd
import plotly.express as px
import glob,os

os.chdir("csv/")
for file in glob.glob("*.csv"):
  df = pd.read_csv(file)
  fig = px.line(df, x = 'timestamp', y = 'value', title = file, template='ggplot2')
  fig.show()
