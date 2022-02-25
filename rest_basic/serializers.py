'create a serializers.py file'
'from rest_framework import seralizers'


from rest_framework import serializers
from .models import *
'This is example of serializer'
'create a class for serializing '
'''class ArticleSerializer(serializers.Serializer):
    'serialization is for converting objects into datatypes understable by'
    'javascript and front end framework(ie native datatype to json format)'
    'creating serializer to fields'
    title = serializers.CharField(max_length=300)
    author = serializers.CharField(max_length=300)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateField()

    'creating methods:-create and update for editing and create before saving'
    def create(self, validated_data):
        return Article.objects.create(validated_data)



    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.author=validated_data.get('author',instance.author)
        instance.email=validated_data.get('email',instance.email)
        instance.date=validated_data.get('date',instance.date)
        instance.save()
        return instance'''


'Actually there are 2 types of serializers:-serializer and Modelserializer'
'This is an example of ModelSerializer'
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields=['id','title','author']











