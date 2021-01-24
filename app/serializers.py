from rest_framework.serializers import ModelSerializer
from app.models import Drink, Instruction, Ingredient

class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = "__all__"


class InstructionSerializer(ModelSerializer):
    ingredient = IngredientSerializer()
    
    class Meta:
        model = Instruction
        fields = "__all__"
    
class DrinkSerializer(ModelSerializer):
    instructions = InstructionSerializer(many=True)
    
    class Meta:
        model = Drink
        fields = "__all__"