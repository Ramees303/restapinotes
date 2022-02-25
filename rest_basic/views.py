from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
'importing '
from .serializers import ArticleSerializer
from .models import Article
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# Create your views here
# viewset provide list ,create,retrive operations instead of get put operation from  Detail (APIView)

'''class ArticleViewset(viewsets.ViewSet):
    def list(self,request):
        article=Article.objects.all()
        serializer=ArticleSerializer(article,many=True)
        return Response(serializer.data)

    def create(self,request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        queryset=Article.objects.all()
        article=get_object_or_404(queryset,pk=pk)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)

    def update(self,request,pk=None):
        article=Article.objects.get(pk=pk)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)'''


'''class ArticleViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()'''


class ArticleViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

'''viewset :-lot of code
generic view set:-less code
Modelviewset:-very less code'''









# generic api views
class HOME(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    #authentications  ,token authentication is better
    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)


class DETAIL(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.CreateModelMixin,
             mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    def get(self,request,id):
        return self.retrieve(id)

    def put(self,request,id):
        return self.update(request,id)

    def delete(self,request,id):
        return self.destroy(request,id)




class Home(APIView):
    def get(self,request):
        article=Article.objects.get()
        serializer=ArticleSerializer(article,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Detail(APIView):

    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article=Article.objects.get(id=id)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,id):
        article=Article.objects.get(id=id)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        article=Article.objects.get(id=id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#@csrf_exempt
#for taking input from the client who dont have a csrf token
@api_view(['GET','POST'])
#used for browsing api
def home(request):
    if request.method=='GET':
        article=Article.objects.all()
        serializer=ArticleSerializer(article,many=True)
        'many=true is used for serializing the queryset'
        return Response(serializer.data)
        #return JsonResponse(serializer.data,safe=False)
        'by default the jasonresponse first data should be a dict instance'
        'safe=false:To pass any other json serializable object and'
        'if we dont put false typeerror occurs'
    elif request.method == 'POST':
        #data=JSONParser().parse(request)
        'jasonparser:-it parses/divide the incoming request json content into '
        'python content type dict'
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        'status =201(created status) the request has to be fullfilled and has result'
        'in one or more new resource being created'
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        'status=400 bad request the server cannot or will not process '
        'the result due to something'

#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def detail(request,pk):
    try:
        article=Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer=ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #data=JSONParser().parse(request)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'204 is no content'

''' def trail(request)
        if request.method=='GET':
            article=Article.objects.all()
            serializer=ArticleSerializer(article)
            return Response(serializer.data)
        elif request.method=='POST':
            serializer=ArticleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
  def detail(request,id):
        try:
            article=Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse (status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            article=Article.objects.get(id=id)
            serializer=ArticleSerializer(article)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        elif request.method=='PUT':
            serializer=ArticleSerializer(article,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method=='DELETE':
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)'''


'''def trail(request):
    if request.method=='GET':
        article=Article.objects.all()
        serializer=ArticleSerializer(article,many=False)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)'''


'''def detail(request,id):
    try:
        article=Article.objects.get(id=id)
    except Article.DoesNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serialzer=ArticleSerializer(article)
        return Response(serialzer.data)
    elif request.method=='PUT':
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        article.delete() return Response(status=status.HTTP_204_NO_CONTENT) '''



'''@api_view(['GET','POST'])
def category(request):
    permissions = (IsAuthenticated,)
    if request.method=='GET':
        category=Category.objects.all()
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data)

    elif request.method=='POST':
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@permission_classes(IsAuthenticated,)
@api_view(['GET','PUT','DELETE'])
def catdetail(request,id):
    try:
        id=Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers=CategorySerializer(id)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializers=CategorySerializer(id,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''