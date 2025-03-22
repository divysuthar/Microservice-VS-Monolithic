from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task


@csrf_exempt
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        return JsonResponse(
            [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks],
            safe=False,
            status=200,
        )
    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            task = Task.objects.create(title=data.get("title", "Untitled"))
            return JsonResponse(
                {"id": task.id, "title": task.title, "completed": task.completed},
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8"))
            task.title = data.get("title", task.title)
            task.completed = data.get("completed", task.completed)
            task.save()
            return JsonResponse(
                {"id": task.id, "title": task.title, "completed": task.completed},
                status=200,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({"message": "Task deleted"}, status=204)
    return JsonResponse({"error": "Method not allowed"}, status=405)
