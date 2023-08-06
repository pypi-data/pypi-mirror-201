from the_spymaster_util.http.errors import APIError


class SpymasterSolversError(APIError):
    pass


SERVICE_ERRORS = frozenset({SpymasterSolversError})
