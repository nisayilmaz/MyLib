from django.core.exceptions import PermissionDenied


class LibrarianPermissionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Librarian').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

