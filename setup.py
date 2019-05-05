from distutils.core import setup
setup(
  name = 'build-dashboard',
  packages = ['build_dashboard'],
  version = '0.1.0',
  description = 'Buildbot CLI Dashboard',
  author = 'Jeffrey Hill',
  author_email = 'jeff@reverentengineer.com',
  url = 'https://github.com/ReverentEngineer/build-dashboard',
  keywords = ['buildbot', 'continuous integration', 'ci', 'cli' ],
  classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 3',
      ],
  scripts = [ 'bin/build_dashboard' ],
  install_requires = ['aiohttp', 'toml', 'asciimatics',],
)
