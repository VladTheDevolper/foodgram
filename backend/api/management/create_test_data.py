import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient

User = get_user_model()


class Command(BaseCommand):
    help = 'Создание тестовых данных'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')
        tags_data = [
            {'name': 'Завтрак', 'slug': 'breakfast'},
            {'name': 'Обед', 'slug': 'lunch'},
            {'name': 'Ужин', 'slug': 'dinner'},
        ]
        tags = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)
            if created:
                self.stdout.write(f'Создан тег: {tag.name}')
        users_data = [
            {
                'email': 'user1@test.ru',
                'username': 'user1',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'password': 'TestPass123'
            },
            {
                'email': 'user2@test.ru',
                'username': 'user2',
                'first_name': 'Петр',
                'last_name': 'Петров',
                'password': 'TestPass123'
            },
        ]
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Создан пользователь: {user.email}')
            users.append(user)
        ingredients = list(Ingredient.objects.all()[:20])
        if not ingredients:
            self.stdout.write(self.style.ERROR(
                'Ингредиенты не найдены! Сначала выполните load_ingredients')
            )
            return
        for user in users:
            for i in range(2):
                recipe = Recipe.objects.create(
                    author=user,
                    name=f'Тестовый рецепт {i+1}'
                         f'от {user.username}.',
                    text=f'Это тестовое описание рецепта {i+1}'
                         f'от пользователя {user.username}.',
                    cooking_time=random.randint(10, 120)
                )
                recipe.tags.set(random.sample(
                    tags,
                    random.randint(1, len(tags))
                ))
                image_content = (
                    b'\x47\x49\x46\x38\x39\x61'
                    b'\x01\x00\x01\x00\x00\x00\x00'
                    b'\x21\xf9\x04\x01\x00\x00\x00'
                    b'\x2c\x00\x00\x00\x00'
                    b'\x01\x00\x01\x00\x00'
                    b'\x02\x02\x44\x01\x00\x3b'
                )
                recipe.image.save(
                    f'recipe_{recipe.id}.gif',
                    ContentFile(image_content),
                    save=True
                )
                recipe_ingredients = []
                for ingredient in random.sample(
                    ingredients,
                    random.randint(3, 7)
                ):
                    recipe_ingredients.append(
                        RecipeIngredient(
                            recipe=recipe,
                            ingredient=ingredient,
                            amount=random.randint(1, 500)
                        )
                    )
                RecipeIngredient.objects.bulk_create(recipe_ingredients)
                self.stdout.write(f'Создан рецепт: {recipe.name}')
        self.stdout.write(self.style.SUCCESS(
            'Тестовые данные успешно созданы!')
        )
