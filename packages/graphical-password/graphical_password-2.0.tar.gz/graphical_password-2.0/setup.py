from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(name='graphical_password',
      version='2.0',
      description='Simple authorization creation based on a sequence of images',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['graphical_password'],
      author_email='egubareva06@mail.ru',
      zip_safe=False)