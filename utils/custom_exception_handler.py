from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    
    if exception_class == 'AuthenticationFailed':
        response.data = {
            'error': 'El email o la contraseña son inválidos'
        }

    if exception_class == 'NotAuthenticated':
        response.data = {
            'error': 'Ingresa al sistema para poder acceder a este recurso'
        } 

    if exception_class == 'InvalidToken':
        response.data = {
            'error': 'La autenticación del token ha expirado. Por favor accede de nuevo'
        } 

    return response
