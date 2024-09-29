# Predicción de Dígitos
Esta aplicación implementa un modelo de inteligencia artificial diseñado para reconocer e identificar dígitos a partir de imágenes. Utiliza técnicas avanzadas de procesamiento de imágenes y aprendizaje automático para realizar predicciones precisas, convirtiendo imágenes de dígitos escritos a mano en su representación numérica correspondiente.

# Estructura del proyecto
El siguiente diagrama describe la estructura actual del proyecto **Predicción de Dígitos**

``` text
.
├── digits_model/
│   ├── digits_model/
│   │   ├── urls.py
│   │   └── ...
│   ├── model/
│   │   └── clf.pickle
│   ├── predicciones/
│   │   ├── apps.py
│   │   └── views.py
│   ├── templates/
│   │   └── index.html
│   └── manage.py
├── test/
│   ├── digit_42.jpg
│   └── ...
├── .gitignore
├── app.py
├── data_generator.ipynb
├── docker-compose.yml
├── dockerfile
├── README.md
└── requirements.txt
```
* `digits_model/`: en este directorio se encuentra contenida la aplicación **backend (REST API)** encargada de **servir el modelo**. Dicho servicio se encuentra desarrollado en el **framework Django**.
  * `digits_model/digits_model/`: en este directorio se encuentra las configuraciones que requiere Django para servir la aplicación como los **settings**, **urls** y **el Web Server Gateway Interface (WSGI)**
  * `digits_model/model/`: en este directorio se encuentra el **modelo clf.pickle** encargado de inferir el dígito representando en una imagen.
  * `digits_model/predicciones/`: este directorio representa la aplicación (app) del proyecto **digits_model**, acá se encuentra definidas las vistas para cada una de las direcciones que posee la aplicación referente a la predicción/inferencia del modelo.
  * `digits_model/templates`: en este directorio se encuentran los archivos `.html` que se renderizan en el cliente.  Una plantilla contiene las partes estáticas de la salida HTML.
  * `digits_model/manage.py`: representa el script de administración de Django con él, podemos realizar acciones como: ejecutar el servidor, realizar migraciones, migraciones de modelo, etc.
* `test/` y `data_generator.ipynb`: este directorio contiene una serie de imágenes para ser utilizadas como test de la aplicación. Dichas imágenes son generedas de manera aleatoria a la hora de ejecutar `data_generator.ipynb`.
* `.gitignore`: archivos ignorados por **git**.
* `app.py`: contiene un pequeño script donde se ilustra cómo importar y ejecutar el modelo **clf.pickle**.
* `docker-compose.yml`: contiene las instrucciones necesarias para ejecutar un contenedor a partir de la imagen Docker de la aplicación.
* `dockerfile`: contiene las instrucciones para crear una imagen de la aplicación.
* `README.md`: contiene la documentación de este proyecto.
* `requirements.txt`: contiene todas las dependencias necesarias para la ejecutar la aplicación.

# Ejecución
A continuación se indica como ejecutar la aplicación de menera local sin usar Docker y de manera local usando Docker.
## Ejecución Local (No Docker)

Para ejecutar la aplicación de manera local **por primera vez** ejecutar los siguientes comandos:
> ⚠️ ***Es importante tener en cuenta que:***
> 
>   1. ***Versión de Python:** 3.11.7*
>   2. *A la hora de ejecutar los comandos que se muestran a continuación asegúrese de que se encuentre ubicado, en consola, en el directorio del proyecto.*

1. **Creación del ambiente virtual**:
    ``` bash
    python -m venv .venv 
    ```
2. **Activación del ambiente virtual**: 
    ```bash
    source .venv/Scripts/activate
    ```
3. **Instalación de dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Ejecutar la aplicación**:
   
    ```bash
    python manage.py runserver
    ```
    > ⚠️ *A la hora de ejecutar la aplicación es importante tener en cuenta que debemos estar ubicados, en consola, en la carpeta **`cd digits_model`***

Si no es la primera vez que ejecutas esta aplicación y previamente ya has realizado los pasos anteriores, solo debes de ejecutar los pasos **2. Activación del ambiente virtual** y **4. Ejecutar la aplicación** de los mencionados anteriormente

## Ejecución Local (Docker)
Para ejecutar la aplicación en Docker de manera local asegúrese en primera instancia de tener instalado Docker y luego ejecute los siguientes comandos:

> ⚠️ ***Es importante tener en cuenta que:** A la hora de ejecutar los comandos que se muestran a continuación asegúrese de que se encuentre ubicado, en consola, en el directorio del proyecto.*

1. **Creación de la imagen virtual:**
   ```docker
   docker build --tag corona-model:v0 .
   ```
2. **Ejecución del contenedor:**
    ```docker
    docker compose up
    ```
Si no es la primera vez que ejecutas la aplicación de manera local usando Docker y ya posees una imagen virtual (imagen del paso **1 .Creación de la imagen virtual**) puedes ejecutar directamente el paso  **2. Ejecución del contenedor**.

---
# 📑 REST API Documentation
## Instroducción
Esta API proporciona un único punto de acceso para hacer predicciones basadas en una imagen de entrada y un modelo de aprendizaje automático especificado. La API acepta una solicitud POST con un formulario que contiene un archivo de imagen y el nombre del modelo, y devuelve el resultado de la predicción.

### Base URL
* **[DEV - Docker]**: http://localhost:80/
* **[DEV - No Docker]**: http://localhost:8000/
* **[PROD]**: http://44.201.153.114:8000/

> ⚠️ ***Es importante tener en cuenta que:** para usar la Base URL de desarrollo debemos de tener en ejecución la aplicación en la máquina local, ya sea en un contenedor o no.*

## Endpoints

### POST `{{Base URL}}/predict/`
Este endpoint acepta un archivo de imagen y un nombre de modelo, y devuelve una predicción basada en el modelo proporcionado.

**Request**.
* **Method**: POST
* **Endpoint**: /predict/
* **Content-Type**: multipart/form-data

**Parámetros**.

El cuerpo (**body**) de la solicitud debe contener los siguientes dos parámetros como **form-data**.

| **Parámetro** | **Tipo** | **Requerido** | **Descripción**                                           |
| ------------- | -------- | ------------- | --------------------------------------------------------- |
| **image**     | file     | Sí            | Imagen que será usada para la inferencia.                 |
| **model**     | string   | Sí            | Nombre del modelo de Machine Learning usado para inferir. |

**Ejemplo request**
```bash
curl -X POST {{Base URL}}/predict/ \
  -F 'image=@/path/to/your/image.jpg' \
  -F 'model=clf.pickle'

> {
    "status_code": 200,
    "query_id": "70cd7b2a-dd66-4fce-b13a-cede33c80422",
    "prediction": 2,
    "execution_time": "2.08 seg"
}
```
donde:
| **Campo**          | **Tipo** | **Descripción**                                                             |
| ------------------ | -------- | --------------------------------------------------------------------------- |
| **success**        | int      | 200 para indicar que la petición fue exitosa.                               |
| **query_id**       | string   | uuid que identifica de manera única la petición.                            |
| **prediction**     | int      | Predicción del modelo basado en la imagen.                                  |
| **execution_time** | string   | Tiempo que le toma al modelo en realizar una predicción medida en segundos. |
| **error**          | string   | Mensaje de error si la consulta falla (opcional)                            |
