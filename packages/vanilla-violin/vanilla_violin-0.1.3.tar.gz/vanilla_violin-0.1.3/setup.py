from setuptools import setup
setup(
  name='vanilla-violin',
  version='0.1.3',
  packages=[
    'vanilla_violin',
    'vanilla_violin.gitlab',
    'vanilla_violin.aws',
  ],
  entry_points={
    'console_scripts': [
      'co=cli.__main__:cli',
    ]
  },
  install_requires=[
    "Click>=8.1.3",
    "ddt>=1.6.0",
    "boto3>=1.26.56",
    "requests>=2.28.1",
    "pytest>=7.2.0",
    "PyYAML>=6.0",
  ],
)
