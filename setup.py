from setuptools import find_packages, setup

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Django plugin for geolocation info."

setup(
    name="drf_geoauth",
    version="0.1.0",
    author="Shoile Abdulazeez Adenuga",
    author_email="shoabdulazeez@gmail.com",
    description="Django plugin for geolocation info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shoileazeez/drf_geodata.git",
    packages=find_packages(include=["geo_data", "geo_data.*"]),
    include_package_data=True,
    install_requires=[
        "APScheduler==3.11.0",
        "asgiref==3.8.1",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "Django==5.1.6",
        "django-ipware==4.0.2",
        "djangorestframework==3.15.2",
        "idna==3.10",
        "IP2Location==8.10.5",
        "requests==2.32.3",
        "pycountry==24.6.1",
        "python-dotenv==1.0.0",
        "sqlparse==0.5.3",
        "tzdata==2025.1",
        "tzlocal==5.3.1",
        "urllib3==2.3.0",
        "timezonefinder==6.5.8",
        "user-agents==2.2.0",
        "iso3166==2.1.1",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",  # Allow more compatibility
)


