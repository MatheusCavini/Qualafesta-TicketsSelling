from rest_framework import serializers

from qualafesta.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date_time', 'location']


