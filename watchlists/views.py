from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import WatchList
from .permissions import *
import os
from django.http import JsonResponse
import json

# Create your views here.
class WatchListAPI(APIView):
    permission_classes = [IsAuthenticated, IsAuthorReadWriteOnly]


    def get(self, request):
        watchlists = WatchList.objects.filter(author=request.user)
        serializer = GetWatchListSerializer(watchlists, many=True)
        return Response({'data': serializer.data})

    
    def delete(self, request):
        data = request.data
        
        serializer = DeleteWatchListSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': 400,
                'data': serializer.errors
            }) 
        
        try:
            watchlist = WatchList.objects.get(id=serializer.data['watchlist_id'], author=request.user)
            watchlist.delete()
            return Response({
                'status': 200,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'data': 'Failed to delete'
            })
        
    
    def post(self, request):
        data = {
            "title": request.data.get('title'),
            "symbol": request.data.get("symbol"),
            'author': request.user
        }
        watchlist_id = request.data.get("id")
        serializer = WatchListSerializer(data=data)
        if serializer.is_valid():
            if not watchlist_id:
                serializer.save(**data)
                return Response({
                    'status': 200,
                    'message': 'Watchlist created',
                    'data': serializer.data
                })
            else:
                try:
                    watchlist = WatchList.objects.get(id=int(watchlist_id))
                    watchlist.title = data.get('title')
                    watchlist.symbol = data.get('symbol')
                    watchlist.save()
                    return Response({
                        'status': 200,
                        'message': 'Watchlist Updated',
                        'data': serializer.data
                    })
                except WatchList.DoesNotExist:
                    return Response({
                        'message': "Failed to edit"
                    })
            
        
        return Response({
            'status': 400,
            'message': 'failed to create watchlist',
            'data': serializer.errors
        })
    

class SymbolAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", None)
        if not query:
            return Response({
                'message': "query params missing"
            })
        if query == 'all':
            symbols = Symbol.objects.all()
        else:
            symbols = Symbol.objects.filter(symbol__icontains=query)
        serializer = SymbolSerializer(symbols, many=True)


        return Response({
            'bestMatches': serializer.data
        })
    
    def post(self, request):
        data = request.data

        serializer = SymbolSerializer(data=data, many=True)
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors
            })

        serializer.save()
        return Response({
            'message': 'created'
        })


class WatchListEditAPI(APIView):
    permission_classes = [IsAuthenticated, IsAuthorReadWriteOnly]


    def get(self, request):
        query = request.GET.get("watchlist_id", None)
        if not query:
            return Response({
                'data': 'missing query params'
            })
        
        watchlists = WatchList.objects.get(author=request.user, id=query)
        serializer = GetWatchListSerializer(watchlists)
        return Response({'data': serializer.data})


class StockValuesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        file_path = os.path.join(os.path.dirname(__file__), 'dummyStock.json')
        with open(file_path) as f:
            data = json.load(f)
        return JsonResponse(data)