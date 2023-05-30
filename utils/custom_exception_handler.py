from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    ERROR_MESSAGES = {
        'AuthenticationFailed': 'El email o la contraseña son inválidos. Verifica que los datos ingresados sean correctos.',
        'NotAuthenticated': 'Ingresa al sistema para poder acceder a este recurso. Asegúrate de iniciar sesión antes de intentar acceder a esta ruta.',
        'InvalidToken': 'La autenticación con este token ha expirado. Por favor, accede nuevamente para obtener un nuevo token de autenticación.',
    }

    GENERIC_ERROR_MESSAGE = 'Ocurrió un error inesperado. Por favor, inténtalo más tarde.'

    if response is not None:
        if exception_class in ERROR_MESSAGES:
            response.data = {
                'error': ERROR_MESSAGES[exception_class].strip()
            }
        else:
            response.data = {
                'error': GENERIC_ERROR_MESSAGE
            }

    return response
