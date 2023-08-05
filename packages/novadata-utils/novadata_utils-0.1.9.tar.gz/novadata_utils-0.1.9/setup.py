from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
    name="novadata_utils",
    version="0.1.9",
    url="https://github.com/TimeNovaData/novadata_utils/",
    license="MIT License",
    author="Flávio Silva",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="flavio.nogueira.profissional@gmail.com",
    keywords="Django, utils, ndt, novadata, nova data, nova, data",
    description="novadata utils",
    packages=find_packages(),
    install_requires=[
        "django",
        "djangorestframework",
        "django-object-actions",
        "django-import-export",
    ],
    project_urls={
        "GitHub": "https://github.com/TimeNovaData/novadata_utils/",
    },
)
