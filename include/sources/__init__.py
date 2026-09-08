# include/sources/__init__.py

from include.sources import ashby, bamboohr

PARSERS = {
    "ashby": ashby.parse,
    "bamboohr": bamboohr.parse,
}