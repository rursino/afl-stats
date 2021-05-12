from setuptools import setup, find_packages

setup(name='afl-stats',
      version='0.1',
      description='AFL stats completed by R.Ursino',
      author='Ross Ursino',
      author_email='rosscursino@gmail.com',
      packages=find_packages(),
      package_data={
          'match_stats': ['data/matchstats.json']
        },
     )