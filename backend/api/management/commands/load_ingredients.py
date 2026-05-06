import json
import os
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из JSON файла'

    def handle(self, *args, **options):
        json_file_path = os.path.join('..', 'data', 'ingredients.json')
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                ingredients_data = json.load(file)
                ingredients_to_create = []
                for ingredient in ingredients_data:
                    ingredients_to_create.append(
                        Ingredient(
                            name=ingredient['name'],
                            measurement_unit=ingredient['measurement_unit']
                        )
                    )
                Ingredient.objects.bulk_create(
                    ingredients_to_create,
                    ignore_conflicts=True
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успешно загружено'
                        f'{len(ingredients_to_create)} ингредиентов'
                    )
                )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл {json_file_path} не найден')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Ошибка при чтении JSON файла')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка: {str(e)}')
            )
