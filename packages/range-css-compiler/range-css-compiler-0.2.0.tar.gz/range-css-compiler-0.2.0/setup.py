
from setuptools import setup
# 公開用パッケージの作成 [ezpip]
import ezpip

# 公開用パッケージの作成 [ezpip]
with ezpip.packager(develop_dir = "./_develop_range_css_compiler/") as p:
	setup(
		name = "range-css-compiler",
		version = "0.2.0",
		description = "More intuitive HTML placement and assignment tool than CSS.",
		author = "le_lattelle",
		author_email = "g.tiger.ml@gmail.com",
		url = "https://github.co.jp/",
		packages = p.packages,
		install_requires = ["relpath", "ezpip", "sout", "fies", "tqdm", "equid", "indent-template", "ezptn"],
		long_description = p.long_description,
		long_description_content_type = "text/markdown",
		license = "CC0 v1.0",
		classifiers = [
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries",
			"License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
		],
		entry_points = """
			[console_scripts]
			rcss = range_css_compiler:console_command
		"""
	)
