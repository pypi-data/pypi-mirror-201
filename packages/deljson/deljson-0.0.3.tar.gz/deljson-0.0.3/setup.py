import setuptools
with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()
    
setuptools.setup(
    name = "deljson",
    version = "0.0.3",
    author = "seanbbear",
    author_email="ccoccc14@gmail.com",
    description="刪除json值",
    long_description=long_description,
    long_description_content_type="text/markdown",                                    
    packages=setuptools.find_packages(),     
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
    )
