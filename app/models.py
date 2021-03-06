from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Resevoir(models.Model):
    capacity = models.FloatField(default=16, help_text="In fluid ounces")
    level = models.FloatField(default=80.00, help_text="In percentage", validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    gpio_pin = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"Resevoir #{self.pk}"

class Ingredient(models.Model):
    COST_CHOICES = [
        ("$", "Cheap"),
        ("$$", "Normal"),
        ("$$$", "Expensive"),
        ("$$$$", "Too much"),
    ]
    name = models.CharField(max_length=60)
    is_alcohol = models.BooleanField(default=True)
    cost = models.CharField(choices=COST_CHOICES, max_length=4)
    resevoir = models.OneToOneField(Resevoir, related_name="ingredients", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        if self.resevoir is not None:
            return f"{self.name} - Sitting in resevoir #{self.resevoir.pk}"
        return f"{self.name}"

class Drink(models.Model):
    name = models.CharField(max_length=140)
    start_sound = models.FileField(upload_to="audio", null=True, blank=True)
    ending_sound = models.FileField(upload_to="audio", null=True, blank=True)

    def __str__(self):
        return self.name


class Instruction(models.Model):
    pour_duration = models.IntegerField(default=500, help_text="How long to fire the motor for. In ms")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="instructions")
    order = models.PositiveIntegerField()
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, related_name="instructions")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "drink"], name="unique instruction order")
        ]
        
    def __str__(self):
        return f"Pour {self.ingredient} for {self.pour_duration / 1000} seconds"

class DrinkCreationRecord(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=120, help_text="Touchscreen, Text message")

class AxisMotor(models.Model):
    """
        Not used for actual state machine logic, used for a very crude panic reset via admin action
        
        If something gets out of whack, an admin can use an admin function to drive the motor until it hits a switch
    """
    name = models.CharField(max_length=64)
    gpio_pin = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name} axis motor pin#{self.gpio_pin}"
