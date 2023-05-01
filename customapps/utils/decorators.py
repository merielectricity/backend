
from functools import wraps
from django.http import JsonResponse

def login_forbidden(view_func,status=403):
    """
    Only allow anonymous users to access this view.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({"error":"Logout and try again"},status=status)

    return _checklogin

def login_required(view_func,status=403):
    """
    Only allow anonymous users to access this view.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({"error":"Login and try again"},status=status)

    return _checklogin