from ..common.exceptions import NotAuthorizedError


def auth_required(func):
    def function(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except NotAuthorizedError:
            self.auth()
            return func(self, *args, **kwargs)

    return function
