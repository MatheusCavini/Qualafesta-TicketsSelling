from rest_framework import serializers

from qualafesta.models import Event, ArtistParticipation


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistParticipation
        fields = ['id', 'artist_name', 'begin_time', 'end_time', 'artist_image']


class EventSerializer(serializers.ModelSerializer):
    artistparticipation_set = ArtistSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date_time', 'location', 'artistparticipation_set']


