from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from .target.keys import API_key
import requests

# Create your views here.
def search(request):
    
    key = API_key
    queryKeywords = ''
    if request.method == 'POST':
        if request.POST.get("search"):
            queryKeywords = request.POST.get("product")
    else:
        queryKeywords = ''
    response = requests.get('https://open.api.ebay.com/shopping?callname=FindProducts&responseencoding=JSON&appid=%s&siteid=0&version=967&QueryKeywords=%s&MaxEntries=45' 
                                %(key, queryKeywords))
    
    productList = response.json()
    if productList['Ack'] == 'Failure':
        errorMessages = productList['Errors'][0]
        if errorMessages['ShortMessage'] == 'Web Service framework internal error.':
            return render(request, 'search/search.html', {"name": productList, "key": "Please enter a keyword for search"})
        elif errorMessages['ShortMessage'] == 'No match found.':
            return render(request, 'search/search.html', {"name": productList, "key": "No match found"})
        else:
            return render(request, 'search/search.html', {"name": productList, "key": "Something goes wrong, please try again!"})
    product = productList["Product"]
    return render(request, 'search/search.html', {"name": product, "key": "Search was found", "word": queryKeywords})
