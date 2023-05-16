from django.http import JsonResponse


def handleNotFoundError(request):
    message = ('No se ha podido encontrar ese recurso')
    response = JsonResponse(data={'error': message})
    response.status_code = 404
    return response


def handleServerError(request):
    message = ('Ha ocurrido un error interno en el servidor')
    response = JsonResponse(data={'error': message})
    response.status_code = 500
    return response
