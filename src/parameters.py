from typing import Literal
from dataclasses import dataclass

from pydantic import BaseModel, root_validator, validator


@dataclass
class AltskinsParametersDataTypes:
    service_values = Literal[
        'bitskins', 'bitskins(A)', 'bitskins(7)', 'bitskins(LS)',
        'dmarket',
        'market.csgo', 'market.csgo(A)', 'market.csgo(LS)',
        'market.dota', 'market.dota(A)', 'market.dota(LS)',
        'market.rust', 'market.rust(A)', 'market.rust(LS)',
        'steamcommunity', 'steamcommunity(A)', 'steamcommunity(LS)',
        'buff.market', 'buff.market(A)',
        'cs.money', 'cs.money(NO HOLD)', 'cs.money(STORE)', 'cs.money(STORE NO HOLD)', 'cs.money(WIKI)',
        'dota.money',
        'loot.farm', 'loot.farm(DEP)',
        'tradeit.gg', 'tradeit.gg(DEP)',
        'swap.gg', 'swap.gg(DEP)', 'swap.gg(M)',
        'cs.trade', 'cs.trade(DEP)',
        'cs.deals', 'cs.deals(DEP)', 'cs.deals(M)',
        'tradeskinsfast', 'tradeskinsfast(DEP)',
        'skins.cash',
        'mannco.trade',
        'gamdom', 'gamdom(DEP)',
        'wtfskins',
        'dota2bestyolo',
        'godota2'
    ]

class AltskinsParametersModel(BaseModel):
    game_title: Literal['all', 'csgo', 'dota', 'rust', 'tf']
    knife: Literal[0, 1] = 1
    stattrak: Literal[0, 1] = 1
    souvenir: Literal[0, 1] = 1
    sticker: Literal[0, 1] = 1
    service1: AltskinsParametersDataTypes.service_values
    service2: AltskinsParametersDataTypes.service_values
    unstable1: Literal[0, 1] = 1
    unstable2: Literal[0, 1] = 1
    hours1: int = 192
    hours2: int = 192
    priceFrom1: float = None
    priceTo1: float = None
    priceFrom2: float = None
    priceTo2: float = None
    salesBS: int = None
    salesTM: int = None
    salesST: int = None
    name: str = None
    service1Minutes: int = 30
    service2Minutes: int = 30
    percentFrom1: int = None
    percentFrom2: int = None
    service1CountFrom: int = None
    service1CountTo: int = None
    service2CountFrom: int = None
    service2CountTo: int = None
    percentTo1: int = None
    percentTo2: int = None
    page: int = 1
    sort: Literal[
        'service1_to_service2_profit_desc', 'service1_to_service2_profit_asc',
        'service2_to_service1_profit_desc', 'service2_to_service1_profit_asc',
        'service1_price_desc', 'service1_price_asc',
        'service2_price_desc', 'service2_price_asc',
        ]

    __game_ids = {
        'all': 100,
        'csgo': 1,
        'dota': 2,
        'rust': 4,
        'tf': 5
    }

    __prefix_by_game = {
        'all': '',
        'csgo': '',
        'dota': 'd_',
        'rust': 'r_',
        'tf': 'tf_'
    }

    __altskins_services = {
        'bitskins': 'showbs', 'bitskins(A)': 'showbsa', 'bitskins(7)': 'showbs7', 'bitskins(LS)': 'showbss',
        'dmarket': 'showdma',
        'market.csgo': 'showtm', 'market.csgo(A)': 'showtma', 'market.csgo(LS)': 'showtmls',
        'market.dota': 'showtm', 'market.dota(A)': 'showtma', 'market.dota(LS)': 'showtmls',
        'market.rust': 'showtm', 'market.rust(A)': 'showtma', 'market.rust(LS)': 'showtmls',
        'steamcommunity': 'showsteam', 'steamcommunity(A)': 'showsteama', 'steamcommunity(LS)': 'showsteamls',
        'buff.market': 'showbuff', 'buff.market(A)': 'showbuffa',
        'cs.money': 'showcsmoney', 'cs.money(NO HOLD)': 'showcsmoneywh', 'cs.money(STORE)': 'showcsmoneyst', 'cs.money(STORE NO HOLD)': 'showcsmoneystwh', 'cs.money(WIKI)': 'showcsmoneyw',
        'dota.money': 'showdotamoney',
        'loot.farm': 'showlootfarmd', 'loot.farm(DEP)': 'showlootfarm',
        'tradeit.gg': 'showtradeit', 'tradeit.gg(DEP)': 'showtradeitd',
        'swap.gg': 'showswap', 'swap.gg(DEP)': 'showswapd', 'swap.gg(M)': 'showswapm',
        'cs.trade': 'showcstrade', 'cs.trade(DEP)': 'showcstraded',
        'cs.deals': 'showcsdeals', 'cs.deals(DEP)': 'showcsdealsd', 'cs.deals(M)': 'showcsdealsm',
        'tradeskinsfast': 'showtsf', 'tradeskinsfast(DEP)': 'showtsfd',
        'skins.cash': 'showskinscash',
        'mannco.trade': 'showmannco',
        'gamdom': 'showgamdom', 'gamdom(DEP)': 'showgamdomd',
        'wtfskins': 'showwtf',
        'dota2bestyolo': 'showyolo',
        'godota2': 'showgodota'
    }

    @root_validator(pre=True)
    def service1_equals_service2(cls, values):
        assert values['service1'] != values['service2'], '"service1" and "service2" can\'t be same'
        return values

    @validator('game_title')
    def create_type(cls, v, values, **kwargs):
        values['type'] = cls.__game_ids[v]
        return v

    @validator('service1', 'service2')
    def correct_services(cls, v, values, **kwargs):
        v = cls.__altskins_services[v]
        v = cls.__prefix_by_game[values['game_title']] + v
        return v

    @validator('sort')
    def correct_sort(cls, v, values, **kwargs):
        temp_values = {}
        temp_values['service1'] = values['service1'].replace(cls.__prefix_by_game[values['game_title']], '')
        temp_values['service2'] = values['service2'].replace(cls.__prefix_by_game[values['game_title']], '')
        sort_dir = ''
        if v[-4:] == 'desc':
            sort_dir = '-'
        if len(v) < 20:
            currency = ''
            if temp_values[v[:8]][4:].startswith('showtm'):
                currency = '_usd'
            v = sort_dir + cls.__prefix_by_game[values['game_title']] + 'price' + str(temp_values[v[:8]][4:]) + currency
        else:
            v = sort_dir + str(temp_values[v[:8]][4:]) + str(temp_values[v[12:20]][4:])

        return v
