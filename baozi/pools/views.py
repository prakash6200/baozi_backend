import base58
from baozi.networks.models import Network
from tronpy import Tron
from baozi.pools.models import Pool
from baozi.users.models import User
from baozi.tokens.models import Token
from baozi.pools.serializers import PoolSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from tronpy.keys import is_base58check_address

client = Tron(network='shasta')
cntr = client.get_contract("TEruqihC6pf7A5fgWRdqBBbwBP4c9AiZBD")

class PoolView(APIView):

    @swagger_auto_schema(
        responses={
            200: PoolSerializer(many=True),
            400: '',
        }
    )
    def get(self, request):

        objects = Pool.objects.all()

        serializer = PoolSerializer(objects, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class PoolByAddressView(APIView):

    @swagger_auto_schema(
        responses={
            200: PoolSerializer(many=True),
            400: '',
        }
    )
    def get(self, request, address):

        if not is_base58check_address(address):
            return Response('invalid user_address', status=status.HTTP_400_BAD_REQUEST)

        objects = Pool.objects.filter(
            providers__address=address
        )

        serializer = PoolSerializer(objects, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, address):
        data = request.data
        print(data)
        # print(data.get('token0'))
        # print(data.get('token1'))

        if not is_base58check_address(address):
            return Response('invalid user_address', status=status.HTTP_400_BAD_REQUEST)

        if not is_base58check_address(data.get('token0')):
            return Response('invalid token0', status=status.HTTP_400_BAD_REQUEST)
        
        if not is_base58check_address(data.get('token1')):
            return Response('invalid token1', status=status.HTTP_400_BAD_REQUEST)
        
        lp_token = cntr.functions.getPair(data.get('token0'), data.get('token1'))
        print(lp_token)
        
        if not is_base58check_address(lp_token):
            return Response('invalid lp_token', status=status.HTTP_400_BAD_REQUEST)

        Token0, _ = Token.objects.get_or_create(address=data.get('token0'))
        
        Token1, _ = Token.objects.get_or_create(address=data.get('token1'))

        pool_object, _ = Pool.objects.get_or_create(
            address=lp_token,
            token0=Token0,
            token1=Token1
        )

        user_object, _ = User.objects.get_or_create(
            address=address
        )

        pool_object.providers.add(user_object)
    
        return Response(
            status=status.HTTP_200_OK
        )

