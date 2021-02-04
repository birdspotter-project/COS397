from django.test import TestCase
import time
import random
import string
from .models import User
from .forms import AccountForm

def gen_name():
    return 'testUser' + str(time.time()).replace('.', '')

class AccountEditingTests(TestCase):

    def create_testuser(self):
        """
        Create test user to be called from every test that contains a time string from when the test starts
        """
        # The following credentials are used for unit testing purposes only
        self.CREDS = {
            'username': gen_name(),
            'password': ''.join(random.choice(string.ascii_letters) for _ in range(9)) # nosec
        }
        self.user = User.objects.create(username=self.CREDS['username'])
        self.user.set_password(self.CREDS['password'])
        self.user.save()

    def test_edit_username_success(self):
        """
        Ensure that a username can be changed if it is not alreay in use
        """
        self.create_testuser()
        changed = {
            'username': 'changedUsername'
        }
        form = AccountForm(data=changed, instance=self.user)
        form.save()
        changed_user = User.objects.get(username=changed['username'])
        self.assertEqual(changed_user.username, changed['username'])
        # lambda is required as the comparison must be callable
        self.assertRaises(User.DoesNotExist,
                          lambda:
                          User.objects.get(username=self.CREDS['username']))

    def test_edit_username_exists(self):
        """
        Ensure that if a username connot be changed to a username currently in use
        """
        self.create_testuser()
        username = gen_name()
        user = User(username=username)
        user.save()
        form = AccountForm(data={'username': self.CREDS['username']},
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
        self.create_testuser()
        name_str = 'test_changed'
        changed = {
            'first_name': name_str,
            'last_name': name_str,
            'email': name_str + '@test.com'
        }
        form = AccountForm(data=changed, instance=self.user)
        if form.is_valid():
            form.save()
        self.assertEqual(self.user.first_name, name_str)
        self.assertEqual(self.user.last_name, name_str)
        self.assertEqual(self.user.email, name_str + '@test.com')

    def test_edit_email_invalid(self):
        """
        Attempt to change a user's email to an invalid email address
        """
        emails = ['test_string', '@test.com', 'test@.', 'test@a.', 'test@.a']
        self.create_testuser()
        for email in emails:
            form = AccountForm(data={'email': email}, instance=self.user)
            if success := form.is_valid():
                form.save()
            self.assertFalse(success)