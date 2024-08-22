
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def add(request):
    return calculate(request, lambda a, b: a + b)


@csrf_exempt
def subtract(request):
    return calculate(request, lambda a, b: a - b)


@csrf_exempt
def multiply(request):
    return calculate(request, lambda a, b: a * b)


@csrf_exempt
def divide(request):
    return calculate(request, lambda a, b: a / b if b != 0 else 'Division by zero!')


def calculate(request, operation):
    try:
        data = json.loads(request.body)
        a = data.get('A')
        b = data.get('B')

        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            return JsonResponse({"error": "Both A and B must be numbers!"}, status=400)

        result = operation(a, b)

        if result == 'Division by zero!':
            return JsonResponse({"error": result}, status=400)

        return JsonResponse({"answer": result})

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid input!"}, status=400)