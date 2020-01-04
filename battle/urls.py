from django.urls import path
from battle.views import home, create_room, join_room, room, battle

app_name = 'battle'
urlpatterns = [
    path('create_room/<int:game_id>/', create_room, name='create_room'),
    path('join_room/<int:room_id>/', join_room, name='join_room'),
    path('room/<int:room_id>/', room, name='room'),
    path('battle/', battle, name='battle'),
    path('', home, name='home'),
]
