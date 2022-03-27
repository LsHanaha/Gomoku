# import tools to create the C extension
from distutils.core import setup, Extension


# Для Установки: 
# $ pip3 install ./algo_module
# из корневой диркектории модуля
module_name = 'algo_module'
# the files your extension is comprised of
c_files = ['src/minmax_init.c',
            'src/estimate.c',
            'src/helpers.c',
            'src/minmax.c',
            'src/module.c',
            'src/steps.c',
            ]

extension = Extension(
    module_name,
    c_files
)

setup(
    name=module_name,
    version='2.0',
    description='minmax for gomoku',
    author='Sergey Shorin',
    author_email='',
    url='',
    ext_modules=[extension]
)