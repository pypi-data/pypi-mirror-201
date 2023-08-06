from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(name='feather-api',
      version='1.2.0',
      description='Python wrapper for Feather\'s API',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/Feather-Official/featherdbtools',
      author='Feather Technology Inc.',
      author_email='support@try-feather.com',
      packages=['featherapi'],
      install_requires=['setuptools', 'requests', 'pandas'],
      setup_requires=['setuptools', 'requests', 'pandas'],
      zip_safe=False)