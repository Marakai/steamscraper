import setuptools

app_name = "steamscraper"

with open("README.md") as fp:
    long_description = fp.read()

main_ns = {}
ver_path = setuptools.convert_path(f'{app_name}/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(
    name=app_name,
    version=main_ns['__version__'],

    description="Extract all subscribed Steam Workshop mods for Ark Survival Evolved",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Michael Hoffmann",
    author_email="michaelh@centaur.id.au",

    packages=setuptools.find_packages(),

    install_requires=[
        'bs4',
        'steam',
    ],

    entry_points={
        'console_scripts':
            [
                f'{app_name}={app_name}.main:main'
            ]
    },

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Intended Audience :: Gamers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
