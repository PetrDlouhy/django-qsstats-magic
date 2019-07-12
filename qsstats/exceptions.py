class QuerySetStatsError(Exception):
    pass

class InvalidInterval(QuerySetStatsError):
    pass

class InvalidOperator(QuerySetStatsError):
    pass

class DateFieldMissing(QuerySetStatsError):
    pass

class QuerySetMissing(QuerySetStatsError):
    pass
