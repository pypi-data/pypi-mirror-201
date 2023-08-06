
# RangeCSS-Compiler [range_css_compiler]

import os
import sys
import fies
import time
import argparse
from sout import sout
# 形式変換 (yaml -> equid) [yaml_style_to_equid]
from .parts import yaml_style_to_equid as y2e
# 2次計画問題の行列を定義するjsコードに変換 [to_qp_mat_js.py]
from .parts import to_qp_mat_js as tqmj
# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]
from .parts import gen_compiled_rcss as gcr

# ファイル名拡張子の変更
def ext_rep(org_filename, new_ext):
	if "." not in org_filename:
		without_ext = org_filename
	else:
		without_ext = ".".join(org_filename.split(".")[:-1])
	ret_filename = without_ext + new_ext
	return ret_filename

# RangeCSSのyaml帳票をjsに変換 [range_css_compiler]
def compile(
	org_yaml_filename,
	output_js_filename = None,
):
	# output_js_filename の自動生成
	if output_js_filename is None:
		output_js_filename = ext_rep(org_yaml_filename, ".js")	# ファイル名拡張子の変更
	# yaml読み込み
	rcss_style = fies[org_yaml_filename, "yaml"]
	# yaml形式のRangeCSS_Styleをequid形式のcond, lossに変換 [yaml_style_to_equid]
	cond, loss, css_id_ls = y2e.yaml_style_to_equid(rcss_style)
	# 2次計画問題の行列を定義するjsコードに変換 [to_qp_mat_js.py]
	js_code = tqmj.to_qp_mat_js(cond, loss)
	# クライアント側jsを生成 (2次計画法でHTMLの動的な割り付けを実施) [gen_compiled_rcss.py]
	ret_js_code = gcr.gen_compiled_rcss(
		js_code,
		css_id_ls
	)
	# 保存
	# デフォルト動作を上書きにしたくない場合は下記を使用
	# if os.path.exists(output_js_filename): raise Exception("[RangeCSS-Compiler error] output filename already exists.")
	fies[output_js_filename, "text"] = ret_js_code

# yamlが変更されるたびに自動でコンパイルする
def loop_compiler(args_dic):
	pre_t = None	# 最終更新日時
	while True:
		now_t = os.path.getmtime(args_dic["input"])	# 最終更新日時
		if now_t != pre_t:
			pre_t = now_t
			print("compiling...")
			try:
				# RangeCSSのyaml帳票をjsに変換 [range_css_compiler]
				compile(
					org_yaml_filename = args_dic["input"],
					output_js_filename = args_dic["output"],	# None指定の場合は自動的にinputファイルから空気を読んだファイル名になる
				)
			except Exception as e:
				print(repr(e))
				print("[range-css-compiler error] An error occurred during compilation.")
			print("waiting...")
		# 少し休む
		time.sleep(0.5)

# コンソールから利用
def console_command():
	# コンソール引数
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required = True, help = "Input yaml(.yml) file path")
	parser.add_argument("-o", "--output", required = False, help = "Output javascript(.js) file path")
	parser.add_argument("-l", "--loop", required = False, help = "Loop compile mode", action = "store_true")
	args_dic = vars(parser.parse_args())
	# loopオプション有無で分岐
	if args_dic["loop"] is True:
		# yamlが変更されるたびに自動でコンパイルする
		loop_compiler(args_dic)
	else:
		# RangeCSSのyaml帳票をjsに変換 [range_css_compiler]
		compile(
			org_yaml_filename = args_dic["input"],
			output_js_filename = args_dic["output"],	# None指定の場合は自動的にinputファイルから空気を読んだファイル名になる
		)
