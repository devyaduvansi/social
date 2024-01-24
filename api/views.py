from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from .models import CustomUser,Friendship
from .serializers import UserSignupSerializer,UserLoginSerializer,UserSearchSerializer,FriendshipSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q 
import json
from django.utils import timezone
from django.utils.timezone import timedelta
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.pagination import PageNumberPagination

class CustomUserSearchPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUpView(APIView):
    def post(self,request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({"token":token,"msg":"Registration Successfully!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({"token":token,"msg":"Login Successfully!"},status=status.HTTP_200_OK)
        else:
            return Response({"msg":"Invalid Credentials!"},status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomUserSearchPaginator 
    def get(self,request,*args, **kwargs):
        search_keyword = self.request.query_params.get('q', '')
        # Search by either name or email
        queryset = CustomUser.objects.filter(
            Q(name__icontains=search_keyword) |
            Q(email__iexact=search_keyword)
        ).exclude(id=self.request.user.id)
        queryset = queryset.order_by('id')
    
        paginator = CustomUserSearchPaginator()
        result_page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = UserSearchSerializer(result_page, many=True, context={'request': request})
    
        paginated_response = {
            'count': len(result_page),
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }

        return Response(paginated_response)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get('to_user_id')
    to_user = CustomUser.objects.get(id=to_user_id)

    existing_friendship = Friendship.objects.filter(Q(from_user=request.user, to_user=to_user) | Q(from_user=to_user, to_user=request.user)).first()
    if existing_friendship:
        return Response({'error': 'Friend request already sent or accepted'}, status=status.HTTP_400_BAD_REQUEST)

    sent_requests_within_minute = Friendship.objects.filter(from_user=request.user, status='pending', created_at__gte=timezone.now() - timedelta(minutes=1)).count()
    if sent_requests_within_minute >= 3:
        return Response({'error': 'You have reached the limit of sent friend requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    friendship_data = {'from_user': request.user.id, 'to_user': to_user_id, 'status': 'pending'}
    serializer = FriendshipSerializer(data=friendship_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    friendship_id = request.data.get('friendship_id')
    friendship = Friendship.objects.get(id=friendship_id)
    # print("friendship to user",friendship.to_user)
    # print("friendship from user",friendship.from_user)
    # print("request.user",request.user)
    if friendship.to_user == request.user:
        friendship.status = 'accepted'
        friendship.save()
        return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    friendship_id = request.data.get('friendship_id')
    friendship = Friendship.objects.get(id=friendship_id)

    if friendship.to_user == request.user:
        friendship.status = 'rejected'
        friendship.save()
        return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = CustomUser.objects.filter(friendship_to__status='accepted', friendship_to__from_user=request.user)
    serializer = UserLoginSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    pending_requests = Friendship.objects.filter(to_user=request.user, status='pending')
    serializer = FriendshipSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to restrict users from sending more than 3 friend requests within a minute.
class FriendRequestThrottle(SimpleRateThrottle):
    scope = 'friend_request'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
