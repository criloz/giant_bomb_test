import json
import urllib.request
from django.core.management.base import BaseCommand
from giant_bomb_test.models import Game, KeyWordsMap
from giant_bomb_test.commons import get_terms


class Command(BaseCommand):
    help = 'Loads all the giantbomb game data. '

    def handle(self, *args, **options):
        url = "http://www.giantbomb.com/api/games/?api_key=6fe6fb576b0c7bef2364938b2248e1628759508d&format=json&offset={offset}&platforms=21"
        offset = 0
        while True:

            # get data from the net
            try:
                with urllib.request.urlopen(url.format(**locals())) as response:
                    json_response = json.loads(response.read().decode("utf-8"))
            except urllib.request.HTTPError as e:
                raise Exception("{0} : {1}".format(e.msg, url))

            limit = json_response["limit"]
            number_of_page_results = json_response["number_of_page_results"]
            number_of_total_results = json_response["number_of_total_results"]
            results = json_response["results"]

            # save games

            for result in results:
                new_game, is_new = Game.objects.get_or_create(api_id=result["id"])
                new_game.aliases = result["aliases"]
                new_game.name = result["name"]
                new_game.description = result["deck"]
                if ("image" in  result) and (result["image"] is not None):
                  new_game.image_url = result["image"]["medium_url"]
                new_game.original_release_date = result["original_release_date"]
                new_game.site_detail_url = result["site_detail_url"]
                new_game.save()
                # save the relationship  between terms and game
                for term in get_terms(new_game.name):
                    key_map, is_new = KeyWordsMap.objects.get_or_create(term=term)
                    key_map.game.add(new_game)

            if limit > number_of_page_results:
                # end the loop, there is no more results
                break

            # print progress
            offset += limit
            giantbomb_progress = offset / number_of_total_results  * 100
            print("{offset} results have been evaluated, {giantbomb_progress}% completed".format(**locals()))



