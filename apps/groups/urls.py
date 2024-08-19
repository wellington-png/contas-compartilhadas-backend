from django.urls import path

from apps.groups.viewsets import JoinGroupByLinkAPIView, JoinGroupByTokenAPIView


urlpatterns = [
    path('join/<int:group_id>/<str:token>/', JoinGroupByTokenAPIView.as_view(), name='join-group-by-token'),
    path('join/<int:group_id>/', JoinGroupByLinkAPIView.as_view(), name='join-group-by-link'),
]