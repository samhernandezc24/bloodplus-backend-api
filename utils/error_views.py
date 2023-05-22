from django.http import JsonResponse
from django.http import HttpResponseNotFound, HttpResponseServerError


def handle_not_found_error(request):
    message = 'No se ha podido encontrar este recurso. o_o?'
    response = JsonResponse(data={'error': message})
    return HttpResponseNotFound(response)


def handle_server_error(request):
    message = 'Ha ocurrido un error interno en el servidor. (>ლ)'
    response = JsonResponse(data={'error': message})
    return HttpResponseServerError(response)
