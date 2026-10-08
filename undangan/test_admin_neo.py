"""Admin presentation regressions; run with config.settings and isolated SQLite."""
from html.parser import HTMLParser
from pathlib import Path
import colorsys
import re
import secrets

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import Client, RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from .models import Tamu, Ucapan


class AdminMarkup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def matching(self, tag, **attrs):
        return [element for name, element in self.elements
                if name == tag and all(element.get(key) == value for key, value in attrs.items())]


class AdminNeoTemplateTests(SimpleTestCase):
    def test_login_opts_into_late_scoped_styles_without_replacing_native_controls(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)
        markup = AdminMarkup(response.content.decode())
        classes = markup.matching('body')[0]['class'].split()
        self.assertIn('neo-internal', classes)
        self.assertIn('neo-admin', classes)
        self.assertIn('login', classes)
        styles = [link['href'].split('?')[0] for link in markup.matching('link', rel='stylesheet')]
        self.assertEqual(styles[-2:], ['/static/css/internal-neo.css', '/static/css/admin-neo.css'])
        self.assertIn('/static/admin/css/login.css', styles)
        self.assertIn('/static/admin/css/responsive.css', styles)
        self.assertEqual(len(markup.matching('button', **{'class': 'theme-toggle'})), 1)
        self.assertTrue(markup.matching('script', src='/static/admin/js/theme.js'))
        form = markup.matching('form', id='login-form')[0]
        self.assertEqual(form['method'], 'post')
        self.assertEqual(form['action'], reverse('admin:login'))
        self.assertTrue(markup.matching('input', name='csrfmiddlewaretoken'))
        self.assertTrue(markup.matching('input', name='username', autocomplete='username'))
        self.assertTrue(markup.matching('input', name='password', autocomplete='current-password'))
        self.assertTrue(markup.matching('input', name='next'))


class AdminNeoMaterialTests(SimpleTestCase):
    def css(self):
        path = Path(settings.BASE_DIR) / 'static/css/admin-neo.css'
        self.assertTrue(path.exists(), 'Django admin needs its own scoped Neo-Brutalism stylesheet')
        return re.sub(r'/\*.*?\*/', '', path.read_text(encoding='utf-8'), flags=re.S)

    def test_admin_styles_are_scoped_square_flat_and_use_shared_navy_tokens(self):
        css = self.css()
        blocks = re.findall(r'([^{}]+)\{([^{}]*)\}', css)
        self.assertGreater(len(blocks), 10, 'Cover native admin components, not just the page background')
        for selectors, declarations in blocks:
            for selector in re.split(r',\s*(?![^()]*\))', selectors.strip()):
                self.assertIn('.neo-admin', selector, 'Never restyle public or custom-dashboard pages')
            for radius in re.findall(r'border-radius\s*:\s*([^;]+);', declarations):
                self.assertEqual(radius.replace('!important', '').strip(), '0')
        self.assertNotRegex(css, r'(?:linear|radial)-gradient\(|blur\(')
        self.assertIn('border: 3px solid var(--neo-border)', css)
        self.assertIn('box-shadow: var(--neo-shadow)', css)
        self.assertIn('box-shadow: var(--neo-small-shadow)', css)
        self.assertIn('border-radius: 0 !important', css)
        self.assertIn('background: var(--neo-brand)', css)
        for token in ('--primary', '--body-fg', '--body-bg', '--link-fg', '--border-color',
                      '--header-bg', '--button-bg', '--default-button-bg', '--object-tools-bg'):
            self.assertRegex(css, re.escape(token) + r':\s*var\(--neo-[\w-]+\)')
        self.assertIn(':focus-visible', css)
        self.assertIn('outline: 3px solid', css)
        self.assertIn('overflow-x: auto', css)
        self.assertIn('prefers-reduced-motion', css)
        for color in re.findall(r'#[0-9a-fA-F]{6}\b', css):
            rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            hue, _, saturation = colorsys.rgb_to_hls(*rgb)
            self.assertFalse(235 < hue * 360 < 335 and saturation > .08, color)

    def test_semantic_messages_keep_aa_contrast_in_light_dark_and_auto_modes(self):
        css = self.css()
        self.assertIn('html[data-theme="dark"] .neo-admin', css)
        self.assertIn('@media (prefers-color-scheme: dark)', css)
        self.assertIn('html[data-theme="auto"] .neo-admin', css)
        self.assertIn('html:not([data-theme]) .neo-admin', css)
        blocks = re.findall(r'([^{}]+)\{([^{}]*)\}', css)
        palettes = []
        for selectors, declarations in blocks:
            tokens = dict(re.findall(r'(--neo-admin-[\w-]+):\s*(#[0-9a-fA-F]{6});', declarations))
            if '--neo-admin-success-ink' in tokens:
                palettes.append((selectors, tokens))
        self.assertEqual(len(palettes), 3, 'Light, explicit dark and system-auto need matching semantic palettes')

        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
            return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))

        def contrast(foreground, background):
            light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
            return (light + .05) / (dark + .05)

        for selectors, tokens in palettes:
            for status in ('success', 'warning', 'error'):
                with self.subTest(theme=selectors.strip(), status=status):
                    self.assertGreaterEqual(contrast(tokens[f'--neo-admin-{status}-ink'],
                                                     tokens[f'--neo-admin-{status}-bg']), 4.5)
        for background in ('#173b66', '#315d88', '#991b1b', '#7f1d1d'):
            with self.subTest(button_background=background):
                self.assertGreaterEqual(contrast('#ffffff', background), 4.5)


class AdminNeoRegressionTests(TestCase):
    """Real admin requests and writes against Django's isolated test database."""

    @classmethod
    def setUpTestData(cls):
        cls.password = secrets.token_urlsafe(24)
        cls.admin = User.objects.create_superuser('neo-admin-test', 'neo@example.test', cls.password)
        cls.guest = Tamu.objects.create(nama='Tamu Neo Test')
        cls.message = Ucapan.objects.create(nama='Pesan Neo Test', pesan='Terima kasih', tamu=cls.guest)

    def setUp(self):
        self.client.force_login(self.admin)

    def assert_admin_shell(self, response, bodyclass=None):
        self.assertEqual(response.status_code, 200)
        markup = AdminMarkup(response.content.decode())
        classes = markup.matching('body')[0]['class'].split()
        self.assertIn('neo-internal', classes)
        self.assertIn('neo-admin', classes)
        if bodyclass:
            self.assertIn(bodyclass, classes)
        styles = [link['href'].split('?')[0] for link in markup.matching('link', rel='stylesheet')]
        self.assertEqual(styles[-2:], ['/static/css/internal-neo.css', '/static/css/admin-neo.css'])
        self.assertTrue(markup.matching('script', src='/static/admin/js/theme.js'))
        return markup

    def test_index_keeps_branding_accessible_theme_toggle_and_post_logout(self):
        response = self.client.get(reverse('admin:index'))
        markup = self.assert_admin_shell(response)
        self.assertContains(response, 'Panel Undangan Pernikahan')
        self.assertTrue(markup.matching('a', href='#content-start'))
        self.assertEqual(len(markup.matching('button', **{'class': 'theme-toggle'})), 1)
        logout = markup.matching('form', id='logout-form')[0]
        self.assertEqual(logout['method'], 'post')
        self.assertEqual(logout['action'], reverse('admin:logout'))
        self.assertTrue(markup.matching('input', name='csrfmiddlewaretoken'))

    def test_changelist_keeps_sidebar_filters_search_actions_and_editable_fields(self):
        response = self.client.get(reverse('admin:undangan_ucapan_changelist'))
        markup = self.assert_admin_shell(response, 'change-list')
        self.assertTrue(markup.matching('nav', id='nav-sidebar'))
        self.assertTrue(markup.matching('button', id='toggle-nav-sidebar'))
        self.assertTrue(markup.matching('input', id='nav-filter'))
        self.assertTrue(markup.matching('input', name='q'))
        self.assertTrue(markup.matching('select', name='action'))
        self.assertTrue(markup.matching('input', name='_selected_action', value=str(self.message.pk)))
        self.assertTrue(markup.matching('table', id='result_list'))
        self.assertTrue(markup.matching('nav', id='changelist-filter'))
        self.assertTrue(markup.matching('input', name='form-TOTAL_FORMS'))
        self.assertTrue(markup.matching('input', name='form-0-disetujui'))
        self.assertContains(response, 'admin/js/actions.js')
        self.assertContains(response, 'admin/js/nav_sidebar.js')

    def test_search_and_filters_still_use_native_queryset(self):
        Ucapan.objects.create(nama='Bukan Pencarian', pesan='Lain', kehadiran=Ucapan.TIDAK)
        response = self.client.get(reverse('admin:undangan_ucapan_changelist'), {
            'q': 'Pesan Neo', 'kehadiran__exact': Ucapan.HADIR,
        })
        self.assert_admin_shell(response, 'change-list')
        self.assertEqual(list(response.context['cl'].queryset.values_list('pk', flat=True)), [self.message.pk])

    def test_pagination_still_exposes_next_page(self):
        Ucapan.objects.bulk_create([Ucapan(nama=f'Pagination {i}', pesan='Test') for i in range(101)])
        response = self.client.get(reverse('admin:undangan_ucapan_changelist'))
        self.assert_admin_shell(response, 'change-list')
        self.assertTrue(response.context['cl'].multi_page)
        self.assertContains(response, '?p=2')
        next_page = self.client.get(reverse('admin:undangan_ucapan_changelist'), {'p': '2'})
        self.assert_admin_shell(next_page, 'change-list')
        self.assertEqual(next_page.context['cl'].page_num, 2)

    def test_change_form_keeps_native_media_and_saves_with_success_message(self):
        url = reverse('admin:undangan_ucapan_change', args=[self.message.pk])
        response = self.client.get(url)
        markup = self.assert_admin_shell(response, 'change-form')
        self.assertTrue(markup.matching('form', id='ucapan_form', method='post'))
        self.assertTrue(markup.matching('input', name='csrfmiddlewaretoken'))
        for name in ('nama', 'jumlah_orang'):
            self.assertTrue(markup.matching('input', name=name))
        self.assertTrue(markup.matching('textarea', name='pesan'))
        self.assertTrue(markup.matching('select', name='kehadiran'))
        self.assertContains(response, 'admin/js/change_form.js')
        self.assertContains(response, 'admin/js/admin/RelatedObjectLookups.js')
        saved = self.client.post(url, {
            'nama': 'Pesan Diubah Neo', 'pesan': 'Pesan baru', 'kehadiran': Ucapan.HADIR,
            'jumlah_orang': '2', 'disetujui': 'on', 'tamu': str(self.guest.pk), '_save': 'Simpan',
        }, follow=True)
        self.assert_admin_shell(saved, 'change-list')
        self.message.refresh_from_db()
        self.assertEqual(self.message.nama, 'Pesan Diubah Neo')
        self.assertEqual(self.message.jumlah_orang, 2)
        self.assertTrue(AdminMarkup(saved.content.decode()).matching('li', **{'class': 'success'}))

    def test_list_editable_post_still_saves(self):
        response = self.client.post(reverse('admin:undangan_ucapan_changelist'), {
            'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000',
            'form-0-id': str(self.message.pk), '_save': 'Simpan',
        })
        self.assertEqual(response.status_code, 302)
        self.message.refresh_from_db()
        self.assertFalse(self.message.disetujui)

    def test_delete_confirmation_remains_two_step_and_csrf_protected(self):
        url = reverse('admin:undangan_ucapan_delete', args=[self.message.pk])
        response = self.client.get(url)
        markup = self.assert_admin_shell(response, 'delete-confirmation')
        self.assertTrue(markup.matching('input', name='csrfmiddlewaretoken'))
        self.assertTrue(markup.matching('input', name='post', value='yes'))
        self.assertTrue(markup.matching('a', **{'class': 'button cancel-link'}))
        self.assertContains(response, 'admin/js/cancel.js')
        self.assertTrue(Ucapan.objects.filter(pk=self.message.pk).exists())
        deleted = self.client.post(url, {'post': 'yes'})
        self.assertRedirects(deleted, reverse('admin:undangan_ucapan_changelist'), fetch_redirect_response=False)
        self.assertFalse(Ucapan.objects.filter(pk=self.message.pk).exists())

    def test_bulk_delete_action_still_requires_confirmation(self):
        url = reverse('admin:undangan_ucapan_changelist')
        selected = {'action': 'delete_selected', '_selected_action': str(self.message.pk)}
        response = self.client.post(url, selected)
        self.assert_admin_shell(response, 'delete-confirmation')
        self.assertTrue(Ucapan.objects.filter(pk=self.message.pk).exists())
        confirmed = self.client.post(url, {**selected, 'post': 'yes'})
        self.assertEqual(confirmed.status_code, 302)
        self.assertFalse(Ucapan.objects.filter(pk=self.message.pk).exists())

    def test_login_and_logout_require_valid_csrf_and_keep_native_redirects(self):
        client = Client(enforce_csrf_checks=True)
        login_url = reverse('admin:login')
        login = client.get(login_url)
        self.assert_admin_shell(login, 'login')
        credentials = {'username': self.admin.username, 'password': self.password,
                       'next': reverse('admin:index')}
        self.assertEqual(client.post(login_url, credentials).status_code, 403)
        token = AdminMarkup(login.content.decode()).matching('input', name='csrfmiddlewaretoken')[0]['value']
        accepted = client.post(login_url, {**credentials, 'csrfmiddlewaretoken': token})
        self.assertRedirects(accepted, reverse('admin:index'), fetch_redirect_response=False)
        index = client.get(reverse('admin:index'))
        token = AdminMarkup(index.content.decode()).matching('input', name='csrfmiddlewaretoken')[0]['value']
        self.assertEqual(client.post(reverse('admin:logout')).status_code, 403)
        logged_out = client.post(reverse('admin:logout'), {'csrfmiddlewaretoken': token})
        self.assertRedirects(logged_out, reverse('undangan:login'), fetch_redirect_response=False)
        self.assertNotIn('_auth_user_id', client.session)

    def test_nonstaff_and_unprivileged_staff_permissions_are_unchanged(self):
        url = reverse('admin:undangan_ucapan_changelist')
        ordinary = User.objects.create_user('neo-ordinary-test')
        self.client.force_login(ordinary)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('admin:login') + '?next=' + url,
                             fetch_redirect_response=False)
        ordinary.is_staff = True
        ordinary.save(update_fields=['is_staff'])
        self.client.force_login(ordinary)
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_popup_and_user_widget_pages_keep_native_classes_and_media(self):
        popup = self.client.get(reverse('admin:undangan_tamu_add'), {'_popup': '1'})
        markup = self.assert_admin_shell(popup, 'popup')
        self.assertFalse(markup.matching('header', id='header'))
        self.assertTrue(markup.matching('input', name='_popup', value='1'))
        user = self.client.get(reverse('admin:auth_user_change', args=[self.admin.pk]))
        self.assert_admin_shell(user, 'change-form')
        self.assertContains(user, 'admin/js/SelectFilter2.js')
        self.assertContains(user, 'admin/js/SelectBox.js')
        self.assertContains(user, 'admin/css/forms.css')
        self.assertTrue(AdminMarkup(user.content.decode()).matching('select', name='groups'))

    def test_inline_formsets_keep_native_management_fields_and_add_row_script(self):
        class UcapanInline(admin.TabularInline):
            model = Ucapan
            extra = 1

        class TamuInlineAdmin(admin.ModelAdmin):
            inlines = (UcapanInline,)

        request = RequestFactory().get(reverse('admin:undangan_tamu_change', args=[self.guest.pk]))
        request.user = self.admin
        request.session = self.client.session
        request._messages = FallbackStorage(request)
        response = TamuInlineAdmin(Tamu, admin.site).changeform_view(request, str(self.guest.pk))
        response.render()
        markup = self.assert_admin_shell(response, 'change-form')
        self.assertTrue(markup.matching('input', name='ucapan-TOTAL_FORMS'))
        self.assertTrue(markup.matching('input', name='ucapan-INITIAL_FORMS'))
        self.assertTrue(markup.matching('input', name='ucapan-0-id', value=str(self.message.pk)))
        self.assertTrue(markup.matching('div', id='ucapan-group'))
        self.assertContains(response, 'admin/js/inlines.js')
        self.assertContains(response, 'data-inline-formset=')

    def test_invalid_form_keeps_native_validation_and_error_summary(self):
        response = self.client.post(reverse('admin:undangan_ucapan_add'), {'_save': 'Simpan'})
        self.assert_admin_shell(response, 'change-form')
        self.assertTrue(response.context['adminform'].form.errors)
        self.assertContains(response, 'class="errornote"')
        self.assertContains(response, 'class="errorlist"')
        self.assertEqual(Ucapan.objects.count(), 1)
