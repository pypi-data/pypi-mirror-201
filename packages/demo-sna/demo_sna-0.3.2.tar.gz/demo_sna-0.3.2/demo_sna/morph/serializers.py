from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        
        fields = ['concept_id', 'lemma', 'form', 'POS', 'inALMA']