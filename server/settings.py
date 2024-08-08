import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()
else:
    print('No .env file found.')
    print('Please check the .env.example file and create the .env file.')
    print('/// SHUTTING DOWN ///')
    exit()

IMAGE_STORAGE_API_KEY = os.getenv("IMAGE_STORAGE_API_KEY")
IMAGE_STORAGE_URL = os.getenv("IMAGE_STORAGE_URL")
