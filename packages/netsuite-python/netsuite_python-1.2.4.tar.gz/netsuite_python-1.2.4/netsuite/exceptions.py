class NetsuiteException(Exception):
    pass


class NetsuiteForbiddenException(NetsuiteException):
    pass


class NetsuiteUnauthorizedException(NetsuiteException):
    pass


class NetsuiteTokenExpiredException(NetsuiteException):
    pass
