from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    readme = fh.read()


setup(
    name="multidirectional_graph",
    version="0.1.3",
    description="Package for plotting multidirectional graphs",
    author="Eduardo Messias de Morais",
    author_email="emdemor415@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=["multidirectional_graph"],
    package_data={
        "multidirectional_graph": [
            "multidirectional_graph/fonts/Oswald/*.ttf",
            "multidirectional_graph/fonts/Roboto/*.ttf",
            "multidirectional_graph/fonts/SourceSerif/*.ttf",
        ]
    },
    data_files=[
        (
            "config",
            [
                "multidirectional_graph/fonts/Oswald/Oswald-Regular.ttf",
                "multidirectional_graph/fonts/SourceSerif/SourceSerifPro-Light.ttf",
            ],
        )
    ],
    include_package_data=True,
    install_requires=["matplotlib"],
)
