# Permissions

def _base_not_required(view_func, *args: str):
    for arg in args:
        setattr(view_func, f'{arg}nr', True)
    return view_func


def admin_not_required(view_func):
    return _base_not_required(view_func, 'a')


def login_not_required(view_func):
    return _base_not_required(view_func, 'l')


def wip_not_required(view_func):
    return _base_not_required(view_func, 'wip')


def no_any_required(view_func):
    return _base_not_required(view_func, 'a', 'l', 'wip')
