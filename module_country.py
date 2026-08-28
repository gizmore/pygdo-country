from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.core.GDT_Bool import GDT_Bool
from gdo.country.GDO_Country import GDO_Country
import csv
from pathlib import Path

from PIL import Image
from gdo.base.GDO import GDO

from gdo.country.GDT_Country import GDT_Country

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from gdo.ui.GDT_Page import GDT_Page


class module_country(GDO_Module):

    FLAG_WIDTH = 32
    FLAG_HEIGHT = 20
    FLAG_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self):
        super().__init__()
        self._priority = 40

    def gdo_classes(self) -> list[type[GDO]]:
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
        self.generate_flag_sprite()

    def generate_flag_sprite(self) -> None:
        """Build a fixed A-Z × A-Z ISO-3166 flag sprite for CSS rendering."""
        letters = self.FLAG_LETTERS
        width = self.FLAG_WIDTH
        height = self.FLAG_HEIGHT
        image_dir = Path(self.file_path('img'))
        with Image.open(image_dir / 'ZZ.png') as source:
            fallback = source.convert('RGBA')
        sprite = Image.new('RGBA', (len(letters) * width, len(letters) * height))
        for y, second in enumerate(letters):
            for x, first in enumerate(letters):
                flag_path = image_dir / f'{first}{second}.png'
                try:
                    if flag_path.is_file():
                        with Image.open(flag_path) as source:
                            flag = source.convert('RGBA')
                    else:
                        flag = fallback.copy()
                except OSError:
                    flag = fallback.copy()
                flag.thumbnail((width, height), Image.Resampling.LANCZOS)
                left = x * width + (width - flag.width) // 2
                top = y * height + (height - flag.height) // 2
                sprite.alpha_composite(flag, (left, top))
        sprite.save(image_dir / 'flags.png', 'PNG')

    @classmethod
    def flag_position(cls, iso2: str) -> str:
        """Return the sprite position for an ISO alpha-2 country code."""
        code = str(iso2 or 'ZZ').upper()
        if len(code) != 2 or any(letter not in cls.FLAG_LETTERS for letter in code):
            code = 'ZZ'
        return f'{-cls.FLAG_LETTERS.index(code[0]) * cls.FLAG_WIDTH}px {-cls.FLAG_LETTERS.index(code[1]) * cls.FLAG_HEIGHT}px'

    def render_flag(self, iso2: str, title: str) -> str:
        position = self.flag_position(iso2)
        return f'<span class="gdo-country" style="background-position:{position}" title="{title}"></span>'

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.add_css('css/pygdo-country.css')

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
