from pydantic_settings import BaseSettings, SettingsConfigDict


class NextCLoudSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    NEXTCLOUD_API_ENDPOINT: str
    NEXTCLOUD_API_NAME: str
    NEXTCLOUD_API_PASSWORD: str

    @property
    def nextcloud_api(self):
        _nextcloud_api = {
            'nextcloud_url': self.NEXTCLOUD_API_ENDPOINT,
            'nc_auth_user': self.NEXTCLOUD_API_NAME,
            'nc_auth_passwd': self.NEXTCLOUD_API_PASSWORD
        }
        return _nextcloud_api
