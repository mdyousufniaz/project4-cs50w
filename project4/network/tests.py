from django.test import TestCase, Client
from django.urls import reverse
from .models import User

# Create your tests here.
class NetworkTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='sheldon', password='sheldon')
        

    def test_index(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_login_page(self):
        response = Client().get('/login')
        self.assertEqual(response.status_code, 200)


    def test_valid_login(self):
        # create a client to test response
        client = Client()


        response = client.post("/login", {
            'username': 'sheldon',
            'password': 'sheldon'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        # Verify the redirection to the index page
        self.assertRedirects(response, reverse('index'))

        # Check if the user is authenticated
        self.assertTrue('_auth_user_id' in client.session)
        
        # Optionally, verify user data or other indications of a successful login
        user_id = client.session['_auth_user_id']
        user = User.objects.get(pk=user_id)
        self.assertEqual(user.username, 'sheldon')
        self.assertTrue(user.is_authenticated)

    def test_invalid_login(self):
        client = Client()
        # Attempt to log in with invalid user credentials
        response = client.post(reverse('login'), {
            'username': 'unknown_user',
            'password': 'wrong_password'
        })

        # Check if the response is rendered with the login page and error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username and/or password.")
        self.assertTemplateUsed(response, 'network/login.html')

        # Verify that the user is not authenticated
        self.assertNotIn('_auth_user_id', client.session)


    def test_get_logout_page(self):
        response = Client().get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
    
    def test_get_register_page(self):
        response = Client().get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/register.html')

    def test_register_new_user_password_mismatch(self):
        client = Client()
        # Attempt to register a new user with mismatching passwords
        response = client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirmation': 'password456'
        })

        # Check that the response is the registration page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")
        self.assertTemplateUsed(response, 'network/register.html')

        # Verify that the user was not created
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_new_user_already_exists(self):


        client = Client()
        # Attempt to register a new user with a username that already exists
        response = client.post(reverse('register'), {
            'username': 'sheldon',
            'email': 'sheldon@example.com',
            'password': 'sheldon',
            'confirmation': 'sheldon'
        })

        # Check that the response is the registration page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already taken.")
        self.assertTemplateUsed(response, 'network/register.html')

    def test_new_user_successful_register_and_login(self):
        client = Client()
        # Attempt to register a new user with matching passwords
        response = client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirmation': 'password123'
        })

        # Check if the registration redirects to the index page
        self.assertRedirects(response, reverse('index'))

        # Verify that the new user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Verify that the new user is logged in
        self.assertTrue('_auth_user_id' in client.session)
        user_id = client.session['_auth_user_id']
        user = User.objects.get(pk=user_id)
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.is_authenticated)

    