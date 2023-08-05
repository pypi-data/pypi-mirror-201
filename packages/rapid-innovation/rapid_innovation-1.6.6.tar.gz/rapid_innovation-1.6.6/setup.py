from setuptools import setup, find_packages

setup(
    name='rapid_innovation',
    version='1.6.6',
    description='Rapid Innovation package',
    url='https://github.com/Rapid-Python/python-package-rapid',
    author='Abhishek Negi',
    author_email='abhisheknegi@rapidinnovation.dev',
    license='MIT',
    python_requires='>=3.7',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    package_data={'app': ['app']},
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

