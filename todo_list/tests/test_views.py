from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model

import datetime
from .. import models
class HomePageTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="trythetest123", points = 0)


    def test_home_page_without_login(self):
        response = self.client.get('/home')
        self.assertEquals(response.status_code, 302)

    def test_home_page_with_login(self):
        self.client.login(username="testuser", password="trythetest123")
        response = self.client.get('/home')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_view_url_by_name_without_login(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 302)

    def  test_view_url_by_name_with_login(self):
        self.client.login(username="testuser", password="trythetest123")
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.client.logout()   

    def test_view_uses_correct_template(self):
        self.client.login(username="testuser", password="trythetest123")
        response = self.client.get('/home')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/home.html')
        self.client.logout()

    def test_view_uses_correct_redirected(self):
        response = self.client.get('/home')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    #fields = ["item","ddl_date","points","completed"]
    def test_post_without_login_valid_form(self):
        data = {'item' : 'test1', 'ddl_date': datetime.date.today(), "points" : 200, "completed": False}
        response = self.client.post('/home',data)
        self.assertEquals(response.status_code, 302)

    def test_post_without_login_invalid_form(self):
        data = data = {'item' : 12, 'ddl_date': 0, "points" : "test", "completed": "False"}
        response = self.client.post('/home',data)
        self.assertEquals(response.status_code, 302)


    def test_post_with_login_valid_form(self):
        self.client.login(username="testuser", password="trythetest123")
        data = {'item' : 'test1', 'ddl_date': datetime.date.today(), "points" : 200, "completed": False}
        response = self.client.post('/home',data)
        item = models.ToDoItem.objects.get(id=1)
        expected_item = f'{item.item}'
        self.assertEquals(expected_item,'test1')
        self.client.logout()
        

    def test_post_with_login_invalid_form(self):
        self.client.login(username="testuser", password="trythetest123")
        data = data = {'item' : 12, 'ddl_date': 0, "points" : "test", "completed": "False"}
        response = self.client.post('/home',data)
        self.assertContains(response,'Item cannot be empty!')
        self.assertFalse(models.ToDoItem.objects.filter(item=12).exists())
        
        self.client.logout()