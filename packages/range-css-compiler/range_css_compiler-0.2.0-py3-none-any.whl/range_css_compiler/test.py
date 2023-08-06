
# RangeCSS-Compiler [range_css_compiler]
# 【動作確認 / 使用例】

import sys
from ezpip import load_develop
# RangeCSS-Compiler [range_css_compiler]
range_css_compiler = load_develop("range_css_compiler", "../", develop_flag = True)

# RangeCSSのyaml帳票をjsに変換 [range_css_compiler]
range_css_compiler.compile(
	org_yaml_filename = "./RangeCSS_Style.yml",
	output_js_filename = "compiled_rcss.js",
)
