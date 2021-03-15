from django.contrib.auth.decorators import user_passes_test


def group_required(*groups):
    def in_groups(u):
        if u.is_authenticated:
            if u.is_admin() or u.groups.filter(name__in=groups).exists():
                return True
        return False
    return user_passes_test(in_groups)


class GROUPS:
    registered = 'Registered'
    privileged = 'Privileged'
    admin = 'Admin'