from urllib.parse import urlparse

from services.entries import ContentType


def get_content_type(url: str) -> ContentType | None:
    domain_map = {
        "www.youtube.com": ContentType.YOUTUBE,
        "youtu.be": ContentType.YOUTUBE,
        "tiktok.com": ContentType.TIKTOK,
        "www.tiktok.com": ContentType.TIKTOK,
        "vt.tiktok.com": ContentType.TIKTOK,
        "vk.com": ContentType.VK,
        "www.vk.com": ContentType.VK,
        "twitch.tv": ContentType.TWITCH,
        "www.twitch.tv": ContentType.TWITCH,
        "clips.twitch.tv": ContentType.TWITCH,
    }
    parsed_url = urlparse(url)
    return domain_map.get(parsed_url.netloc, None)
