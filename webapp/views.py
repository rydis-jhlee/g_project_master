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
from sale.models import *
from core.decorators import *


class AdminPageView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(group_master_permission)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminPageView, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        sale_agent_list = list()

        sale_agents = SaleAgent.objects.filter(status=1)
        for sale_agent in sale_agents:
            sale_agent_list.append({
                'sale_agent_id': sale_agent.sale_agent_id,
                'sale_agent_name': sale_agent.name,
                'sale_agent_building_name': sale_agent.building_name
            })

        return render(request, "g_project.html", {'sale_agent_list': sale_agent_list})

