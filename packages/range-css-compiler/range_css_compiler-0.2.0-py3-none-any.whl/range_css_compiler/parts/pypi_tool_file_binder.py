
# pypi公開ツール用のファイル同梱ラップスクリプト [pypi_tool_file_binder.py]

# applier_utils.js
applier_utils = """
// rcssのスタイルをhtmlの配置に適用するapplierの部品 [applier_utils.js]

// 辞書の全keyにprefixを付ける関数
function addPrefixToDictKeys(dict, prefix) {
	var newDict = {};
	for (let key in dict) {
		newDict[prefix + key] = dict[key];
	}
	return newDict;
}

// 辞書内包の偽物
function createDict(n, k, v) {
	const dict = {};
	for (let i = 0; i < n; i++) {
		dict[k(i)] = v(i);
	}
	return dict;
}

// 配置の最適化
function opt_core(frame_info){
	const_vars_dic = addPrefixToDictKeys(frame_info, "rcss_frame_");	// 辞書の全keyにprefixを付ける関数
	mat_dic = def_mat(const_vars_dic);
	res = solve_qp_0(mat_dic["Dmat"], mat_dic["dvec"], mat_dic["Amat"], mat_dic["bvec"]);
	res_x_dic = createDict(	// 辞書内包の偽物
		mat_dic["var_ls"].length,	// n
		(i) => mat_dic["var_ls"][i],	// keyの規定
		(i) => res["solution"][i]	// valueの規定
	);
	return res_x_dic
}

// listの最終要素取得
function last(arg_ls) {
	var n = arg_ls.length;
	return arg_ls[n - 1];
}

// res_x_dic を solved_styleに変換
function res_x_to_solved_style(res_x_dic, css_id_ls){
	var inner_key_ls = ["posX", "posY", "width", "height"];
	var rcss_solved_style = [];
	for (css_id of css_id_ls){
		rcss_solved_style.push({"css_id": css_id});
		for (key of inner_key_ls){
			var concat_key = `${css_id}_${key}`;
			var value = res_x_dic[concat_key];
			last(rcss_solved_style)[key] = value;
		}
	}
	return rcss_solved_style;
}

// 左上を(0,0)としたframe_infoを作る
function make_fi_0(frame_info){
    frame_info_0 = {...frame_info, posX: 0, posY: 0};
    return frame_info_0
}

// frame_infoの一致性確認
function compare_fi(frame_info_1, frame_info_2) {
    const keys = ["posX", "posY", "width", "height"];
    for (let i = 0; i < keys.length; i++) {
        const key = keys[i];
        if (frame_info_1[key] != frame_info_2[key]) {return false;}
    }
    return true;
}

// 結果がキャッシュされた配置最適化
let pre_frame_info = {};
let so_cache = null;
function cached_style_opt(frame_info){
    // frame_infoの一致性確認
    if (compare_fi(frame_info, pre_frame_info)) {
        return so_cache;
    }
    // 配置の最適化
    var res_x_dic = opt_core(frame_info);
    // res_x_dic を solved_styleに変換
    var rcss_solved_style = res_x_to_solved_style(res_x_dic, css_id_ls);
    // cacheに保存
    pre_frame_info = frame_info;
    so_cache = rcss_solved_style;
    return rcss_solved_style
}

// 左上の基準点をずらす
function shift_pos(rcss_solved_style_0, frame_info){
    var rcss_solved_style = [];
    for(one_ele_style of rcss_solved_style_0){
        rcss_solved_style.push({
            ...one_ele_style,
            "posX": one_ele_style["posX"] + frame_info["posX"],
            "posY": one_ele_style["posY"] + frame_info["posY"],
        });
    }
    return rcss_solved_style;
}

// 配置最適化計算
function style_opt(frame_info){
    // 左上を(0,0)としたframe_infoを作る
    var frame_info_0 = make_fi_0(frame_info);
    // 結果がキャッシュされた配置最適化
    var rcss_solved_style_0 = cached_style_opt(frame_info_0);
    // 左上の基準点をずらす
    return shift_pos(rcss_solved_style_0, frame_info);
}

// frameのオフセット位置・サイズの計算
function calc_frame_info(){
    // frameの位置と大きさを表すオブジェクトの取得
    var e = document.getElementById("rcss_frame");
    var rect = e.getBoundingClientRect();
    // frame_infoオブジェクトの形にまとめる
    var frame_info = {
        "posX": rect.left,
        "posY": rect.top,
        "width": rect.width,
        "height": rect.height,
    }
    return frame_info;
}

// 1つの要素についてstyleを適用
function apply_style_one_ele(one_ele_style){
    // 対象要素を見つける
    var target = document.getElementById(one_ele_style["css_id"]);
    // cssのスタイル適用
    target.style.position = "fixed";
    target.style.left = one_ele_style["posX"];
    target.style.top = one_ele_style["posY"];
    target.style.width = one_ele_style["width"];
    target.style.height = one_ele_style["height"];
}

// スタイル適用関数
function apply_rcss_style(rcss_solved_style){
    for(one_ele_style of rcss_solved_style){
        if (one_ele_style["css_id"] == "rcss_frame") {continue;}
        // 1つの要素についてstyleを適用
        apply_style_one_ele(one_ele_style);
    }
}
"""

# browserified_quadprog.js
browserified_quadprog = """
(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
var qp = require('quadprog');

// 行列の転置
function transpose(matrix) {
	// 行列の列数を取得する
	const cols = matrix[0].length;
	// 行列を転置するための結果配列を作成する
	const result = [];
	for (let i = 0; i < cols; i++) {
		result.push([]);
	}
	// 行列を転置する
	for (let i = 0; i < matrix.length; i++) {
		for (let j = 0; j < cols; j++) {
			result[j][i] = matrix[i][j];
		}
	}
	return result;
}

// 行列の引数の開始インデックスを1に変更する
function idx_01(tensor) {
	// テンソルが配列である場合
	if (Array.isArray(tensor)) {
		// テンソルを変換するための結果配列を作成する
		const result = tensor.map((v) => idx_01(v));
		// テンソルの最初にundefinedを追加する
		result.unshift(undefined);
		return result;
	}
	// テンソルが配列でない場合
	return tensor;
}

// テンソルの1始まりのインデックスを0始まりに変換
function idx_original(tensor) {
	// テンソルが配列である場合
	if (Array.isArray(tensor)) {
		// テンソルを変換するための結果配列を作成する
		const result = tensor.map((v) => idx_original(v));
		// テンソルの最初の要素を削除する
		result.shift();
		return result;
	}
	// テンソルが配列でない場合
	return tensor;
}

// 結果辞書のvalueがlistのものについてインデックスを0始まりにする関数
function idx_original_dict(dict) {
	// 結果を格納する空の辞書を作成する
	const result = {};
	// 辞書のすべてのキーを反復処理する
	for (const key of Object.keys(dict)) {
		// 値が配列の場合はidx_original()関数を適用する
		if (Array.isArray(dict[key])) {
			result[key] = idx_original(dict[key]);
		}
		// 値が配列でない場合はそのまま放置する
		else {
			result[key] = dict[key];
		}
	}
	// 結果の辞書を返す
	return result;
}

// ブラウザ版quadprog (インデックスを0始まりにしたもの)
solve_qp_0 = function(	// 明示的にglobal-scopeに束縛
	Dmat,	// 目的関数の2次の係数 (0.5 x^T Dmat x)
	dvec,	// 目的関数の1次の係数 (x^T dvec)
	Amat,	// 不等式制約の係数行列 (Amat x >= bvec)
	bvec	// 不等式制約の切片ベクトル (Amat x >= bvec)
){
	// A行列を転置する
	var Amat = transpose(Amat);	// 行列の転置
	// 行列の引数の開始インデックスを1に変更する
	var Dmat = idx_01(Dmat);
	var dvec = idx_01(dvec);
	var Amat = idx_01(Amat);
	var bvec = idx_01(bvec);
	res = qp.solveQP(Dmat, dvec, Amat, bvec);
	// 結果辞書のvalueがlistのものについてインデックスを0始まりにする関数
	return idx_original_dict(res);
}

// // 使用例

// var Dmat = [
// 	[2, 0],
// 	[0, 2],
// ];
// var dvec = [0, 0];
// var Amat = [
// 	[1, 0],
// 	[-1, 0],
// 	[0, 1],
// 	[0, -1],
// ];
// var bvec = [10, -20, 7, -7];

// // ブラウザ版quadprog (インデックスを0始まりにしたもの)
// res = solve_qp_0(
// 	Dmat,	// 目的関数の2次の係数 (0.5 x^T Dmat x)
// 	dvec,	// 目的関数の1次の係数 (x^T dvec)
// 	Amat,	// 不等式制約の係数行列 (Amat x >= bvec)
// 	bvec	// 不等式制約の切片ベクトル (Amat x >= bvec)
// );

// // 結果確認
// console.log(res);

},{"quadprog":2}],2:[function(require,module,exports){
"use strict";

module.exports = require("./lib/quadprog");

},{"./lib/quadprog":7}],3:[function(require,module,exports){
"use strict";

function dpofa(a, lda, n, info) {
    let jm1, t, s;

    for (let j = 1; j <= n; j += 1) {
        info[1] = j;
        s = 0;
        jm1 = j - 1;
        if (jm1 < 1) {
            s = a[j][j] - s;
            if (s <= 0) {
                break;
            }
            a[j][j] = Math.sqrt(s);
        } else {
            for (let k = 1; k <= jm1; k += 1) {

                // t = a[k][j] - ddot(k - 1, a[1][k], 1, a[1][j], 1);
                t = a[k][j];
                for (let i = 1; i < k; i += 1) {
                    t -= a[i][j] * a[i][k];
                }
                t /= a[k][k];
                a[k][j] = t;
                s += t * t;
            }
            s = a[j][j] - s;
            if (s <= 0) {
                break;
            }
            a[j][j] = Math.sqrt(s);
        }
        info[1] = 0;
    }
}

module.exports = dpofa;

},{}],4:[function(require,module,exports){
"use strict";

function dpori(a, lda, n) {
    let kp1, t;

    for (let k = 1; k <= n; k += 1) {
        a[k][k] = 1 / a[k][k];
        t = -a[k][k];

        // dscal(k - 1, t, a[1][k], 1);
        for (let i = 1; i < k; i += 1) {
            a[i][k] *= t;
        }

        kp1 = k + 1;
        if (n < kp1) {
            break;
        }
        for (let j = kp1; j <= n; j += 1) {
            t = a[k][j];
            a[k][j] = 0;

            // daxpy(k, t, a[1][k], 1, a[1][j], 1);
            for (let i = 1; i <= k; i += 1) {
                a[i][j] += t * a[i][k];
            }
        }
    }
}

module.exports = dpori;

},{}],5:[function(require,module,exports){
"use strict";

function dposl(a, lda, n, b) {
    let k, t;

    for (k = 1; k <= n; k += 1) {

        // t = ddot(k - 1, a[1][k], 1, b[1], 1);
        t = 0;
        for (let i = 1; i < k; i += 1) {
            t += a[i][k] * b[i];
        }

        b[k] = (b[k] - t) / a[k][k];
    }

    for (let kb = 1; kb <= n; kb += 1) {
        k = n + 1 - kb;
        b[k] /= a[k][k];
        t = -b[k];

        // daxpy(k - 1, t, a[1][k], 1, b[1], 1);
        for (let i = 1; i < k; i += 1) {
            b[i] += t * a[i][k];
        }
    }
}

module.exports = dposl;

},{}],6:[function(require,module,exports){
"use strict";

const vsmall = require("./vsmall");
const dpori = require("./dpori");
const dposl = require("./dposl");
const dpofa = require("./dpofa");

function qpgen2(dmat, dvec, fddmat, n, sol, lagr, crval, amat, bvec, fdamat, q, meq, iact, nnact = 0, iter, work, ierr) {
    let l1, it1, nvl, nact, temp, sum, t1, tt, gc, gs, nu, t1inf, t2min, go;

    const r = Math.min(n, q);

    let l = 2 * n + (r * (r + 5)) / 2 + 2 * q + 1;

    for (let i = 1; i <= n; i += 1) {
        work[i] = dvec[i];
    }
    for (let i = n + 1; i <= l; i += 1) {
        work[i] = 0;
    }
    for (let i = 1; i <= q; i += 1) {
        iact[i] = 0;
        lagr[i] = 0;
    }

    const info = [];

    if (ierr[1] === 0) {
        dpofa(dmat, fddmat, n, info);
        if (info[1] !== 0) {
            ierr[1] = 2;
            return;
        }
        dposl(dmat, fddmat, n, dvec);
        dpori(dmat, fddmat, n);
    } else {
        for (let j = 1; j <= n; j += 1) {
            sol[j] = 0;
            for (let i = 1; i <= j; i += 1) {
                sol[j] += dmat[i][j] * dvec[i];
            }
        }
        for (let j = 1; j <= n; j += 1) {
            dvec[j] = 0;
            for (let i = j; i <= n; i += 1) {
                dvec[j] += dmat[j][i] * sol[i];
            }
        }
    }

    crval[1] = 0;
    for (let j = 1; j <= n; j += 1) {
        sol[j] = dvec[j];
        crval[1] += work[j] * sol[j];
        work[j] = 0;
        for (let i = j + 1; i <= n; i += 1) {
            dmat[i][j] = 0;
        }
    }
    crval[1] = -crval[1] / 2;
    ierr[1] = 0;

    const iwzv = n;
    const iwrv = iwzv + n;
    const iwuv = iwrv + r;
    const iwrm = iwuv + r + 1;
    const iwsv = iwrm + (r * (r + 1)) / 2;
    const iwnbv = iwsv + q;

    for (let i = 1; i <= q; i += 1) {
        sum = 0;
        for (let j = 1; j <= n; j += 1) {
            sum += amat[j][i] * amat[j][i];
        }
        work[iwnbv + i] = Math.sqrt(sum);
    }

    nact = nnact;

    iter[1] = 0;
    iter[2] = 0;

    function fnGoto50() {
        iter[1] += 1;

        l = iwsv;
        for (let i = 1; i <= q; i += 1) {
            l += 1;
            sum = -bvec[i];
            for (let j = 1; j <= n; j += 1) {
                sum += amat[j][i] * sol[j];
            }
            if (Math.abs(sum) < vsmall) {
                sum = 0;
            }
            if (i > meq) {
                work[l] = sum;
            } else {
                work[l] = -Math.abs(sum);
                if (sum > 0) {
                    for (let j = 1; j <= n; j += 1) {
                        amat[j][i] = -amat[j][i];
                    }
                    bvec[i] = -bvec[i];
                }
            }
        }

        for (let i = 1; i <= nact; i += 1) {
            work[iwsv + iact[i]] = 0;
        }

        nvl = 0;
        temp = 0;
        for (let i = 1; i <= q; i += 1) {
            if (work[iwsv + i] < temp * work[iwnbv + i]) {
                nvl = i;
                temp = work[iwsv + i] / work[iwnbv + i];
            }
        }
        if (nvl === 0) {
            for (let i = 1; i <= nact; i += 1) {
                lagr[iact[i]] = work[iwuv + i];
            }
            return 999;
        }

        return 0;
    }

    function fnGoto55() {
        for (let i = 1; i <= n; i += 1) {
            sum = 0;
            for (let j = 1; j <= n; j += 1) {
                sum += dmat[j][i] * amat[j][nvl];
            }
            work[i] = sum;
        }

        l1 = iwzv;
        for (let i = 1; i <= n; i += 1) {
            work[l1 + i] = 0;
        }
        for (let j = nact + 1; j <= n; j += 1) {
            for (let i = 1; i <= n; i += 1) {
                work[l1 + i] = work[l1 + i] + dmat[i][j] * work[j];
            }
        }

        t1inf = true;
        for (let i = nact; i >= 1; i -= 1) {
            sum = work[i];
            l = iwrm + (i * (i + 3)) / 2;
            l1 = l - i;
            for (let j = i + 1; j <= nact; j += 1) {
                sum -= work[l] * work[iwrv + j];
                l += j;
            }
            sum /= work[l1];
            work[iwrv + i] = sum;
            if (iact[i] <= meq) {
                continue;
            }
            if (sum <= 0) {
                continue;
            }
            t1inf = false;
            it1 = i;
        }

        if (!t1inf) {
            t1 = work[iwuv + it1] / work[iwrv + it1];
            for (let i = 1; i <= nact; i += 1) {
                if (iact[i] <= meq) {
                    continue;
                }
                if (work[iwrv + i] <= 0) {
                    continue;
                }
                temp = work[iwuv + i] / work[iwrv + i];
                if (temp < t1) {
                    t1 = temp;
                    it1 = i;
                }
            }
        }

        sum = 0;
        for (let i = iwzv + 1; i <= iwzv + n; i += 1) {
            sum += work[i] * work[i];
        }
        if (Math.abs(sum) <= vsmall) {
            if (t1inf) {
                ierr[1] = 1;

                return 999; // GOTO 999
            }
            for (let i = 1; i <= nact; i += 1) {
                work[iwuv + i] = work[iwuv + i] - t1 * work[iwrv + i];
            }
            work[iwuv + nact + 1] = work[iwuv + nact + 1] + t1;

            return 700; // GOTO 700
        }
        sum = 0;
        for (let i = 1; i <= n; i += 1) {
            sum += work[iwzv + i] * amat[i][nvl];
        }
        tt = -work[iwsv + nvl] / sum;
        t2min = true;
        if (!t1inf) {
            if (t1 < tt) {
                tt = t1;
                t2min = false;
            }
        }

        for (let i = 1; i <= n; i += 1) {
            sol[i] += tt * work[iwzv + i];
            if (Math.abs(sol[i]) < vsmall) {
                sol[i] = 0;
            }
        }

        crval[1] += tt * sum * (tt / 2 + work[iwuv + nact + 1]);
        for (let i = 1; i <= nact; i += 1) {
            work[iwuv + i] = work[iwuv + i] - tt * work[iwrv + i];
        }
        work[iwuv + nact + 1] = work[iwuv + nact + 1] + tt;

        if (t2min) {
            nact += 1;
            iact[nact] = nvl;

            l = iwrm + ((nact - 1) * nact) / 2 + 1;
            for (let i = 1; i <= nact - 1; i += 1) {
                work[l] = work[i];
                l += 1;
            }

            if (nact === n) {
                work[l] = work[n];
            } else {
                for (let i = n; i >= nact + 1; i -= 1) {
                    if (work[i] === 0) {
                        continue;
                    }
                    gc = Math.max(Math.abs(work[i - 1]), Math.abs(work[i]));
                    gs = Math.min(Math.abs(work[i - 1]), Math.abs(work[i]));
                    if (work[i - 1] >= 0) {
                        temp = Math.abs(gc * Math.sqrt(1 + gs * gs /
                            (gc * gc)));
                    } else {
                        temp = -Math.abs(gc * Math.sqrt(1 + gs * gs /
                            (gc * gc)));
                    }
                    gc = work[i - 1] / temp;
                    gs = work[i] / temp;

                    if (gc === 1) {
                        continue;
                    }
                    if (gc === 0) {
                        work[i - 1] = gs * temp;
                        for (let j = 1; j <= n; j += 1) {
                            temp = dmat[j][i - 1];
                            dmat[j][i - 1] = dmat[j][i];
                            dmat[j][i] = temp;
                        }
                    } else {
                        work[i - 1] = temp;
                        nu = gs / (1 + gc);
                        for (let j = 1; j <= n; j += 1) {
                            temp = gc * dmat[j][i - 1] + gs * dmat[j][i];
                            dmat[j][i] = nu * (dmat[j][i - 1] + temp) -
                                dmat[j][i];
                            dmat[j][i - 1] = temp;

                        }
                    }
                }
                work[l] = work[nact];
            }
        } else {
            sum = -bvec[nvl];
            for (let j = 1; j <= n; j += 1) {
                sum += sol[j] * amat[j][nvl];
            }
            if (nvl > meq) {
                work[iwsv + nvl] = sum;
            } else {
                work[iwsv + nvl] = -Math.abs(sum);
                if (sum > 0) {
                    for (let j = 1; j <= n; j += 1) {
                        amat[j][nvl] = -amat[j][nvl];
                    }
                    bvec[nvl] = -bvec[nvl];
                }
            }

            return 700; // GOTO 700
        }

        return 0;
    }

    function fnGoto797() {
        l = iwrm + (it1 * (it1 + 1)) / 2 + 1;
        l1 = l + it1;
        if (work[l1] === 0) {
            return 798; // GOTO 798
        }
        gc = Math.max(Math.abs(work[l1 - 1]), Math.abs(work[l1]));
        gs = Math.min(Math.abs(work[l1 - 1]), Math.abs(work[l1]));
        if (work[l1 - 1] >= 0) {
            temp = Math.abs(gc * Math.sqrt(1 + gs * gs / (gc * gc)));
        } else {
            temp = -Math.abs(gc * Math.sqrt(1 + gs * gs / (gc * gc)));
        }
        gc = work[l1 - 1] / temp;
        gs = work[l1] / temp;

        if (gc === 1) {
            return 798; // GOTO 798
        }
        if (gc === 0) {
            for (let i = it1 + 1; i <= nact; i += 1) {
                temp = work[l1 - 1];
                work[l1 - 1] = work[l1];
                work[l1] = temp;
                l1 += i;
            }
            for (let i = 1; i <= n; i += 1) {
                temp = dmat[i][it1];
                dmat[i][it1] = dmat[i][it1 + 1];
                dmat[i][it1 + 1] = temp;
            }
        } else {
            nu = gs / (1 + gc);
            for (let i = it1 + 1; i <= nact; i += 1) {
                temp = gc * work[l1 - 1] + gs * work[l1];
                work[l1] = nu * (work[l1 - 1] + temp) - work[l1];
                work[l1 - 1] = temp;
                l1 += i;
            }
            for (let i = 1; i <= n; i += 1) {
                temp = gc * dmat[i][it1] + gs * dmat[i][it1 + 1];
                dmat[i][it1 + 1] = nu * (dmat[i][it1] + temp) -
                    dmat[i][it1 + 1];
                dmat[i][it1] = temp;
            }
        }

        return 0;
    }

    function fnGoto798() {
        l1 = l - it1;
        for (let i = 1; i <= it1; i += 1) {
            work[l1] = work[l];
            l += 1;
            l1 += 1;
        }

        work[iwuv + it1] = work[iwuv + it1 + 1];
        iact[it1] = iact[it1 + 1];
        it1 += 1;
        if (it1 < nact) {
            return 797; // GOTO 797
        }

        return 0;
    }

    function fnGoto799() {
        work[iwuv + nact] = work[iwuv + nact + 1];
        work[iwuv + nact + 1] = 0;
        iact[nact] = 0;
        nact -= 1;
        iter[2] += 1;

        return 0;
    }

    go = 0;
    while (true) { // eslint-disable-line no-constant-condition
        go = fnGoto50();
        if (go === 999) {
            return;
        }
        while (true) { // eslint-disable-line no-constant-condition
            go = fnGoto55();
            if (go === 0) {
                break;
            }
            if (go === 999) {
                return;
            }
            if (go === 700) {
                if (it1 === nact) {
                    fnGoto799();
                } else {
                    while (true) { // eslint-disable-line no-constant-condition
                        fnGoto797();
                        go = fnGoto798();
                        if (go !== 797) {
                            break;
                        }
                    }
                    fnGoto799();
                }
            }
        }
    }

}

module.exports = qpgen2;

},{"./dpofa":3,"./dpori":4,"./dposl":5,"./vsmall":8}],7:[function(require,module,exports){
"use strict";

const qpgen2 = require("./qpgen2");

function solveQP(Dmat, dvec, Amat, bvec = [], meq = 0, factorized = [0, 0]) {
    const crval = [];
    const iact = [];
    const sol = [];
    const lagr = [];
    const work = [];
    const iter = [];

    let message = "";

    // In Fortran the array index starts from 1
    const n = Dmat.length - 1;
    const q = Amat[1].length - 1;

    if (!bvec) {
        for (let i = 1; i <= q; i += 1) {
            bvec[i] = 0;
        }
    }

    if (n !== Dmat[1].length - 1) {
        message = "Dmat is not symmetric!";
    }
    if (n !== dvec.length - 1) {
        message = "Dmat and dvec are incompatible!";
    }
    if (n !== Amat.length - 1) {
        message = "Amat and dvec are incompatible!";
    }
    if (q !== bvec.length - 1) {
        message = "Amat and bvec are incompatible!";
    }
    if ((meq > q) || (meq < 0)) {
        message = "Value of meq is invalid!";
    }

    if (message !== "") {
        return {
            message
        };
    }

    for (let i = 1; i <= q; i += 1) {
        iact[i] = 0;
        lagr[i] = 0;
    }

    const nact = 0;
    const r = Math.min(n, q);

    for (let i = 1; i <= n; i += 1) {
        sol[i] = 0;
    }
    crval[1] = 0;
    for (let i = 1; i <= (2 * n + (r * (r + 5)) / 2 + 2 * q + 1); i += 1) {
        work[i] = 0;
    }
    for (let i = 1; i <= 2; i += 1) {
        iter[i] = 0;
    }

    qpgen2(Dmat, dvec, n, n, sol, lagr, crval, Amat, bvec, n, q, meq, iact, nact, iter, work, factorized);

    if (factorized[1] === 1) {
        message = "constraints are inconsistent, no solution!";
    }
    if (factorized[1] === 2) {
        message = "matrix D in quadratic function is not positive definite!";
    }

    return {
        solution: sol,
        Lagrangian: lagr,
        value: crval,
        unconstrained_solution: dvec, // eslint-disable-line camelcase
        iterations: iter,
        iact,
        message
    };
}

exports.solveQP = solveQP;

},{"./qpgen2":6}],8:[function(require,module,exports){
"use strict";

let epsilon = 1.0e-60;
let tmpa;
let tmpb;

do {
    epsilon += epsilon;
    tmpa = 1 + 0.1 * epsilon;
    tmpb = 1 + 0.2 * epsilon;
} while (tmpa <= 1 || tmpb <= 1);

module.exports = epsilon;

},{}]},{},[1]);
"""

# compiled_rcss_template.js
compiled_rcss_template = """

/* 2次計画ソルバーのコード */
BUNDLE

/* 最適化対象の行列を定義するコード */
MAT_DEF_CODE

/* rcssの対象となるcss_idのリスト */
css_id_ls = CSS_ID_LIST;

/* rcssのスタイルをhtmlの配置に適用するapplierの部品 */
APPLIER_UTILS

// スタイル適用関数 (部分適用・前回実行中に次回が呼び出されないように)
wa_running = false;
function wrapped_apply(){
	// 前回の処理が未完了の場合に処理しない
	if (wa_running == true) {return;}
	// 処理中
	wa_running = true;
	// 最適化計算
	var frame_info = calc_frame_info();	// frameのオフセット位置・サイズの計算
	var rcss_solved_style = style_opt(frame_info);	// 配置最適化計算
	// スタイル適用関数
	apply_rcss_style(rcss_solved_style);
	// 処理完了
	wa_running = false;
}

// サイズ変更・スクロールイベントでスタイル再適用
window.addEventListener('scroll', wrapped_apply);	// スタイル適用関数 (style情報を部分適用)
window.addEventListener('resize', wrapped_apply);	// スタイル適用関数 (style情報を部分適用)
// 初回に1回スタイル適用
wrapped_apply();	// スタイル適用関数 (style情報を部分適用)
"""
