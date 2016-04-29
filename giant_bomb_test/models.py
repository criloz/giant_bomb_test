from django.db import models


class Game(models.Model):
    """
        this model store the basic info about each game
    """
    api_id = models.IntegerField(unique=True)
    name = models.TextField()
    aliases = models.TextField(null=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    original_release_date = models.DateTimeField(null=True)
    site_detail_url = models.URLField(null=True)


class KeyWordsMap(models.Model):
    """
        this model relation a game with a term or keyword
        this allow to search games by term in a easy way

        behind the scene this will create a join table between the keywords and the game table
    """
    term = models.CharField(max_length=255, unique=True)
    game = models.ManyToManyField(Game, related_name="keywords")