from django.http import HttpResponse
from django.shortcuts import redirect

# custom decorator which is the role and permission of a user


def unauthurizedUser(view_func):
    def wrapping_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapping_func


# to which shall be allowed..
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapping_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Sorry You  are not permit to enter..!!')

        return wrapping_func

    return decorator


def admin_only(view_func):
    def wrapping_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'customers':
                return redirect('user')

            if group == 'admin':
                return view_func(request, *args, **kwargs)

    return wrapping_func
