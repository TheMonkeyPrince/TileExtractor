import asyncio

from utils import latlon2xy, recreate_folder
from download_images import download_images
from utils import *
from config import *

def download_tiles(zoom, start_lat, start_lon, stop_lat, stop_lon, output_dir):
    start_x, start_y = latlon2xy(zoom, start_lat, start_lon)
    stop_x, stop_y = latlon2xy(zoom, stop_lat, stop_lon)
    
    print(start_x, start_y)
    print(stop_x, stop_y)

    print(f"Number of tiles to download: {(stop_x - start_x) * (stop_y - start_y)}")
    c = input("Continue ? Y/N ")
    if not c.lower().startswith("y"):
        print("Aborting")
        return False

    image_urls = []
    image_names = []

    for x in range(start_x, stop_x):
        for y in range(start_y, stop_y):                   
            url = f"https://mt0.google.com/vt?lyrs=s&x={x}&s=&y={y}&z={zoom}"
            filename = f"{zoom}_{x}_{y}.png"
            image_urls.append(url)
            image_names.append(filename)

    asyncio.run(download_images(image_urls, image_names, output_dir))
    print("All tiles have been downloaded !")
    return True
