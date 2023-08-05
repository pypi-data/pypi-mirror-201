import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="simplysklearn", 
    version="0.2.3",
    author="Kim Hyun Bin",
    author_email="KIMH0004@e.ntu.edu.sg",
    description="Python package to automate machine learning process to showcase metric values for nearly all Scikit-Learn's models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanilladucky/simplysklearn",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 
                      'pandas', 
                      'scikit-learn',
                      'seaborn',
                      'matplotlib',
                      'tqdm', 
                      'xgboost',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)