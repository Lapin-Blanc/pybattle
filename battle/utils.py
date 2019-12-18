from channels.db import database_sync_to_async

from .exceptions import ClientError
from .models import Room, Lobby


def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    if room_id == "Lobby":        
        room, created = Lobby.objects.get_or_create(
            title='Lobby',
        )    
        return room    
    # Find the room they requested (by ID)
    try:
        print(room_id)
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    return room

def delete_room(room_id, user):
    """
    Tries to delete a room, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        Room.objects.get(pk=room_id).delete()
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    
