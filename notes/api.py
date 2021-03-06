from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .models import Note, Tag

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    color = serializers.CharField(max_length=15)

class NoteSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        user = self.context['request'].user

        note = Note.objects.create(user=user, **validated_data)

        return note

    user = UserSerializer(required=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        fields = ('title', 'content', 'user', 'tags')



class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        user = self.request.user
        # import pdb; pdb.set_trace()

        if user.is_anonymous:
            return Note.objects.all()
        else:
            return Note.objects.filter(user=user)
