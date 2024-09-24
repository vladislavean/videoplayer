# from app.storage import NextCLoudSettings
#
#
# class StorageServer:
#
#     @classmethod
#     def create_file_info(cls):
#         ...
#
#     @classmethod
#     def upload_file_to_server_by_ssh(cls):
#         ...
import requests
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import HTTPException


async def download_video(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        return StreamingResponse(BytesIO(response.content), media_type="video/mp4")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {url}. {str(e)}")
