from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        product = Product.objects.get(pk=1)
        
        self.order1 = Order.objects.create(
            user=self.user1
        )

        self.order1.products.add(product)

        self.order2 = Order.objects.create(
            user=self.user2
        )

        self.order2.products.add(product)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_delete_order(self):
        response = self.client.delete(f'/api/orders/{self.order1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_add_item_current_order(self):
    #     product = Product.objects.get(pk=1)
    #     self.order1.products.add(product)

    #     response = self.client.post(f'api/products/1/add_to_order')
    #     self.assertEqual(self.order1.completed_on, None)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # TODO: Complete Order test

    def test_complete_order(self):
        order = self.order1
        order.save()
        
        url = f"/api/orders/{order.id}/complete"
        data = {
            "paymentTypeId": 1
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
