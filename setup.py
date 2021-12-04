from pathlib import Path
import setuptools

entry_points = []
for _file in (Path(__file__).parent / 'src').rglob("*/game.py"):
    module_name = _file.parent.name
    entry_points.append(f"{module_name}={module_name}.game:main")


setuptools.setup(
    name='pyrpggame',
    version='0.1.0',
    description='top-down RPG made in pygame.',
    long_description='top-down RPG made in pygame.',
    long_description_content_type='text/markdown',
    author='Sujith Sudarshan',
    author_email='sh1457@gmail.com',
    python_requires='>=3.6.0',
    url='https://github.com/sh1457/rpg-pygame',
    packages=setuptools.find_packages(where='src',
                                      exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': entry_points,
    },
    install_requires=['pygame', 'pyopengl'],
    extras_require={
        'fancy feature': ['numpy'],
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
