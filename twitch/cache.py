from datetime import timedelta, datetime
from typing import Dict, Optional


class Cache:
    EXPIRATION_FIELD: str = "CACHE_EXPIRATION"

    def __init__(self, duration: Optional[timedelta] = None):
        self._store: Dict[str, dict] = {}
        self._duration: timedelta = duration or timedelta(minutes=30)

    def get(self, key: str, ignore_expiration: bool = False) -> Optional[dict]:
        if self.has(key) and (ignore_expiration or not self.expired(key)):
            return self._store[key]['value']
        else:
            return None

    def set(self, key: str, value: dict, duration: Optional[timedelta] = None) -> datetime:
        expiration: datetime = datetime.now() + (duration or self._duration)

        self._store[key] = {**{'value': value}, **{f'{Cache.EXPIRATION_FIELD}': expiration}}
        return expiration

    def has(self, key: str) -> bool:
        return key in self._store.keys()

    def expired(self, key: str) -> bool:
        return self.has(key) and self._store[key][Cache.EXPIRATION_FIELD] < datetime.now()

    def set_expiration(self, key: str, expiration: datetime) -> None:
        if self.has(key):
            self._store[key][Cache.EXPIRATION_FIELD] = expiration

    def extend(self, key: str, duration: timedelta) -> Optional[datetime]:
        if self.has(key):
            self._store[key][Cache.EXPIRATION_FIELD] += duration
            return self._store[key][Cache.EXPIRATION_FIELD]

    def flush(self) -> None:
        self._store.clear()

    def remove(self, key) -> None:
        if self.has(key):
            del self._store[key]

    def clean(self) -> None:
        [self.remove(key) for key in list(self._store.keys()) if self.expired(key)]
