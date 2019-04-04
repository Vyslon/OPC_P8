from django.core.management.base import BaseCommand, CommandError
from Substitute_Platform.models import Products, Categories
from django.db import transaction
import requests
from django.db.utils import IntegrityError, DataError


class Command(BaseCommand):
    help = 'Update/Fulfill database content using OpenFoodFacts API'

    def handle(self, *args, **options):
        """
        Update or Fulfill the database using OpenFoodFacts API
        """
        url_categories = "https://fr.openfoodfacts.org/categories.json"
        categories = requests.get(url_categories).json()
        nbCategories = 30
        nbByPages = 21
        p_id = 0

        for id in range(nbCategories):
            try:
                Categories.objects.create(name=categories['tags'][id]['id'])
            except (IntegrityError, DataError, KeyError, IndexError):
                pass

        for id in range(nbCategories):
            url_categorie = categories['tags'][id]['url']
            for id_product in range(1, nbCategories):
                url_products = url_categorie + '/' + str(id_product) + '.json'
                products = requests.get(url_products).json()
                print(url_products)
                for nbProduct in range(0, nbByPages):
                    with transaction.atomic():
                        try:
                            cat_for_prod = [Categories.objects.filter(
                                name=products['products'][nbProduct]['categories_hierarchy'][0])[0],
                                Categories.objects.filter(name=products['products'][nbProduct]['categories_hierarchy'][1])[0],
                                Categories.objects.filter(name=products['products'][nbProduct]['categories_hierarchy'][2])[0],
                            ]
                            if len(cat_for_prod) > 0:
                                product = Products.objects.create(
                                    name=products['products'][nbProduct]['product_name_fr'],
                                    stores=products['products'][nbProduct]['stores'],
                                    nutrition_grade=products['products'][nbProduct]['nutrition_grades'][0],
                                    url_openfoodfact=products['products'][nbProduct]['url'],
                                    image_url=products['products'][nbProduct]['image_front_url'],
                                )
                                product.categories.set(cat_for_prod)

                        except (IndexError, KeyError, IntegrityError, DataError):
                            pass
