import colorsys
import re

from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.test import SimpleTestCase


class NavyClayPaletteTests(SimpleTestCase):
    def assert_navy_palette(self, path):
        with open(finders.find(path), encoding='utf-8') as handle:
            css = handle.read()
        self.assertIn('#173b66', css, 'The public accent must use navy')
        colors = []
        for value in re.findall(r'#[0-9a-fA-F]{6}\b', css):
            colors.append((value, [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]))
        for match in re.finditer(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', css):
            colors.append((match.group(0), [int(match.group(i)) / 255 for i in (1, 2, 3)]))
        purple = []
        for value, channels in colors:
            hue, lightness, saturation = colorsys.rgb_to_hls(*channels)
            if 235 < hue * 360 < 335 and saturation > .08:
                purple.append(value)
        self.assertEqual(purple, [], 'Purple fills, text, borders and tinted shadows must be removed')

    def test_landing_palette_is_navy_without_purple(self):
        self.assert_navy_palette('css/landing-clay.css')

    def test_shared_login_register_palette_is_navy_without_purple(self):
        self.assert_navy_palette('css/auth-clay.css')

    def test_primary_button_gradients_keep_readable_white_text(self):
        def luminance(hex_color):
            value = hex_color.lstrip('#')
            if len(value) == 3:
                value = ''.join(channel * 2 for channel in value)
            channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
            linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
            return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))

        checked = 0
        for path in ('css/landing-clay.css', 'css/auth-clay.css'):
            with open(finders.find(path), encoding='utf-8') as handle:
                css = handle.read()
            for selectors, declarations in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
                if not any(name in selectors for name in ('.btn-gold', '.nav-btn-cta', '.btn-submit', '.swal2-confirm')):
                    continue
                gradient = re.search(r'background:\s*linear-gradient\(([^;]+)\);', declarations)
                if not gradient:
                    continue
                checked += 1
                for stop in re.findall(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b', gradient.group(1)):
                    with self.subTest(path=path, selectors=selectors.strip(), stop=stop):
                        self.assertGreaterEqual(1.05 / (luminance(stop) + .05), 4.5)
        self.assertGreaterEqual(checked, 4, 'Cover normal and hover gradients on both public layouts')

    def test_public_browser_theme_color_matches_blue_surface(self):
        for name in ('undangan/landing.html', 'auth/login.html', 'auth/register.html'):
            with self.subTest(template=name):
                source = get_template(name).template.source
                self.assertIn('<meta name="theme-color" content="#f3f7fb">', source)
