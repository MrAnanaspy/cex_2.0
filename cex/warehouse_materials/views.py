from django.shortcuts import render, get_object_or_404
from .models import WarehouseMaterial


def index(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)

def warehouse_material(request):
    if request.method == 'GET':
        materials = WarehouseMaterial.objects.all()
        return render(request, 'material_storage.html', {'materials':materials})
    if request.method == 'POST':
        pass
    return render(request, 'material_storage.html')

def add_material(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)

def add_stamp(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)

def add_shape(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)