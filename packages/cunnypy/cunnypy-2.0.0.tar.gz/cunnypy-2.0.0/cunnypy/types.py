from typing import Literal, Optional, TypedDict

SiteNames = Literal[
    "safebooru",
    "realbooru",
    "gelbooru",
    "hypnohub",
    "rule34",
    "xbooru",
    "tbib",
    "atfbooru",
    "sankaku",
    "lolibooru",
    "danbooru",
    "konachannet",
    "konachan",
    "yandere",
]


class MutliBooru(TypedDict):
    """Typing class to help make sure users type out correct args.

    Attributes:
        booru: The name or alias of the booru.
        limit: The maximum number of posts to return. Defaults to 10. The maximum value is 1000.
        creds: A dictionary of credentials to use for authentication.
        tags: A string of tags to browse for
    Usage:
        {"booru": "gel", "limit": 10, "page": 1, "creds": {'api_key': 123, 'user_id': 123}}.
    """

    booru: SiteNames | str
    limit: Optional[int]
    page: Optional[int]
    creds: Optional[dict[str, str]]
