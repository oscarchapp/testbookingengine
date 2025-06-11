"""
    Functions for handling AJAX requests in the PMS application.
"""

# Standard library imports
from django.http import JsonResponse, HttpRequest

# Django imports
from django.db.models import Q

# Application imports
from pms.models import Room


def room_search(request: 'HttpRequest') -> JsonResponse:

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Petición no es AJAX'}, status=405)

    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    keyword = request.GET.get('keyword', '').strip()

    query = Q(name__icontains=keyword) | Q(room_type__name__icontains=keyword)
    rooms = Room.objects.filter(query).select_related('room_type') if keyword else Room.objects.all()

    data = []
    for room in rooms:
        data.append({
            'id': room.id,
            'name': room.name,
            'room_type': room.room_type.name if room.room_type else 'Sin tipo',
        })

    return JsonResponse({'rooms': data})
