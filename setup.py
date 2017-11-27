from setuptools import setup, find_packages


version = "0.3.7"

setup(
    name='dataswim',
    packages=find_packages(),
    version=version,
    description='Utilities to swim in a data lake',
    author='synw',
    author_email='synwe@yahoo.com',
    url='https://github.com/synw/dataswim',
    download_url='https://github.com/synw/dataswim/releases/tag/' + version,
    keywords=['data_visualization', "data_exploration"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pandas',
        'pandas_profiling',
        'dataset',
        "pytablewriter",
        'goerr',
        'holoviews==1.9.0',
        'bokeh==0.12.10',
        'altair==1.2.1',
        'gencharts',
    ],
    zip_safe=False
)
