import typing as tp
from .http import HttpClient
import loguru

if tp.TYPE_CHECKING:
    import aiohttp
    import os
    from types import TracebackType


class NewsDash:
    def __init__(
        self,
        api_key: str,
        *,
        session: tp.Optional["aiohttp.ClientSession"] = None,
        file_logging: tp.Union[
            bool,
            list[
                "os.PathLike",
                tp.Union[bool, str],
                tp.Union[bool, str],
                tp.Union[bool, str],
            ],
        ] = False,
    ) -> None:
        self.logger = loguru.logger
        self.api_key = api_key
        if file_logging != False:
            file = file_logging[0]
            rotation = file_logging[1]
            retention = file_logging[2]
            compression = file_logging[3]
            self.logger.add(
                file, rotation=rotation, retention=retention, compression=compression
            )
        self._http_client = HttpClient(session=session, logger=self.logger)

    async def __aexit__(
        self,
        exc_type: tp.Optional[tp.Type[BaseException]],
        exc_val: tp.Optional[BaseException],
        exc_tb: tp.Optional["TracebackType"],
    ) -> None:
        if self._http_client.session is not None:
            await self._http_client.session.close()

    async def __aenter__(self) -> "newsdash":
        return self

    async def close(self) -> None:
        self.logger.info("Closing session")
        if self._http_client.session is not None:
            await self._http_client.session.close()

    @property
    def http_client(self) -> HttpClient:
        return self._http_client

    async def get_everything(
        self,
        *,
        query: str = None,
        searchIn: tp.Union[
            tp.Literal["title"], tp.Literal["description"], tp.Literal["body"]
        ] = None,
        sources: str = None,
        domains: str = None,
        excludeDomains: str = None,
        date_from: str = None,
        date_to: str = None,
        language: tp.Union[
            tp.Literal[
                "ar",
                "de",
                "en",
                "es",
                "fr",
                "he",
                "it",
                "nl",
                "no",
                "pt",
                "ru",
                "sv",
                "ud",
                "zh",
            ]
        ] = None,
        sortBy: tp.Union[tp.Literal["relevancy", "popularity", "publishedAt"]] = None,
        pageSize: int = None,
        page: int = None,
    ) -> tp.Any:
        params = {}
        if query is not None:
            if not isinstance(query, str):
                raise TypeError("query should be a string")
            params["q"] = query
        if searchIn is not None:
            if isinstance(searchIn, str):
                if searchIn not in ["title", "description", "body"]:
                    raise ValueError(
                        "searchIn should be one of 'title', 'description', or 'body'"
                    )
            else:
                raise TypeError("searchIn should be a string")
            params["searchIn"] = searchIn
        if sources is not None:
            if not isinstance(sources, str):
                raise TypeError("sources should be a string")
            params["sources"] = sources
        if domains is not None:
            if not isinstance(domains, str):
                raise TypeError("domains should be a string")
            params["domains"] = domains
        if excludeDomains is not None:
            if not isinstance(excludeDomains, str):
                raise TypeError("excludeDomains should be a string")
                params["excludeDomains"] = excludeDomains
        if date_from is not None:
            if not isinstance(date_from, str):
                raise TypeError("date_from should be a string")
            params["from"] = date_from
        if date_to is not None:
            if not isinstance(date_to, str):
                raise TypeError("date_to should be a string")
            params["to"] = date_to
        if language is not None:
            if isinstance(language, str):
                if language not in [
                    "ar",
                    "de",
                    "en",
                    "es",
                    "fr",
                    "he",
                    "it",
                    "nl",
                    "no",
                    "pt",
                    "ru",
                    "sv",
                    "ud",
                    "zh",
                ]:
                    raise ValueError(
                        "language should be one out of the languages provided by newsapi"
                    )
            else:
                raise TypeError("language should be a string")
            params["language"] = language
        if sortBy is not None:
            if isinstance(sortBy, str):
                if sortBy not in ["relevancy", "popularity", "publishedAt"]:
                    raise ValueError(
                        "sortBy should be one out of relevancy, popularity or publishedAt"
                    )
            else:
                raise TypeError("sortBy should be a string")
            params["sortBy"] = sortBy
        if pageSize is not None:
            if isinstance(pageSize, int):
                if pageSize < 0:
                    raise ValueError("pageSize should be greater than 0")
            else:
                raise TypeError("pageSize should be an integer")
            params["pageSize"] = pageSize
        if page is not None:
            if isinstance(page, int):
                if page < 0:
                    raise ValueError("page should be greater than 0")
            else:
                raise TypeError("page should be an integer")
            params["page"] = page
        headers = {"X-Api-Key": self.api_key}
        data = await self._http_client.get(
            "https://newsapi.org/v2/everything", "GET", headers=headers, params=params
        )
        return data

    async def get_top_headlines(
        self,
        *,
        country: tp.Union[
            tp.Literal[
                "ae",
                "ar",
                "at",
                "au",
                "be",
                "bg",
                "br",
                "ca",
                "ch",
                "cn",
                "co",
                "cu",
                "cz",
                "de",
                "eg",
                "fr",
                "gb",
                "gr",
                "hk",
                "hu",
                "id",
                "ie",
                "il",
                "in",
                "it",
                "jp",
                "kr",
                "lt",
                "lv",
                "ma",
                "mx",
                "my",
                "ng",
                "nl",
                "no",
                "nz",
                "ph",
                "pl",
                "pt",
                "ro",
                "rs",
                "ru",
                "sa",
                "se",
                "sg",
                "si",
                "sk",
                "th",
                "tr",
                "tw",
                "ua",
                "us",
                "ve",
                "za",
            ]
        ] = None,
        category: tp.Union[
            tp.Literal[
                "business",
                "entertainment",
                "general",
                "health",
                "science",
                "sports",
                "technology",
            ]
        ] = None,
        sources: str = None,
        query: str = None,
        pageSize: int = None,
        page: int = None,
    ) -> tp.Any:
        params = {}
        if country is not None:
            if country not in [
                "ae",
                "ar",
                "at",
                "au",
                "be",
                "bg",
                "br",
                "ca",
                "ch",
                "cn",
                "co",
                "cu",
                "cz",
                "de",
                "eg",
                "fr",
                "gb",
                "gr",
                "hk",
                "hu",
                "id",
                "ie",
                "il",
                "in",
                "it",
                "jp",
                "kr",
                "lt",
                "lv",
                "ma",
                "mx",
                "my",
                "ng",
                "nl",
                "no",
                "nz",
                "ph",
                "pl",
                "pt",
                "ro",
                "rs",
                "ru",
                "sa",
                "se",
                "sg",
                "si",
                "sk",
                "th",
                "tr",
                "tw",
                "ua",
                "us",
                "ve",
                "za",
            ]:
                raise ValueError(
                    "country should be one out of the countries provided by news api"
                )
            params["country"] = country
        if category is not None:
            if category not in [
                "business",
                "entertainment",
                "general",
                "health",
                "science",
                "sports",
                "technology",
            ]:
                raise ValueError(
                    "category should be one out of the categories provided by news api"
                )
            params["category"] = category
        if sources is not None:
            if not isinstance(sources, str):
                raise TypeError("sources should be an string")
            params["sources"] = sources
        if query is not None:
            if not isinstance(query, str):
                raise TypeError("query should be an string")
            params["q"] = query
        if pageSize is not None:
            if not isinstance(pageSize, int):
                raise TypeError("pageSize should be an integer")
            params["pageSize"] = pageSize
        if page is not None:
            if not isinstance(page, int):
                raise TypeError("page should be an integer")
            params["page"] = page
        headers = {"X-Api-Key": self.api_key}
        data = await self._http_client.get(
            "https://newsapi.org/v2/top-headlines",
            "GET",
            headers=headers,
            params=params,
        )
        return data

    async def get_sources(
        self,
        *,
        country: tp.Union[
            tp.Literal[
                "ae",
                "ar",
                "at",
                "au",
                "be",
                "bg",
                "br",
                "ca",
                "ch",
                "cn",
                "co",
                "cu",
                "cz",
                "de",
                "eg",
                "fr",
                "gb",
                "gr",
                "hk",
                "hu",
                "id",
                "ie",
                "il",
                "in",
                "it",
                "jp",
                "kr",
                "lt",
                "lv",
                "ma",
                "mx",
                "my",
                "ng",
                "nl",
                "no",
                "nz",
                "ph",
                "pl",
                "pt",
                "ro",
                "rs",
                "ru",
                "sa",
                "se",
                "sg",
                "si",
                "sk",
                "th",
                "tr",
                "tw",
                "ua",
                "us",
                "ve",
                "za",
            ]
        ] = None,
        language: tp.Union[
            tp.Literal[
                "ar",
                "de",
                "en",
                "es",
                "fr",
                "he",
                "it",
                "nl",
                "no",
                "pt",
                "ru",
                "se",
                "ud",
                "zh",
            ]
        ] = None,
        category: tp.Union[
            tp.Literal[
                "business",
                "entertainment",
                "general",
                "health",
                "science",
                "sports",
                "technology",
            ]
        ] = None,
    ) -> tp.Any:
        params = {}
        if country is not None:
            if country not in [
                "ae",
                "ar",
                "at",
                "au",
                "be",
                "bg",
                "br",
                "ca",
                "ch",
                "cn",
                "co",
                "cu",
                "cz",
                "de",
                "eg",
                "fr",
                "gb",
                "gr",
                "hk",
                "hu",
                "id",
                "ie",
                "il",
                "in",
                "it",
                "jp",
                "kr",
                "lt",
                "lv",
                "ma",
                "mx",
                "my",
                "ng",
                "nl",
                "no",
                "nz",
                "ph",
                "pl",
                "pt",
                "ro",
                "rs",
                "ru",
                "sa",
                "se",
                "sg",
                "si",
                "sk",
                "th",
                "tr",
                "tw",
                "ua",
                "us",
                "ve",
                "za",
            ]:
                raise ValueError(
                    "country should be one out of the countries provided by news api"
                )
            params["country"] = country
        if category is not None:
            if category not in [
                "business",
                "entertainment",
                "general",
                "health",
                "science",
                "sports",
                "technology",
            ]:
                raise ValueError(
                    "category should be one out of the categories provided by newsapi"
                )
            params["category"] = category
        if language is not None:
            if language not in [
                "ar",
                "de",
                "en",
                "es",
                "fr",
                "he",
                "it",
                "nl",
                "no",
                "pt",
                "ru",
                "se",
                "ud",
                "zh",
            ]:
                raise ValueError(
                    "language should be one out of languages provided by newsapi"
                )
        headers = {"X-Api-Key": self.api_key}
        data = await self._http_client.get(
            "https://newsapi.org/v2/top-headlines",
            "GET",
            headers=headers,
            params=params,
        )
        return data
