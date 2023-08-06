import re


class SocialMedia:
    PLATFORMS = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        SocialMedia.PLATFORMS[cls.PLATFORM_NAME] = cls

    @staticmethod
    def from_username(username):
        # create a new instance of the child class
        raise NotImplementedError

    @staticmethod
    def matches_username(username):
        raise NotImplementedError

    @classmethod
    def register_platform(cls, name, platform_class):
        cls.PLATFORMS[name] = platform_class

    @staticmethod
    def parse(text):
        """Extract social media objects from user text."""
        social_media = []
        # simple text pre-processing
        # remove "is" using `re.sub`
        text = re.sub(r"\bis\b", " ", text)
        # remove repeated whitespaces
        text = re.sub(r'\s+', ' ', text)
        for platform_class in SocialMedia.PLATFORMS.values():
            for match in platform_class.USERNAME_REGEX.finditer(text):
                username = match.group("username")
                platform = platform_class(username)
                if platform and platform not in social_media:
                    social_media.append(platform)

        return social_media
