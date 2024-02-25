from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import asyncio
import random
from io import BytesIO
import requests


app = Flask(__name__)

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def generate_bedwars_image_async(username, interval, mode):
    try:
        additional_info_url = f"https://stats.pika-network.net/api/profile/{username}/"
        additional_info_response = await fetch_data(additional_info_url)

        if additional_info_response.get("username"):
            special_value_username = additional_info_response["username"]
            bedwars_stats_url = f"https://stats.pika-network.net/api/profile/{special_value_username}/leaderboard?type=bedwars&interval={interval}&mode={mode}"
            bedwars_stats_response = await fetch_data(bedwars_stats_url)

            if bedwars_stats_response:
                result_image = await generate_image(username, interval, mode, bedwars_stats_response, additional_info_response, special_value_username)
                return result_image

    except Exception as e:
        print(e)

async def generate_image(username, interval, mode, pika_data, additional_data, special_value_username):
    result_image = Image.new('RGBA', (1280, 720), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(result_image)

    # Background
    background_url = random.choice([
        'https://wallpapercave.com/wp/wp5171323.jpg',
        'https://wallpapercave.com/wp/wp2057070.jpg',
        'https://cdn.wallpapersafari.com/68/88/T4sQgh.jpg',
        'https://wallpapersmug.com/download/1280x720/2d07b6/cute-anime-girl-cake.jpg',
        'https://wallpapercave.com/wp/wp5705541.jpg',
        'https://wallpapercave.com/wp/wp6485728.jpg',
        'https://wallpapercave.com/wp/wp4779055.png',
        'https://wallpapercave.com/wp/wp5780419.jpg',
        'https://wallpapercave.com/wp/wp1812974.jpg',
        'https://wallpapercave.com/wp/wp1812998.jpg'
    ])
    background_image = Image.open(BytesIO(requests.get(background_url).content)).convert('RGBA')
    background_image = background_image.resize((1280, 720), resample=Image.LANCZOS)
    result_image.paste(background_image, (0, 0))

    # Overlay image
    idk_image_url = 'https://i.ibb.co/Rp6Fg9h/Untitled-tytytytyt1.png'
    idk_image = Image.open(BytesIO(requests.get(idk_image_url).content)).convert('RGBA')
    result_image.paste(idk_image, (0, 0), idk_image)

    # Add skin to the image if available
    skin_url = f"https://visage.surgeplay.com/full/512/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(skin_url) as response:
            if response.status == 200:
                skin_image = Image.open(BytesIO(await response.read())).convert('RGBA')
                skin_image = skin_image.resize((300, 500), resample=Image.LANCZOS)
                result_image.paste(skin_image, (950, 10), skin_image)
            else:
                # Use default skin image
                default_skin_image = Image.open("default_skin.png").convert('RGBA')
                default_skin_image = default_skin_image.resize((300, 500), resample=Image.LANCZOS)
                result_image.paste(default_skin_image, (950, 10), default_skin_image)

    # Drawing text and statistic
    draw.text((10, 30), f"{username}'s {mode} ({interval.capitalize()})", fill='white', font=ImageFont.truetype("wow.ttf", 40))
    draw.text((15, 30), f"{username}'s {mode} ({interval.capitalize()})", fill='red', font=ImageFont.truetype("wow.ttf", 40))
    stat_positions = [
        ("Wins", get_entry_value(pika_data, "Wins"), (100, 200)),
        ("Losses", get_entry_value(pika_data, "Losses"), (400, 200)),
        ("Final deaths", get_entry_value(pika_data, "Final deaths"), (400, 320)),
        ("Final kills", get_entry_value(pika_data, "Final kills"), (100, 320)),
        ("Beds broken", get_entry_value(pika_data, "Beds destroyed"), (100, 560)),
        ("Beds lost", get_entry_value(pika_data, "Losses"), (400, 560)),
        ("Kills", get_entry_value(pika_data, "Kills"), (100, 450)),
        ("Deaths", get_entry_value(pika_data, "Deaths"), (400, 450)),
    ]

    for stat_name, stat_value, position in stat_positions:
        draw.text(position, f"{stat_value}", fill='white', font=ImageFont.truetype("arial.ttf", 40))

    highest_winstreak_value = get_entry_value(pika_data, "Highest winstreak reached")
    draw.text((755, 440), f"{highest_winstreak_value}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    games_played = get_entry_value(pika_data, "Games played")
    draw.text((745, 570), f"{games_played}", fill='white', font=ImageFont.truetype("arial.ttf", 36))

    if additional_data.get("clan"):
        clan_name = additional_data["clan"].get("name", "No Clan")
        draw.text((980, 570), f"Clan: {clan_name}", fill='purple', font=ImageFont.truetype("arial.ttf", 40))
    else:
        draw.text((985, 630), "No Guild", fill='white', font=ImageFont.truetype("arial.ttf", 40))

    if additional_data.get("rank"):
        rank_level = additional_data["rank"].get("level", "N/A")
        draw.text((980, 630), f"Rank Level: {rank_level}", fill='pink', font=ImageFont.truetype("arial.ttf", 36))
    else:
        draw.text((980, 660), "No Levels Found!", fill='red', font=ImageFont.truetype("arial.ttf", 36))

    return result_image

def get_entry_value(data, key):
  entry_data = data.get(key, {}).get('entries', None)
  if entry_data is not None:
      return entry_data[0].get('value', 'N/A')
  else:
      return 0

@app.route('/bw/<username>/<interval>/<mode>')
async def generate_bedwars_image(username, interval, mode):
    result_image = await generate_bedwars_image_async(username, interval, mode)
    if result_image:
        image_buffer = BytesIO()
        result_image.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        return send_file(image_buffer, mimetype='image/png')
    else:
        return "Failed to fetch data.", 500

@app.route('/')
def index():
    return """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                text-align: center;
                padding-top: 50px;
            }
            h1 {
                color: #333333;
                font-size: 36px;
                margin-bottom: 30px;
            }
            p {
                color: #666666;
                font-size: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Zumi Bot's Stats API</h1>
        <p>We provide awesome statistics for your gaming needs!</p>
    </body>
    </html>
    """   

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=33645)
