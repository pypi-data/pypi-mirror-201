from setuptools import setup, find_packages
from distutils.dir_util import remove_tree
# import glob
# remove_tree(['dist']) 

setup(
    name="mlmd-dataset-management",
    version="2.3.10",
    description="MLMD Dataset Management",
    long_description="MLMD Dataset Management",
    long_description_content_type="text/markdown",
    url="",
    author="Thinh Nguyen, Huyen Vu, Dung Huynh",
    author_email="nguyenlongthinh@gmail.com, vtphuyen1987@yahoo.com, ducdung8378@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["azure-storage-blob","requests","ml-metadata==1.0.0","python-dotenv","google-cloud-storage","mysql-connector-python==8.0.25", "google-cloud-secret-manager", "google-api-python-client", "protobuf==3.19.5", "numpy<=1.23.0", "google-cloud-firestore==2.7.2"],
    entry_points = {
        'console_scripts': ['dm=cli.dataset_manager:main']
    }
)