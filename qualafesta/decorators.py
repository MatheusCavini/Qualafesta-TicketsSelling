from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.models import Group

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                group = Group.objects.get(name=group_name)
                if group in request.user.groups.all():
                    return view_func(request, *args, **kwargs)
            return redirect('pagina_de_erro')  
        return wrapper
    return decorator
