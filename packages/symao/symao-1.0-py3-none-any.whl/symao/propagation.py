from seeing.sympyHelpers import *
from seeing.formulary import *
from seeing.integrator import *


def createPropagationFormulary(
        cartesian=False,
        infinite_domain=False,
        circleLimits=True):

    approximations = [
    "Rayleigh-Sommerfeld",
    "Approximate Rayleigh-Sommerfeld",
    "Near Fresnel",
    "Far Fresnel",
    "Fraunhofer"]

    x0, y0, x1, y1, theta0, theta1 = sp.symbols('x_0, y_0 x_1, y_1 theta_0 theta_1', real=True)
    k, ll, a, z1, focal, rho, r1, r0, u, FN = sp.symbols('k lambda a z_1 f rho r_1 r_0 u FN', real=True, positive=True)
    ez0, ez0r = sp.symbols('E_0 E_0r')
    ez1 = sp.Function('E_1')(x1, y1, z1)
    ez1r = sp.Function('E_1r')(r1, theta1, z1)

    k = 2 * sp.S.Pi / ll
    
    def xyCircle():
        rrr = sp.S(1) - (x0 / sp.S(a))**sp.S(2) - (y0 / sp.S(a))**sp.S(2)
        return (rrr / sp.Abs(rrr) + 1) / 2


    def xyLens():
        ffn = FN * a * 2
        kl = sp.S(2) * sp.pi / ll
        rr1 = x0**sp.S(2) + y0**sp.S(2)
        return sp.exp(- sp.I * (kl * rr1 / (2 * ffn)))


    def rLens():
        ffn = FN * a * 2
        kl = sp.S(2) * sp.pi / sp.S(ll)
        return sp.exp(-sp.I * (kl / (2 * ffn)) * (r0**2))


    def getPropagationMethod(
            approximation="Rayleigh-Sommerfeld",
            infinite_domain=False,
            cartesian=False,
            circleLimits=True):

        _cartesian_circle_limits = (x0, -a, a), (y0, -sp.sqrt(sp.Abs(a * a - x0 * x0)), sp.sqrt(sp.Abs(a * a - x0 * x0)))
        _cartesian_limits = (x0, -a, a), (y0, -a, a)
        _radial_limits = (theta0, 0, sp.S(2) * sp.S.Pi), (r0, 0, a)
        _cartesian_limits_inf = (x0, -sp.oo, sp.oo), (y0, -sp.oo, sp.oo)
        _radial_limits_inf = [(r0, 0, sp.oo)]

        if not cartesian:
            if infinite_domain:
                _limits = _radial_limits_inf
            else:
                _limits = _radial_limits
        else:
            if infinite_domain:
                _limits = _cartesian_limits_inf
            else:
                if circleLimits:
                    _limits = _cartesian_circle_limits
                else:
                    _limits = _cartesian_limits

        iexpr23 = (k * z1 / (sp.I * 2 * sp.S.Pi)) * (sp.exp(sp.I * k * rho) / (rho**2))
        iexpr01 = iexpr23 * (1 - 1 / (sp.I * k * rho))

        common_fresnel_term0 = (sp.exp(sp.I * k * z1) / (z1))
        common_fresnel_term1 = (k / (2 * sp.S.Pi * sp.I))

#       common_fresnel_term = ( k * sp.exp(sp.I*k*z1)/(sp.I*2*sp.S.Pi*z1) )
        common_fresnel_term = common_fresnel_term0 * common_fresnel_term1

        iexpr4 = (common_fresnel_term) * sp.exp(sp.I * k * (r1**2) / (2 * z1)) * \
            sp.exp(sp.I * k * (r0**2) / (2 * z1)) * sp.besselj(0, k * r0 * r1 / z1)
        iexpr5 = common_fresnel_term * \
            sp.exp(sp.I * k * ((x1 - x0)**2 + (y1 - y0)**2) / (2 * z1))
        iexpr6 = common_fresnel_term * \
            sp.besselj(0, k * r0 * r1 / z1) * sp.exp(sp.I * k * (r0**2) / (2 * z1))
        iexpr7 = common_fresnel_term * \
            sp.exp(sp.I * k * (x0 * x1 + y0 * y1) / z1) * sp.exp(sp.I * k * (x0**2 + y0**2) / (2 * z1))
        iexpr8 = sp.exp(-sp.I * k * r0 * r1 * sp.sin(theta1 - theta0 + sp.S.Pi / 2) / z1) * k
        iexpr9 = sp.exp(-sp.I * k * (x0 * x1 + y0 * y1) / z1) * k * 2 * sp.S.Pi

        if approximation == "Rayleigh-Sommerfeld":
            if not cartesian:
                _integrand = iexpr01.subs(rho, sp.sqrt(
                    (x1 - x0)**2 + (y1 - y0)**2 + z1**2))
                dsub = {
                    x1: r1 * sp.cos(theta1),
                    x0: r0 * sp.cos(theta0),
                    y0: r0 * sp.sin(theta0),
                    y1: r1 * sp.sin(theta1)}
                _integrand = _integrand.subs(dsub)
            else:
                _integrand = iexpr01.subs(rho, sp.sqrt(
                    (x1 - x0)**2 + (y1 - y0)**2 + z1**2))
        elif approximation == "Approximate Rayleigh-Sommerfeld":
            if not cartesian:
                _integrand = iexpr23.subs(rho, sp.sqrt(
                    (x1 - x0)**2 + (y1 - y0)**2 + z1**2))
                dsub = {
                    x1: r1 * sp.cos(theta1),
                    x0: r0 * sp.cos(theta0),
                    y0: r0 * sp.sin(theta0),
                    y1: r1 * sp.sin(theta1)}
                _integrand = _integrand.subs(dsub)
            else:
                _integrand = iexpr23.subs(rho, sp.sqrt(
                    (x1 - x0)**2 + (y1 - y0)**2 + z1**2))
        elif approximation == "Near Fresnel":
            if not cartesian:
                _integrand = iexpr4
            else:
                _integrand = iexpr5
        elif approximation == "Far Fresnel":
            if not cartesian:
                _integrand = iexpr6
            else:
                _integrand = iexpr7
        elif approximation == "Fraunhofer":
            if not cartesian:
                _integrand = iexpr8
            else:
                _integrand = iexpr9

        if not cartesian:
            _integrand = 2 * sp.S.Pi * r0 * ez0r * _integrand
        else:
            _integrand *= ez0

        _name = approximation + "Integral"
        if cartesian:
            _name += ', ' + "cartesian coords"
        else:
            _name += ', ' + "cilyndrical coords"
        if infinite_domain:
            _name += ', ' + "infinite domain"
        else:
            _name += ', ' + "finite domain"

        return (_name, _integrand, _limits)
    
    
    prop_f = Formulary()
    for appr in approximations:
        _name, _integrand, _limits = getPropagationMethod(
            appr, infinite_domain, cartesian, circleLimits)
        _integral = sp.Integral(_integrand, *_limits)
        if cartesian:
            prop_f.addFormula(appr, sp.Eq(ez1, _integral))
            prop_f.addFormula(appr+" Arg", _integral.function)
        else:
            prop_f.addFormula(appr, sp.Eq(ez1r, _integral))

    if cartesian:
        prop_f.addFormula('xyCircle', xyCircle() )
        prop_f.addFormula('xyLens', xyLens() )
    else:
        prop_f.addFormula('rLens', rLens() )
    
    return prop_f


'''
class propagationStep(object):
    def __init__(method, lll, aa, subdiv_points):
        self.lll = lll
        #lll = 500e-9
        self.aa = aa
        self.subdiv_points = subdiv_points
        #aa =  0.05
        #FN = 30
        #dd = 2*aa
        #focal_dist = dd*FN
        self.method = method

    def setsp.Input(Ez0):
        self.Ez0 = Ez0

    def propagate(distance, outputRadius):
        subdiv_points = self.subdiv_points
        paramAndRange2 = [('x1', -outputRadius, outputRadius, subdiv_points, 'linear'), ('y1', -outputRadius, outputRadius, subdiv_points, 'linear')]
        # dictionary for Fraunhofer method, at the focal plane of a lens
        subsDictC = {ez0: self.Ez0, ll: self.lll, a:self.aa}
        ff = propMethodsCartesian
        sDict = subsDictC
        pr = paramAndRange2
        (lh, rh, eeq) = ff.getFormula(self.method)
        sDict[z1] = distance
        rh = rh.subs(sDict)
        fplot1 = msp.It.sp.IntegralEval(lh, rh, pr, [(subdiv_points, 'linear'), (subdiv_points, 'linear')])
        return fplot1
'''
