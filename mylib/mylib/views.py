from django.shortcuts import render
from django.views import View


class HomepageView(View):
    def get(self, request):
        return render(request, 'mylib/index.html')




