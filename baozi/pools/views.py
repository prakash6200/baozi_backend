import base58
from baozi.networks.models import Network
from baozi.pools.models import Pool
from baozi.users.models import User
from baozi.tokens.models import Token
from baozi.pools.serializers import PoolSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from tronpy.keys import is_base58check_address


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

    # def post(self, request, address):

        data = request.data
        Address = data.get('lp_token_address')
        Token0, _ = Token.objects.get_or_create(address=data.get('token0'))
        Token1, _ = Token.objects.get_or_create(address=data.get('token1'))
        Providers, _ = User.objects.get_or_create(address=address)

        saveInfo = Pool.objects.get_or_create(address=Address, token0=Token0, token1=Token1, providers=Providers)
        # pool.save()
        # saveInfo = Pool(address=Address, token0=Token0, token1=Token1, providers=Providers)
        # saveInfo = Pool.objects.pools(Address, Token0, Token1, Providers)
        print(saveInfo)
        # print(Address, Token0, Token1, Providers)

        # print(address, token0, token1)

        # saveInfo = Pool.objects.get_or_create(address=address, token0_id=token0, token1_id=token1)
        # print(saveInfo)
        # print(pool)

        # saveInfo.save()

        # saveInfo.pools.add(Providers)

        return Response(
            status=status.HTTP_200_OK
        )

    def post(self, request, address):
        data = request.data
        Address = data.get('lp_token_address')
        Token0, _ = Token.objects.get_or_create(address=data.get('token0'))
        Token1, _ = Token.objects.get_or_create(address=data.get('token1'))
        Providers, _ = User.objects.get_or_create(address=address)
        # Providers = 3
        # providers = data.get('providers')

        # if not is_base58check_address(token0):
        #     return Response('invalid token0', status=status.HTTP_400_BAD_REQUEST)

        # if not is_base58check_address(token1):
        #     return Response('invalid token1', status=status.HTTP_400_BAD_REQUEST)

        # if not is_base58check_address(address):
            # return Response('invalid address', status=status.HTTP_400_BAD_REQUEST)

        # print(address, token0, token1)

        saveInfo = Pool.objects.get_or_create(address=Address, token0=Token0, token1=Token1)
        print(saveInfo)
        return Response(
            # data=TokenSerializer(token).data,
            status=status.HTTP_200_OK
        )