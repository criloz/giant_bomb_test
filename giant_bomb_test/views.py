from giant_bomb_test.models import Game
from rest_framework import serializers, viewsets, filters
from rest_framework import generics
from rest_framework import routers
from giant_bomb_test.commons import get_terms

__all__ = ["GameViewSet", "router"]

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


 
class GameSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Game
        fields = ('name', 'aliases', 'description', 'image_url', 'original_release_date', 'site_detail_url')
        
        
class GameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects


    def get_queryset(self):
        """
        restricts the returned games to a given keyword or keywords,
        by filtering against a `search` query parameter in the URL.
        """
        queryset = self.queryset
        search = self.request.query_params.get('search', None)
        
        if search is not None:
            queryset = queryset.filter(keywords__term__in=get_terms(search)).distinct()
        else:
            queryset = queryset.none()
        return queryset

router.register(r'games', GameViewSet)
