class NoOpTraceId:
    """
    A trace ID tracks the path of a request through your application.
    A trace collects all the segments generated by a single request.
    A trace ID is required for a segment.
    """
    VERSION = '1'
    DELIMITER = '-'

    def __init__(self):
        """
        Generate a no-op trace id.
        """
        self.start_time = '00000000'
        self.__number = '000000000000000000000000'

    def to_id(self):
        """
        Convert TraceId object to a string.
        """
        return "%s%s%s%s%s" % (NoOpTraceId.VERSION, NoOpTraceId.DELIMITER,
                               self.start_time,
                               NoOpTraceId.DELIMITER, self.__number)
