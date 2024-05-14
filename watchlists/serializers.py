from rest_framework import serializers
from .models import  WatchList, Symbol
from accounts.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email']


class WatchListSerializer(serializers.ModelSerializer):
    
    author = AuthorSerializer(many=False, read_only=True)
    class Meta:
        model = WatchList
        fields = ['title', 'symbol', 'author']
    
    def create(self, validated_data):
        return super().create(validated_data)
   


class GetWatchListSerializer(serializers.ModelSerializer):
    
    author = AuthorSerializer(many=False, read_only=True)
    class Meta:
        model = WatchList
        fields = ['title', 'symbol', 'author', 'id']
    
 
class DeleteWatchListSerializer(serializers.Serializer):
    watchlist_id = serializers.IntegerField()


class SymbolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Symbol
        fields = ['symbol', 'type', 'name', 'region']
