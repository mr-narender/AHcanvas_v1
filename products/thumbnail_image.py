from PIL import Image
import os


directory = '/workspace/AHcanvas_v1/media'
for file in os.listdir(directory):
    if file.endswith(('jpeg', 'png', 'jpg')):
        filepath = os.path.join(directory, file)
        outfile = os.path.join(directory, 'resized_'+file)
        with Image.open(directory+'/'+file) as im:
            im.thumbnail((350, 250))
            im.save(outfile)
