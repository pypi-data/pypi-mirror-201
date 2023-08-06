import re

from userlex.social_media import SocialMedia


class Instagram(SocialMedia):
    PLATFORM_NAME = "instagram"

    USERNAME_REGEX = re.compile(r'insta(?:gram)?:?\s+@(?P<username>\S+)\b', re.IGNORECASE)

    def __init__(self, username):
        self.username = username

    @property
    def url(self):
        return f"https://www.instagram.com/{self.username}/"

    @staticmethod
    def from_username(username):
        return Instagram(username)

    @staticmethod
    def matches_username(username):
        return bool(Instagram.USERNAME_REGEX.fullmatch(username))
