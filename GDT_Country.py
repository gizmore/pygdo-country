from gdo.core.GDT_ObjectSelect import GDT_ObjectSelect
from gdo.country.GDO_Country import GDO_Country


class GDT_Country(GDT_ObjectSelect):

    def __init__(self, name: str):
        super().__init__(name)
        self._table = GDO_Country.table()
