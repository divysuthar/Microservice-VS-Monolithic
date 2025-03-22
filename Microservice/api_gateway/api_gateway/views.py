from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def task_proxy(request, task_id=None):
    tasks = 'tasks'
    if task_id is not None:
        tasks += f'/{task_id}'
    url = f'http://127.0.0.1:8002/{tasks}/'  # Points to task_service
    print(url)
    headers = {'Content-Type': 'application/json'}
    try:
        if request.method == 'GET':
            response = requests.get(url, params=request.GET, headers=headers)
        elif request.method == 'POST':
            response = requests.post(url, data=request.body, headers=headers)
        elif request.method == 'PUT':
            response = requests.put(url, data=request.body, headers=headers)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
        return JsonResponse(response.json(), status=response.status_code, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Service error: {str(e)}'}, status=503)