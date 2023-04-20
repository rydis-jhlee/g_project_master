import requests
import json
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView
from pathlib import Path
from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def g_project(request):
    # 코드 구현
    return render(request, "g_project.html")

