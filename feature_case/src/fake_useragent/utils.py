import json
import os

str_types = (str,)


def load():
    """Load the browsers.json data file."""
    data_file = os.path.join(
        os.path.dirname(__file__), "data", "browsers.json"
    )
    browsers = []
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                browsers.append(json.loads(line))
    return browsers
