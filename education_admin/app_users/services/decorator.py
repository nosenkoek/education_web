class CollectionPermission:
    """
    Класс-декоратор для сбора объектов в словарь для фабрики
    Attr:
        name: название/ключ для объекта PermissionBase
        permission_dict: словарь с объектами PermissionBase
    """
    def __init__(self, name: str, permission_dict: dict):
        self.name = name
        self.permission_dict = permission_dict

    def __call__(self, obj):
        self.permission_dict.update({self.name: obj})
        return obj
