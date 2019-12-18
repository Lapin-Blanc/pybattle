from django.db import models
from django.urls import reverse

class Lobby(models.Model):    
    title = models.CharField(max_length=50, default="Lobby")
    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return self.title
    def __str__(self):
        return "Lobby"
    
class Room(models.Model):
    """
    A room for people to chat in during a game.
    """

    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    blockly_workspace = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    player_one = models.CharField(max_length=50, null=True)
    player_two = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return "{} : {} vs {}".format(self.game.title, str(self.player_one), str(self.player_two))

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id
    
    def get_absolute_url(self):
        return reverse('battle:room', args=[self.id])

class  Game(models.Model):
    # Game title
    title = models.CharField(max_length=255)
    initial_blockly_workspace = models.TextField(default='''
        <xml>
            <block type="simulation_loop" id="initial_loop" x="36" y="32" deletable="false" movable="false"></block>
        </xml>
        ''')

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        """
        Returns the Channels Game name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "game-%s" % self.id
