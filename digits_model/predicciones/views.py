from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from PIL import Image
import pickle
import numpy as np
import time
import uuid
from rest_framework.parsers import MultiPartParser


# Esta vista permite renderizar el home


def index(request):
    return render(request, 'index.html')


# Definir los parámetros para documentación swagger
image_param = openapi.Parameter(
    'image', openapi.IN_FORM, description="Imagen que será usada para la inferencia.", type=openapi.TYPE_FILE, required=True)

model_param = openapi.Parameter(
    'model', openapi.IN_FORM, description="Nombre del modelo de Machine Learning usado para inferir.", type=openapi.TYPE_STRING, required=True)


@csrf_exempt
@swagger_auto_schema(
    method='post',
    manual_parameters=[image_param, model_param],
    operation_summary="Realiza una predicción basada en una imagen y un modelo especificado",
    operation_description="Este endpoint acepta una imagen y el nombre de un modelo de Machine Learning. Devuelve una predicción basada en la imagen proporcionada y el modelo especificado.",
    responses={200: 'Predicción realizada con éxito',
               400: 'Petición realizada incorrectamente'}
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
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
            return JsonResponse({'error': f'El modelo con nombre {model_name} no fue encontrado'}, status=400)

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
