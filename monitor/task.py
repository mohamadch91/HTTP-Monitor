from .models import Endpoint,Request
import requests

def check_urls():
    print("starting check_urls")
    endpoints=Endpoint.objects.all()
    for endpoint in endpoints.iterator():
        try:
            response=requests.get(endpoint.address)
            status_code=response.status_code
            if (status_code>=200 and status_code<300):
                endpoint.success_count+=1
            else:
                endpoint.fail_count+=1
            request=Request(endpoint=endpoint,status_code=status_code)
            request.save()
        except:
            request=Request(endpoint=endpoint,status_code=500)
            request.save()