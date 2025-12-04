import os

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.country.GDO_Country import GDO_Country
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
        out = GDO_Country.table().get_by_aid('1').render_html()
        self.assertIn('.png', out, 'render does not work.')
