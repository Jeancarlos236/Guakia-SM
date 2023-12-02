from account.serializer import UserSerializer
from rest_framework import serializers

from .models import Comment, Post, PostAttachment, Trend

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostAttachment
        fields=('id','get_image')


class PostSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    attachments=PostAttachmentSerializer(read_only=True, many=True)
    
    class Meta:
        model=Post
        fields=('id','body','likes_count','comments_count','created_by','created_at_formatted','attachments','is_private')
        
class CommentSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    
    class Meta:
        model=Comment
        fields=('id','body','created_by','created_at_formatted',)
        
class PostDetailSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    comments=CommentSerializer(read_only=True, many=True)
    attachments=PostAttachmentSerializer(read_only=True, many=True)

    
    class Meta:
        model=Post
        fields=('id','body','likes_count','comments_count','created_by','comments','created_at_formatted','attachments')

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id','hashtag','occurences',)
