from django.test import TestCase, Client
from django.contrib.auth.forms import PasswordChangeForm
from django.core.management import call_command


import time
import random
import string

from .models import User, GroupRequest
from .forms import AccountForm, RegisterForm
from birdspotter.utils import GROUPS



def gen_name():
    """
    Create a username based off of current time
    """
    return 'testUser' + str(time.time()).replace('.', '')


def gen_password():
    """
    Create a password with 9 random letters
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(9)) # nosec

def gen_creds():
    username = gen_name()
    CREDS = {
            'username': username,
            'email': '%s@test.com' % username,
            'password': gen_password()
        }
    return CREDS


def create_testuser():
    CREDS = gen_creds()
    user = User.objects.create(username=CREDS['username'])
    user.set_password(CREDS['password'])
    user.save()
    user.make_active()
    return (user, CREDS)


class AccountEditingTests(TestCase):

    def test_edit_username_success(self):
        """
        Ensure that a username can be changed if it is not alreay in use
        """
        user, CREDS = create_testuser()
        changed = {
            'username': 'changedUsername'
        }
        form = AccountForm(data=changed, instance=user)
        form.save()
        changed_user = User.objects.get(username=changed['username'])
        self.assertEqual(changed_user.username, changed['username'])
        # lambda is required as the comparison must be callable
        self.assertRaises(User.DoesNotExist,
                          lambda:
                          User.objects.get(username=CREDS['username']))

    def test_edit_username_exists(self):
        """
        Ensure that if a username connot be changed to a username currently in use
        """
        _, CREDS = create_testuser()
        username = gen_name()
        user = User(username=username)
        user.save()
        form = AccountForm(data={'username': CREDS['username']},
                           instance=user)
        #run validation on AccountForm and get error for username
        if form.is_valid():
            form.save()
        username_errors = form.errors['username']
        self.assertTrue('Username already exists' in username_errors[0])

    def test_edit_personal_info(self):
        """
        Ensure that 
        """
        user, _ = create_testuser()
        name_str = 'test_changed'
        changed = {
            'first_name': name_str,
            'last_name': name_str,
            'email': name_str + '@test.com'
        }
        form = AccountForm(data=changed, instance=user)
        if form.is_valid():
            form.save()
        self.assertEqual(user.first_name, name_str)
        self.assertEqual(user.last_name, name_str)
        self.assertEqual(user.email, name_str + '@test.com')

    def test_edit_email_invalid(self):
        """
        Attempt to change a user's email to an invalid email address
        """
        emails = ['test_string', '@test.com', 'test@.', 'test@a.', 'test@.a']
        user, _ = create_testuser()
        for email in emails:
            form = AccountForm(data={'email': email}, instance=user)
            if success := form.is_valid():
                form.save()
            self.assertFalse(success)


class ChangePasswordTests(TestCase):
    base_url = '/accounts/password_change/'

    ERROR_MESSAGES = {
        'similar': 'The password is too similar to the username.',
        'short': 'This password is too short. It must contain at least 8 characters.',
        'common': 'This password is too common.',
        'numeric': 'This password is entirely numeric.'
    }

    def setup(self):
        self.user, creds = create_testuser()
        self.client = Client()
        self.client.login(username=creds['username'], password=creds['password'])
        return creds

    def run_request(self, old_password, new_password, new_password2=""):
        content = {
            'old_password': old_password,
            'new_password1': new_password,
            'new_password2': new_password if not new_password2 else new_password2
        }
        resp = self.client.post(self.base_url, content)
        return resp

    # api tests
    def test_changepassword(self):
        creds = self.setup()
        new_password = gen_password()
        resp = self.run_request(creds['password'], new_password)
        result = User.objects.get(username=resp.wsgi_request.user.username)
        self.assertTrue(result.check_password(new_password))

    def test_incorrect_old_password(self):
        self.setup()
        new_password = gen_password()
        resp = self.run_request('', new_password)
        result = User.objects.get(username=resp.wsgi_request.user.username)
        self.assertFalse(result.check_password(new_password))

    def test_passwords_dont_match(self):
        creds = self.setup()
        new_password = gen_password()
        new_password2 = new_password + 'no match'
        resp = self.run_request(creds['password'], new_password, new_password2)
        result = User.objects.get(username=resp.wsgi_request.user.username)
        self.assertFalse(result.check_password(new_password) and result.check_password(new_password2))

    # form validator tests
    def test_user_similarity(self):
        creds = self.setup()
        user = User.objects.get(username=creds['username'])
        new_password = creds['username'] + '12'
        content = {
            'old_password': creds['password'],
            'new_password1': new_password,
            'new_password2': new_password
        }
        form = PasswordChangeForm(user, content)
        form.is_valid()
        self.assertTrue(form.errors['new_password2'][0] == self.ERROR_MESSAGES['similar'])

    def test_password_too_short(self):
        creds = self.setup()
        user = User.objects.get(username=creds['username'])
        new_password = gen_password()[:3]
        content = {
            'old_password': creds['password'],
            'new_password1': new_password,
            'new_password2': new_password
        }
        form = PasswordChangeForm(user, content)
        form.is_valid()
        self.assertTrue(form.errors['new_password2'][0] == self.ERROR_MESSAGES['short'])

    def test_password_common(self):
        creds = self.setup()
        user = User.objects.get(username=creds['username'])
        # 3rd most common password accoring to nordpass.com
        new_password = 'picture1' #nosec
        content = {
            'old_password': creds['password'],
            'new_password1': new_password,
            'new_password2': new_password
        }
        form = PasswordChangeForm(user, content)
        form.is_valid()
        self.assertTrue(form.errors['new_password2'][0] == self.ERROR_MESSAGES['common'])

    def test_password_numeric(self):
        creds = self.setup()
        user = User.objects.get(username=creds['username'])
        new_password = '161876292354838259283908' #nosec
        content = {
            'old_password': creds['password'],
            'new_password1': new_password,
            'new_password2': new_password
        }
        form = PasswordChangeForm(user, content)
        form.is_valid()
        self.assertTrue(form.errors['new_password2'][0] == self.ERROR_MESSAGES['numeric'])

class RegisterUserTests(TestCase):
    """
    Tests for the registration endpoint and form validation
    """

    @classmethod
    def setUp(cls):
        cls.client = Client()

    def gen_content(self, creds):
        content = {
            'username': creds['username'],
            'email': creds['email'],
            'password1': creds['password'],
            'password2': creds['password'],
            'first_name': creds['username'][:8],
            'last_name': creds['username'][8:],
        }
        return content

    def create_registration_request(self, creds):
        """
        Create a registration request via the api
        """
        content = self.gen_content(creds)
        resp = self.client.post('/accounts/request_access/', content)
        return resp

    def test_register_user(self):
        """
        Create a registraton request and ensure that the user is inactive
        """
        creds = gen_creds()
        self.create_registration_request(creds)
        # check if the group reguest is generated
        self.assertTrue(GroupRequest.objects.get(pk=1))
        # check that the user was created and set to inactive
        user = User.objects.get(username=creds['username'])
        self.assertFalse(user.is_active)

    def test_username_in_use(self):
        """
        Attempts to register user with username already in use
        """
        creds = gen_creds()
        self.create_registration_request(creds)
        user = User.objects.get(username=creds['username'])
        self.assertTrue(user is not None)
        # get the GroupRequest for the above registration request
        gr = GroupRequest.objects.get(user=user)
        self.create_registration_request(creds)
        # check to see that there is only 1 registration request and that the second one was denied
        self.assertTrue(len(GroupRequest.objects.filter(user=gr.user)) == 1)

    def test_form_username_in_use(self):
        """
        Test if form validation passed with username that already exits
        in the application
        """
        creds = self.gen_content(gen_creds())
        username = creds['username']
        # create the first user
        form1 = RegisterForm(data=creds)
        form1.save()
        # validate the Register form for the second user
        form2 = RegisterForm(data=creds)
        form2.is_valid()
        username_errors = form2.errors['username']
        self.assertTrue(username_errors)
        self.assertTrue(f'Username {username} is already in use' in username_errors[0])


class PermissionsTests(TestCase):
    """
    Check the the correct groups are assigned and fields are set on registration 
    and making a user an admin
    """
    @classmethod
    def setUp(cls):
        """
        Called once when the class is called to ensure groups are initialized
        """
        call_command('create_groups')

    def create_admin_context(self):
        """
        Create an admin user and log it into the client
        """
        user, creds = create_testuser()
        user.make_admin()
        self.client = Client()
        self.client.login(username=creds['username'], password=creds['password'])
        return user

    def test_registered_on_register(self):
        """
        Test that user is given the Registered group upon registering
        """
        creds = gen_creds()
        self.create_admin_context()
        # create registration request
        resp = self.client.post('/accounts/request_access/', {
                'username': creds['username'],
                'email': creds['email'],
                'password1': creds['password'],
                'password2': creds['password'],
                'first_name': creds['username'][:8],
                'last_name': creds['username'][8:],
            })
        user = User.objects.get(username=creds['username'])
        self.assertTrue(user is not None)
        # get GroupRequest for user and approve it
        group_request = GroupRequest.objects.get(user=user)
        group_request.approve_request(resp.wsgi_request)
        # check that the user now has the 'Registered' group
        self.assertTrue(user.groups.filter(name=GROUPS['default']).exists())

    def test_make_admin(self):
        """
        Test that make_admin() function adds user to Admin group and sets is_staff flag
        """
        self.create_admin_context()
        user, _ = create_testuser()
        user.make_admin()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)


class GroupRequestTests(TestCase):
    """
    approve_request
        Registered (covered in test_registered_on_register)
        Admin (covered in test_make_admin)
    deny_request
    """

    @classmethod
    def setUp(cls):
        """
        Called once when the class is called to ensure groups are initialized
        """
        call_command('create_groups')

    def create_admin_context(self):
        """
        Create an admin user and log it into the client
        """
        user, creds = create_testuser()
        user.make_admin()
        self.client = Client()
        self.client.login(username=creds['username'], password=creds['password'])
        return user

    def test_deny_request(self):
        """
        Test that the correct fields are set when denying a GroupRequest
        """
        self.create_admin_context()
        test_user, _ = create_testuser()
        gr = GroupRequest.objects.create(user=test_user)
        # generate a request object to pass to deny_request()
        resp = self.client.get('/')
        gr.deny_request(resp.wsgi_request)
        # check that the request is not approved and was reviewed as the defualt is False
        self.assertFalse(gr.approved)
        self.assertTrue(gr.reviewed_by)
