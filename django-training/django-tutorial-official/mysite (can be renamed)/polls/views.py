from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, World. You ate at the polls index.")
