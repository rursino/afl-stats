from distutils.core import setup

setup(name='afl-stats',
      version='0.1',
      description='AFL stats completed by R.Ursino',
      author='Ross Ursino',
      author_email='rosscursino@gmail.com',
      packages=['match_stats', 'player_stats'],
      package_data={
          'match_stats': ['data/matchstats.json']
        },
     )