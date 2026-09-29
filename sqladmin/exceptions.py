from typing import cast

from wtforms import Form


class SQLAdminException(Exception):
    pass


class InvalidModelError(SQLAdminException):
    pass


class NoConverterFound(SQLAdminException):
    pass


class ValidationError(SQLAdminException):
    def __init__(self, *form_errors: str, **field_errors: str):
        self.form_errors = form_errors
        self.field_errors = field_errors

    def enrich_form(self, form: Form) -> None:
        for field_name, error in self.field_errors.items():
            cast(list[str], form._fields[field_name].errors).append(error)

        if self.form_errors:
            form.form_errors += self.form_errors
        elif not self.field_errors:
            # default error
            form.form_errors.append("Validation error")


class ImproperlyConfigured(SQLAdminException, ValueError):
    """SQLAdmin was set up in a way that cannot work.

    Raised as soon as the mistake can be detected: usually when the view or
    backend is created, or on the first admin request when it depends on how
    the `Admin` was configured. Also a `ValueError`, so existing
    ``except ValueError`` handlers still work.
    """


class InvalidRelationshipError(ImproperlyConfigured):
    """A model has no relationship under the name SQLAdmin was told to use.

    Raised at startup when an RBAC model or view is misconfigured, e.g. when
    `DBAuthorizationBackend(groups_attr=...)` names a missing relationship.
    """


class PermissionEscalationError(SQLAdminException, PermissionError):
    """A group editor tried to grant a permission they may not grant.

    See `GroupAdmin.can_grant`.
    """
