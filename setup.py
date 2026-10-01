from setuptools import find_packages, setup

setup(
    name="china-partner-opportunity-engine",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.9",
    install_requires=["jsonschema>=4.23,<5"],
    entry_points={"console_scripts": ["china-partner=china_partner_engine.cli:main"]},
)
