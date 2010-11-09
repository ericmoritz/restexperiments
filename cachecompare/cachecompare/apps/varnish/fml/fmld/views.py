from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_control

# Get the sample fb data
from cachecompare import sample_fb_data


@cache_control(max_age=30 * 60)
def index(request):
    fb_data = sample_fb_data
    return render_to_response("index.html", {"data": fb_data})
