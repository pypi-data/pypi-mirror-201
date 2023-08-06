from django.conf import settings
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.auth import get_user_model


def is_anonymous_user(user):
    if  user is None or user.is_anonymous:
        return True
    User = get_user_model()
    username = getattr(user, User.USERNAME_FIELD)
    if hasattr(settings, 'ANONYMOUS_USER_NAME'):
        anon_username = settings.ANONYMOUS_USER_NAME

    else:
        from guardian.conf import settings as guardian_settings
        anon_username = guardian_settings.ANONYMOUS_USER_NAME
    return anon_username and anon_username == username


def changelist_no_args(action_name, model):
    def decorator(function):
        def wrapper(self, request, *args, **kwargs):
            if 'action' in request.POST:
                if (type(action_name) == list and request.POST['action'] in action_name) or request.POST['action'] == action_name:
                    if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                        post = request.POST.copy()
                        for u in model.objects.all():
                            post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                        request._set_post(post)
            function(self, request, *args, **kwargs)
            return super(self.__class__, self).changelist_view(request, *args, **kwargs)
        return wrapper
    return decorator