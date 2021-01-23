from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from app.apps import machine
from app.models import Drink, DrinkCreationRecord

@api_view(["POST"])
def awaken(request):
    machine.awaken()
    return Response({"message": "Machine Awakened"})

@api_view(["POST"])
def drink_selected(request):
    if drink_id := request.data.get("drink", None):
        drink = Drink.objects.get(id=drink_id)
        DrinkCreationRecord.objects.create(
            drink=drink,
            source=request.data.get("source", "Touchscren")
        )
        machine.on_drink_selection(drink)
        return Response({"message": "Drink prepared"})
    return Response(status=HTTP_400_BAD_REQUEST)