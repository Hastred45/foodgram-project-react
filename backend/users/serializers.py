from rest_framework import serializers

# from recipes.models import Recipe
from users.models import Subscription, User


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed'
        )
        write_only_fields = ('password',)

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user_id = self.context.get('request').user.id
        return Subscription.objects.filter(
            author=obj.id, user=user_id).exists()

    def create(self, validated_data):
        """Создание нового пользователя."""
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user = self.context.get('request').user
        return Subscription.objects.filter(
            author=obj.author, user=user).exists()

    def get_recipes(self, obj):
        """Получение списка рецептов автора."""
        from recipes.serializers import SmallRecipeSerializer
        limit = self.context.get('request').GET.get('recipes_limit')
        recipe_obj = obj.author.recipes.all()
        if limit:
            recipe_obj = recipe_obj[:int(limit)]
        serializer = SmallRecipeSerializer(recipe_obj, many=True)
        return serializer.data
