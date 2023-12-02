from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.html import strip_tags
from notification.utils import create_notification
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework_simplejwt.authentication import JWTAuthentication  # force

from .forms import ProfileForm, SignupForm
from .models import FriendshipRequest, User
from .serializer import FriendshipRequestSerializer, UserSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication]) #force
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar':request.user.get_avatar()
        })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    errors = {}

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user= form.save()
        user.is_active=False
        user.save()
        
        url=f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'
        
        send_mail(
            "Account Confirmation",
            f'Please click this to confirm your email for your Guakia SocialMedia: {url} ',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,)
        
        
        return JsonResponse({'message': 'success'})
    else:
        error_message = strip_tags(str(form.errors))
        for field_name, error_list in form.errors.items():
            field_label = form.fields[field_name].label
            field_error = f'{field_label}: {", ".join(error_list)}'
            error_message = error_message.replace(field_error, '')
            errors[field_name] = field_error.strip()

        message = 'Error'
        return JsonResponse({'message': message, 'errors': errors})


@api_view(['GET'])
@authentication_classes([JWTAuthentication]) #force
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication]) #force
def my_friendship_suggestions(request):
    serializer=UserSerializer(request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication]) #force
def editprofile(request):
    user=request.user
    email=request.data.get('email')
    
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})

    else:
        form=ProfileForm(request.data, request.FILES, request.POST, instance=user)
        
        if form.is_valid(): 
            form.save()
        
        serializer=UserSerializer(user)
        
        return JsonResponse({'message': 'information updated','user':serializer.data})

@api_view(['POST'])
@authentication_classes([JWTAuthentication]) #force
def editpassword(request):
    user=request.user
    form=PasswordChangeForm(data=request.POST, user=user)
        
    if form.is_valid():
        form.save()    
        
        return JsonResponse({'message':'success'})
    
    else:
        message=form.errors.as_json()
        
        return JsonResponse({'message': message}, safe=False)

@api_view(['POST'])
@authentication_classes([JWTAuthentication]) #force
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        friendrequest=FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
        
        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication]) #force
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)
    
    return JsonResponse({'message': 'friendship request updated'})
