from setuptools import setup, find_packages

setup(
    name='SynapEvo',
    version='0.1.1',
    license='MIT',
    author="Ashutosh Adhikari,Ananya Datta,Aditya Kothari",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Adhikari-Ashutosh/DARWiN',
    keywords='ML NeuralNET',
    install_requires=[
          'numpy',
      ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
)