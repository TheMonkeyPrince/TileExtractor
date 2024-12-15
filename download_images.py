import aiohttp
import asyncio
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"

async def download_image(session, url, save_path):
    """Downloads a single image asynchronously."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                save_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                print(f"Downloaded: {url}")
            else:
                print(f"Failed to download {url}: {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

async def download_images(image_urls, image_names, output_dir):
    """Downloads multiple images concurrently."""
    headers = {"User-Agent": USER_AGENT}
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i, url in enumerate(image_urls):
            save_path = Path(output_dir) / image_names[i]
            tasks.append(download_image(session, url, save_path))
        await asyncio.gather(*tasks)

