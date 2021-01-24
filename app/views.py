from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from app.models import Drink, DrinkCreationRecord
from app.serializers import DrinkSerializer
import RPi.GPIO as GPIO


from app.machine import DrinkManufacturer

# the object that the view functions act on
machine = DrinkManufacturer()


@api_view(["POST"])
def awaken(request):
    machine.awaken()
    return Response({"message": "Machine Awakened"})

@api_view(["GET","POST"])
def drinks(request):
    if request.method == "POST":
        drink_id = request.data.get("drink_id", None)
        if drink_id:
            drink = Drink.objects.get(id=drink_id)
            DrinkCreationRecord.objects.create(
                drink=drink,
                source=request.data.get("source", "Touchscren")
            )
            machine.on_drink_selection(drink)
            return Response({"message": "Drink prepared"})
        return Response(status=HTTP_400_BAD_REQUEST)
    drinks = Drink.objects.all()
    serializer = DrinkSerializer(drinks, many=True)
    return Response(serializer.data, status=HTTP_200_OK)
