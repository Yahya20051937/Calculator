from Errors.handling_functions import brackets_handling_algorithm, signs_algorithm


def brackets_handling(func):
    def error_handler(array, *args, **kwargs):
        if brackets_handling_algorithm(
                array):
            return func(array, *args, **kwargs)
        else:
            return 'Error'

    return error_handler


def signs_handling(func):
    def error_handler(array, *args, **kwargs):
        if signs_algorithm(array):
            return func(array, *args, **kwargs)
        else:
            return 'Error'

    return error_handler
