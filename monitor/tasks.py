from .models import Endpoint,Request
import requests

def check_urls():
    print("starting check_urls")
    endpoints=Endpoint.objects.all()
    for endpoint in endpoints.iterator():
        try:
            url=endpoint.address
            # check for http
            if not url.startswith('http'):
                url='http://'+url
            response=requests.get(url)
            status_code=response.status_code
            if (status_code>=200 and status_code<300):
                endpoint.success_count+=1
                endpoint.save()
                
            else:
                endpoint.fail_count+=1
                endpoint.save()
            request=Request(endpoint=endpoint,status_code=status_code)
            request.save()
        except:
            endpoint.fail_count+=1
            endpoint.save()
            request=Request(endpoint=endpoint,status_code=500)
            request.save()