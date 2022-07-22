from django.shortcuts import redirect

class UnauthenticatedRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('homepage')



