from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import AddMaterial
from .models import WarehouseMaterial, AllMaterials


def index(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)

def warehouse_material(request):
    if request.method == 'GET':
        materials = WarehouseMaterial.objects.all()
        form = AddMaterial()
        return render(request, 'material_storage.html', {'materials':materials, 'form':form})

    if request.method == 'POST':
        pass

    return render(request, 'material_storage.html')

def add_material(request):
    if request.method == 'POST':
        material = WarehouseMaterial()
        form = AddMaterial(request.POST)

        # Заполнение данными из формы
        if form.is_valid():
            material.stamp = form.cleaned_data['stamp']
            material.type = form.cleaned_data['type']
            material.size = form.cleaned_data['size']
            material.initial_weight = form.cleaned_data['initial_weight']
            material.actual_weight = form.cleaned_data['initial_weight']
            material.certificate = form.cleaned_data['certificate']
            material.melting = form.cleaned_data['melting']
            material.batch = form.cleaned_data['batch']
            material.place = form.cleaned_data['place']
            material.save()
        return HttpResponseRedirect(reverse( 'warehouse_material'))
    else:
        stamps = AllMaterials.objects.all()
        form = AddMaterial()
        return render(request, 'add_material.html', {'form':form, 'stamps':stamps})

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