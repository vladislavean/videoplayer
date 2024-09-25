import uuid
from fastapi import HTTPException
from app.storage.settings import StorageSettings
from app.database.settings import PostgreSettings
import asyncssh
import tempfile


class StorageSSH:
    async def _connection_by_ssh(
            self,
    ):
        try:
            connection = await asyncssh.connect(host=PostgreSettings.DB_HOST,
                                                port=22,
                                                username=StorageSettings.SSH_NAME,
                                                password=StorageSettings.SSH_PASS)
            return connection
        except asyncssh.connection.ServiceNotAvailable as e:
            raise HTTPException(status_code=500, detail=f"Connection Faild! ServiceNotAvailable. {e}")
        except asyncssh.connection.PermissionDenied as e:
            raise HTTPException(status_code=403, detail=f"Permission Denied. {e}")

    async def upload_archive(
            self,
            archive_id: uuid.UUID,
            archive_in_bytes: bytes,
            street_id: str
    ):
        async with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(archive_in_bytes)
            temp_file_path = temp_file.name

        connection = await self._connection_by_ssh()
        async with connection.start_sftp() as sftp_client:
            await sftp_client.put(temp_file_path, f'/files/{street_id}/{archive_id}.mp4')

