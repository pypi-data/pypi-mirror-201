# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from consul import Consul

from hagworm.extend.config import ConfigureBase


class Configure(ConfigureBase):
    """配置类
    """

    __slots__ = [r'_client', r'_path']

    def __init__(self, host, port, path=r'config/', **kwargs):

        super().__init__()

        self._client = Consul(host, port, **kwargs)

        self._path = path

    def _get(self, section, key):

        _, data = self._client.kv.get(f'{self._path}{section}/{key}')

        if data and r'Value' in data:
            return data[r'Value'].decode(r'utf-8')
        else:
            return None

    def reload(self):

        for _key, _section, _type in self._key_section.values():

            if _type is str:
                self.__setattr__(_key, self._get(_section, _key))
            elif _type is int:
                self.__setattr__(_key, int(self._get(_section, _key)))
            elif _type is float:
                self.__setattr__(_key, float(self._parser.getfloat(_section, _key)))
            elif _type is bool:
                self.__setattr__(_key, bool(self._parser.getboolean(_section, _key)))
            else:
                self.__setattr__(_key, _type.decode(self._parser.get(_section, _key)))

        return self
