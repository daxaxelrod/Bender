from django.contrib import admin

from app.models import Ingredient, Resevoir, Instruction, Drink, DrinkCreationRecord

class InstructionInline(admin.TabularInline):
    model = Instruction

class DrinkAdmin(admin.ModelAdmin):
    inlines = [
        InstructionInline
    ]

class ResevoirAdmin(admin.ModelAdmin):

    def percentage(obj):
        return obj.level * obj.capacity / 100
    percentage.short_description = f"Ozs Remaining"
    
    def capacity(obj):
        return obj.capacity
    capacity.short_description = "Bottle Capacity (Ozs)"

    def level(obj):
        return obj.level
    level.short_description = "Full %"

    list_display = ["gpio_pin", level, percentage , capacity]





    def get_c(self, obj):
        return obj.a + obj.b


# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Resevoir, ResevoirAdmin)
admin.site.register(Instruction)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(DrinkCreationRecord)