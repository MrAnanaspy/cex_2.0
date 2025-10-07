from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import AddMaterial, MaterialStamp, DeleteStamp
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
    if request.method == 'POST':
        stamp = AllMaterials()
        form = MaterialStamp(request.POST)

        # Заполнение данными из формы
        if form.is_valid():
            stamp.stamp = form.cleaned_data['stamp']
            stamp.type = form.cleaned_data['category']
            stamp.density = form.cleaned_data['density']
            stamp.description = form.cleaned_data['description']

            stamp.save()
        return HttpResponseRedirect(reverse('warehouse_material'))
    else:
        stamps = AllMaterials.objects.all().order_by('stamp')
        form = MaterialStamp()
    return render(request, 'add_stamp.html', {'form':form, 'stamps':stamps})

def edit_stamp(request, stamp):
    if request.method == 'POST':
        print(request.POST)
        if 'confirmation' in request.POST:
            form = DeleteStamp(request.POST)

            if form.is_valid():
                if DeleteStamp.clean_delete(form):
                    stamp = get_object_or_404(AllMaterials, pk=stamp)
                    stamp.delete()
                return HttpResponseRedirect(reverse('warehouse_material'))
        else:
            stamp = get_object_or_404(AllMaterials, pk=stamp)
            form = MaterialStamp(request.POST)

            # Заполнение данными из формы
            if form.is_valid():
                stamp.stamp = form.cleaned_data['stamp']
                stamp.type = form.cleaned_data['category']
                stamp.density = form.cleaned_data['density']
                stamp.description = form.cleaned_data['description']

                stamp.save()
            return HttpResponseRedirect(reverse('warehouse_material'))
    else:
        stamp = get_object_or_404(AllMaterials, pk=stamp)
        storage = WarehouseMaterial.objects.filter(stamp=stamp)
        quantity_on = 0
        quantity_off = 0
        weight = 0.0

        for mater in storage:
            if mater.actual_weight != 0:
                quantity_on +=1
            else:
                quantity_off +=1
            weight += mater.actual_weight

        initial_data = {
            'stamp': stamp.stamp,
            'category': stamp.type,
            'density': stamp.density,
            'description': stamp.description
        }
        form = MaterialStamp(initial=initial_data)
        form_del = DeleteStamp()
    return render(request, 'edit_stamp.html', {'form':form, 'form_del':form_del, 'stamp':stamp, 'weight':weight, 'quantity_off':quantity_off, 'quantity_on': quantity_on})

def add_shape(request):
    context = {
        'products': ['Товар 1', 'Товар 2', 'Товар 3'],
    }
    return render(request, 'material_storage.html', context)