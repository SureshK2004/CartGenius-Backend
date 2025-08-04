from django.urls import path
from django.http import JsonResponse

def test_view(request):
    return JsonResponse({'message': 'Product route is working'})

urlpatterns = [
    path('', test_view),
]
