from django.contrib import admin

from app.models import Ingredient, Resevoir, Instruction, Drink, DrinkCreationRecord, AxisMotor
from app.views import machine 

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

MOTOR_MAP = {
    6: machine.model.horizontal_patter_motor
    17: machine.model.shaker_motor
    27: machine.model.vertical_platter_motor
}

class AxisMotorAdmin(admins.ModelAdmin):

    def drive_motors_in_direction(direction, queryset):
        machine.model.set_global_direction(direction)
        ids = [x.gpio_pin for x in queryset]
        for id in ids:
            MOTOR_MAP[id].drive()

    def drive_motor_forward(modeladmin, request, queryset):
        self.drive_motors_in_direction(True, queryset)
        
    def drive_motor_backwards(modeladmin, request, queryset):
        self.drive_motors_in_direction(False, queryset)

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Resevoir, ResevoirAdmin)
admin.site.register(Instruction)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(DrinkCreationRecord)
admin.site.register(AxisMotor, AxisMotorAdmin)