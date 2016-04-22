try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG_DESCRIPTION = None

required_packages = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='randomization_tests',
      version='1.0.0',
      description='Randomization tests for two-sample comparison',
      long_description=LONG_DESCRIPTION,
      classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
      ],
      keywords='significance testing',
      author='Eugen Stripling',
      author_email='eugen.stripling@kuleuven.be',
      url='https://github.com/estripling/randomization_tests',
      packages=['randomization_tests'],
      license='GPLv3+',
      install_requires=required_packages,
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      zip_safe=False,
      )
