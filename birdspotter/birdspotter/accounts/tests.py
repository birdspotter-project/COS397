from django.test import TestCase, Client
from django.contrib.auth.forms import PasswordChangeForm

import time
import random
import string

from .models import User
from .forms import AccountForm


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

    @classmethod
    def setup():
        self.client = Client()

    def test_reguster_user(self):
        creds = gen_creds()
        self.client.post()

    