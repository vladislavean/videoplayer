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
import uuid

import requests
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, Response
import httpx


async def download_video(url: str, archive_id: uuid.UUID):
    async with httpx.AsyncClient() as client:
        response_video = await client.get(url)

    if response_video.status_code == 200:
        video_stream = BytesIO(response_video.content)
        return Response(content=video_stream.getvalue(), headers={
            "Content-Disposition": f"attachment; filename={str(archive_id)}.mp4",
            "Content-Type": response_video.headers.get("Content-Type", "application/octet-stream"),
        })
    else:
        raise HTTPException(status_code=500, detail=f"Error download video from {url}")


async def streaming_video(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return StreamingResponse(BytesIO(response.content), media_type="video/mp4")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error streaming video: {url}. {str(e)}")
