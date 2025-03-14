from collections import namedtuple


Product = namedtuple('Product', ['name'])
ELN = 0
AUTOCALL = 1
products = [None, None]
products[ELN] = Product("eln").name
products[AUTOCALL] = Product("autocall").name