from django.urls import path
from battle.views import home, create_room, join_room, room

app_name = 'battle'
urlpatterns = [
    path('create_room/<int:game_id>/', create_room, name='create_room'),
    path('join_room/<int:room_id>/', join_room, name='join_room'),
    path('room/<int:room_id>/', room, name='room'),
    path('', home, name='home'),
]
