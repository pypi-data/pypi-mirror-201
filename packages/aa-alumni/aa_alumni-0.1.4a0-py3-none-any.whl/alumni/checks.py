from django.core.checks import Info


def esi_endpoint_offline(*args, **kwargs):
    errors = []
    errors.append(Info(
        'Corp History Endpoint Offline',
        hint='Alumni will be unable to update Character Corporation Histories until CCP restore this endpoint https://github.com/esi/esi-issues/blob/master/changelog.md#2023-01-09'))
    return errors
