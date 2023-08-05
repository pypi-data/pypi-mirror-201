from setuptools import setup, find_packages

setup(
    name='rapid_innovation',
    version='1.7.3',
    description='Rapid Innovation package',
    url='https://github.com/Rapid-Python/python-package-rapid',
    author='Abhishek Negi',
    author_email='abhisheknegi@rapidinnovation.dev',
    license='MIT',
    python_requires='>=3.7',
    install_requires=[],
    packages=find_packages(),
    package_data={'': ['app/*']},
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

