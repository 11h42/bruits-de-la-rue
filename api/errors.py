# Api error code : XYYZZ
# X API version
# YY Model attached
# ZZ error number

error_codes = {
    # global
    "10900": "The json sent is not a valid json",
    "10666": "Une erreur inconnue est survenue",
    "10215": "La date de debut de votre annonce doit etre anterieure a la date de fin",
    "10216": "Vous n'avez pas le droit de modifier cette annonce",
    "10217": "Vous ne pouvez accepter votre propre annonce"
}


class BadParameterError(Exception):
    """
    Bad parameter exception
    """

    def __init__(self, parameter):
        self.code = 10410
        self.message = error_codes['10410'] % parameter