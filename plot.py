import pandas as pd
import plotly.express as px
import plotly.io as pio
import glob
import os
import sys
from PIL import Image


def main():
    os.chdir(sys.argv[1])

    # read only csv files
    for file in glob.glob("*.csv"):
        df = pd.read_csv(file)
        title_plot = file.replace(".csv", "")
        # create a png image from csv file
        fig = px.line(df, x='timestamp', y='value', title=title_plot, template='ggplot2')
        fig.update_layout(autosize=False, width=1200, height=768, title_font_size=10)
        pio.write_image(fig, title_plot + '.png')

    image_list = []
    index_image = 0
    im1 = None
    for image in sorted(glob.glob("*.png")):
        image_open = Image.open(image)
        im = image_open.convert('RGB')
        if index_image == 0:
            im1 = im
        if index_image != 0:
            image_list.append(im)
        index_image += 1

    # create a pdf file with all images generated
    im1.save(r'report.pdf', save_all=True, append_images=image_list)

    # clean up images
    for file in os.listdir('.'):
      if file.endswith('.png'):
        os.remove(file)


if __name__ == "__main__":
    main()
