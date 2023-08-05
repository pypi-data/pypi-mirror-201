from typing import Iterator

from hypersquirrel.scraper.ehen import _to_post_id


def interpret(url: str) -> Iterator[dict]:
    post_id = _to_post_id(url)
    yield {
        "fileid": post_id,
        "filename": f"ehentai {post_id}",
        "sourceurl": url,
        "tags": [
            "ehentai"
        ]
    }
