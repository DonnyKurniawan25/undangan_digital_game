from html.parser import HTMLParser
import secrets

from django.contrib.auth.models import AnonymousUser, User
from django.template.loader import get_template, render_to_string
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from .models import Undangan


class FormFields(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.forms = []
        self.inputs = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'form':
            self.forms.append(attrs)
        if tag == 'input' and attrs.get('name'):
            self.inputs[attrs['name']] = attrs


class ClayAuthDesignTests(SimpleTestCase):
    def render_auth(self, template):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        return render_to_string(template, request=request)

    def test_login_uses_clay_without_changing_form_contract(self):
        html = self.render_auth('auth/login.html')
        self.assertTrue('class="clay-auth"' in html, 'Login must opt in to the clay auth design')
        self.assertTrue('css/auth-clay.css' in html, 'Login must load its isolated stylesheet')
        parser = FormFields(html)
        self.assertEqual(parser.forms[0]['method'].lower(), 'post')
        self.assertEqual(parser.forms[0]['action'], reverse('undangan:login'))
        self.assertEqual(set(parser.inputs), {'csrfmiddlewaretoken', 'username', 'password'})
        self.assertEqual(parser.inputs['password']['type'], 'password')
        self.assertEqual(parser.inputs['password']['autocomplete'], 'current-password')
        self.assertIn(reverse('undangan:register'), html)
        self.assertIn(reverse('undangan:landing'), html)

    def test_register_uses_clay_and_preserves_all_required_fields(self):
        html = self.render_auth('auth/register.html')
        self.assertTrue('class="clay-auth"' in html, 'Register must opt in to the clay auth design')
        self.assertTrue('css/auth-clay.css' in html, 'Register must load its isolated stylesheet')
        parser = FormFields(html)
        self.assertEqual(parser.forms[0]['method'].lower(), 'post')
        self.assertEqual(parser.forms[0]['action'], reverse('undangan:register'))
        required = {'nama', 'username', 'email', 'password', 'password_confirm'}
        self.assertEqual(set(parser.inputs), required | {'csrfmiddlewaretoken'})
        for name in required:
            self.assertIn('required', parser.inputs[name])
        self.assertEqual(parser.inputs['email']['type'], 'email')
        for name in ('password', 'password_confirm'):
            self.assertEqual(parser.inputs[name]['type'], 'password')
            self.assertEqual(parser.inputs[name]['autocomplete'], 'new-password')
        self.assertIn(reverse('undangan:login'), html)
        self.assertIn(reverse('undangan:landing'), html)

    def test_admin_and_dashboard_templates_do_not_load_auth_design(self):
        for name in ('dashboard/base_dashboard.html', 'superadmin/base_superadmin.html'):
            with self.subTest(template=name):
                source = get_template(name).template.source
                self.assertNotIn('auth-clay.css', source)
                self.assertNotIn('clay-auth', source)


class AuthFormRegressionTests(TestCase):
    """Exercise preserved auth flows using an isolated test database only."""

    def test_login_by_username_and_email_still_redirects_to_dashboard(self):
        password = secrets.token_urlsafe(20)
        user = User.objects.create_user('claylogintest', email='claylogin@example.test', password=password)
        for identifier in (user.username, user.email):
            with self.subTest(identifier=identifier):
                response = self.client.post(reverse('undangan:login'), {
                    'username': identifier, 'password': password,
                })
                self.assertRedirects(response, reverse('undangan:dashboard'), fetch_redirect_response=False)
                self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
                self.client.logout()

    def test_registration_still_creates_account_and_initial_invitation(self):
        password = secrets.token_urlsafe(20)
        response = self.client.post(reverse('undangan:register'), {
            'nama': 'Pengguna Uji Clay', 'username': 'clayregistertest',
            'email': 'clayregister@example.test',
            'password': password, 'password_confirm': password,
        })
        self.assertRedirects(response, reverse('undangan:dashboard'), fetch_redirect_response=False)
        user = User.objects.get(username='clayregistertest')
        self.assertTrue(user.check_password(password))
        self.assertEqual(Undangan.objects.filter(user=user).count(), 1)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_server_rejections_still_render_clay_error_messages(self):
        login = self.client.post(reverse('undangan:login'), {'username': '', 'password': ''})
        self.assertEqual(login.status_code, 200)
        self.assertContains(login, 'Username atau kata sandi tidak sesuai')
        self.assertContains(login, 'role="alert"')
        register = self.client.post(reverse('undangan:register'), {
            'username': 'claymismatchtest', 'password': 'mismatch-one', 'password_confirm': 'mismatch-two',
        })
        self.assertEqual(register.status_code, 200)
        self.assertContains(register, 'Konfirmasi kata sandi tidak cocok')
        self.assertFalse(User.objects.filter(username='claymismatchtest').exists())
