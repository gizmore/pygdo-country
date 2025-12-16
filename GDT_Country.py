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

    ##########
    # Render #
    ##########

    def render_name(self) -> str:
        if v := self.get_value():
            return v.render_name()
        return t('none')
