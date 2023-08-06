import aiohttp
import typing as tp
from .exceptions import HTTPException


class HttpClient:
    def __init__(
        self, *, session: tp.Optional[aiohttp.ClientSession] = None, logger
    ) -> None:
        self.session = session
        self.logger = logger

    async def connect(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self.logger.info("successfully connected to the http client")

    async def get(
        self, url: str, method: str, params: dict = {}, headers: dict = {}
    ) -> tp.Any:
        if self.session is None:
            await self.connect()
        if self.session is not None:
            async with self.session.request(
                method, url, params=params, headers=headers
            ) as response:
                if 300 > response.status >= 200:
                    return await response.json()
                else:
                    resp = await response.json()
                    message = f"received status code {response.status} with code > {resp['code']}"
                    self.logger.error(message)
                    raise HTTPException.from_response(await response.json())
        else:
            raise HTTPException("No session was provided")
