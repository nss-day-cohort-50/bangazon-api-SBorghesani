import random
import faker_commerce
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User
from bangazon_api.helpers import STATE_NAMES
from bangazon_api.models import Category, Store
from bangazon_api.models.product import Product


class ProductTests(APITestCase):
    def setUp(self):
        """

        """
        call_command('seed_db', user_count=2)
        self.user1 = User.objects.filter(store__isnull=False).first()
        self.token = Token.objects.get(user=self.user1)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        category = Category.objects.first()

        data = {
            "name": self.faker.ecommerce_name(),
            "price": random.randint(50, 1000),
            "description": self.faker.paragraph(),
            "quantity": random.randint(2, 20),
            "location": random.choice(STATE_NAMES),
            "imagePath": "",
            "categoryId": category.id
        }
        response = self.client.post('/api/products', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])


    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        product = Product.objects.first()
        data = {
            "name": product.name,
            "price": product.price,
            "description": self.faker.paragraph(),
            "quantity": product.quantity,
            "location": product.location,
            "imagePath": "",
            "categoryId": product.category.id
        }
        response = self.client.put(f'/api/products/{product.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        product_updated = Product.objects.get(pk=product.id)
        self.assertEqual(product_updated.description, data['description'])

    def test_delete_product(self):
        store = Store.objects.get(pk=1)
        category = Category.objects.first()
        product = Product()
        product.name = "testProduct"
        product.price = 245
        product.store = store
        product.description = "testProduct"
        product.quantity = 2
        product.location = "testProduct"
        product.image_path = "null"
        product.category = category

        product.save()

        url = f'/api/products/{product.id}'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())
