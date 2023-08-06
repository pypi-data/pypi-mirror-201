from setuptools import setup
setup(
	name="whole",
	version="1.0.0.0.0.4",
	packages=["whole"],
    install_requires=[],
    entry_points="""
    [console_scripts]
    t = whole.TCP_UDP:TU
    s = whole.Stock:StockData
    """,
)