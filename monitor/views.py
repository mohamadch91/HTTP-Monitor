
# Create your views here.
from .serializers import EndpointSerializer,RequestSerializer,EndpointRegisterSerializer

from .models import Endpoint,Request
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .authenticate import get_user
import datetime
import copy
class EndpointCreateView(generics.CreateAPIView):
    #Check for user authentication
    serializer_class = EndpointSerializer   
    def post(self, request: Request, *args, **kwargs)-> Response:
        #get user from request
        user_id=get_user(request)
        if user_id is None:
            return Response({"message":"You are not authorized to create an endpoint"}, status=status.HTTP_401_UNAUTHORIZED)
        user=get_object_or_404(User,pk=user_id)
        user_Endpoint=Endpoint.objects.filter(user=user).count()
        #check if user has reached the limit of 20 endpoints
        if user_Endpoint<20:
            request_data={
                "user":user.id,
                "address":request.data['address'],
                "fail_limit":request.data['fail_limit']
            }
            #create endpoint
            serializer = EndpointRegisterSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                response_data=copy.deepcopy(serializer.data)
                del response_data['user']
                response = {
                    "message":"Endpoint created successfully",
                    "data":response_data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"You have reached the limit of 20 endpoints"}, status=status.HTTP_400_BAD_REQUEST)

        
        

class UserEndpointView(APIView):
    #Check for user authentication
    serializer_class = EndpointSerializer
    def get(self,request)-> Response:
        #all endpoints of the user
        user_id=get_user(request)
        if user_id is None:
            return Response({"message":"You are not authorized to view endpoints"}, status=status.HTTP_401_UNAUTHORIZED)
        user=get_object_or_404(User,pk=user_id)
        serializers=EndpointSerializer(Endpoint.objects.filter(user=user),many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

class EndpointStatsView(generics.RetrieveAPIView):
    #Check for user authentication
    serializer_class = EndpointSerializer
    queryset=Endpoint.objects.all()
    def get(self, request, *args, **kwargs)-> Response:
        user_id=get_user(request)
        if user_id is None:
            return Response({"message":"You are not authorized to view endpoints"}, status=status.HTTP_401_UNAUTHORIZED)
        user=get_object_or_404(User,pk=user_id)
        #get endpoint id from url
        id=kwargs['pk']
        #get endpoint
        endpoint=get_object_or_404(Endpoint,id=id)
        #check if the user is the owner of the endpoint
        if (endpoint.user==user):
            #get all requests for this endpoint in the last 24 hours
            yesterday=datetime.datetime.utcnow()-datetime.timedelta(days=1)
            requests=Request.objects.filter(endpoint=endpoint,created_at__gte=yesterday)
            #check if there are requests
            if (requests.count()>0):
                response=[]
                #get the status of each request
                for request in requests:
                    status_code=request.status_code
                    status_type="success" if status_code>=200 and status_code<300 else "fail"
                    endpoint=request.endpoint.address
                    response.append({"status":status_type,"endpoint":endpoint,"status_code":status_code,"created_at":request.created_at})
                return Response(response, status=status.HTTP_200_OK)
            else:
                #if there are no requests
                response={"message":"No requests found  for this endpoint in the last 24 hours"}
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            
        else:
            #if the user is not the owner of the endpoint
            response={"message":"You are not authorized to view this endpoint"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
   
class EndpointWarningView(generics.ListAPIView):
    #check if user authenticated
    queryset = Endpoint.objects.all()
    def get (self, request, *args, **kwargs)->Response:
        user_id = get_user(request)
        if user_id is None:
            return Response({"message":"You are not authorized to view endpoints"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = get_object_or_404(User, pk=user_id)
        #get the endpoint id from the url
        id=self.kwargs['pk']
        endpoint=get_object_or_404(Endpoint,id=id)
        #check if the user is the owner of the endpoint
        if(endpoint.user == user):
            #check if the endpoint fail limit is exceeded
            if (endpoint.fail_count>endpoint.fail_limit):
                #get the requests that have status code greater or equal than 300
                requests=Request.objects.filter(endpoint=endpoint,status_code__gte=300)
                #get the difference between the fail count and the fail limit
                diffrence=endpoint.fail_count-endpoint.fail_limit
                response=[]
                length=requests.count()
                #loop through the failed requests and create a response
                for i in range(diffrence):
                    serializer=RequestSerializer(requests[length-i-1])
                    serilizer_data=copy.deepcopy(serializer.data)
                    del serilizer_data['id']
                    del serilizer_data['endpoint']
                    serilizer_data['endpoint']=endpoint.address
                    serilizer_data['status']="Fail"
                    response_data={
                        "message":"Endpoint Fail Limit Exceeded",
                        "data":serilizer_data
                        
                    }
                    response.append(response_data)
                return Response(response, status=status.HTTP_200_OK)
                
            else:
                #if the endpoint fail limit is not exceeded return a success response
                response={"message":"Endpoint is working properly"}
                return Response(response, status=status.HTTP_200_OK)
        else:
            #if the user is not the owner of the endpoint return a bad request response
            response={"message":"You are not authorized to view this endpoint"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        

            
