from PIL import Image
import os

from utils import latlon2xy
from config import *


def merge_tiles(zoom, start_lat, start_lon, stop_lat, stop_lon, source_dir, output_dir, one_tile_mode=False, output_tile_width=608, output_tile_height=608):    
    x_start, y_start = latlon2xy(zoom, start_lat, start_lon)
    x_stop, y_stop = latlon2xy(zoom, stop_lat, stop_lon)
    
    w = (x_stop - x_start) * 256
    h = (y_stop - y_start) * 256
    if w == 0 or h == 0:
        print("No tile to merge")
        return


    print("Image width:", w)
    print("Image height:", h)
    
    result = Image.new("RGB", (w, h))
    
    for x in range(x_start, x_stop):
        for y in range(y_start, y_stop):
            
            filename = f"{source_dir}/{zoom}_{x}_{y}.png"
            
            if not os.path.exists(filename):
                print("-- missing", filename)
                continue
                    
            x_paste = (x - x_start) * 256
            y_paste = h - (y_stop - y) * 256
            
            image = Image.open(filename)            
            result.paste(image, (x_paste, y_paste))
            del image
    
    os.mkdir(f"{output_dir}/")
    if one_tile_mode:
        output_image = f"{output_dir}/result.png"
        result.save(output_image)
        print(f"Image saved as {output_image}")
        return

    # Calculate the number of tiles needed
    tile_width = output_tile_width
    tile_height = output_tile_height

    num_tiles_x = (w + tile_width - 1) // tile_width
    num_tiles_y = (h + tile_height - 1) // tile_height

    tile_index = 0
    for tile_x in range(num_tiles_x):
        for tile_y in range(num_tiles_y):
            left = tile_x * tile_width
            upper = tile_y * tile_height
            right = min(left + tile_width, w)
            lower = min(upper + tile_height, h)

            # Crop the image into a tile
            tile = result.crop((left, upper, right, lower))

            # Save the tile as a separate image
            tile_filename = f"{output_dir}/{tile_index}.png"
            tile.save(tile_filename)

            tile_index += 1

    print(f"Results saved in {output_dir}")
