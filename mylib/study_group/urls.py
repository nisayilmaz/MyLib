from django.urls import path
from .views import StudyGroupView, ListStudyGroupView,JoinStudyGroup


urlpatterns = [
    path('room/<str:title>', StudyGroupView.as_view(), name='room'),
    path('<int:pk>', JoinStudyGroup.as_view(), name='join'),
    path('', ListStudyGroupView.as_view(), name='study_groups')
]
