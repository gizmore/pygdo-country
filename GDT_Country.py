from gdo.base.GDO import GDO
from gdo.base.Trans import t
from gdo.core.GDT_Char import GDT_Char
from gdo.core.GDT_ObjectSelect import GDT_ObjectSelect
from gdo.country.GDO_Country import GDO_Country


class GDT_Country(GDT_Char, GDT_ObjectSelect):

    def __init__(self, name: str):
        super().__init__(name)
        self.table(GDO_Country.table())
        self.maxlen(2)
        self.ascii()
        self.case_s()

    def gdo_column_define(self) -> str:
        return GDT_Char.gdo_column_define(self)

    def query_gdos(self, val: str) -> list[GDO]:
        if len(val) == 2:
            if gdo := self._table.get_by_aid(val):
                return [gdo]
        if gdt := self._table.column('country_name'):
            return self._table.select().where(f"{gdt.get_name()} LIKE '%{GDO.escape(val)}%'").exec().fetch_all()
        return GDO.EMPTY_LIST

    ##########
    # Render #
    ##########

    def render_name(self) -> str:
        if v := self.get_value():
            return v.render_name()
        return t('none')

    def render_html(self) -> str:
        if v := self.get_value():
            return v.render_html()
        from gdo.country.module_country import module_country
        return f'<span class="gdo-country"><img src="{module_country.instance().www_path(f"img/ZZ.png")}" title="{t('no_country')}" alt="{t('no_country')}" /></span>'
