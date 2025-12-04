from gdo.base.GDO_Module import GDO_Module
from gdo.country.GDO_Country import GDO_Country
import csv

class module_country(GDO_Module):

    def gdo_classes(self):
        return [
            GDO_Country,
        ]

    async def gdo_install(self):
        bulk = []
        headers = GDO_Country.table().columns_only('country_name', 'country_iso2')
        with open(self.file_path('data/all.csv'), newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bulk_data = [row['name'], row['alpha-2']]
                bulk.append(bulk_data)
        GDO_Country.table().bulk_insert(headers, bulk)
