from dataclasses import dataclass


@dataclass
class CacheStats:

    hits: int = 0
    misses: int = 0

