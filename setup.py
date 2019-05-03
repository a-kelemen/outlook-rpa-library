import setuptools


setuptools.setup(name='emailprocesslibrary',
      version='0.1',
      description='Library for outlook automation.',
      url='',
      author='Andras Kelemen',
      author_email='kelemenandras11@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(exclude=['EmailProcessLibrary.tests']),

      install_requires=[
        'pywin32',
        'robotframework',
      ],
      test_suite="tests",
      tests_require=['nose'],
      zip_safe=False
      )