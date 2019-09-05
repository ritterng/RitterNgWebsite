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
        print("Start to test the home page without login")
        response = self.client.get('/todo/home/')
        self.assertEquals(response.status_code, 302)

    def test_home_page_with_login(self):
        print("Start to test the home page with login")
        self.client.login(username="testuser", password="trythetest123")
        response = self.client.get('/todo/home/')
        self.assertEquals(response.status_code, 200)
        self.client.logout()

    def test_view_url_by_name_without_login(self):
        print("Start to test the home view by name without login")
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 302)

    def  test_view_url_by_name_with_login(self):
        print("Start to test the home view by name with login")
        self.client.login(username="testuser", password="trythetest123")
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.client.logout()   

    def test_view_uses_correct_template(self):
        print("Start to test if the home page use the correct template")
        self.client.login(username="testuser", password="trythetest123")
        response = self.client.get('/todo/home/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/home.html')
        self.client.logout()

    def test_view_uses_correct_redirected(self):
        print("Start to test if the redirection correct")
        response = self.client.get('/todo/home/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    #fields = ["item","ddl_date","points","completed"]
    def test_post_without_login_valid_form(self):
        print("Start to test the post method with valid form and without login")
        data = {'item' : 'test1', 'ddl_date': datetime.date.today(), "points" : 200, "completed": False}
        response = self.client.post('/todo/home/',data)
        self.assertEquals(response.status_code, 302)

    def test_post_without_login_invalid_form(self):
        print("Start to test the post method with invalid form and without login")
        data = data = {'item' : 12, 'ddl_date': 0, "points" : "test", "completed": "False"}
        response = self.client.post('/todo/home/',data)
        self.assertEquals(response.status_code, 302)


    def test_post_with_login_valid_form(self):
        print("Start to test the post method with valid form and with login")
        self.client.login(username="testuser", password="trythetest123")
        data = {'item' : 'test1', 'ddl_date': datetime.date.today(), "points" : 200, "completed": False}
        response = self.client.post('/todo/home/',data)
        item = models.ToDoItem.objects.get(id=1)
        expected_item = f'{item.item}'
        self.assertEquals(expected_item,'test1')
        self.client.logout()
        

    def test_post_with_login_invalid_form(self):
        self.client.login(username="testuser", password="trythetest123")
        print("Start to test the post method with invalid form and with login")
        data = data = {'item' : 12, 'ddl_date': 0, "points" : "test", "completed": "False"}
        response = self.client.post('/todo/home/',data)
        self.assertContains(response,'Item cannot be empty!')
        self.assertFalse(models.ToDoItem.objects.filter(item=12).exists())
        
        self.client.logout()

class IndexPageTest(TestCase):

    def setUp(self):
        pass
    
    def test_index_page(self):
        print("Start to test the index page by url")
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_page_by_name(self):
        print("Start to test the index page by name")
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_index_page_with_correct_template(self):
        print("Start to test if the index page uses correect template")
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class DeletePageTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="testuser", password="trythetest123", points = 0)
        self.user2 = User.objects.create_user(username="testuser2", password="trythetest123", points = 0)

    def test_delete_page_with_correct_user(self):
        print("Start to test the delete page with correct user and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = False, owner = self.user1)
        item.save()
        item_id = item.id
        self.client.login(username="testuser", password="trythetest123")
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/delete/'+str(item_id))
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        self.client.logout()

    def test_delete_page_with_incorrect_user(self):
        print("Start to test the delete page with incorrect user and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = False, owner = self.user1)
        item.save()
        item_id = item.id
        self.client.login(username="testuser2", password="trythetest123")
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/delete/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertEquals(response.status_code, 302)
        item.delete()

    def test_delete_page_without_login(self):
        print("Start to test the delete page without login and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = False, owner = self.user1)
        item.save()
        item_id = item.id
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/delete/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertEquals(response.status_code, 302)
        item.delete()

    def test_delete_page_wrong_item_without_login(self):
        print("Start to test the delete page without and incorrect item")
        item_id = 3000
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/delete/'+str(item_id))
        self.assertEquals(response.status_code, 302)

    def test_delete_page_wrong_item_with_login(self):
        print("Start to test the delete page with login and incorrect item")
        self.client.login(username="testuser2", password="trythetest123")
        item_id = 3000
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/delete/'+str(item_id))
        self.assertEquals(response.status_code, 302)

    def test_delete_page_without_item_id(self):
        print("Start to test the delete page without item")
        response = self.client.get('/todo/delete/')
        self.assertEquals(response.status_code, 404)

    def test_delete_page_without_item_id_with_login(self):
        print("Start to test the delete page without item and user")
        self.client.login(username="testuser2", password="trythetest123")
        response = self.client.get('/todo/delete/')
        self.assertEquals(response.status_code, 404)

class CorssOffTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="testuser", password="trythetest123", points = 0)
        self.user2 = User.objects.create_user(username="testuser2", password="trythetest123", points = 0)

    def test_cross_off_page_with_correct_user(self):
        print("Start to test the corss page with correct user and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = False, owner = self.user1)
        item.save()
        item_id = item.id
        self.client.login(username="testuser", password="trythetest123")
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == False)
        response = response = self.client.get('/todo/cross-off/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == True)
        item.delete()

    def test_cross_off_page_with_incorrect_user(self):
        print("Start to test the corss page with incorrect user and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = False, owner = self.user1)
        item.save()
        item_id = item.id
        self.client.login(username="testuser2", password="trythetest123")
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == False)
        response = response = self.client.get('/todo/cross-off/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == False)
        self.assertTrue(response.status_code, 302)
        item.delete()

    def test_cross_page_without_login(self):
        print("Start to test the cross-off page without login and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = False, owner = self.user1)
        item.save()
        item_id = item.id
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == False)
        response = self.client.get('/todo/cross-off/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == False)
        self.assertEquals(response.status_code, 302)
        item.delete()

    def test_cross_off_page_wrong_item_without_login(self):
        print("Start to test the cross-off page without and incorrect item")
        item_id = 3000
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/cross-off/'+str(item_id))
        self.assertEquals(response.status_code, 302)

    def test_cross_off_page_wrong_item_with_login(self):
        print("Start to test the cross-off page with login and incorrect item")
        self.client.login(username="testuser2", password="trythetest123")
        item_id = 3000
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/cross-off/'+str(item_id))
        self.assertEquals(response.status_code, 302)

    def test_cross_off_page_without_item_id(self):
        print("Start to test the cross_off page without item")
        response = self.client.get('/todo/cross-off/')
        self.assertEquals(response.status_code, 404)

    def test_cross_off_page_without_item_id_with_login(self):
        print("Start to test the cross_off page without item and user")
        self.client.login(username="testuser2", password="trythetest123")
        response = self.client.get('/todo/cross-off/')
        self.assertEquals(response.status_code, 404)

class UncrossTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="testuser", password="trythetest123", points = 0)
        self.user2 = User.objects.create_user(username="testuser2", password="trythetest123", points = 0)

    def test_uncross_page_with_correct_user(self):
        print("Start to test the uncross page with correct user and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = True, owner = self.user1)
        item.save()
        item_id = item.id
        self.client.login(username="testuser", password="trythetest123")
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == True)
        response = response = self.client.get('/todo/uncross/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == False)
        item.delete()

    def test_uncross_off_page_with_incorrect_user(self):
        print("Start to test the uncorss page with incorrect user and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = True, owner = self.user1)
        item.save()
        item_id = item.id
        self.client.login(username="testuser2", password="trythetest123")
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == True)
        response = response = self.client.get('/todo/uncross/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == True)
        self.assertTrue(response.status_code, 302)
        item.delete()

    def test_uncross_page_without_login(self):
        print("Start to test the uncross page without login and correct item")
        item = models.ToDoItem(item = "testcase", ddl_date = datetime.date.today(), points = 200, completed = True, owner = self.user1)
        item.save()
        item_id = item.id
        self.assertTrue(models.ToDoItem.objects.filter(id = item_id).exists())
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == True)
        response = self.client.get('/todo/uncross/'+str(item_id))
        self.assertTrue(models.ToDoItem.objects.get(id = item_id).completed == True)
        self.assertEquals(response.status_code, 302)
        item.delete()

    def test_uncross_page_wrong_item_without_login(self):
        print("Start to test the uncross page without and incorrect item")
        item_id = 3000
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/uncross/'+str(item_id))
        self.assertEquals(response.status_code, 302)

    def test_uncross_page_wrong_item_with_login(self):
        print("Start to test the uncross page with login and incorrect item")
        self.client.login(username="testuser2", password="trythetest123")
        item_id = 3000
        self.assertFalse(models.ToDoItem.objects.filter(id = item_id).exists())
        response = self.client.get('/todo/uncross/'+str(item_id))
        self.assertEquals(response.status_code, 302)

    def test_uncross_page_without_item_id(self):
        print("Start to test the uncross page without item")
        response = self.client.get('/todo/uncross/')
        self.assertEquals(response.status_code, 404)

    def test_uncross_page_without_item_id_with_login(self):
        print("Start to test the uncross page without item and user")
        self.client.login(username="testuser2", password="trythetest123")
        response = self.client.get('/todo/uncross/')
        self.assertEquals(response.status_code, 404)

class EditTest(TestCase):
    pass

class WishListHomeTest(TestCase):
    pass