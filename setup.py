from setuptools import setup, find_packages


version = "0.4.12"

setup(
    name='dataswim',
    packages=find_packages(),
    version=version,
    description='Utilities to swim in a data lake',
    author='synw',
    author_email='synwe@yahoo.com',
    url='https://github.com/synw/dataswim',
    download_url='https://github.com/synw/dataswim/releases/tag/' + version,
    keywords=['data_visualization', "data_exploration", "charts"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pandas',
        'scikit-learn',
        'dataset',
        "pytablewriter",
        'goerr',
        'holoviews==1.9.1',
        'bokeh==0.12.11',
        'altair==1.2.1',
        'gencharts',
        'influxdb',
        'chartjspy',
        "seaborn",
        "arrow",
    ],
    zip_safe=False
)
