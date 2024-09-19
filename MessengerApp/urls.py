# users/urls.py
from django.urls import path
from .views import user_list, user_create, user_detail, user_update, user_delete, user_partial_update, user_filter_by_date,user_filter_and_send_email

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/create/<str:name>/<str:date>/', user_create, name='user-create'),
    path('users/create/<str:name>/<str:date>/<str:username>/', user_create, name='user-create-username'),
    path('users/create/<str:name>/<str:date>/<str:username>/<str:note>/', user_create, name='user-create-with-all-fields'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users/update/<int:pk>/<str:name>/<str:date>/', user_update, name='user-update'),
    path('users/update/<int:pk>/<str:name>/<str:date>/<str:username>/<str:note>/', user_update, name='user-update-with-all-fields'),
    path('users/partial-update/<int:pk>/', user_partial_update, name='user-partial-update'),
    path('users/partial-update/<int:pk>/<str:name>/', user_partial_update, name='user-partial-update-name'),
    path('users/partial-update/<int:pk>/<str:name>/<str:date>/', user_partial_update, name='user-partial-update-name-date'),
    path('users/partial-update/<int:pk>/<str:name>/<str:date>/<str:username>/', user_partial_update, name='user-partial-update-name-date-username'),
    path('users/partial-update/<int:pk>/<str:name>/<str:date>/<str:username>/<str:note>/', user_partial_update, name='user-partial-update-with-all-fields'),
    path('users/delete/<int:pk>/', user_delete, name='user-delete'),
     path('users/filter-by-date/', user_filter_by_date, name='user-filter-by-date'),
     path('users/filter-and-send-email/', user_filter_and_send_email, name='user-filter-and-send-email'),
]
