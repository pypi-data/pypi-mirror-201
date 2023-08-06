from typing import Any, List


class AsyncIterator:

    def __init__(self, values: List[Any]):
        self.values = values
        self.idx = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.values:
            raise StopAsyncIteration
        return self.values.pop(0)
