from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from battle.models import Game, Room

# Create your views here.
@login_required
def home(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    games = Game.objects.order_by("title")
    rooms = Room.objects.filter(player_one__isnull = True)|Room.objects.filter(player_two__isnull = True)

    # Render that in the index template
    return render(request, "battle/home.html", {
        "games": games,
        "rooms": rooms,
    })

@login_required
def create_room(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    room = Room(player_one=request.user.username, game=game, blockly_workspace=game.initial_blockly_workspace)
    room.save()
    return redirect(room)

@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if not room.player_one:
        room.player_one = request.user.username
    elif not room.player_two:
        room.player_two = request.user.username
    room.save()
    return redirect(room)


@login_required
def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'battle/room.html', {'room': room})

def battle(request):
    return render(request, 'battle.html')