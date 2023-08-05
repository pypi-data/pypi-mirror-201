import setuptools
setuptools.setup(
    # State the generic information about the package
    name='uintel',
    version='0.3.16',
    author="Sam Archie",
    author_email="sam.archie@urbanintelligence.co.nz",
    description="Urban Intelligence's unified Python data analysis toolkit",
    long_description=open('README.md').read().replace("docs/images/blue_logo.svg", "https://urbanintelligence.co.nz/wp-content/uploads/2022/05/Artboard-1-copy-23.svg"),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://uintel.github.io/pyui/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',        
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',        
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: English'
    ],
    # State the dependecies of the package
    install_requires=['matplotlib', 'colour', 'slack_sdk', 'sqlalchemy', 'sqlalchemy_utils', 'psycopg2', 'pyyaml', 'tqdm', 'paramiko', 'boto3', 'geopandas', 'esridump', 'requests', 'topojson', 'OWSLib'],
    extras_require={
        "full": ["gdal", "rasterio"]
    },
    # Include all package files when installing (hence moving over the mplstyle and ttf files)
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={"uintel.fonts": ["*.ttf"], "uintel.styles": ["*.mplstyle"]},
)