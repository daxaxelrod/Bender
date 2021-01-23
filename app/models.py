from django.db import models

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
    
    def __str__(self):
        return f"{self.name}"

class Resevoir(models.Model):
    capacity = models.FloatField(default=16, help_text="In fluid ounces")
    level = models.FloatField(default=80.00, help_text="In percentage")
    current_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    motor_number = models.IntegerField(unique=True)

class Instruction(models.Model):
    pour_duration = models.IntegerField(default=500, help_text="How long to fire the motor for. In ms")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

class Drink(models.Model):
    name = models.CharField(max_length=140)
    ingredients = models.ManyToManyField(Ingredient)
    start_sound = models.FileField(upload_to="audio")
    ending_sound = models.FileField(upload_to="audio")
    

class DrinkCreationRecord(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    created_at = models.DateField(auto_created=True)
    source = models.CharField(max_length=120, help_text="Touchscreen, Text message")
