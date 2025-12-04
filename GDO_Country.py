from functools import lru_cache

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Trans import t
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Char import GDT_Char
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_UInt import GDT_UInt


class GDO_Country(GDO):

    def gdo_persistent(self) -> bool:
        return True

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('country_id'),
            GDT_Char('country_iso2').maxlen(2).not_null(),
            GDT_String('country_name').not_null(),
            GDT_UInt('country_population'),
            GDT_UInt('country_phone_code'),
        ]

    def get_iso2(self) -> str:
        return self.gdo_val('country_iso2')

    def render_name(self):
        return t(f'c_{self.get_iso2()}')

    @lru_cache(maxsize=None)
    def render_html(self):
        from gdo.country.module_country import module_country
        return f'<img src="{module_country.instance().www_path(f"img/{self.get_iso2()}.png")} title="{self.render_name()}">" alt="{self.render_name()}" />'
