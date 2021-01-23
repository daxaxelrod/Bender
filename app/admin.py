from django.contrib import admin

from app.models import Ingredient, Resevoir, Instruction, Drink, DrinkCreationRecord

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Resevoir)
admin.site.register(Instruction)
admin.site.register(Drink)
admin.site.register(DrinkCreationRecord)