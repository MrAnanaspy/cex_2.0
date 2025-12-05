from django.http import JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests as req
import json
from itertools import chain
from django.shortcuts import redirect


def tools(request):
    serch = request.GET.get('q')
    if serch:
        if serch.startswith('D '):
            tools_mill = Milling.objects.filter(diameter__icontains=serch)
            tools_drill = Drill.objects.filter(diameter__icontains=serch)
            combined_content = list(chain(tools_mill, tools_drill))
        else:
            tools_mill = Milling.objects.filter(name__icontains=serch)
            tools_drill = Drill.objects.filter(name__icontains=serch)
            combined_content = list(chain(tools_mill, tools_drill))
    else:
        tools_mill = Milling.objects.all()
        tools_drill = Drill.objects.all()
        combined_content = list(chain(tools_mill, tools_drill))

    return render(request, 'tools/tools.html', {'tools':combined_content})

def info_tool(request, id):
    tool = get_object_or_404(Milling, id=id)
    if request.method == 'POST':
        form = MillingForm(request.POST)
        if form.is_valid():  # ← ВАЖНО: проверка валидности!
            form = MillingForm(request.POST, instance=tool)
            if form.is_valid():
                form.save()  # Это обновит существующую запись
                return HttpResponseRedirect(reverse('tools'))
        else:
            tool = Milling.objects.get(id=id)
            tool_form = MillingForm(instance=tool)

        return render(request, 'tools/inf_tool.html', {'form': tool_form})
    else:
        # Получаем HTML страницу
        tool_form = MillingForm(instance=tool)


        return render(request, 'tools/inf_tool.html', {'form':tool_form})

def parse_tool(request):
    if request.method == 'POST':
        try:
            # Проверяем Content-Type
            if request.content_type != 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': 'Неверный Content-Type. Ожидается application/json'
                }, status=400)

            # Парсим JSON данные
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Невалидный JSON'
                }, status=400)

            external_url = data.get('url')

            if not external_url:
                return JsonResponse({
                    'success': False,
                    'error': 'URL не предоставлен'
                }, status=400)

            # Ваша логика парсинга
            response = req.get(external_url)
            html = response.text

            # Создаем объект BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Примеры извлечения данных
            data_list = soup.find('div', class_='cnc-product-description__left')

            title = soup.find('h1', class_='cnc-product-detail__title')

            # Находим все ссылки

            description_text = ''
            descriptions = data_list.find_all('p', class_=False)

            for description in descriptions:
                description_text += description.text

            img = data_list.find('img')

            specifications = data_list.find_all('div', class_='cnc-product-features__feature')
            attributes = {}
            for specification in specifications:
                attributes[specification.find('span').text] = specification.find('div').text.strip().replace('\n', '')

            # Возвращаем JSON ответ
            return JsonResponse({
                'success': True,
                'data': {
                    'url': external_url,
                    'title': title.text,
                    'description': description_text,
                    'img': img.get('src'),
                    'attributes': attributes,
                    'message': 'Парсинг выполнен успешно'
                }
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Внутренняя ошибка сервера: {str(e)}'
            }, status=500)
    return None


@csrf_exempt
def add_tool(request, type):
    if request.method == 'POST':
        # Проверяем Content-Type
        if request.content_type != 'application/json':
            return JsonResponse({
                'success': False,
                'error': 'Неверный Content-Type. Ожидается application/json'
            }, status=400)

        # Парсим JSON данные
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            print("Ошибка JSON:", e)
            return JsonResponse({
                'success': False,
                'error': 'Невалидный JSON'
            }, status=400)
        if type == 'mill':
            # Валидация обязательных полей
            external_name = data.get('name')
            if not external_name:
                print("Ошибка: Отсутствует название")
                return JsonResponse({
                    'success': False,
                    'error': 'Название не предоставлено'
                }, status=400)

            external_description = data.get('description')
            if not external_description:
                print("Ошибка: Отсутствует описание")
                return JsonResponse({
                    'success': False,
                    'error': 'Описание не предоставлено'
                }, status=400)

            external_monolit = data.get('monolit')
            external_quantity = data.get('quantity', 0)
            external_image_url = data.get('image_url', '')
            external_attributes = data.get('attributes', {})
            external_url = data.get('url', '')

            print(f"Обработка данных: name={external_name}, quantity={external_quantity}")

            # Создаем и сохраняем инструмент
            try:
                tool = Milling()

                # Генерируем уникальный ID на основе имени
                tool.name = external_name
                tool.quantity = external_quantity
                tool.id_monolit = external_monolit
                tool.image_url = external_image_url
                tool.attributes = external_attributes
                tool.description = external_description
                tool.url_market = external_url

                # Обработка диаметра из атрибутов
                diameter_value = external_attributes.get('øD фрезы:')
                if diameter_value:
                    try:
                        diameter_clean = str(diameter_value).replace('мм', '').strip()
                        tool.diameter = float(diameter_clean)
                        print(f"Установлен диаметр: {tool.diameter}")
                    except (ValueError, TypeError) as e:
                        print(f"Ошибка преобразования диаметра: {e}")
                        tool.diameter = 0
                else:
                    tool.diameter = 0

                tool.work_diameter = tool.diameter

                print("Сохранение инструмента в БД...")
                tool.save()
                print("Инструмент успешно сохранен!")

                return JsonResponse({
                    'success': True,
                    'status': 'success',
                    'message': 'Инструмент успешно создан',
                    'redirect_url': '/tools/'
                })
            except Exception as e:
                print(f"Общая ошибка: {e}")
                import traceback
                print(traceback.format_exc())

                return JsonResponse({
                    'success': False,
                    'error': f'Внутренняя ошибка сервера: {str(e)}'
                }, status=500)
        if type == 'drill':
            external_name = data.get('name')
            if not external_name:
                print("Ошибка: Отсутствует название")
                return JsonResponse({
                    'success': False,
                    'error': 'Название не предоставлено'
                }, status=400)

            external_description = data.get('description')
            if not external_description:
                print("Ошибка: Отсутствует описание")
                return JsonResponse({
                    'success': False,
                    'error': 'Описание не предоставлено'
                }, status=400)

            external_monolit = data.get('monolit')
            external_quantity = data.get('quantity', 0)
            external_image_url = data.get('image_url', '')
            external_attributes = data.get('attributes', {})
            external_url = data.get('url', '')

            print(f"Обработка данных: name={external_name}, quantity={external_quantity}")

            # Создаем и сохраняем инструмент
            try:
                tool = Drill()

                # Генерируем уникальный ID на основе имени
                tool.name = external_name
                tool.quantity = external_quantity
                tool.id_monolit = external_monolit
                tool.image_url = external_image_url
                tool.attributes = external_attributes
                tool.description = external_description
                tool.url_market = external_url

                # Обработка диаметра из атрибутов
                diameter_value = external_attributes.get('Диаметр, D:')
                if diameter_value:
                    try:
                        diameter_clean = str(diameter_value).replace('мм', '').strip()
                        tool.diameter = float(diameter_clean)
                        print(f"Установлен диаметр: {tool.diameter}")
                    except (ValueError, TypeError) as e:
                        print(f"Ошибка преобразования диаметра: {e}")
                        tool.diameter = 0
                else:
                    tool.diameter = 0

                tool.work_diameter = tool.diameter

                print("Сохранение инструмента в БД...")
                tool.save()
                print("Инструмент успешно сохранен!")

                return JsonResponse({
                    'success': True,
                    'status': 'success',
                    'message': 'Инструмент успешно создан',
                    'redirect_url': '/tools/'
                })
            except Exception as e:
                print(f"Общая ошибка: {e}")
                import traceback
                print(traceback.format_exc())

                return JsonResponse({
                    'success': False,
                    'error': f'Внутренняя ошибка сервера: {str(e)}'
                }, status=500)
            return JsonResponse({
                'success': True,
                'status': 'success',
                'message': 'Инструмент успешно создан',
                'redirect_url': '/tools/'
            })
        return JsonResponse({
            'success': True,
            'status': 'success',
            'message': 'Инструмент успешно создан',
            'redirect_url': '/tools/'
        })


    if request.method == 'GET':
        if type == 'mill':
            return render(request, 'tools/add_mill.html')
        if type == 'drill':
            return render(request, 'tools/add_drill.html')
        if not request.GET.get('href', '').strip():
            return render(request, 'tools/add_mill.html')
        else:
            url = request.GET.get('href', '').strip()
            response = req.get(url)
            html = response.text

            # Создаем объект BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Примеры извлечения данных
            data_list = soup.find('div', class_='cnc-product-description__left')

            title = soup.find('h1', class_='cnc-product-detail__title')

            # Находим все ссылки

            description_text = ''
            descriptions = data_list.find_all('p', class_=False)

            for description in descriptions:
                description_text += description.text

            img = data_list.find('img')

            specifications = data_list.find_all('div', class_='cnc-product-features__feature')
            attributes = {}
            for specification in specifications:
                attributes[specification.find('span').text] = specification.find('div').text.strip().replace('\n', '')

            return render(request, 'tools/add_mill.html')
    return render(request, 'tools/add_mill.html')

