import numpy as np
import sympy as sp

from seeing.sympyHelpers import *
from seeing.formulary import *
from seeing.integrator import *


def noll_to_zern(jj):
    if (jj == 0):
        raise ValueError("Noll indices start at 1, 0 is invalid.")
    nn = 0
    jj1 = jj - 1
    while (jj1 > nn):
        nn += 1
        jj1 -= nn
    mm = (-1)**jj * ((nn % 2) + 2 * int((jj1 + ((nn + 1) % 2)) / 2.0))
    return nn, mm


def order_to_max_noll(nn):
    return (nn + 2) * (nn + 1) // 2


def NollIndex(nn, mm):
    n4 = nn % 4
    if (mm > 0 and (n4 == 0 or n4 == 1)) or (mm < 0 and (n4 == 2 or n4 == 3)):
        k = 0
    else:
        k = 1
    return nn * (nn + 1) // 2 + abs(mm) + k


def kronDelta(ii, jj):
    if ii == jj:
        return 1
    else:
        return 0


def emValue(mm):
    if mm == 0:
        return 2
    else:
        return 1


def createZernikeFormulary():
    
    r, rho = sp.symbols('r rho', positive=True)
    aa = sp.symbols('a')
    l, j, n, m, max_order = sp.symbols('l j n m n_max', integer=True)
    vlj, theta, f, x0, y0 = sp.symbols('v_lj theta f x0, y0', real=True)
    dotInt = sp.symbols('I_v')
    Cnm = sp.symbols('c_n^m')

    Tnm = sp.Function("T_n^m")(theta)
    Rnm = sp.Function("R_n^m")(rho)
    Znm = sp.Function("Z_n^m")(rho, theta)
    Ynm = sp.Function("Y_n^m")(rho, theta)
    ZnmCart = sp.Function("Z_n^m")(x0, y0)
    VnmFunc = sp.Function("V_n^m")(r)
    ZnmD = sp.Function("Z_n^m_d")(r, theta)
    YnmD = sp.Function("Y_n^m_d")(r, theta)
    f1 = sp.Function("f_1")(rho, theta)
    f2 = sp.Function("f_2")(rho, theta)

    # Real Zernike Polynomials
    def cCoeff():
        _rhs = sp.Piecewise((sp.sqrt(n + 1), m == 0),
                            (sp.sqrt(2 * (n + 1)), m != 0))
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)


    def tangetialFunc():
        _rhs = sp.Piecewise((-sp.sin(m * theta), m < 0),
                            (sp.cos(m * theta), m >= 0))
        _lhs = Tnm
        return sp.Eq(_lhs, _rhs)


    def complexTangetialFunc():
        _rhs = sp.exp(sp.I * m * theta)
        _lhs = Tnm
        return sp.Eq(_lhs, _rhs)


    def radialFunc():
        ma = sp.Abs(m)
        p = (n - ma) / 2
        _rhs = ((-1)**p) * (rho**ma) * sp.jacobi(p, ma, 0, 1 - 2 * rho**2)
        _lhs = Rnm
        return sp.Eq(_lhs, _rhs)


    def realZernike():
        _rhs = radialFunc().rhs * tangetialFunc().rhs
        _lhs = Znm
        return sp.Eq(_lhs, _rhs)


    def realZernikeCartesian():
        _rhs = realZernike().rhs.subs(rho,sp.sqrt(x0**2+y0**2)/aa).subs(theta,sp.atan2(x0,y0))
        _lhs = ZnmCart
        return sp.Eq(_lhs, _rhs)


    def realZernikeNormalized():
        _rhs = cCoeff().rhs * realZernike().rhs
        _lhs = Znm
        return sp.Eq(_lhs, _rhs)

    # Complex Zernike Polynomials

    def complexZernike():
        _rhs = sp.sqrt(2) * radialFunc().rhs * complexTangetialFunc().rhs / 2
        _lhs = Ynm
        return sp.Eq(_lhs, _rhs)


    def complexZernikeNormalized():
        _rhs = sp.sqrt(n + 1) * radialFunc().rhs * complexTangetialFunc().rhs
        _lhs = Ynm
        return sp.Eq(_lhs, _rhs)

    # with this wiegths and this transformation scheme, (realZernike,
    # complexZernike) and (realZernikeNormalized, complexZernikeNormalized)
    # are coerent


#    def realZFromComplexZ(zcf, nn, mm):
#        zc1 = zcf(n, m).subs({m: mm, n: nn})
#        zc2 = zcf(n, m).subs({m: -mm, n: nn})
#        if mm >= 0:
#            _rhs = (zc1 + zc2) / np.sqrt(2)
#        elif mm < 0:
#            _rhs = 1j * (zc1 - zc2) / np.sqrt(2)    
#        _lhs = Znm
#        return sp.Eq(_lhs, _rhs)


    def _vlj():
        p = (n - m) / 2
        q = (n + m) / 2
        _rhs = (-1)**p * (m + l + j * 2) * sp.binomial(m + j + l - 1,
                                                       l - 1) * sp.binomial(j + l - 1,
                                                                            l - 1) * sp.binomial(l - 1,
                                                                                                 p - j) / sp.binomial(q + l + j,
                                                                                                                      l)
        _lhs = vlj
        return sp.Eq(_lhs, _rhs)


    def Vnm():
        ma = sp.Abs(m)
        p = (n - ma) / 2
        q = (n + ma) / 2
        _rhs = sp.exp(sp.I * f) * sp.Sum((-2 * sp.I * f)**(l - 1) * sp.Sum((-1)**p * (ma + l + j * 2) * sp.binomial(ma + j + l - 1,
                                                                                                              l - 1) * sp.binomial(j + l - 1,
                                                                                                                                   l - 1) * sp.binomial(l - 1,
                                                                                                                                                        p - j) / sp.binomial(q + l + j,
                                                                                                                                                                             l) * (sp.besselj(ma + l + j * 2,
                                                                                                                                                                                              2 * sp.pi * r) / (l * (2 * sp.pi * r)**l)),
                                                                     (j,
                                                                      0,
                                                                      p)),
                                      (l,
                                       1,
                                       max_order))
        _lhs = VnmFunc
        return sp.Eq(_lhs, _rhs)


    def diffractedZernikeAtFocus():
        #    return ((-1)**((n+m)/2) * sp.besselj( n+1, 2*sp.pi*r) / (2*sp.pi*r) ) * tangetialFunc(m)
        # return 2*sp.pi*(-1**(n+1)) * ( sp.besselj( n+1, 2*sp.pi*r) / (2*sp.pi*r)
        # ) * sp.Piecewise( (-sp.sin(m*theta), m<0), (sp.cos(m*theta), m>=0) )
        _rhs = 2 * sp.pi * (sp.besselj(n + 1, 2 * sp.pi * r) / (2 * sp.pi * r)) * \
            sp.Piecewise((-sp.sin(m * theta), m < 0), (sp.cos(m * theta), m >= 0))
        _lhs = ZnmD
        return sp.Eq(_lhs, _rhs)


    def diffractedComplexZernikeAtFocus():
        # return 2*sp.pi* (-1**(n+1)) * ( sp.besselj( n+1, 2*sp.pi*r) /
        # (2*sp.pi*r) ) * complexTangetialFunc(m) / sp.sqrt(2)
        _rhs = 2 * sp.pi * (sp.besselj(n + 1, 2 * sp.pi * r) /
                            (2 * sp.pi * r)) * complexTangetialFunc().rhs / sp.sqrt(2)
        _lhs = YnmD
        return sp.Eq(_lhs, _rhs)


    def diffractedZernike():
        _rhs = 2 * Vnm().rhs * tangetialFunc().rhs
        _lhs = ZnmD
        return sp.Eq(_lhs, _rhs)


    def diffractedComplexZernike():
        _rhs = 2 * Vnm().rhs * complexTangetialFunc().rhs / sp.sqrt(2)
        _lhs = YnmD
        return sp.Eq(_lhs, _rhs)


    def checkOrthoPair():
        f2c = sp.conjugate(f2)
        _rhs = sp.Integral(f1 * f2 * rho, (rho, 0, 1), (theta, 0, 2 * sp.pi))
        _lhs = dotInt
        return sp.Eq(_lhs, _rhs)

    
    def circleDotProduct():
        f2c = sp.conjugate(f2)
        itR = sp.re(f1 * f2c * rho) / sp.S.Pi
        itI = sp.im(f1 * f2c * rho) / sp.S.Pi
        i1 = sp.N(sp.integrate(itR, (theta, 0, 2 * sp.pi), (rho, 0, 1)))
        i2 = sp.N(sp.integrate(itI, (theta, 0, 2 * sp.pi), (rho, 0, 1)))
        _rhs = i1 + sp.I * i2
        _lhs = dotInt
        return sp.Eq(_lhs, _rhs)

    _zernikeFormulas = Formulary("Zernike",                                                                          
                                   ['cCoeff',
                                    'tangetialFunc',
                                    'complexTangetialFunc',
                                    'radialFunc',
                                    'realZernike',
                                    'realZernikeCartesian',
                                    'realZernikeNormalized',
                                    'complexZernike',
                                    'complexZernikeNormalized',
                                    #'realZFromComplexZ',
                                    '_vlj',
                                    'Vnm',
                                    'diffractedZernikeAtFocus',
                                    'diffractedComplexZernikeAtFocus',   
                                    'diffractedZernike',
                                    'diffractedComplexZernike',
                                    'checkOrthoPair',
                                    #'checkZernikeOrthoPair',
                                    'circleDotProduct',
#                                    'zernikeAnalysysReal',
#                                    'zernikeSynthesysReal',
#                                    'zernikeAnalysysComplex',
#                                    'zernikeSynthesysComplex',
                                    #'capital_v_vector',
#                                    'createZernikeFormulary'
                                   ],
                                  [  cCoeff(),
                                     tangetialFunc(),
                                     complexTangetialFunc(),
                                     radialFunc(),
                                     realZernike(),
                                     realZernikeCartesian(),
                                     realZernikeNormalized(),
                                     complexZernike(),
                                     complexZernikeNormalized(),
                                     #realZFromComplexZ(),
                                     _vlj(),
                                     Vnm(),
                                     diffractedZernikeAtFocus(),
                                     diffractedComplexZernikeAtFocus(),
                                     diffractedZernike(),
                                     diffractedComplexZernike(),
                                     checkOrthoPair(),
                                     #checkZernikeOrthoPair(),
                                     circleDotProduct(),
#                                     zernikeAnalysysReal(),
#                                     zernikeSynthesysReal(),
#                                     zernikeAnalysysComplex(),
#                                     zernikeSynthesysComplex(),
                                     #capital_v_vector(),
#                                     createZernikeFormularyOld()
                                  ])

    return _zernikeFormulas


def cov_expr_jk(expr, jj_value, kk_value):
    nj_value, mj_value = noll_to_zern(jj_value)
    nk_value, mk_value = noll_to_zern(kk_value)
    rexpr = subsParamsByName(expr, {'j': jj_value, 'k': kk_value, 'n_j': nj_value, 'm_j': abs(mj_value), 'n_k': nk_value, 'm_k': abs(mk_value)})
    return rexpr


def getZernikeDomain(nn):
    x1 = np.linspace(-1.0, 1.0, nn)
    y1 = np.linspace(-1.0, 1.0, nn)
    X1, Y1 = np.meshgrid(x1, y1)
    rr = np.sqrt(X1**2 + Y1**2)
    rr[np.where(rr > 1.0)] = np.nan
    return rr, np.arctan2(Y1, X1)
    

def evaluateZernike(zerninke_mode_expression, sampling_points):
    zerninke_mode_lambda = sp.lambdify(
        [rho, theta], zerninke_mode_expression, 'numpy')
#    r1 = 1.0 - np.geomspace(1.0/sampling_points, 1.0, sampling_points, endpoint=True)
    r1 = np.power(np.linspace(0.0, 1.0, sampling_points), 1.0 / 2.0)
    theta1 = np.linspace(0, 2 * np.pi, sampling_points)
    r1, theta1 = np.meshgrid(r1, theta1)
    X1 = r1 * np.sin(theta1)
    Y1 = r1 * np.cos(theta1)
    Z1 = np.asarray(zerninke_mode_lambda(r1, theta1))
    return X1, Y1, Z1

'''
    def checkZernikeOrthoPair(n1, m1, n2, m2):
        f1 = realZernikeNormalized(n1, m1)
        f2 = realZernikeNormalized(n2, m2)
        _rhs = checkOrthoPair(f1, f2)
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)

    # inputFunction defined over the unit disc, in ro, theta
    def zernikeAnalysysReal(inputFunction, max_noll):
        result = [0] * max_noll
        for ni in range(max_noll):
            nn, mm = noll_to_zern(ni + 1)
            z_ni = realZernikeNormalized(n, m).subs({m: int(mm), n: int(nn)})
            result[ni] = circleDotProduct(inputFunction, z_ni).rhs
            print(ni + 1, nn, mm, result[ni] / emValue(mm))
        _rhs = result
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)

    def zernikeSynthesysReal(decomposition):
        result = sp.S(0)
        for ni, coefficient in enumerate(decomposition):
            nn, mm = noll_to_zern(ni + 1)
            z_ni = realZernikeNormalized(n, m).subs({m: int(mm), n: int(nn)})
            result += coefficient * z_ni
            print(ni + 1, nn, mm, coefficient)
        _rhs = result
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)


    def zernikeAnalysysComplex(inputFunction, max_noll):
        result = [0] * max_noll
        for ni in range(max_noll):
            nn, mm = noll_to_zern(ni + 1)
            z_ni = complexZernikeNormalized(n, m).subs({m: mm, n: nn})
            result[ni] = circleDotProduct(inputFunction, z_ni)
            print(ni + 1, nn, mm, result[ni])
        _rhs = result
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)


    def zernikeSynthesysComplex(decomposition):
        result = sp.S(0)
        for ni, coefficient in enumerate(decomposition):
            nn, mm = noll_to_zern(ni + 1)
            z_ni = complexZernikeNormalized(n, m).subs({m: mm, n: nn})
            result += coefficient * z_ni
            print(ni + 1, nn, -mm, coefficient)
        _rhs = result
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)


    def capital_v_vector(max_noll, f):
        result = [0] * max_noll
        for ni in range(max_noll):
            nn, mm = noll_to_zern(ni + 1)
            z_ni = CVVZernike(nn, mm, rho, theta)
            result[ni] = z_ni
        _rhs = result
        _lhs = Cnm
        return sp.Eq(_lhs, _rhs)
        
        
    def createZernikeFormularyOld(lastMode):
        zf = Formulary()
        for i in range(2, lastMode + 1):
            idx = noll_to_zern(i)
            idstr = str(idx[0]) + str(idx[1])
            zzz = sp.symbols('Z_' + idstr)
            az = realZernike(n, m).subs({m: int(idx[1]), n: int(idx[0])})
            zname = 'Z' + idstr
            zf.addFormula(zname, (zzz, az, sp.Eq(zzz, az)))
        return zf
'''

