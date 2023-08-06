from setuptools import find_packages, setup

__version__ = "0.1.0"

setup(
    name="web-utils-soft",
    version=__version__,
    description="Python Project package",
    long_description="Project to set web utils to get data from the web",
    author="Wilson Ramirez",
    author_email="wil_ramirez02@hotmail.com",
    license="MIT",
    packages=find_packages(),
    # install_requires=["numpy", "pandas"],
    entry_points={
        "console_scripts": [
            "get-data=app.json_utils:get_json",
            "get-image=app.image_utils:get_image",
        ]
    },
)
