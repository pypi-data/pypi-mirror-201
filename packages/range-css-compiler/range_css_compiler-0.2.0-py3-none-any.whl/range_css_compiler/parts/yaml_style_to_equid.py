# 形式変換 (yaml -> equid) [yaml_style_to_equid]

import sys
import erf
import fies
import json
import copy
import ezptn
import equid as eq
from sout import sout

# 2項演算をlistに対して繰り返し適用 (formula型を想定)
def formula_reduce(
	arg_ls,	# 系列
	func,	# 二項演算
	head	# 初項
):
	if len(arg_ls) == 0: return head
	return func(
		formula_reduce(arg_ls[:-1], func, head),
		arg_ls[-1]
	)

# 省略された場合のデフォルト値
default_dic = {
	"children": [],
	"align": "vertical",
	"margin_x0": "0px", "margin_x1": "0px",
	"margin_y0": "0px", "margin_y1": "0px",
	"width": "~", "height": "~",
}

# 数値パース (失敗時はNoneを返す)
@erf(ValueError = None)
def parse_float(res_fixed):
	return float(res_fixed)

# 「数値px」の形を認識して返す (当てはまらない場合は_UNMATCH, 空文字列の場合は_EMPTYを返す)
def recog_px_num(arg_str):
	if arg_str == "": return "_EMPTY"
	parsed = ezptn.match("%spx", arg_str)
	if len(parsed) != 1: return "_UNMATCH"
	# 数値パース (失敗時はNoneを返す)
	num = parse_float(parsed[0][0])
	if num is None: return "_UNMATCH"
	return num

# 幅指定のパース ("10px~[30px]" など)
def parse_range_str(arg_str):
	parse_error = Exception("[RangeCSS error] Failed to parse range_str.")
	# 範囲かどうかで分岐
	if "~" in arg_str:
		# デフォルト値があるかで分岐
		if "[" in arg_str:
			parsed = ezptn.match("%s~%s[%s]", arg_str)
			if len(parsed) != 1: raise parse_error
			a, b, c = parsed[0]
			# 「数値px」の形を認識して返す (当てはまらない場合は_UNMATCH, 空文字列の場合は_EMPTYを返す)
			a_num = recog_px_num(a)
			b_num = recog_px_num(b)	# 「数値px」の形を認識して返す (当てはまらない場合はNoneを返す)
			c_num = recog_px_num(c)	# 「数値px」の形を認識して返す (当てはまらない場合はNoneを返す)
			if "_UNMATCH" in (a_num, b_num, c_num): raise parse_error
			if c_num == "_EMPTY": raise parse_error
			return (
				(None if a_num == "_EMPTY" else a_num),
				(None if b_num == "_EMPTY" else b_num),
				c_num
			)
		else:
			parsed = ezptn.match("%s~%s", arg_str)
			if len(parsed) != 1: raise parse_error
			a, b = parsed[0]
			# 「数値px」の形を認識して返す (当てはまらない場合は_UNMATCH, 空文字列の場合は_EMPTYを返す)
			a_num = recog_px_num(a)
			b_num = recog_px_num(b)	# 「数値px」の形を認識して返す (当てはまらない場合はNoneを返す)
			if "_UNMATCH" in (a_num, b_num): raise parse_error
			return (
				(None if a_num == "_EMPTY" else a_num),
				(None if b_num == "_EMPTY" else b_num),
				None
			)
	else:
		# 単純数値指定
		num = recog_px_num(arg_str)	# 「数値px」の形を認識して返す (当てはまらない場合は_UNMATCH, 空文字列の場合は_EMPTYを返す)
		if num == "_UNMATCH" or num == "_EMPTY":
			raise parse_error
		return (num, num, None)

# タプルをrange_strに変換
def tuple_to_range_str(arg_tuple):
	min_v, max_v, def_v = arg_tuple
	return "%s~%s%s"%(
		("" if min_v is None else "%spx"%min_v),
		("" if max_v is None else "%spx"%max_v),
		("" if def_v is None else "[%spx]"%def_v),
	)

# 省略された指定を補完
def normalize_yaml_style(rcss_style, default_len):
	# 汚染防止の複製
	norm_rcss_style = copy.deepcopy(rcss_style)
	# rcss_idごとに正規化
	for rcss_id in norm_rcss_style:
		one_block = norm_rcss_style[rcss_id]
		# 省略の補完
		for key in default_dic:	# 省略された場合のデフォルト値
			if key in one_block: continue
			one_block[key] = default_dic[key]
		# デフォルト値の補完 (動作の安定のため)
		target_keys = ["margin_x0", "margin_x1", "margin_y0", "margin_y1", "width", "height"]
		for key in target_keys:
			# 幅指定のパース ("10px~[30px]" など)
			parsed_r = parse_range_str(one_block[key])
			# 固定指定でないときのみデフォルト指定を加える
			min_v, max_v, def_v = parsed_r
			if def_v is not None: continue
			if min_v == max_v:
				if None not in (min_v, max_v): continue
			one_block[key] = tuple_to_range_str((min_v, max_v, default_len))	# タプルをrange_strに変換
	return norm_rcss_style

# 自身のsizeと子どもたちのsize, marginとの関係式の生成s
def gen_size_rel_conds(
	parent_id,	# 親のrcss_id
	c_id_ls,	# 子のrcss_idのリスト
	align	# vertical / horizontal
):
	cond_ls = []
	if align == "vertical":
		for c_id in c_id_ls:
			cond_ls.append(
				eq[parent_id+"_width"] ==
				eq[c_id+"_margin_x0"] +
				eq[c_id+"_width"] +
				eq[c_id+"_margin_x1"]
			)
		cond_ls.append(
			eq[parent_id+"_height"] ==
			sum([
				eq[c_id+"_margin_y0"] +
				eq[c_id+"_height"] +
				eq[c_id+"_margin_y1"]
				for c_id in c_id_ls
			])
		)
	elif align == "horizontal":
		cond_ls.append(
			eq[parent_id+"_width"] ==
			sum([
				eq[c_id+"_margin_x0"] +
				eq[c_id+"_width"] +
				eq[c_id+"_margin_x1"]
				for c_id in c_id_ls
			])
		)
		for c_id in c_id_ls:
			cond_ls.append(
				eq[parent_id+"_height"] ==
				eq[c_id+"_margin_y0"] +
				eq[c_id+"_height"] +
				eq[c_id+"_margin_y1"]
			)
	else:
		raise Exception("[RangeCSS error] invalid align.")
	return cond_ls

# 子どもたちのposに関する式の生成 (子どもの人数分)
def gen_pos_rel_conds(
	parent_id,	# 親のrcss_id
	c_id_ls,	# 子のrcss_idのリスト
	align	# vertical / horizontal
):
	cond_ls = []
	if align == "vertical":
		for c_id in c_id_ls:
			cond_ls.append(
				eq[c_id+"_posX"] ==
				eq[parent_id+"_posX"] +
				eq[c_id+"_margin_x0"]
			)
		pos0 = eq[parent_id+"_posY"]
		for c_id in c_id_ls:
			pos0 += eq[c_id+"_margin_y0"]
			cond_ls.append(
				eq[c_id+"_posY"] == pos0)
			pos0 += eq[c_id+"_height"] + eq[c_id+"_margin_y1"]
	elif align == "horizontal":
		pos0 = eq[parent_id+"_posX"]
		for c_id in c_id_ls:
			pos0 += eq[c_id+"_margin_x0"]
			cond_ls.append(
				eq[c_id+"_posX"] == pos0)
			pos0 += eq[c_id+"_width"] + eq[c_id+"_margin_x1"]
		for c_id in c_id_ls:
			cond_ls.append(
				eq[c_id+"_posY"] ==
				eq[parent_id+"_posY"] +
				eq[c_id+"_margin_y0"]
			)
	else:
		raise Exception("[RangeCSS error] invalid align.")
	return cond_ls

# rcss_id 1つについて立式 (関係する子要素との関係も式に盛り込まれる)
def one_formulate(rcss_style, rcss_id):
	cond_ls, loss_ls = [], []
	# range_strによる制約条件を加える
	def add_r_str_cond(eq_var, range_str):
		min_v, max_v, def_v = parse_range_str(range_str)	# 幅指定のパース ("10px~[30px]" など)
		if min_v is not None: cond_ls.append(eq_var >= min_v)
		if max_v is not None: cond_ls.append(eq_var <= max_v)
		if def_v is not None: loss_ls.append((eq_var - def_v) ** 2)
	# rcss_idで指定される要素の情報
	self_info = rcss_style[rcss_id]
	# 自身のsizeに関する制約
	for axis in ["width", "height"]:
		add_r_str_cond(eq[rcss_id+"_%s"%axis], self_info[axis])	# range_strによる制約条件を加える
	# 自身のmarginに関する制約
	for mtype in ["margin_x0", "margin_x1", "margin_y0", "margin_y1"]:
		add_r_str_cond(eq[rcss_id+"_%s"%mtype], self_info[mtype])	# range_strによる制約条件を加える
	# 子要素がある場合の制約
	if len(self_info["children"]) > 0:
		# 自身のsizeと子どもたちのsize, marginとの関係式の生成
		cond_ls += gen_size_rel_conds(rcss_id,
			self_info["children"], self_info["align"])
		# 子どもたちのposに関する式の生成 (子どもの人数分)
		cond_ls += gen_pos_rel_conds(rcss_id,
			self_info["children"], self_info["align"])
	return cond_ls, loss_ls

# yaml形式のRangeCSS_Styleをequid形式のcond, lossに変換
def yaml_style_to_equid(rcss_style):
	# 省略された指定を補完
	norm_rcss_style = normalize_yaml_style(rcss_style, default_len = 10.0)
	# 要素ごとに式を作って統合
	cond_ls, loss_ls, css_id_ls = [], [], []
	for rcss_id in rcss_style:
		# rcss_id 1つについて立式 (関係する子要素との関係も式に盛り込まれる)
		one_c_ls, one_l_ls = one_formulate(norm_rcss_style, rcss_id)
		# 格納
		cond_ls += one_c_ls
		loss_ls += one_l_ls
		css_id_ls.append(rcss_style[rcss_id]["css_id"])
	# 統合
	cond = formula_reduce(cond_ls, lambda a, b: a & b, True)	# 2項演算をlistに対して繰り返し適用 (formula型を想定)
	loss = formula_reduce(loss_ls, lambda a, b: a + b, 0)	# 2項演算をlistに対して繰り返し適用 (formula型を想定)
	return cond, loss, css_id_ls
