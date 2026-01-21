"""
統計計算ツール
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Optional


class StatisticsCalculator:
    """統計計算を行うクラス"""
    
    @staticmethod
    def basic_statistics(data: List[float]) -> Dict:
        """基本統計量を計算"""
        arr = np.array(data)
        
        return {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "mode": float(stats.mode(arr, keepdims=True)[0][0]) if len(arr) > 0 else None,
            "std": float(np.std(arr, ddof=0)),  # 母標準偏差
            "std_sample": float(np.std(arr, ddof=1)),  # 標本標準偏差
            "variance": float(np.var(arr, ddof=0)),  # 母分散
            "variance_sample": float(np.var(arr, ddof=1)),  # 標本分散
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "range": float(np.max(arr) - np.min(arr)),
            "q1": float(np.percentile(arr, 25)),
            "q3": float(np.percentile(arr, 75)),
            "iqr": float(np.percentile(arr, 75) - np.percentile(arr, 25)),
            "skewness": float(stats.skew(arr)),
            "kurtosis": float(stats.kurtosis(arr))
        }
    
    @staticmethod
    def t_test_one_sample(data: List[float], mu0: float) -> Dict:
        """1標本t検定"""
        t_stat, p_value = stats.ttest_1samp(data, mu0)
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "df": len(data) - 1
        }
    
    @staticmethod
    def t_test_two_sample(data1: List[float], data2: List[float], 
                         equal_var: bool = True) -> Dict:
        """2標本t検定"""
        t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "df": len(data1) + len(data2) - 2 if equal_var else None
        }
    
    @staticmethod
    def t_test_paired(data1: List[float], data2: List[float]) -> Dict:
        """対応のあるt検定"""
        t_stat, p_value = stats.ttest_rel(data1, data2)
        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "df": len(data1) - 1
        }
    
    @staticmethod
    def chi_square_test(observed: List[List[float]]) -> Dict:
        """カイ二乗検定"""
        chi2, p_value, dof, expected = stats.chi2_contingency(observed)
        return {
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "degrees_of_freedom": int(dof),
            "expected_frequencies": expected.tolist()
        }
    
    @staticmethod
    def f_test(data1: List[float], data2: List[float]) -> Dict:
        """F検定（等分散性の検定）"""
        var1 = np.var(data1, ddof=1)
        var2 = np.var(data2, ddof=1)
        f_stat = var1 / var2 if var2 > 0 else 0
        
        df1 = len(data1) - 1
        df2 = len(data2) - 1
        p_value = 2 * min(stats.f.cdf(f_stat, df1, df2), 1 - stats.f.cdf(f_stat, df1, df2))
        
        return {
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "df1": df1,
            "df2": df2
        }
    
    @staticmethod
    def correlation_test(x: List[float], y: List[float]) -> Dict:
        """相関係数の検定"""
        r, p_value = stats.pearsonr(x, y)
        return {
            "correlation": float(r),
            "p_value": float(p_value),
            "n": len(x)
        }
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Dict:
        """単回帰分析"""
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # 決定係数
        r_squared = r_value ** 2
        
        return {
            "slope": float(slope),
            "intercept": float(intercept),
            "r_squared": float(r_squared),
            "correlation": float(r_value),
            "p_value": float(p_value),
            "std_err": float(std_err)
        }
    
    @staticmethod
    def multiple_regression(X: List[List[float]], y: List[float]) -> Dict:
        """重回帰分析（簡易版）"""
        from sklearn.linear_model import LinearRegression
        
        model = LinearRegression()
        model.fit(X, y)
        
        # 予測値
        y_pred = model.predict(X)
        
        # 決定係数
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # 調整済み決定係数
        n = len(y)
        k = len(X[0]) if X else 0
        adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - k - 1) if n > k + 1 else r_squared
        
        return {
            "coefficients": model.coef_.tolist(),
            "intercept": float(model.intercept_),
            "r_squared": float(r_squared),
            "adjusted_r_squared": float(adjusted_r_squared)
        }
