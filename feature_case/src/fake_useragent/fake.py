import random

from fake_useragent import settings
from fake_useragent.errors import FakeUserAgentError
from fake_useragent.log import logger
from fake_useragent.utils import load, str_types


class FakeUserAgent:
    def __init__(
        self,
        browsers=["chrome", "edge", "firefox", "safari"],
        os=["windows", "macos", "linux"],
        platforms=["pc", "mobile", "tablet"],
        min_percentage=0.0,
        min_version=0.0,
        fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        safe_attrs=tuple(),
    ):
        # Check inputs
        assert isinstance(browsers, (list, str)), "browsers must be list or string"
        if isinstance(browsers, str):
            browsers = [browsers]
        self.browsers = [b.lower() for b in browsers]

        assert isinstance(os, (list, str)), "OS must be list or string"
        if isinstance(os, str):
            os = [os]
        # OS replacement (windows -> [win10, win7])
        self.os = []
        for os_name in os:
            os_name = os_name.lower()
            if os_name in settings.OS_REPLACEMENTS:
                self.os.extend(settings.OS_REPLACEMENTS[os_name])
            else:
                self.os.append(os_name)

        assert isinstance(platforms, (list, str)), "platforms must be list or string"
        if isinstance(platforms, str):
            platforms = [platforms]
        self.platforms = [p.lower() for p in platforms]

        # Include common mobile/tablet OS values when those platforms are requested
        if any(p in {"mobile", "tablet"} for p in self.platforms):
            for extra_os in ("android", "ios"):
                if extra_os not in self.os:
                    self.os.append(extra_os)

        assert isinstance(
            min_percentage, float
        ), "Minimum usage percentage must be float"
        self.min_percentage = min_percentage

        assert isinstance(min_version, (int, float)), "Minimum version must be int or float"
        self.min_version = float(min_version)

        assert isinstance(fallback, str), "fallback must be string"
        self.fallback = fallback

        assert isinstance(
            safe_attrs, (list, set, tuple)
        ), "safe_attrs must be list\\tuple\\set of strings or unicode"

        if safe_attrs:
            str_types_safe_attrs = [isinstance(attr, str_types) for attr in safe_attrs]

            assert all(
                str_types_safe_attrs
            ), "safe_attrs must be list\\tuple\\set of strings or unicode"
        self.safe_attrs = set(safe_attrs)

        # Next, load our local data file into memory (browsers.json)
        self.data_browsers = load()

    def _normalize_request(self, value):
        """Normalize browser name input using replacements and shortcuts."""
        for repl_value, replacement in settings.REPLACEMENTS.items():
            value = value.replace(repl_value, replacement)
        value = value.lower()
        return settings.SHORTCUTS.get(value, value)

    def _entry_matches(self, entry, browser_name):
        """Return True if an entry matches the current filters and browser_name."""
        browser_ok = (
            entry["browser"] in self.browsers
            if browser_name == "random"
            else entry["browser"] == browser_name
        )
        return (
            browser_ok
            and entry["os"] in self.os
            and entry["percent"] >= self.min_percentage
            and entry["type"] in self.platforms
            and entry["version"] >= self.min_version
        )

    def _filter_browsers(self, browser_name):
        return [entry for entry in self.data_browsers if self._entry_matches(entry, browser_name)]

    # This method will return an object
    # Usage: ua.getBrowser('firefox')
    def getBrowser(self, request):
        try:
            request = self._normalize_request(request)
            filtered_browsers = self._filter_browsers(request)

            # Pick a random browser user-agent from the filtered browsers
            # And return the full dict
            return random.choice(filtered_browsers)  # noqa: S311
        except (KeyError, IndexError):
            if self.fallback is None:
                raise FakeUserAgentError(
                    f"Error occurred during getting browser: {request}"
                )  # noqa
            else:
                logger.warning(
                    f"Error occurred during getting browser: {request}, "
                    "but was suppressed with fallback.",
                )
                # Return fallback object
                return {
                    "useragent": self.fallback,
                    "system": "Chrome 114.0 Win10",
                    "browser": "chrome",
                    "version": 114.0,
                    "os": "win10",
                    "type": "pc",
                }

    # This method will use the method below, returning a string
    # Usage: ua['random']
    def __getitem__(self, attr):
        return self.__getattr__(attr)

    # This method will returns a string
    # Usage: ua.random
    def __getattr__(self, attr):
        if attr in self.safe_attrs:
            return super(UserAgent, self).__getattr__(attr)

        try:
            attr = self._normalize_request(attr)
            filtered_browsers = self._filter_browsers(attr)

            # Pick a random browser user-agent from the filtered browsers
            # And return the useragent string.
            return random.choice(filtered_browsers).get("useragent")  # noqa: S311
        except (KeyError, IndexError):
            if self.fallback is None:
                raise FakeUserAgentError(
                    f"Error occurred during getting browser: {attr}"
                )  # noqa
            else:
                logger.warning(
                    f"Error occurred during getting browser: {attr}, "
                    "but was suppressed with fallback.",
                )

                return self.fallback

    @property
    def chrome(self):
        return self.__getattr__("chrome")

    @property
    def googlechrome(self):
        return self.chrome

    @property
    def google_chrome(self):
        return self.chrome

    @property
    def firefox(self):
        return self.__getattr__("firefox")

    @property
    def ff(self):
        return self.firefox

    @property
    def safari(self):
        return self.__getattr__("safari")

    @property
    def edge(self):
        return self.__getattr__("edge")

    @property
    def random(self):
        return self.__getattr__("random")

    @property
    def getChrome(self):
        return self.getBrowser("chrome")

    @property
    def getFirefox(self):
        return self.getBrowser("firefox")

    @property
    def getSafari(self):
        return self.getBrowser("safari")

    @property
    def getEdge(self):
        return self.getBrowser("edge")

    @property
    def getRandom(self):
        return self.getBrowser("random")


# Alias for convenience
UserAgent = FakeUserAgent
