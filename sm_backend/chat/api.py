from account.models import User
from django.http import JsonResponse
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework_simplejwt.authentication import JWTAuthentication  # force

from .models import Conversation, ConversationMessage
from .serializer import (ConversationDetailSerializer,
                         ConversationMessageSerializer, ConversationSerializer)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def conversation_list(request):
    conversations=Conversation.objects.filter(users__in=list([request.user]))
    serializer=ConversationSerializer(conversations,many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def conversation_detail(request,pk):
    conversation=Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer=ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def conversation_get_or_create(request, user_pk):
    user=User.objects.get(pk=user_pk)
    conversations=Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))
    
    if conversations.exists():
        conversation=conversations.first()
        
    else:
        conversation=Conversation.objects.create()
        conversation.users.add(user,request.user)
        conversation.save()
        
    serializer=ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def conversation_sent_message(request,pk):
    conversation=Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user!= request.user:
            sent_to=user
    
    conversation_message=ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
        )
    
    serializer=ConversationMessageSerializer(conversation_message)
    
    
    return JsonResponse(serializer.data,safe=False)
