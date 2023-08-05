from arkdata.models.account import Account
# from models.admin import Admin
from arkdata.models.ammunition import Ammunition
from arkdata.models.armour import Armour
from arkdata.models.artifact import Artifact
from arkdata.models.attachment import Attachment
from arkdata.models.cart_item import CartItem
from arkdata.models.command import Command
from arkdata.models.consumable import Consumable
from arkdata.models.creature import Creature
from arkdata.models.dye import Dye
from arkdata.models.egg import Egg
from arkdata.models.farm import Farm
from arkdata.models.order_item import OrderItem
from arkdata.models.product import Product
from arkdata.models.recipe import Recipe
from arkdata.models.resource import Resource
from arkdata.models.saddle import Saddle
from arkdata.models.seed import Seed
from arkdata.models.skin import Skin
from arkdata.models.structure import Structure
from arkdata.models.tool import Tool
from arkdata.models.trophy import Trophy
from arkdata.models.user import User
from arkdata.models.weapon import Weapon
from arkdata.models.server import Server
from arkdata.models.sessions import Session


__all__ = ['Account',
           'Ammunition',
           'Armour',
           'Artifact',
           'Attachment',
           'CartItem',
           'Command',
           'Consumable',
           'Creature',
           'Dye',
           'Egg',
           'Farm',
           'OrderItem',
           'Product',
           'Recipe',
           'Resource',
           'Saddle',
           'Seed',
           'Skin',
           'Structure',
           'Tool',
           'Trophy',
           'User',
           'Weapon',
           'Server',
           'Session'
           ]


def seed_all():
    for model in __all__:
        eval(f'{model}.seed_table()')


def create_all():
    for model in __all__:
        eval(f'{model}.create_table()')


def clear_all():
    for model in __all__:
        eval(f'{model}.clear_table()')


def drop_all():
    for model in __all__:
        eval(f'{model}.drop_table()')
