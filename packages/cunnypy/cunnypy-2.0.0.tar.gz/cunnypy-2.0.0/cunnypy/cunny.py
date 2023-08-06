import asyncio
import random
import re
from pathlib import Path
from typing import Any, List, Optional, no_type_check

import aiofiles
import httpx
import rtoml
import xmltodict

from .classes import Booru, BooruPost
from .types import MutliBooru, SiteNames

__all__ = ("search", "multi_search", "autocomplete")

headers = {"User-Agent": "Cunnypy/v2.0.0 (https://pypi.org/project/cunnypy)"}
max_posts = 100


async def _get_booru(booru: SiteNames | str) -> "Booru":
    """Utility function to grad the right booru from `boorus.toml`.

    Args:
        booru: booru name or alias.

    Returns:
        Booru dataclass.

    Raises:
        ValueError: Errors out when it can't find a booru.
    """
    booru_file = Path(__file__).parent / "boorus.toml"
    async with aiofiles.open(booru_file, "r") as f:
        boorus = rtoml.load(await f.read())

        for k, v in boorus.items():
            if k == booru or booru in v["aliases"]:
                return Booru(k, v["base"], v["api"], v["page_var"], v["auto"], v["auto_var"])
        raise ValueError(f"No booru exists with alias/name: {booru}")


@no_type_check
async def _parse_data(data: dict[Any, Any]) -> BooruPost:
    keys = " ".join(data.keys())

    post_id = data.get(re.search(r"(@?id)", keys).group())
    file_url = data.get(re.search(r"(@?file_url|file\b)", keys).group(0))
    md5 = data.get(re.search(r"(@?md5|hash|file\b)", keys).group())
    sample = data.get(re.search(r"(@?sample(?:_url)? | large_file_url)", keys).group())
    preview = data.get(re.search(r"(@?preview(?:(?:_file)?_url)?)", keys).group())
    rating = data.get(re.search(r"(@?rating)", keys).group())
    source = data.get(re.search(r"(@?sources?)", keys).group())
    tags = data.get(re.search(r"(@?tags?(?:_string)?)", keys).group())

    if isinstance(file_url, dict):
        file_url = file_url.get("url")
    if isinstance(md5, dict):
        md5 = md5.get("md5")
    if isinstance(sample, dict):
        sample = sample.get("url")
    if isinstance(preview, dict):
        preview = preview.get("url")
    if isinstance(tags, dict):
        tags = tags.get("general")
    if isinstance(source, list):
        source = source[0]

    return BooruPost(post_id, md5, file_url, sample, preview, rating, source, tags)


async def _search(
    name: SiteNames | str,
    tags: str,
    limit: Optional[int] = 10,
    page: Optional[int] = 1,
    credentials: Optional[dict[str, str]] = None,
    auto: Optional[bool] = None,
) -> Optional[List[BooruPost]]:
    booru = await _get_booru(name)
    if not limit:
        limit = 10
    limit = max_posts if limit > max_posts else limit

    # Checks
    if booru.name == "gelbooru" and "rating:safe" in tags:
        tags.replace("rating:safe", "rating:general")

    if auto:
        auto_tags = [await autocomplete(booru.name, tag) for tag in tags.split(" ")]
        final_tags = [tag[0] for tag in auto_tags]
        tags = " ".join(final_tags)

    # Setup parameters
    params = {
        "limit": limit,
        "tags": tags,
        booru.page_var: page,
        **(credentials or {}),
    }

    async with httpx.AsyncClient(headers=headers, base_url=booru.base_url, follow_redirects=True, max_redirects=1) as c:
        res = await c.get(booru.api_url, params=params)  # type:ignore[arg-type]
        res.raise_for_status()

        # Return if no posts found
        if not res.text:
            return []

        # Extract the JSON data from the response object
        data = xmltodict.parse(res.text) if res.text.startswith("<?xml") else res.json()

        # Extract the list of posts
        match booru.name:
            case "hypnohub" | "realbooru" | "safebooru" | "tbib" | "xbooru":
                if int(data.get("posts").get("@count")) == 0:
                    return []
                data = data["posts"]["post"]

                if not isinstance(data, list):  # ??????????????
                    data = [data]
            case "gelbooru":
                data = data["post"]
            case "e621" | "e926":
                data = data["posts"]
            case "danbooru":
                data = [d for d in data if not d.get("is_banned")]
            case _:
                data = data

        # Parse all the data
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(_parse_data(d)) for d in data]

        # Return BooruPosts
        return [task.result() for task in tasks]


async def search(
    booru: SiteNames | str,
    tags: str,
    limit: Optional[int] = 10,
    page: Optional[int] = 1,
    gatcha: Optional[bool] = None,
    auto: Optional[bool] = None,
    credentials: dict[str, str] | None = None,
) -> Optional[List[BooruPost]]:
    """Searches the specified booru for posts matching the specified tags.

    Args:
        booru: The name or alias of the booru to search on.
        tags: The tags to search for.
        limit: The maximum number of posts to return. Defaults to 10. The maximum value is 1000.
        page: The starting page to fetch posts from. Defaults to 1.
        gatcha: Whether to use gatcha mode or not. If True, the posts will be randomized. Defaults to False.
        auto: Whether to run autocomplete on the tags you have provided.
        credentials: A dictionary of credentials to use for authentication.

    Returns:
        A list of Post objects representing the matching posts, or None if the search returned no results.

    Raises:
        httpx.HTTPError: If there is an error with the HTTP request.
        AttributeError: If an alias fails to fetch the appropriate booru.

    Usage:
        >>> import cunnypy
        >>> import asyncio
        ...
        >>> async def main():
        ...     posts = await cunnypy.search("gelbooru", "megumin", limit=20, gatcha=True)
        ...     print(posts)
        ...
        >>> asyncio.run(main())
    """
    posts = await _search(booru, tags, limit, page, credentials, auto)

    if gatcha:
        random.shuffle(posts)  # type:ignore[arg-type]
    return posts


async def multi_search(
    booru_args: list[MutliBooru], tags: str, gatcha: Optional[bool] = None
) -> Optional[list[BooruPost]]:
    """Searches multiple boorus for posts matching the specified tags.

    Args:
        booru_args: Specialized args for handling booru name, limit, page and credentials.
        tags: The tags to search for.
        gatcha: Whether to use gatcha mode or not. If True, the posts will be randomized. Defaults to False.

    Returns:
        A list of Post objects representing the matching posts, or None if the search returned no results.

    Raises:
        ExceptionGroup: Exception group of errors if there is an error with the tasks.
    Usage:
        >>> import cunnypy
        >>> import asyncio
        ...
        >>> async def main():
        ...     posts = await cunnypy.ms([{'booru':'gel'},{'booru':'safe'}], "megumin", gatcha=True)
        ...     print(posts)
        ...
        >>> asyncio.run(main())
    """
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(
                _search(
                    b["booru"],
                    tags,
                    b.get("limit"),
                    b.get("page"),
                    b.get("creds"),
                    auto=True,  # Autocomplete enabled by default to attempt maximum compatibility.
                )
            )
            for b in booru_args
        ]

    results = [task.result() for task in tasks]
    posts = [p for x in results for p in x if x]  # type:ignore[union-attr]
    if gatcha:
        random.shuffle(posts)
    return posts


async def autocomplete(site: SiteNames | str, query: str, limit: Optional[int] = 20) -> list[str]:
    """Retrieves a list of autocomplete suggestions for the given booru.

    Args:
        site: The name or alias of the booru to search on.
        query: The string to search for, which will be used to retrieve the autocomplete suggestions.
        limit: The maximum number of suggestions to return. Defaults to 20. The maximum value is 100.

    Returns:
        list[str]: A list of strings representing the autocomplete suggestions.
    Usage:
        >>> import asyncio
        >>> import cunnypy
        ...
        >>> async def main():
        ...     auto = await cunnypy.auto("gel", "megumi*")
        ...     print(auto)
        ...
        >>> asyncio.run(main())
        "['megumin', 'megumin_(cosplay)', 'megumiya', ...]"
    """
    booru = await _get_booru(site)
    query = f"{query}*" if booru.name == "aftbooru" and "*" not in query else query  # thanks ATF

    async with httpx.AsyncClient(headers=headers, base_url=booru.base_url) as c:
        params = {
            "limit": min(limit, 100),  # type:ignore[type-var]
            booru.autocomplete_var: query,
        }
        res = await c.get(f"{booru.autocomplete_url}", params=params)
        res.raise_for_status()

        return [d.get("value") or d.get("name") or d.get("name_en") for d in res.json()]
