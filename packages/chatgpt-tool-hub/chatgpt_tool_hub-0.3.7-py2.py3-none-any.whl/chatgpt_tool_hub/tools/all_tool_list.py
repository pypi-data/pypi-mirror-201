from typing import Any, List

from chatgpt_tool_hub.chains.api.base import APIChain
from chatgpt_tool_hub.models.base import BaseLLM
from chatgpt_tool_hub.tools.base_tool import BaseTool
from chatgpt_tool_hub.tools.debug import DebugTool
from chatgpt_tool_hub.tools.meteo.api_docs_prompts import OPEN_METEO_DOCS
from chatgpt_tool_hub.tools.meteo.meteo_weather import MeteoWeatherTool
from chatgpt_tool_hub.tools.python.python_repl import PythonREPLTool
from chatgpt_tool_hub.tools.terminal.base import Terminal
from chatgpt_tool_hub.tools.web_requests import RequestsGetTool, RequestsWrapper


def _get_terminal() -> BaseTool:
    return Terminal()


def _get_python_repl() -> BaseTool:
    return PythonREPLTool()


def _get_requests() -> BaseTool:
    return RequestsGetTool(requests_wrapper=RequestsWrapper())


def _get_debug() -> BaseTool:
    return DebugTool()


def _get_arxiv() -> BaseTool:
    from chatgpt_tool_hub.tools.dev.arxiv_search import ArxivTool, ArxivAPIWrapper
    return ArxivTool(api_wrapper=ArxivAPIWrapper())


def _get_open_meteo_api(llm: BaseLLM) -> BaseTool:
    return MeteoWeatherTool(api_chain=APIChain.from_llm_and_api_docs(llm, OPEN_METEO_DOCS))


def _get_wolfram_alpha(**kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.wolfram_alpha import WolframAlphaQueryRun, WolframAlphaAPIWrapper

    return WolframAlphaQueryRun(api_wrapper=WolframAlphaAPIWrapper(**kwargs))


def _get_google_search(**kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.google_search.google_search import GoogleSearchJson, GoogleSearchAPIWrapper

    return GoogleSearchJson(api_wrapper=GoogleSearchAPIWrapper(**kwargs))


def _get_searxng_search(**kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.dev.searxng_search import SearxSearchTool, SearxSearchWrapper

    return SearxSearchTool(api_wrapper=SearxSearchWrapper(**kwargs))


def _get_bing_search(**kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.bing_search import BingSearch, BingSearchAPIWrapper

    return BingSearch(api_wrapper=BingSearchAPIWrapper(**kwargs))


def _get_wikipedia(**kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.wikipedia.wikipedia import WikipediaTool, WikipediaAPIWrapper

    return WikipediaTool(api_wrapper=WikipediaAPIWrapper(**kwargs))


def _get_news_api(llm: BaseLLM, **kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.news import NEWS_DOCS, NewsTool

    return NewsTool(api_chain=APIChain.from_llm_and_api_docs(
        llm, NEWS_DOCS, headers={"X-Api-Key": kwargs["news_api_key"]}
    ))


def _get_browser(**kwargs: Any) -> BaseTool:
    from chatgpt_tool_hub.tools.web_requests.browser import BrowserTool

    return BrowserTool(requests_wrapper=RequestsWrapper(**kwargs))


BASE_TOOLS = {
    "python": _get_python_repl,
    "requests": _get_requests,
    "terminal": _get_terminal,
    "debug": _get_debug,
    "arxiv": _get_arxiv
}

BOT_TOOLS = {
    "meteo-weather": _get_open_meteo_api,
}

BOT_WITH_KEY_TOOLS = {
    "news": (_get_news_api, ["news_api_key"]),
}

OPTIONAL_ADVANCED_TOOLS = {
    "wolfram-alpha": (_get_wolfram_alpha, ["wolfram_alpha_appid"]),
    "google-search": (_get_google_search, ["google_api_key", "google_cse_id"]),
    "bing-search": (_get_bing_search, ["bing_subscription_key"]),
    "searxng-search": (_get_searxng_search, ["searx_host"]),
    "wikipedia": (_get_wikipedia, ["top_k_results"]),
}

CUSTOM_TOOL = {
    "browser": (_get_browser, ["phantomjs_exec_path", "proxy"])
}


# used by chatgpt-on-wechat now , don't move it
def get_all_tool_names() -> List[str]:
    """Get a list of all possible tool names."""
    return (
        list(BASE_TOOLS)
        + list(BOT_TOOLS)
        + list(BOT_WITH_KEY_TOOLS)
        + list(OPTIONAL_ADVANCED_TOOLS)
        + list(CUSTOM_TOOL)
    )
