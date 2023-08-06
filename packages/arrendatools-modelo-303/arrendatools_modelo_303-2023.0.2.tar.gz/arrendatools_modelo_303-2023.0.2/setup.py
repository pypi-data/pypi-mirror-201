from setuptools import setup

__version__ = "2023.0.2"

setup(
    name='arrendatools_modelo_303',
    version=__version__,
    description='Módulo de Python que genera un string para la importación de datos en el modelo 303 de la Agencia Tributaria de España (PRE 303 - Servicio ayuda modelo 303)',
    url='https://github.com/hokus15/ArrendaToolsModelo303',
    author='hokus15',
    author_email='hokus@hotmail.com',
    license='MIT',
    packages=['arrendatools_modelo_303'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
