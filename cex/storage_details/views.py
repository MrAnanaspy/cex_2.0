import json

from django.shortcuts import render
from django.http import JsonResponse
from .forms import AddSpecification
from .models import Specification, Detail, MultiplierDetail, MultiplierStandardProducts


def create_specification(request):
    if request.method == 'GET':


        form = AddSpecification()
        return render(request, 'storage_details/create_specification.html', {
            'form':form,
        })
    if request.method == "POST":
        if "create" in request.POST:
            form = AddSpecification(request.POST)
            specification = Specification()
            detail = request.POST.get('subcategories')
            print(detail)
            multiplier_detail = MultiplierDetail()
            multiplier_standard_products = MultiplierStandardProducts()

            if form.is_valid():


                specification.EAM = form.cleaned_data['EAM']
                specification.name = form.cleaned_data['name']



            return render(request, 'storage_details/create_specification.html')
        else:
            form = AddSpecification()
            eam = request.GET.get('EAM')
            form.EAM = eam
            name = request.GET.get('name')
            form.name = name
            category = request.GET.get('category')
            form.category = category
            description = request.GET.get('description')
            form.description = description
            subcategories = request.GET.getlist('subcategories')
            form.subcategories = subcategories
            subcategories = request.GET.getlist('detail')
            form.subcategories = subcategories
            return render(request, 'storage_details/create_specification.html', {'form':form,})
    else:
        return render(request, 'storage_details/create_specification.html')