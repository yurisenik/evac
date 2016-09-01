import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from backend.models import Item

def redirect_to_index(request):
    return HttpResponseRedirect('/')


def index_veiw(request):
    return render(request, 'index.html')


def get_last_n_items(request,n):
    items = Item.objects.all().order_by('-pk')[:int(n)]
    data = {}
    for item in items:
        if item.geom:

            data[item.id_ext] = {
                'lat': item.geom.y,
                'lng': item.geom.x,
                'message': '{0}, {1}, {2}, {3}'.format(item.from_place, str(item.date),
                                                       item.mark.title, item.number)
            }
    return HttpResponse(json.dumps(data), content_type='application/json')
