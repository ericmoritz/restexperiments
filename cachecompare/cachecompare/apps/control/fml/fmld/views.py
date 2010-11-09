from django.shortcuts import render_to_response

# Get the sample fb data
from cachecompare import sample_fb_data


def index(request):
    fb_data = sample_fb_data
    return render_to_response("index.html", {"data": fb_data})
