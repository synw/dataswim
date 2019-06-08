from setuptools import setup, find_packages

version = "0.4.26"

setup(
    name='dataswim',
    packages=find_packages(),
    version=version,
    description='Diving equipment for data lake',
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
        'stuf',
        "pytablewriter",
        'goerr',
        'holoviews',
        'bokeh',
        'altair',
        'gencharts',
        'influxdb',
        'chartjspy',
        "seaborn",
        "arrow",
        "folium",
        "nltk",
        "deepdish",
    ],
    zip_safe=False
)
