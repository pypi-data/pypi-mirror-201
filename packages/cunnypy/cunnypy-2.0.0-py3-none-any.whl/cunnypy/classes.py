import os
from typing import Any, Optional

import aiofiles
import attr
import httpx


def _match_rating(rating: str) -> str:
    """Utility function to change single letter rating to full name."""
    match rating:
        case "s":
            return "safe"
        case "q":
            return "questionable"
        case "e":
            return "explicit"
        case "g":
            return "general"
        case _:
            return rating


def _format_tags(tags: str | dict[Any, Any]) -> str:
    if not isinstance(tags, str):
        try:
            tags = " ".join(tag["name_en"] for tag in tags)
        except (AttributeError, TypeError):
            tags = " ".join(tag for tag in tags)
        return tags
    return tags


@attr.frozen
class Booru:
    """Data class used to represent a booru.

    Attributes:
        base_url: The base URL of the booru.
        api_url: The API URL of the booru.
        autocomplete_url: The URL used for autocomplete functionality.
        autocomplete_var: The variable used to fetch the autocomplete results.
    """

    name: str
    base_url: str
    api_url: str
    page_var: str
    autocomplete_url: str
    autocomplete_var: str


@attr.frozen
class BooruPost:  # type: ignore[no-untyped-def]
    """Dataclass that holds all the data for a post from a Booru.

    Attributes:
        id: The unique identifier of the post.
        md5: The MD5 hash of the post file.
        file_url: The URL of the post file.
        sample_url: The URL of the post sample file (if available).
        preview_url: The URL of the post preview file (if available).
        rating: The rating of the post (e.g. safe, questionable, explicit).
        source: The source URL of the post (if available).
        tags: A string of tags associated with the post.
    """

    id: int = attr.ib()  # noqa[A003]
    md5: str = attr.ib()
    file_url: str = attr.ib()
    sample_url: Optional[str] = attr.ib(repr=False)
    preview_url: Optional[str] = attr.ib(repr=False)
    rating: str = attr.ib(converter=lambda x: _match_rating(x))  # type:ignore[var-annotated]
    source: Optional[str] = attr.ib()
    tags: str = attr.ib(  # type:ignore[var-annotated]
        converter=lambda x: _format_tags(x),
        repr=False,
    )

    async def download_image(self, directory: str) -> str:
        """Utility method to download the current post to a directory.

        Args:
            directory: A path to the directory you want to save the image too

        Returns:
            The path to the downloaded file.

        Usage:
            >>> import cunnypy
            >>> import asyncio
            ...
            >>> async def main():
            ...     posts = await cunnypy.search("gelbooru", "megumin", limit=20, gatcha=True)
            ...     file = await posts[0].download_image("path/to/directory")
            ...     print(file)
            ...
            >>> asyncio.run(main())
            "path/to/directory/835a7d915ec267e363aaf37f2a025141.jpg"
        """
        async with httpx.AsyncClient() as client:
            res = await client.get(self.file_url)
            res.raise_for_status()
            file_name = f"{self.md5}.{res.headers['content-type'].split('/')[-1]}"
            file_path = os.path.join(directory, file_name)

            async with aiofiles.open(file_path, "wb") as f:
                await f.write(res.content)
        return file_path
