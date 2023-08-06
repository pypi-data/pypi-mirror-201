import warnings

from jinja2 import Environment
from jinja2.ext import Extension

from .filters import FilterModule


class MatrixFiltersExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        filters = FilterModule().filters()
        for x in filters:
            if x in environment.filters:
                warnings.warn(
                    "Filter name collision detected changing "
                    "filter name to ans_{0} "
                    "to avoid clobbering".format(x),
                    RuntimeWarning,
                )
                filters["ans_" + x] = filters[x]
                del filters[x]

        # Register provided filters
        environment.filters.update(filters)
