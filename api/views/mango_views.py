from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
# from django.middleware.csrf import get_token

from ..models.mango import Mango
from ..serializers import MangoSerializer

# Create your views here.
class Mangos(generics.ListCreateAPIView):
    def get(self, request):
        """Index request"""
        # 1. Query/find the mango objects we wanna see
        # .all() will find all the mangos
        # we want to use .filter() to locate only the mangos the "current user"/ signed in user "owns" (the `owner` field on the `Mango`)
        mangos = Mango.objects.filter(owner=request.user.id)
        # 2. Serialize: Format the data we just found
        data = MangoSerializer(mangos, many=True).data
        # 3. Return a response
        return Response(data)

    serializer_class = MangoSerializer
    def post(self, request):
        """Create request"""
        # The currently signed-in user
        print(request.user)
        
        # 1. Set up new mango data
        # expecting to receive data that looks like:
        # { 'mango': { 'name': 'mangoo', ... } }
        # mango_data is a dictionary
        mango_data = request.data['mango']
        mango_user = request.user.id
        # Manage the ownership of the mango - whoever is the current user should be this mango's owner
        print(type(mango_data)) # This is a dictionary
        # Use square-bracket syntax to access key/value pairs & add the owner
        mango_data['owner'] = mango_user

        # one-liner:
        # request.data['mango']['owner'] = request.user.id

        # 2. Serializer - create the new mango
        # mango = MangoSerializer(data=request.data['mango'])
        mango = MangoSerializer(data=mango_data)
        # print(mango.__dict__)
        # 2a. Validate the new mango
        if mango.is_valid():
            # 2b. Save the mango to the db
            mango.save()
            print(mango.data)
            # 3. Return response w/ data
            return Response(mango.data, status=status.HTTP_201_CREATED)
        else:
            # 3. Return response w/ errors
            return Response(mango.errors, status=status.HTTP_400_BAD_REQUEST)

class MangoDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, pk):
        """Show request"""
        # 1. Query - get one mango
        mango = get_object_or_404(Mango, pk=pk)
        print(mango.owner)
        # 1a. Throw an error if the user making the request
        # doesn't own this mango
        # Rest framework has an error called `PermissionDenied`
        if request.user != mango.owner:
            raise PermissionDenied('You do not own this mango.')
        # 2. Serializer - format the mango
        data = MangoSerializer(mango).data
        # 3. Return response
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        # 1. Query - find one mango based on the pk URL parameter
        mango = get_object_or_404(Mango, pk=pk)
        # 1a. Permission check:
        if request.user != mango.owner:
            raise PermissionDenied('You do not own this mango.')

        # 2. Delete - nothing to serialize
        mango.delete()
        # 3. Return response (204 status means no data to include)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # partial_update supports missing data incoming in the request
    # based on our serializer rules
    # this is a patch request with bonus functionality
    def partial_update(self, request, pk):
        """Update Request"""
        # 1. Query - get just one mango, based on the provided ID (primary key)
        mango = get_object_or_404(Mango, pk=pk)
        # 1a. Permissions check - do they own the mango?
        # if not - raise an error
        if request.user != mango.owner:
        # if not request.user == mango.owner:
            raise PermissionDenied('You do not own this mango.')

        # 1b. Override the 'owner' field on the incoming data
        # prevent people from changing the owner - it should always be the same
        mango_data = request.data['mango']
        mango_data['owner'] = request.user.id

        # 2. Serializer - provide the current mango and the new data
        # to try to perform an update
        ms = MangoSerializer(mango, data=mango_data, partial=True)
        # 2a. Validate those changes
        if ms.is_valid():
            # 2b. Save to the database
            ms.save()
            # 3. Return response w/ data
            return Response(ms.data)
        # 3. Return response w/ errors
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
