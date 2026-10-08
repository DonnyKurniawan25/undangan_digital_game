from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse


class ClayLandingTests(SimpleTestCase):
    def render_landing(self, user=None):
        request = RequestFactory().get('/')
        request.user = user or AnonymousUser()
        return render_to_string(
            'undangan/landing.html',
            {'jumlah_tamu': 0, 'jumlah_ucapan': 0},
            request=request,
        )

    def test_landing_loads_clay_design_with_existing_demo_and_auth_links(self):
        html = self.render_landing()
        self.assertIn('css/landing-clay.css', html)
        self.assertIn('class="clay-landing"', html)
        self.assertIn(reverse('undangan:register'), html)
        self.assertIn(reverse('undangan:login'), html)
        for route in (
            'beranda', 'beranda_lombok', 'beranda_tropis',
            'beranda_desa', 'beranda_gedung', 'beranda_safari',
        ):
            self.assertIn(reverse('undangan:' + route), html)
        self.assertEqual(html.count('class="faq-question"'), 6)

    def test_signed_in_users_keep_dashboard_and_superadmin_actions(self):
        html = self.render_landing(SimpleNamespace(is_authenticated=True, is_superuser=True))
        self.assertIn('btn-hero-dashboard', html)
        self.assertIn(reverse('undangan:dashboard'), html)
        self.assertIn(reverse('undangan:superadmin_index'), html)
        self.assertNotIn('btn-hero-register', html)
