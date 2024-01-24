
from django.urls import path
from .views import SignUpView,UserLoginView,UserSearchAPIView,send_friend_request, accept_friend_request, reject_friend_request, list_friends,list_pending_requests

urlpatterns = [
    path('signup/',SignUpView.as_view(), name='signup'),
    path('login/',UserLoginView.as_view(), name='login'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend/request/', send_friend_request, name='send_friend_request'),
    path('friend/accept/', accept_friend_request, name='accept_friend_request'),
    path('friend/reject/', reject_friend_request, name='reject_friend_request'),
    path('friend/list/', list_friends, name='list_friends'),
    path('friend/pending_requests/', list_pending_requests, name='pending_requests'),
]