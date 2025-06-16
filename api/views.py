from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def register(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400) 

@api_view(['POST'])
def logout(request):
    # Simple logout (invalidate token on client side)
    return Response({"message": "Logged out"}, status=200)



