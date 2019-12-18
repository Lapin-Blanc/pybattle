from django.conf import settings
from django.template.loader import render_to_string

from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from .exceptions import ClientError
from .utils import get_room_or_error, delete_room

from battle.models import Room

class ChatRoomConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            # Accept the connection
            self.accept()
        # Store which rooms the user has joined on this connection
        self.rooms = set()

    def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        for room_id in list(self.rooms):
            try:
                self.leave_room(room_id)
            except ClientError:
                raise ClientError("CANNOT_LEAVE_ROOM")

    def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        try:
            if command == "join":
                # Make them join the room
                self.join_room(content["room"])
            elif command == "send":                
                self.send_room(content["room"], content["message"])
            elif command == "leave":
                self.leave_room(content["room"])
        except ClientError as e:
            # Catch any errors and send it back
            self.send_json({"error": e.code})

    ##### Command helper methods called by receive_json

    def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = get_room_or_error(room_id, self.scope["user"])

        # Send a join message
        async_to_sync(self.channel_layer.group_send)(
            room.group_name,
            {
                "type": "chat.join",
                "room_id": room_id,
                "username": self.scope["user"].username,
            }
        )

        # Store that we're in the room
        self.rooms.add(room_id)
        
        # Add us to the group so we get room messages
        async_to_sync(self.channel_layer.group_add)(
            room.group_name,
            self.channel_name,
        )
        
        # Instruct their client to finish opening the room
        self.send_json({
            "join": room_id,
            "title": str(room),
        })
        
        # Notify Lobby when someone create/join a game
        if room_id != "Lobby":
            room = get_room_or_error("Lobby", self.scope["user"])
            async_to_sync(self.channel_layer.group_send)(
                room.group_name,
                {
                    "type": "room.join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )

    def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = get_room_or_error(room_id, self.scope["user"])
        # Remove that we're in the room
        self.rooms.discard(room_id)
        # Remove us from the group so we no longer get room messages
        async_to_sync(self.channel_layer.group_discard)(
            room.group_name,
            self.channel_name,
        )
        # Send a leave message to group
        async_to_sync(self.channel_layer.group_send)(
            room.group_name,
            {
                "type": "chat.leave",
                "room_id": room_id,
                "username": self.scope["user"].username,
            }
        )

        if not room_id == "Lobby":
            # Remove player from room
            if room.player_one == self.scope["user"].username:
                room.player_one = None
            if room.player_two == self.scope["user"].username:
                room.player_two = None
            if room.player_one or room.player_two:
                room.save()
            else:
                delete_room(room_id, self.scope["user"])
        
        # Notify lobby
        if room_id != "Lobby":
            room = get_room_or_error("Lobby", self.scope["user"])
            async_to_sync(self.channel_layer.group_send)(
                room.group_name,
                {
                    "type": "room.leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        
        # Instruct the client to finish closing the room
        self.send_json({
            "leave": room_id,
            "title": str(room),
        })

    def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED : " + str(self.rooms) + " " + str(room_id))
        # Get the room and send to the group about it
        room = get_room_or_error(room_id, self.scope["user"])
        async_to_sync(self.channel_layer.group_send)(
            room.group_name,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join

    def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )

    def chat_code(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        if not self.scope["user"].username == event["username"]:
            self.send_json(
                {
                    "msg_type": settings.MSG_TYPE_CODE,
                    "room": event["room_id"],
                    "username": event["username"],
                    "message": event["message"],
                },
            )

    def room_join(self, event):
        """
        Called when someone has joined a room.
        """
        # Send a message down to the client
        rooms = Room.objects.filter(player_one__isnull = True)|Room.objects.filter(player_two__isnull = True)
        rooms_list = render_to_string('battle/rooms_list.html', {'rooms': rooms})
        self.send_json(
            {
                "msg_type": settings.MSG_TYPE_NOTIFY,
                "room": event["room_id"],
                "username": event["username"],
                "rooms_list": rooms_list,
            },
        )
    def room_leave(self, event):
        """
        Called when someone has left a room.
        """
        # Send a message down to the client
        rooms = Room.objects.filter(player_one__isnull = True)|Room.objects.filter(player_two__isnull = True)
        html = render_to_string('battle/rooms_list.html', {'rooms': rooms})
        self.send_json(
            {
                "msg_type": settings.MSG_TYPE_NOTIFY,
                "room": event["room_id"],
                "username": event["username"],
                "rooms_list": html,
            },
        )
