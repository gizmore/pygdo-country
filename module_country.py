from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core.GDT_Bool import GDT_Bool
from gdo.country.GDO_Country import GDO_Country
import csv

from gdo.country.GDT_Country import GDT_Country


class module_country(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 40

    def gdo_classes(self):
        return [
            GDO_Country,
        ]

    async def gdo_install(self):
        if not GDO_Country.table().select().where("country_id='DE'").exec().fetch_row():
            bulk = []
            headers = GDO_Country.table().columns_only('country_name', 'country_id')
            with open(self.file_path('data/all.csv'), newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bulk_data = [row['name'], row['alpha-2']]
                    bulk.append(bulk_data)
            GDO_Country.table().bulk_insert(headers, bulk)

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Bool('country_signup_detection').initial('1'),
        ]

    def cfg_signup_detection(self) -> bool:
        return self.get_config_value('country_signup_detection')

    def gdo_user_settings(self) -> list[GDT]:
        return [
            GDT_Country('country_ethnics'),
            GDT_Country('country_living'),
        ]
