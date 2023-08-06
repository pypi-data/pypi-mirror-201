from __future__ import annotations

from encrawler.spiders.bing import BingSpider
# 抄的pandas的, 学习pandas的import机制


__docformat__ = "restructuredtext"

# Let users know if they're missing any of our hard dependencies
_hard_dependencies = ("requests", "loguru", "pydantic", "tqdm", "lxml")
_missing_dependencies = []

for _dependency in _hard_dependencies:
    try:
        __import__(_dependency)
    except ImportError as _e:
        _missing_dependencies.append(f"{_dependency}: {_e}")

if _missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(_missing_dependencies)
    )
del _hard_dependencies, _dependency, _missing_dependencies






from spiders.bing import BingSpider, BingNewsSpider




__all__ = [
    "BingSpider", "BingNewsSpider"
]

