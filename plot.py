import pandas as pd
import plotly.express as px
import plotly.io as pio
import glob,os,sys
from PIL import Image

os.chdir(sys.argv[1])

for file in glob.glob("*.csv"):
  df = pd.read_csv(file)
  titlePlot = file.replace(".csv", "")
  fig = px.line(df, x = 'timestamp', y = 'value', title = titlePlot, template='ggplot2')
  fig.update_layout(autosize=False,width=1200,height=768,title_font_size=10)
  pio.write_image(fig, titlePlot + '.png')

imagelist = []
indexImage = 0
im1 = None
for image in glob.glob("*.png"):
  imageOpen = Image.open(image)
  im = imageOpen.convert('RGB')
  if indexImage == 0:
      im1 = im
  if indexImage != 0:
      imagelist.append(im)
  indexImage +=1

im1.save(r'report.pdf',save_all=True, append_images=imagelist)
