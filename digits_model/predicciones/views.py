from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pickle
from PIL import Image
import numpy as np
import time
import uuid


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def predict(request):
    print(f"RQUEST: {request.POST}")
    print(f"Metodo: {request.method}")
    print(f"Files: {request.FILES}")
    if request.method == 'POST':
        start_time = time.time()

        # Verifica si se recibió una imagen en la solicitud
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'Por favor inserte una imagen'}, status=400)

        model_name = request.POST.get('model')

        # Verifica que exista el parámetro model
        if not model_name:
            return JsonResponse({'error': 'Falta el parámetro model'}, status=400)

        try:
            with open(f"./model/{model_name}", "rb") as f:
                clf = pickle.load(f)
        except:
            return JsonResponse({'error': f'El modelo con nombre {model_name} no fue encontrado'})

        # Obtener la imagen desde el archivo enviado
        image_file = request.FILES['image']
        img = Image.open(image_file)

        img = img.convert('L')  # Convertir a escala de grises
        # Redimensionar a 8x8 píxeles como en el dataset de sklearn
        img = img.resize((8, 8))

        number = np.round((np.array(img) / 255.0) * 16)

        # Hacer la predicción
        prediction = clf.predict(number.reshape(1, -1))

        execution_time = time.time() - start_time

        print(f"Prediccion: {int(prediction[0])}")
        return JsonResponse({
            'status_code': 200,
            'query_id': uuid.uuid4(),
            'prediction': int(prediction[0]),
            'execution_time': f'{execution_time:.2f} seg'
        })
