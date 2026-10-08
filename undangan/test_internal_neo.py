import re
import secrets
from pathlib import Path

from django.contrib.auth.models import User
from django.template.loader import get_template
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from undangan.views_dashboard import _ambil_undangan_user


USER_PAGES = (
    'dashboard', 'dashboard_ai', 'dashboard_pengaturan', 'dashboard_mempelai',
    'dashboard_acara', 'dashboard_galeri', 'dashboard_rekening', 'dashboard_tamu',
    'dashboard_ucapan', 'dashboard_pembayaran',
)
SUPER_PAGES = (
    'superadmin_index', 'superadmin_users', 'superadmin_undangan',
    'superadmin_transaksi', 'superadmin_ucapan', 'superadmin_ai',
    'superadmin_pengaturan',
)


class InternalNeoPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='neo_ui_test_user', password=secrets.token_urlsafe(24))
        cls.owner = User.objects.create_superuser(username='neo_ui_test_owner', password=secrets.token_urlsafe(24))
        cls.invitation = _ambil_undangan_user(cls.user)

    def assert_neo_page(self, page_name, role):
        response = self.client.get(reverse('undangan:' + page_name))
        self.assertEqual(response.status_code, 200, page_name)
        self.assertTrue('class="neo-internal neo-' + role + '"' in response.content.decode(), 'Missing Neo-Brutalism layout: ' + page_name)
        self.assertContains(response, 'css/internal-neo.css?v=')
        self.assertContains(response, '<meta name="theme-color" content="#f3f7fb">')
        self.assertNotContains(response, 'css/auth-clay.css')
        self.assertNotContains(response, 'css/landing-clay.css')
        return response

    def test_every_user_page_inherits_navy_neo_layout(self):
        self.client.force_login(self.user)
        for page in USER_PAGES:
            with self.subTest(page=page):
                self.assert_neo_page(page, 'user')

    def test_every_superadmin_page_inherits_navy_neo_layout(self):
        self.client.force_login(self.owner)
        for page in SUPER_PAGES:
            with self.subTest(page=page):
                self.assert_neo_page(page, 'superadmin')

    def test_anonymous_requests_still_cannot_open_internal_pages(self):
        for page in USER_PAGES + SUPER_PAGES:
            with self.subTest(page=page):
                response = self.client.get(reverse('undangan:' + page))
                self.assertEqual(response.status_code, 302)

    def test_regular_user_still_cannot_open_superadmin(self):
        self.client.force_login(self.user)
        for page in SUPER_PAGES:
            with self.subTest(page=page):
                response = self.client.get(reverse('undangan:' + page))
                self.assertNotEqual(response.status_code, 200)

    def test_user_form_saves_are_still_owner_scoped(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('undangan:dashboard_pengaturan'), {
            'judul': 'Undangan Pengujian Neo',
            'slug': self.invitation.slug,
            'tema': self.invitation.tema,
        })
        self.assertEqual(response.status_code, 302)
        self.invitation.refresh_from_db()
        self.assertEqual(self.invitation.judul, 'Undangan Pengujian Neo')


class InternalNeoIsolationTests(SimpleTestCase):
    def test_public_pages_keep_clay_and_do_not_import_internal_theme(self):
        for name, expected in (
            ('undangan/landing.html', 'clay-landing'),
            ('auth/login.html', 'clay-auth'),
            ('auth/register.html', 'clay-auth'),
        ):
            with self.subTest(template=name):
                source = get_template(name).template.source
                self.assertIn(expected, source)
                self.assertNotIn('internal-neo.css', source)
                self.assertNotIn('neo-internal', source)

    def test_active_media_tabs_keep_white_text_on_navy_fill(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/internal-neo.css').read_text()
        self.assertTrue(re.search(r'\.neo-internal \.media-source-tab\.active\s*\{[^}]*background:\s*var\(--neo-primary\)', css), 'Active media tabs need an opaque navy fill')
        self.assertTrue(re.search(r'\.neo-internal \.media-source-tab\.active\s*\{[^}]*color:\s*var\(--neo-primary-text\)', css), 'Active media tabs need readable white text')

    def test_narrow_grid_and_filter_hooks_do_not_force_desktop_width(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/internal-neo.css').read_text()
        self.assertTrue('.neo-internal .card { min-width: 0;' in css, 'Grid cards must be allowed to shrink')
        self.assertTrue('grid-template-columns: minmax(0, 1fr)' in get_template('dashboard/ai.html').template.source)
        for name in ('superadmin/undangan.html', 'superadmin/ucapan.html'):
            self.assertTrue('class="neo-filter-select"' in get_template(name).template.source, name)
        self.assertTrue('class="neo-slug-field"' in get_template('dashboard/pengaturan.html').template.source)

    def test_admin_selector_labels_inherit_their_header_ink(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertTrue('.neo-admin .module h2 label { color: inherit;' in css, 'Selector header labels must not become navy-on-navy')

    def test_admin_chosen_permissions_label_stays_readable(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertTrue('.neo-admin .selector-chosen-title label { color: var(--neo-primary-text);' in css)

    def test_admin_legacy_neutral_ink_tracks_the_active_theme(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertTrue('.neo-admin [style*="#555"] { color: var(--neo-muted)' in css)

    def test_dark_feature_badge_uses_fill_not_link_ink(self):
        source = get_template('dashboard/index.html').template.source
        self.assertTrue('class="badge" style="background: var(--neo-primary); color: #fff; font-size: 10px;"' in source)

    def test_sidebar_feature_badge_uses_primary_fill(self):
        source = get_template('dashboard/base_dashboard.html').template.source
        self.assertTrue('margin-left: auto; background: var(--neo-primary); color: #fff;' in source)

    def test_slug_field_can_wrap_at_narrow_desktop_card_width(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/internal-neo.css').read_text()
        self.assertTrue('.neo-internal .neo-slug-field { flex-wrap: wrap;' in css)
        self.assertTrue('.neo-internal .neo-slug-field .form-input { flex: 1 1 200px;' in css)

    def test_admin_inline_success_ink_tracks_the_active_theme(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertTrue('.neo-admin [style*="#2b8a3e"] { color: var(--neo-success)' in css)

    def test_banner_aliases_are_flat_navy_material(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/internal-neo.css').read_text()
        self.assertTrue('--banner-bg: var(--neo-soft);' in css)
        self.assertTrue('--banner-border: var(--neo-border);' in css)

    def test_internal_templates_do_not_keep_backdrop_blur(self):
        root = Path(__file__).resolve().parents[1]
        for group in ('dashboard', 'superadmin'):
            for path in (root / 'templates' / group).glob('*.html'):
                self.assertFalse(re.search(r'backdrop-filter:\s*blur\(', path.read_text()), str(path))

    def test_music_url_placeholder_fits_narrow_active_plan_cards(self):
        self.assertTrue('placeholder="https://.../lagu.mp3"' in get_template('dashboard/pengaturan.html').template.source)

    def test_calendar_hover_uses_opaque_primary_and_white_ink(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertTrue('.neo-admin .calendar td a:hover,' in css)
        self.assertTrue('background-color: var(--neo-primary); color: var(--neo-primary-text); opacity: 1;' in css)

    def test_calendar_does_not_interpolate_through_low_contrast(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertTrue('.neo-admin .calendar td a { transition: none; }' in css)

    def test_permission_selector_action_labels_can_wrap(self):
        css = (Path(__file__).resolve().parents[1] / 'static/css/admin-neo.css').read_text()
        self.assertRegex(css, r'\.neo-admin \.selector-chooseall,\s*\.neo-admin \.selector-clearall\s*\{[^}]*height: auto;[^}]*min-height: 44px;')

    def test_existing_mode_controls_and_mobile_menus_remain_present(self):
        dashboard = get_template('dashboard/base_dashboard.html').template.source
        superadmin = get_template('superadmin/base_superadmin.html').template.source
        for source, markers in (
            (dashboard, ('dashboard_theme', 'toggleTheme()', 'id="android-bottom-bar"', 'openBottomSheet()', 'closeBottomSheet()')),
            (superadmin, ('superadmin_theme', 'toggleSuperTheme()', 'id="super-android-bottom-bar"', 'openSuperBottomSheet()', 'closeSuperBottomSheet()')),
        ):
            for marker in markers:
                self.assertIn(marker, source)
