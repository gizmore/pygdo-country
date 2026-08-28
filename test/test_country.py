import os

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.base.ModuleLoader import ModuleLoader
from gdo.country.GDO_Country import GDO_Country
from gdo.country.GDT_Country import GDT_Country
from gdo.country.module_country import module_country
from gdotest.TestUtil import GDOTestCase, reinstall_module, WebPlug


class CountryTest(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        reinstall_module('country')
        WebPlug.COOKIES = {}
        Application.init_cli()
        loader.init_modules(True, True)
        loader.init_cli()

    async def test_country(self):
        out = GDO_Country.table().get_by_aid('DE').render_html()
        self.assertIn('background-position:-96px -80px', out, 'render does not use ISO sprite coordinates.')
        self.assertIn('Germany', out, 'render#2 does not work.')

    async def test_01_generates_the_full_country_sprite(self):
        from PIL import Image
        sprite = module_country.instance().file_path('img/flags.png')
        with Image.open(sprite) as image:
            self.assertEqual((26 * 32, 26 * 20), image.size)

    async def test_02_has_portable_icon(self):
        self.assertEqual('⚑', GDT_Country('country').render_icon(Mode.render_cli))

    async def test_03_card_renders_the_country_name(self):
        field = GDT_Country('country').val('DE')
        self.assertIn(field.render_name(), field.render_card())

    async def test_04_country_resolution_prefers_exact_iso(self):
        field = GDT_Country('country')
        self.assertEqual('DE', field.get_by_name('de').get_id())
