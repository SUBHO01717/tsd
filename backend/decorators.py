from django.core.exceptions import PermissionDenied
from accounts.models import *
from backend.models import *

def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request, *args, **kwargs):
            try:
                user_role = request.user.UserProfile.userrole
                if user_role in allowed_roles:
                    return func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            except UserProfile.DoesNotExist:
                raise PermissionDenied
        return wrap
    return decorator
