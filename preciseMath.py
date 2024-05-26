import math
from decimal import Decimal, getcontext

precision = 200
getcontext().prec = precision

def pi():
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165")
    return pi

def sin(θ):
    # θ の値を [-π, π] の範囲に収める
    θ = θ % (2 * pi())
    
    # sin(θ) の計算
    result = Decimal(0)
    term = θ  # 最初の項は θ そのもの
    i = 1
    while abs(term) > 1e-200:  # 項が非常に小さくなるまで計算を続ける
        result += term
        i += 2
        term = (-1) ** (i // 2) * (θ ** i) / Decimal(factorial(i))
    return result

def cos(θ):
    # θ の値を [-π, π] の範囲に収める
    θ = θ % (2 * pi())
    
    # cos(θ) の計算
    result = Decimal(0)
    term = 1  # 最初の項は 1
    i = 0
    while abs(term) > 1e-200:  # 項が非常に小さくなるまで計算を続ける
        result += term
        i += 2
        term = (-1) ** (i // 2) * (θ ** i) / Decimal(factorial(i))
    return result

def root(n, value):
    # 関数定義
    f = lambda x: x**n - value
    df = lambda x: n*x**(n-1)
    
    # 初期値の設定
    x0 = 1
    
    # ニュートン法で解を計算
    while True:
        x = x0 - f(x0) / df(x0)
        if abs(x-x0) < Decimal("0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"):
            break
        else:
            x0 = x
    
    return x

def factorial(n):
    # n の階乗を計算
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
