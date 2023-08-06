import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PySide2-Fluent-Widgets",
    version="0.6.8",
    keywords="pyside2 fluent widgets",
    author="zhiyiYo",
    author_email="shokokawaii@outlook.com",
    description="A fluent design widgets library based on PySide2",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="LGPLv3",
    url="https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PySide2",
    packages=setuptools.find_packages(),
    install_requires=[
        "PySide2-Frameless-Window",
        "darkdetect",
    ],
    extras_require = {
        'full': ['scipy', 'pillow', 'colorthief']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent'
    ],
    project_urls={
        'Documentation': 'https://pyqt-fluent-widgets.readthedocs.io/',
        'Source Code': 'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PySide2',
        'Bug Tracker': 'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues',
    }
)
