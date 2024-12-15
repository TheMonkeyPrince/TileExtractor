import os
from datetime import datetime
from download_tiles import download_tiles
from merge_tiles import merge_tiles
from utils import recreate_folder
from config import *


recreate_folder(DOWNLOAD_FOLDER)
if download_tiles(ZOOM, START_LAT, START_LON, STOP_LAT, STOP_LON, DOWNLOAD_FOLDER):
    os.makedirs(RESULT_FOLDER, exist_ok=True)
    merge_tiles(ZOOM, START_LAT, START_LON, STOP_LAT, STOP_LON, DOWNLOAD_FOLDER, f"{RESULT_FOLDER}/{datetime.now().timestamp()}", one_tile_mode=ONE_TILE_MODE, output_tile_width=OUTPUT_TILE_WIDTH, output_tile_height=OUTPUT_TILE_HEIGHT)