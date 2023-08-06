from setuptools import setup, find_packages

setup(name='server_chat_pyqt_ponomarevdv4205',
      version='0.2',
      description='Server packet',
      packages=find_packages(),
      author_email='ponomarevdv4205@yandex.ru',
      author='Dima Ponomarev',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )