from setuptools import setup

setup(
    name="fmxl",
    version="0.1.1",
    description="Manage file name and attribute in Spreadsheet.",
    url="https://github.com/permadisatya/file-manager-with-excel",
    author="Permadi Satya",
    author_email="satya.permadi.d@gmail.com",
    license="",
    packages=["fmxl"],
    install_requires=['openpyxl==3.0.10'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.10',
    ],
)