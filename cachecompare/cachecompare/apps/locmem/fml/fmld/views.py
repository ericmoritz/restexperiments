from django.shortcuts import render_to_response
from django.core.cache import cache

# Get the sample fb data
from cachecompare import sample_fb_data


def index(request):
    key = 'cachecompare'
    fb_data = cache.get(key)
    if not fb_data:
        fb_data = sample_fb_data
        cache.set(key, fb_data, 30 * 60)
    return render_to_response("index.html", {"data": fb_data})
