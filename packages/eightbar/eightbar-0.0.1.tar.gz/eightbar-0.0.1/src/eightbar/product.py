import dataclasses


@dataclasses.dataclass
class Product:
    url: str
    name: str
    tag: str
