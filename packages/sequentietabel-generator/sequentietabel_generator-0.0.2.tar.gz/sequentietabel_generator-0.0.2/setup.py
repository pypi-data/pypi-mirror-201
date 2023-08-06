import setuptools

setuptools.setup(
    name="sequentietabel_generator",
    version="0.0.2",
    description = "Een python script om een sequentietabel te genereren uit een protocol.",
    readme = "README.md",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    dependencies = [
        "pandas"
    ],
    install_requires=["pandas"],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "sequentietabel_generator = sequentietabel_generator.cli:main",
        ]
    }
)