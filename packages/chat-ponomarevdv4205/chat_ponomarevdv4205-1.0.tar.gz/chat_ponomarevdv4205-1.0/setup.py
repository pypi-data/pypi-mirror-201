from setuptools import setup, find_packages

setup(name='chat_ponomarevdv4205',
      version='1.0',
      description='Chat',
      packages=find_packages(),
      author_email='ponomarevdv4205@yandex.ru',
      author='Dima Ponomarev',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )
