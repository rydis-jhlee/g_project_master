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


class AdminSearchView(View):
    @method_decorator(csrf_exempt)
    #@method_decorator(group_master_permission)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminSearchView, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        sale_agent_list = list()

        sale_agents = SaleAgent.objects.filter(status=1)
        for sale_agent in sale_agents:
            sale_agent_list.append({
                'sale_agent_id': sale_agent.sale_agent_id,
                'sale_agent_name': sale_agent.name,
                'sale_agent_building_name': sale_agent.building_name
            })

        return render(request, "admin_search.html", {'sale_agent_list': sale_agent_list})


class RiderGrantView(View):
    @method_decorator(csrf_exempt)
    #@method_decorator(group_master_permission)
    def dispatch(self, request, *args, **kwargs):
        return super(RiderGrantView, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        data = {
            "works" : {
                "더반푸드": [
                    "대륭14 605호",
                    "대륭14 605호"
                ],
                "푸드팩토리": [
                    "대륭14 605호",
                    "대륭14 605호"
                ]
            },
            "counts" : {
                "더반푸드": 4,
                "푸드팩토리": 5
            }
        }

        return render(request, "rider_grant.html", data)


class InchSimulatorView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InchSimulatorView, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        return render(request, "simulator.html")

