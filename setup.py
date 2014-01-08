from distutils.core import setup

setup(name='neicutil',
      version='0.1dev',
      description='NEIC Python Utility Library',
      author='Mike Hearne',
      author_email='mhearne@usgs.gov',
      url='',
      packages=['neicutil'],
      install_requires=['numpy', 'matplotlib', 'scipy'],
)
