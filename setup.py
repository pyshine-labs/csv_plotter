from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().strip().splitlines()

setup(
    name='csv-drag-drop-plotter',
    version='1.0.0',
    author='PyShine',
    author_email='contact@pyshine.com',
    description='Drag‑and‑drop CSV plotting desktop application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pyshine-labs/csv_plotter',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'csv-plotter=main:main',
        ],
        'gui_scripts': [
            'csv-plotter-gui=main:main',
        ],
    },
)