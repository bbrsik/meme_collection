import os
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv()
else:
    print('No .env file found.')
    print('Please check the .env.example file and create the .env file.')
    print('/// SHUTTING DOWN ///')
    exit()

UPLOAD_DIR = "../uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

