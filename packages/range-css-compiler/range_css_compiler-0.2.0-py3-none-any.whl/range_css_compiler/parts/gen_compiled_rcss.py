
# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]

import sys
import fies
import json
from sout import sout
import indent_template
from relpath import rel2abs
# pypi公開ツール用のファイル同梱ラップスクリプト [pypi_tool_file_binder.py]
from . import pypi_tool_file_binder as ptfb

# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]
def gen_compiled_rcss(
	mat_def_js_code,	# 行列定義部のjavascriptコード
	css_id_ls	# css_idの一覧
):
	compiled_rcss_js_code = indent_template.replace(
		ptfb.compiled_rcss_template,	# compiled_rcss_template.jsの読み込み [pypi_tool_file_binder.py]
		{
			"BUNDLE": ptfb.browserified_quadprog,	# browserified_quadprog.jsの読み込み [pypi_tool_file_binder.py]
			"MAT_DEF_CODE": mat_def_js_code,
			"CSS_ID_LIST": json.dumps(css_id_ls, ensure_ascii = False),
			"APPLIER_UTILS": ptfb.applier_utils,	# applier_utils.jsの読み込み [pypi_tool_file_binder.py]
		}
	)
	return compiled_rcss_js_code
