from django.contrib import admin
import RPi.GPIO as GPIO
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

    list_display = ["id", "gpio_pin", level, percentage , capacity]

    def get_c(self, obj):
        return obj.a + obj.b


    # all pins are setup in apps.py
    def turn_on_resevoirs(modeladmin, request, queryset):
        for res in queryset:
            GPIO.setup(res.gpio_pin, GPIO.OUT)
            GPIO.output(res.gpio_pin, GPIO.LOW)

    def turn_off_resevoirs(modeladmin, request, queryset):
        for res in queryset:
            GPIO.setup(res.gpio_pin, GPIO.OUT)
            GPIO.output(res.gpio_pin, GPIO.HIGH)



    actions = [turn_on_resevoirs, turn_off_resevoirs]



MOTOR_MAP = {
    23: machine.machine.model.horizontal_patter_motor,
    17: machine.machine.model.shaker_motor,
    27: machine.machine.model.vertical_platter_motor
}

class AxisMotorAdmin(admin.ModelAdmin):

    def drive_motors_in_direction(self, direction, queryset):
        machine.machine.model.set_global_direction(direction)
        ids = [x.gpio_pin for x in queryset]
        for id in ids:
            MOTOR_MAP[id].drive(25)

    def drive_motor_forward(modeladmin, request, queryset):
        modeladmin.drive_motors_in_direction(True, queryset)

    def drive_motor_backwards(modeladmin, request, queryset):
        modeladmin.drive_motors_in_direction(False, queryset)

    actions = [drive_motor_forward, drive_motor_backwards]
    list_display = ["__str__", "get_last_switch_hit"]

    def get_last_switch_hit(self, obj):
        return MOTOR_MAP[obj.gpio_pin].last_hit_switch

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Resevoir, ResevoirAdmin)
admin.site.register(Instruction)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(DrinkCreationRecord)
admin.site.register(AxisMotor, AxisMotorAdmin)
