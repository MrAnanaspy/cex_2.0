from django.shortcuts import render

# Create your views here.
def create_appeal(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)
