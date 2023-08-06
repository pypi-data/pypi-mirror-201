"""
延迟加载实现
"""
from types import ModuleType
from importlib import import_module


class LazyLoader(ModuleType):
    """
    模块 延迟加载
    :params: local_name: 模块引用名称
    :params: module_life_cycle: 模块生命周期( 建议使用全局变量 globals() )
    :params: import_name: 导入模块名称
    """
    def __init__(
        self, local_name, module_life_cycle, import_name=None
    ):
        self._local_name = local_name
        self._module_life_cycle = module_life_cycle
        super().__init__(import_name or local_name)

    def _loader(self):
        module = import_module(self.__name__)
        self._module_life_cycle[self._local_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, name):
        module = self._loader()
        return getattr(module, name)

    def __dir__(self):
        module = self._loader()
        return dir(module)
