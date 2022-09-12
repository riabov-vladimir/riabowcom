from django.shortcuts import render, HttpResponse


def test(request):
    """
    Backdoor for testing. Especially handy for testing CRONJOBS due to difficulties with discovering them on-the-go.
    :param request:
    :return:
    """
    # ЗДЕСЬ МОГЛА БЫТЬ ВАША ФУНКЦИЯ
    return HttpResponse(' ---------------- задача выполнена -----------------------')