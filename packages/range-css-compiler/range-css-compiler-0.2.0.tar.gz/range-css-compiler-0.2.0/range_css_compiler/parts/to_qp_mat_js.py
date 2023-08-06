
# 2次計画問題の行列を定義するjsコードに変換 [to_qp_mat_js.py]

import sys
import fies
import json
import random
import numpy as np
import equid as eq
from sout import sout
from tqdm import tqdm

# クラス判定のための糖衣構文
formula_class = eq

# formula型かどうかを判定
def is_formula(arg_obj):
	if type(arg_obj) == formula_class: return True
	return False

# 変数の列挙
def listup_args(formula_ls):
	var_dic = {}
	for f in formula_ls:
		for var_name in f.listup_vars():
			var_dic[var_name] = True
	var_ls = list(var_dic)
	return var_ls

# 再帰的な二項演算を一列に分解する
def div_rec_dual(
	arg_formula,	# 対象の式
	op	# 演算子
):
	f = arg_formula
	# 再帰終了条件
	if is_formula(f) is False: return [f]	# formula型かどうかを判定
	if f._type != op: return [f]
	# 1つずつバラす
	left, right = f._args
	return div_rec_dual(left, op) + div_rec_dual(right, op)

# 進捗の表示
pre_per_shell = [None]
def show_progress(idx, all_n, prompt = "processing"):
	per_value = int(idx / all_n * 100)
	if per_value == pre_per_shell[0]: return False
	print("%s [%d%%]..."%(prompt, per_value))
	pre_per_shell[0] = per_value
	return True

# 不等号の向きなどを見て「j <= 0」としたときのjを作る
def gen_j(one_cond):
	l_f, r_f = one_cond._args
	sign = (-1 if ">" in one_cond._type else 1)
	j = (l_f - r_f) * sign
	return j

# jから係数を取り出す
def pickup_k(j, var_ls):
	# 右辺の計算
	right = -j.fix(**{v: 0 for v in var_ls})
	# 左辺の計算 (各変数の係数)
	left = [
		(j + right).fix(**{
			v: int(v == var_name)
			for v in var_ls
		})
		for var_name in var_ls
	]
	return left, right

# 条件式1つ(equid型)から係数を取り出し
def one_cond_to_qp(one_cond, var_ls):
	# bool式の特別処理
	if type(one_cond) == type(True):
		zeros = [0 for _ in var_ls]
		return ("eq", zeros,
			(0 if one_cond is True else 1)
		)
	# 等式 / 不等式を判別
	cond_type = {
		"==": "eq",
		"<=": "le", ">=": "le", "<": "le", ">": "le",	# 注意: 不等号の向きにかかわらず最終的には同じ向きの不等式の形に変形される
	}[one_cond._type]
	# 不等号の向きなどを見て「j <= 0」としたときのjを作る
	j = gen_j(one_cond)
	# jから係数を取り出す
	left, right = pickup_k(j, var_ls)
	return cond_type, left, right

# condを二次計画の係数に変換
def cond_to_qp(cond, var_ls):
	# andで分解する
	cond_ls = div_rec_dual(cond, "and")	# 再帰的な二項演算を一列に分解する
	# 各condを整形
	left_dic = {"eq": [], "le": []}
	right_dic = {"eq": [], "le": []}
	for one_cond in tqdm(cond_ls):
		# show_progress(idx, len(cond_ls))	# 進捗の表示
		if one_cond is True: continue
		# 条件式1つ(equid型)から係数を取り出し
		cond_type, left, right = one_cond_to_qp(one_cond, var_ls)
		# left_dic[cond_type].append(left)
		# right_dic[cond_type].append(right)
		if cond_type == "eq":
			left_dic["le"].append(left)
			right_dic["le"].append(right)
			left_dic["le"].append([-e for e in left])
			right_dic["le"].append(-right)
		else:
			left_dic["le"].append(left)
			right_dic["le"].append(right)
	# 格納
	A = left_dic["eq"]
	b = right_dic["eq"]
	G = left_dic["le"]
	h = right_dic["le"]
	return G, h, A, b

# 式が想定外の項を含まないことの確認 (乱数アルゴリズム; NGの場合は落とす)
def validate_loss(loss, a1_ls, a2_ls, var_ls, const_vars):
	# 定数項の算出
	c = loss.fix(**{v: 0 for v in var_ls})
	# 想定されるequid式の組み立て
	pred_loss = c
	for v, a1, a2 in zip(var_ls, a1_ls, a2_ls):
		pred_loss += a2 * eq[v] ** 2 + a1 * eq[v]
	# 乱数で検証
	rand_dic = {v: random.random() for v in var_ls}
	eps = 1e-4
	delta = (pred_loss.fix(**rand_dic) - loss.fix(**rand_dic))
	# const_varsについては影響がないはずなので、乱数を入れて束縛してみる
	fixed_delta = delta.fix(**{var: random.random() for var in const_vars})
	if abs(fixed_delta) > eps:
		raise Exception("[error] 式の形が想定外の可能性があります。")

# formula型混入チェッカー
def formula_in_list_cheker(arg_ls):
	for e in arg_ls:
		if type(e) == type(eq["_DUMMY_VAR"]): return True
	return False

# lossを二次計画の係数に変換
def loss_to_qp(loss, var_ls, const_vars):
	# 次の形を想定: a2 * var^2 + a1 * var + a0 + ...
	a1_ls, a2_ls = [], []
	for var_name in var_ls:
		d_loss = loss.diff(var_name)
		a1 = eq.fix(d_loss, **{var_name: 0})
		temp = eq.fix(d_loss, **{var_name: 1})
		a2 = (temp - a1) / 2
		a1_ls.append(a1)
		a2_ls.append(a2)
	# const_vars の混入チェック
	if formula_in_list_cheker(a1_ls + a2_ls) is True:	# formula型混入チェッカー
		raise Exception("[error] formula型が混入しないはずの場所に混入しています。実装を確認してください。")
	# 擬似的に正定値化
	eps = 1e-8
	a2_ls = [(eps if e < eps else e) for e in a2_ls]
	# 式が想定外の項を含まないことの確認 (乱数アルゴリズム; NGの場合は落とす)
	validate_loss(loss, a1_ls, a2_ls, var_ls, const_vars)
	# P, qの形に変換
	P = [
		[
			(a2_ls[i] * 2 if v_in == v_out else 0)
			for i, v_in in enumerate(var_ls)
		]
		for v_out in var_ls
	]
	q = a1_ls
	return P, q

# equidのcond, lossを二次計画問題の係数行列の形に変換する
def to_qp_form(cond, loss, const_vars):
	# 変数の列挙
	raw_var_ls = listup_args(formula_ls = [cond, loss])
	var_ls = [var for var in raw_var_ls if var not in const_vars]
	# condを二次計画の係数に変換
	G, h, A, b = cond_to_qp(cond, var_ls)
	# lossを二次計画の係数に変換
	P, q = loss_to_qp(loss, var_ls, const_vars)
	return var_ls, P, q, G, h, A, b

# tensorの要素ごと負号
def mat_neg(tensor):
	if type(tensor) != type([]): return -tensor
	return [mat_neg(e) for e in tensor]

# qp_mat_jsのコードテンプレート
qp_mat_js_code_template = """
// 定数項を束縛した2次計画の係数行列を生成
function def_mat(const_vars_dic){
	return {
		"var_ls": %s,
		"Dmat": %s,
		"dvec": %s,
		"Amat": %s,
		"bvec": %s,
	};
}
"""

# formula型を含むテンソルをjsコードに変換 (あとから部分適用する形)
def formula_tensor_to_js(org_tensor, vars_dic_name):
	# listの場合
	if type(org_tensor) == type([]):
		partial_js_tensor = [
			formula_tensor_to_js(e, vars_dic_name)
			for e in org_tensor
		]
		return "[%s]"%(", ".join(partial_js_tensor))
	# 数値の場合
	if type(org_tensor) != type(eq["_DUMMY_VAR"]): return str(org_tensor)
	# formulaの場合
	formula = org_tensor
	for _ in range(5): formula = formula.simplify()
	js_code = formula.to_js()
	return "%s(%s)"%(js_code, vars_dic_name)

# 2次計画問題の行列を定義するjsコードに変換 [to_qp_mat_js.py]
def to_qp_mat_js(cond, loss):
	# 変数のまま行列中に残す変数
	const_vars = ["rcss_frame_width", "rcss_frame_height", "rcss_frame_posX", "rcss_frame_posY"]
	# equidのcond, lossを二次計画問題の係数行列の形に変換する
	var_ls, P, q, G, h, A, b = to_qp_form(cond, loss, const_vars)
	# const_varsを渡すと行列を定義するjsコードを作成
	js_code = qp_mat_js_code_template%(
		json.dumps(var_ls, ensure_ascii = False),
		formula_tensor_to_js(P, vars_dic_name = "const_vars_dic"),	# formula型を含むテンソルをjsコードに変換 (あとから部分適用する形)
		formula_tensor_to_js(q, vars_dic_name = "const_vars_dic"),	# formula型を含むテンソルをjsコードに変換 (あとから部分適用する形)
		formula_tensor_to_js(mat_neg(G), vars_dic_name = "const_vars_dic"),	# formula型を含むテンソルをjsコードに変換 (あとから部分適用する形)
		formula_tensor_to_js(mat_neg(h), vars_dic_name = "const_vars_dic"),	# formula型を含むテンソルをjsコードに変換 (あとから部分適用する形)
	)
	return js_code
