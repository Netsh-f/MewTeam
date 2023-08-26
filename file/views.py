# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

def _handle_uploaded_file(f):
    with open("111.doc", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)