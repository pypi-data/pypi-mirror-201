import itertools

from sympy import (Expr, Add, Mul, S, Integral, Eq, Sum, Symbol,
                    expand as _expand, Not)
from sympy.core.compatibility import default_sort_key
from sympy.core.parameters import global_parameters
from sympy.core.sympify import _sympify
from sympy.core.relational import Equal, Unequal
from sympy.logic.boolalg import BooleanFunction, And
from sympy.stats import variance, covariance, rv
from sympy.stats.rv import (RandomSymbol, pspace, dependent,
                            given, sampling_E, RandomIndexedSymbol, is_random,
                            PSpace, sampling_P)
from sympy.concrete.expr_with_limits import ExprWithLimits
from sympy.core.cache import cacheit
from sympy.core.expr import AtomicExpr
from sympy.core.containers import Tuple
from _collections import defaultdict
import std

__all__ = ['Probability', 'Expectation', 'Variance', 'Covariance']


@is_random.register(Expr)
def _(x):
    atoms = x.free_symbols
    if len(atoms) == 1 and x in atoms:
        return False
    return any([is_random(i) for i in atoms])


@is_random.register(RandomSymbol)  # type: ignore
def _(x):
    return True


class Distributed(BooleanFunction):
    """
    Asserts that x is a random expression/symbol of the distribution S
    """

    def subs(self, *args, **kwargs):
        if len(args) == 1:
            eq, *_ = args
            if eq.is_Equal:
                args = eq.args
                return self.func(self.lhs._subs(*args, **kwargs).simplify(), self.rhs._subs(*args, **kwargs).simplify(), equivalent=[self, eq]).simplify()
            if isinstance(eq, dict):
                return self
            if eq.is_Quantifier:
                return self.bfn(self.subs, eq)
        return BooleanFunction.subs(self, *args, **kwargs)

    def _latex(self, p):
        return r"%s \sim %s" % tuple(p._print(a) for a in self.args)

    def _sympystr(self, p):
        return r"%s ~ %s" % tuple(p._print(a) for a in self.args)

    @classmethod
    def eval(cls, x, s):
        if not s.is_distribution:
            raise TypeError('expecting Set, not %s' % s)

        ret = s.contains(x)
        if not isinstance(ret, Distributed) and (ret in (S.true, S.false) or ret.is_set):
            return ret

    @property
    def lhs(self):
        """The left-hand side of the relation."""
        return self._args[0]

    @property
    def rhs(self):
        """The right-hand side of the relation."""
        return self._args[1]

    def simplify(self, *_, **__):
        return self

    
class Conditioned(Expr):
    """
    Symbolic expression for the conditional randomal variables.
    """
    is_random = True
    
    lhs = property(lambda self: self.args[0])
    rhs = property(lambda self: self.args[1])
    
    @cacheit
    def _eval_domain_defined(self, x, **_):        
        return self.lhs.domain_defined(x) & self.rhs.domain_defined(x)            

    def simplify_condition_on_random_variable(self):
        condition = self.lhs.simplify_condition_on_random_variable()
        if condition is self.lhs:
            return self
        return self.func(condition, self.rhs)
    
    def __bool__(self):
        if self.is_bool:
            return False
        return True

    def __new__(cls, prob, given, evaluate=True):
        if prob.is_BooleanAtom:
            return prob

        assert prob.is_random, prob
        assert given.is_random, given
        
        prob = _sympify(prob)
        given = _sympify(given)
        if prob.is_Conditioned:
            return Expr.__new__(cls, prob.lhs, prob.rhs & given)
        if prob.is_And:
            if given.is_And:
                if given._argset & prob._argset:
                    prob = prob.func(*prob._argset - given._argset)
            else:
                if given in prob._argset:
                    prob = prob.func(*prob._argset - {given})
                elif given.is_Equal:
                    lhs, rhs = given.args
                    if rhs.is_Surrogate:
                        _given = Equal(lhs, rhs.arg.var, evaluate=False)
                        if _given in prob._argset:
                            prob = prob.func(*prob._argset - {_given})
                        
        return Expr.__new__(cls, prob, given)

    def doit(self, **hints):
        return given(self.lhs, self.rhs)

    @property
    def dtype(self):        
        return self.lhs.dtype
    
    @cacheit
    def _eval_shape(self):
        return self.lhs.shape
    
    def _latex(self, p):
        # return r"%s \middle \vert %s" % (p._print(self.lhs), p._print(self.rhs))
        return r"%s \mathrel{\bigg|} %s" % (p._print(self.lhs), p._print(self.rhs))

    def _eval_is_real(self):
        return self.lhs.is_real
    
    def _eval_is_complex(self):
        return self.lhs.is_complex

    def _eval_is_integer(self):
        return self.lhs.is_integer

    def _eval_is_finite(self):
        return self.lhs.is_finite

    def _eval_is_extended_negative(self):
        return self.lhs.is_extended_negative

    def _eval_is_extended_positive(self):
        return self.lhs.is_extended_positive

    @property
    def is_bool(self):
        return self.lhs.is_bool

    def domain_definition(self):
        return Unequal(Probability(self.rhs), 0)
        
    def invert(self):
        return self.func(self.lhs.invert(), self.rhs)
        
    def as_boolean(self):
        if not self.is_bool:
            return self.func(self.lhs.as_boolean(), self.rhs)

    def yield_random_symbols(self):
        yield from self.lhs.yield_random_symbols()

    def simplify(self, deep=False):
        lhs, rhs = self.args
        if lhs.is_And:
            _argset = lhs._argset
            if rhs in _argset:
                lhs = And(*{*_argset} - {rhs})
                return self.func(lhs, rhs, evaluate=False)
            
            elif rhs.is_Equal:
                x, x_var = rhs.args
                if x_var.is_Surrogate:
                    rhs = Equal(x, x_var.arg.var, evaluate=False)
                    if rhs in _argset:
                        lhs = And(*{*_argset} - {rhs})
                        return self.func(lhs, rhs, evaluate=False)
                    
        return Expr.simplify(self, deep)

    def _try_to_substitute(self, other, new):
        if not other.is_Conditioned:
            return
        
        if self.lhs != other.lhs:
            return
        
        rhs = self.rhs
        _rhs = other.rhs
        if rhs.is_And and _rhs.is_And:
            rhs = rhs.args
            _rhs = _rhs.args
            if len(rhs) == len(_rhs):
                conds = []
                for eq, _eq in zip(rhs, _rhs):
                    if new := eq._try_to_substitute(_eq, new):
                        ...
                    else:
                        return

                return new
            
        elif rhs.is_Equal and _rhs.is_Equal:
            if new := rhs._try_to_substitute(_rhs, new):
                return new
    
    def _subs(self, old, new, **hints):
        if _new := self._try_to_substitute(old, new):
            return _new
        
        return Expr._subs(self, old, new)

    def __iter__(self):
        raise TypeError
    
    def __getitem__(self, indices, **kw_args):
        lhs, rhs = self.args
        return self.func(lhs[indices], rhs, evaluate=False)


class Surrogate(AtomicExpr):
    is_symbol = True
    is_comparable = False
    
    def __new__(cls, symbol):
        obj = Expr.__new__(cls, symbol)
        return obj
    
    @property
    def var(self):
        return self.arg.var
    
    @property
    def dtype(self):
        return self.arg.dtype
    
    @cacheit
    def _eval_shape(self):
        return self.arg.shape
    
    def __contains__(self, other):
        return other in self.symbol
    
# precondition, self and other are structurally equal!
    def _dummy_eq(self, other):
        return self.arg == other

    def structurally_equal(self, other):
        return self.arg.structurally_equal(other)

    def __iter__(self):
        raise TypeError
      
    def __getitem__(self, indices):
        return Surrogate(self.arg.__getitem__(indices))
    
    def _sympystr(self, p): 
        return self.arg._sympystr(p)
    
    def _latex(self, p):
        return self.arg._latex(p, color='magenta')
    
    def _eval_is_extended_positive(self):
        return self.arg._eval_is_extended_positive()
    
    def _eval_is_extended_negative(self):
        return self.arg._eval_is_extended_negative()
    
    def _eval_is_nonzero(self):
        return self.arg._eval_is_nonzero()
    
    def _eval_is_zero(self):
        return self.arg._eval_is_zero()
    
    def _eval_is_finite(self):
        return self.arg._eval_is_finite()
    
    def _eval_is_extended_integer(self):
        return self.arg._eval_is_extended_integer()
    
    def _eval_is_super_integer(self):
        return self.arg._eval_is_super_integer()
    
    def _eval_is_extended_rational(self):
        return self.arg._eval_is_extended_rational()
    
    def _eval_is_hyper_rational(self):
        return self.arg._eval_is_hyper_rational()
    
    def _eval_is_super_rational(self):
        return self.arg._eval_is_super_rational()
    
    def _eval_is_extended_real(self):
        return self.arg._eval_is_extended_real()
    
    def _eval_is_hyper_real(self):
        return self.arg._eval_is_hyper_real()
    
    def _eval_is_super_real(self):
        return self.arg._eval_is_super_real()
    
    def _eval_is_extended_complex(self):
        return self.arg._eval_is_extended_complex()
    
    def _eval_is_hyper_complex(self):
        return self.arg._eval_is_hyper_complex()
    
    def _eval_is_algebraic(self):
        return self.arg._eval_is_algebraic()
    
    def _eval_is_hermitian(self):
        return self.arg._eval_is_hermitian()
    
    def _eval_is_imaginary(self):
        return self.arg._eval_is_imaginary()
    
    def _eval_is_random(self):
        return self.arg.is_random
    
    @property
    def distribution(self):
        return self.arg.distribution

    def as_boolean(self):
        from sympy import Equal
        return Equal(self.arg, self, evaluate=False)

    def __and__(self, other):
        """Overloading for & operator"""
        if other.is_random:
            if not other.is_bool:
                other = other.as_boolean()
            return self.as_boolean() & other 

        return super(Surrogate, self).__and__(other)

    def copy(self, **kwargs):
        return self.arg.copy(**kwargs)


# when X is a discrete random variable, define P(X) = P(X=x), which is necessarily nomore than 1, Sum[X](P(X)) = 1
# when X is a continuous random variable, define P(X) = P(X=x) = PDF(X)(x) which is possibly greater than 1, Integral[X](P(X)) = 1
class Probability(Expr):
    """
    Symbolic expression for the probability.

    Examples
    ========

    >>> from sympy.stats import Probability, Normal
    >>> from sympy import Integral
    >>> X = Normal("X", 0, 1)
    >>> prob = Probability(X > 1)
    >>> prob
    Probability(X > 1)

    Integral representation:

    >>> prob.rewrite(Integral)
    Integral(sqrt(2)*exp(-_z**2/2)/(2*sqrt(pi)), (_z, 1, oo))

    Evaluation of the integral:

    >>> prob.evaluate_integral()
    sqrt(2)*(-sqrt(2)*sqrt(pi)*erf(sqrt(2)/2) + sqrt(2)*sqrt(pi))/(4*sqrt(pi))
    """
    is_extended_negative = False
    is_extended_real = True
    is_finite = True
    
    @cacheit
    def _eval_domain_defined(self, x, **_):        
        return self.arg.domain_defined(x)            

    def marginalize(self, given, *rest):
        assert given.is_symbol and given.is_random
        prob = self.func.marginalize_condition(self.arg, given)
        if rest:
            prob = prob.marginalize(*rest)
            
        return prob
                
    @classmethod    
    def marginalize_condition(cls, condition, given):        
        if condition.is_And:
            expr = []
            hit = False
            for eq in condition.args:
                if eq.is_Equal:
                    lhs, rhs = eq.args
                    if lhs.is_symbol and pspace(lhs).symbol == rhs:
                        if lhs._has(given):
                            if lhs == given:
                                hit = True
                                continue
                            
                            if given.is_Indexed:               
                                start = given.indices[0]
                                stop = start + 1
                            elif given.is_Sliced:
                                start, stop = given.index
                            else:
                                expr.append(eq)
                                continue                                                       
                                                                                                  
                            lhs = lhs.split(slice(start, stop))
                            if not lhs.is_BlockMatrix:
                                hit = True
                            else:
                                rhs = rhs.split(slice(start, stop))                                
                                for lhs, rhs in zip(lhs.args, rhs.args):
                                    eq = Equal(lhs, rhs)
                                    if lhs == given:
                                        hit = True
                                    else:
                                        expr.append(eq)
                            continue
                expr.append(eq)
            if hit:
                return cls(And(*expr))
        elif condition.is_Conditioned:
            self = cls(condition.lhs).marginalize(given)
            return self.func(self.arg, given=condition.rhs)
        elif condition.is_Equal:
            if given.is_Sliced:
                start, stop = given.index
                lhs, rhs = condition.lhs.split(slice(start, stop)), condition.rhs.split(slice(start, stop))
                assert lhs.is_BlockMatrix and rhs.is_BlockMatrix                
                condition = And(*(condition.func(l, r) for l, r in zip(lhs.args, rhs.args)))
            elif given.is_Indexed:                
                condition = condition.split([slice(*index) for index in given.indices])
            if condition.is_And:
                return cls.marginalize_condition(condition, given)
            
    @property
    def dtype(self):
        from sympy.core.symbol import dtype
        return dtype.real
    
    def __new__(cls, *prob, given=None, evaluate=False): 
        booleans = []
        limits = []
        for arg in prob:
            if isinstance(arg, (tuple, Tuple)):
                limits.append(Tuple(*arg))
                continue
            
            if arg.is_BooleanTrue:
                continue
            
            if arg.is_BooleanFalse:
                return S.Zero
            
            assert arg.is_random
            if arg.is_symbol:
                booleans.append(Equal(arg, pspace(arg).symbol))
            elif arg.is_Conditioned:
                lhs, rhs = arg.args
                if lhs.is_symbol:
                    if lhs.is_Surrogate:
                        booleans.append(arg.func(Equal(lhs.arg, lhs), rhs))
                    else:
                        booleans.append(arg.func(Equal(lhs, pspace(lhs).symbol), rhs))
                else:
                    booleans.append(arg)
            else:
                assert arg.is_Boolean, type(arg)
                booleans.append(arg)

        if not booleans:
            return S.One

        expr = And(*booleans)
        if given is not None:
            expr = rv.given(expr, given)

        vars = [v for v in expr.random_symbols if not v.is_Surrogate]
        std.deleteIndices(limits, lambda limits, i : cls.is_redundant(limits, i, vars))

        return Expr.__new__(cls, expr, *limits)

    @classmethod
    def is_redundant(cls, limits, i, vars):
        limit = limits[i]
        if len(limit) > 1:
            x, w = limit
            if x.has(*vars):
                if x.is_Indexed or x.is_Sliced:
                    if not any(i.is_random for i in x.indices):
                        limits[i] = Tuple(x.base, w)
            else:
                return True
        
    def doit(self, **hints):
        condition = self.args[0]
        given_condition = None
        numsamples = hints.get('numsamples', False)
        for_rewrite = not hints.get('for_rewrite', False)

        if isinstance(condition, Not):
            return S.One - self.func(condition.args[0], given_condition, evaluate=for_rewrite).doit(**hints)

        if condition.has(RandomIndexedSymbol):
            return pspace(condition).probability(condition, given_condition, evaluate=for_rewrite)

        if isinstance(given_condition, RandomSymbol):
            condrv = condition.random_symbols
            if len(condrv) == 1 and condrv[0] == given_condition:
                from sympy.stats.frv_types import BernoulliDistribution
                return BernoulliDistribution(self.func(condition).doit(**hints), 0, 1)
            if any([dependent(rv, given_condition) for rv in condrv]):
                return Probability(condition, given_condition)
            else:
                return Probability(condition).doit()

        if given_condition is not None and not given_condition.is_Relational:
            raise ValueError("%s is not a relational or combination of relationals" % (given_condition))

        if given_condition == False or condition is S.false:
            return S.Zero
        
        if not condition.is_Relational:
            return self
        
        if condition is S.true:
            return S.One

        if numsamples:
            return sampling_P(condition, given_condition, numsamples=numsamples)
        if given_condition is not None:  # If there is a condition
            # Recompute on new conditional expr
            return Probability(given(condition, given_condition)).doit()

        # Otherwise pass work off to the ProbabilitySpace
        ps = pspace(condition)
        if ps  == PSpace():
            return Probability(condition, given_condition)

        try:
            return ps.probability(condition).simplify()
        except:
            return self

    def _eval_rewrite_as_Integral(self, arg, condition=None, **kwargs):
        return self.func(arg, condition=condition).doit(for_rewrite=True)

    _eval_rewrite_as_Sum = _eval_rewrite_as_Integral

    def evaluate_integral(self):
        return self.rewrite(Integral).doit()

    def normalize_limits(self, limits):
        for i, limit in enumerate(limits):
            if len(limit) > 1:
                limits[i] = (limit[-1],)
        return limits

    @cacheit
    def _eval_is_pdf(self):
        expr = self.arg
        random_symbols = {v for v in expr.random_symbols if not v.is_Surrogate}

        if expr.is_Conditioned:
            expr = expr.lhs

        conds = expr.args if expr.is_And else [expr]
        if all(cond.is_Equal for cond in conds): 
            for cond in conds:
                lhs = cond.args[0]
                if lhs in random_symbols and not lhs.is_integer and lhs.is_symbol:
                    return True
        
    @property
    def is_pdf(self):
        return self._eval_is_pdf()

    def _latex(self, p):
        expr, *limits = self.args
        symbol_P = 'p' if self.is_pdf else 'P'
        if limits:
            limits = self.normalize_limits(limits)
            return r'\mathbb{%s}_{%s}\left(%s\right)' % (
                symbol_P,
                ','.join([p._print(s) for s, *_ in limits]), 
                p._print(expr))
        else:
            return r'\mathbb{%s}\left(%s\right)' % (symbol_P, p._print(expr))

    def _sympystr(self, p):
        expr, *limits = self.args
        if limits:
            limits = self.normalize_limits(limits)
            return 'P[%s](%s)' % (','.join([p._print(s) for s, *_ in limits]), p._print(expr))
        else:
            return 'P(%s)' % p._print(expr)

    def domain_definition(self):        
        return self.arg.domain_definition()
    
    def _subs(self, old, new, **hints):
        if old.is_Conditioned and not old.lhs.is_bool or new.is_Conditioned and not new.lhs.is_bool:
            old = old.as_boolean()
            new = new.as_boolean()
            
        else:
            random_symbols = self.args[0].random_symbols
            if old in random_symbols:
                if not old.is_Surrogate:
                    old = old.surrogate
                    if old in random_symbols:
                        if new.is_random:
                            new = new.surrogate
                    else:
                        return self

        return Expr._subs(self, old, new, **hints)

    @classmethod
    def simplify_Equal(cls, self, lhs, rhs):
        """
        precondition: self.lhs is a Probability object!
        """
        if lhs.is_Probability and len(lhs.args) == 1 and rhs.is_Probability and len(rhs.args) == 1:
            lhs = self.lhs.arg.simplify_condition_on_random_variable()
            if lhs is not self.lhs.arg:
                rhs = self.rhs.arg.simplify_condition_on_random_variable()
                if rhs is not self.rhs.arg:
                    return self.func(lhs, rhs)

    def yield_random_symbols(self):
        expr, *limits = self.args
        
        if expr.is_Conditioned:
            lhs, rhs = expr.args
            for v in lhs.yield_random_symbols():
                if v.is_Surrogate:
                    yield v.arg

            for v in rhs.yield_random_symbols():
                if v.is_Surrogate:
                    yield v.arg
        else:
            for v in expr.yield_random_symbols():
                if v.is_Surrogate:
                    yield v.arg

        for x, *ab in limits:
            for w in ab:
                yield from w.yield_random_symbols()

    def _eval_is_random(self):
        for v in self.arg.random_symbols:
            if v.is_Surrogate:
                return True
    

class Expectation(ExprWithLimits):
    """
    Symbolic expression for the expectation.

    Examples
    ========

    >>> from sympy.stats import Expectation, Normal, Probability, Poisson
    >>> from sympy import symbols, Integral, Sum
    >>> mu = symbols("mu")
    >>> sigma = symbols("sigma", positive=True)
    >>> X = Normal("X", mu, sigma)
    >>> Expectation(X)
    Expectation(X)
    >>> Expectation(X).evaluate_integral().simplify()
    mu

    To get the integral expression of the expectation:

    >>> Expectation(X).rewrite(Integral)
    Integral(sqrt(2)*X*exp(-(X - mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (X, -oo, oo))

    The same integral expression, in more abstract terms:

    >>> Expectation(X).rewrite(Probability)
    Integral(x*Probability(Eq(X, x)), (x, -oo, oo))

    To get the Summation expression of the expectation for discrete random variables:

    >>> lamda = symbols('lamda', positive=True)
    >>> Z = Poisson('Z', lamda)
    >>> Expectation(Z).rewrite(Sum)
    Sum(Z*lamda**Z*exp(-lamda)/factorial(Z), (Z, 0, oo))

    This class is aware of some properties of the expectation:

    >>> from sympy.abc import a
    >>> Expectation(a*X)
    Expectation(a*X)
    >>> Y = Normal("Y", 1, 2)
    >>> Expectation(X + Y)
    Expectation(X + Y)

    To expand the ``Expectation`` into its expression, use ``expand()``:

    >>> Expectation(X + Y).expand()
    Expectation(X) + Expectation(Y)
    >>> Expectation(a*X + Y).expand()
    a*Expectation(X) + Expectation(Y)
    >>> Expectation(a*X + Y)
    Expectation(a*X + Y)
    >>> Expectation((X + Y)*(X - Y)).expand()
    Expectation(X**2) - Expectation(Y**2)

    To evaluate the ``Expectation``, use ``doit()``:

    >>> Expectation(X + Y).doit()
    mu + 1
    >>> Expectation(X + Expectation(Y + Expectation(2*X))).doit()
    3*mu + 1

    To prevent evaluating nested ``Expectation``, use ``doit(deep=False)``

    >>> Expectation(X + Expectation(Y)).doit(deep=False)
    mu + Expectation(Expectation(Y))
    >>> Expectation(X + Expectation(Y + Expectation(2*X))).doit(deep=False)
    mu + Expectation(Expectation(Y + Expectation(2*X)))

    """

    def __new__(cls, expr, *limits, **kwargs):
        # only the last limit can be the weight limit
        expr = _sympify(expr)
        if not expr.is_random:
            return expr
        
        weights = []
        
        def deleteIndices(limit):
            nonlocal weights 
            x, *ab = limit
            if not x.is_random:
                weights += [x, *ab]
                return True

        if (ret := std.deleteIndices(limits, deleteIndices)) is not None:
            limits = ret
                
        random_symbols = expr.random_symbols
        if limits:
            varsAltered = defaultdict(set)
            for x, *ab in limits:
                if ab or not x.shape:
                    continue

                for xk in random_symbols:
                    if not xk.is_Indexed:
                        continue
                     
                    if xk.base == x:
                        varsAltered[x].add((xk,))
                    elif x.is_Sliced and x.base == xk.base:
                        if len(x.args) <= len(xk.args):
                            for (start, stop), k in zip(x.indices, xk.indices):
                                if start <= k < stop:
                                    varsAltered[x].add((xk,))
                
            if varsAltered:
                limits = [*limits]
                for x, xks in varsAltered.items():
                    i = std.indexFor(limits, lambda limit: limit[0] == x)
                    std.splice(limits, i, 1, *xks)

        else:
            limits = [(x,) for x in random_symbols]
            
        if weights:
            limits.append(tuple(weights))

        if (given := kwargs.get('given')) is not None:
            if given.is_symbol:
                given = Equal(given, given.var)
            expr = Conditioned(expr, given)

        return ExprWithLimits.__new__(cls, expr, *limits)

    @classmethod
    def unnest(cls, expr, limits, symbols, **assumptions):
        if not limits and symbols:
            return expr.copy(**assumptions)
        return Expr.__new__(cls, expr, *limits, **assumptions)

    def _eval_is_complex(self):
        return True

    def _has_weights(self):
        return not self.args[-1][0].is_random

    @property
    def limits(self):
        return self.args[1:-1] if self._has_weights() else self.args[1:]
    
    @property
    def weights(self):
        return self.args[-1] if self._has_weights() else Tuple()

    @property
    def expr(self):
        return self.args[0]

    @property
    def dtype(self):
        return self.expr.dtype

    @cacheit
    def _eval_shape(self):
        return self.expr.shape

    def expand(self, **hints):
        expr = self.args[0]

        if not is_random(expr):
            return expr

        if isinstance(expr, Add):
            return Add.fromiter(Expectation(a).expand() for a in expr.args)

        expand_expr = _expand(expr)
        if isinstance(expand_expr, Add):
            return Add.fromiter(Expectation(a).expand() for a in expand_expr.args)

        elif isinstance(expr, Mul):
            rv = []
            nonrv = []
            for a in expr.args:
                if is_random(a):
                    rv.append(a)
                else:
                    nonrv.append(a)
            return Mul.fromiter(nonrv) * Expectation(Mul.fromiter(rv))

        return self

    def doit(self, **hints):
        if self.limits:
            function = self.expr
            for limit in self.limits:
                x, distribution = limit                
                _x = x.copy(distribution=distribution)
                expr = function._subs(x, _x)
                if expr.is_Conditioned:
                    expr = expr.doit()
                if not expr.is_random:  # expr isn't random?
                    return expr
                ps = pspace(expr)
                if ps == PSpace():
                    return self.func(expr)
                # Otherwise case is simple, pass work off to the ProbabilitySpace
                function = ps.compute_expectation(expr, evaluate=True)
                if hasattr(function, 'doit'):
                    function = function.doit(**hints)
            return function
        else:
            deep = hints.get('deep', True)
            expr = self.args[0]
            numsamples = hints.get('numsamples', False)
            for_rewrite = not hints.get('for_rewrite', False)
    
            if deep:
                expr = expr.doit(**hints)
    
            if not expr.is_random or isinstance(expr, Expectation):  # expr isn't random?
                return expr
            if numsamples:  # Computing by monte carlo sampling?
                evalf = hints.get('evalf', True)
                return sampling_E(expr, numsamples=numsamples, evalf=evalf)
    
            if expr.has(RandomIndexedSymbol):
                return pspace(expr).compute_expectation(expr)
    
            # A few known statements for efficiency
    
            if expr.is_Add:  # We know that E is Linear
                return Add(*[self.func(arg).doit(**hints)
                        if not isinstance(arg, Expectation) else self.func(arg)
                             for arg in expr.args])
            if expr.is_Mul:
                if expr.atoms(Expectation):
                    return expr
    
            ps = pspace(expr)
            if ps == PSpace():
                return self.func(expr)
            # Otherwise case is simple, pass work off to the ProbabilitySpace
            result = ps.compute_expectation(expr, evaluate=for_rewrite)
            if hasattr(result, 'doit') and for_rewrite:
                return result.doit(**hints)
            else:
                return result

    def _eval_rewrite_as_Probability(self, arg, condition=None, **kwargs):
        rvs = arg.atoms(RandomSymbol)
        if len(rvs) > 1:
            raise NotImplementedError()
        if len(rvs) == 0:
            return arg

        rv = rvs.pop()
        if rv.pspace is None:
            raise ValueError("Probability space not known")

        symbol = rv.symbol
        if symbol.name[0].isupper():
            symbol = Symbol(symbol.name.lower())
        else :
            symbol = Symbol(symbol.name + "_1")

        if rv.pspace.is_Continuous:
            return Integral(arg.replace(rv, symbol) * Probability(Eq(rv, symbol), condition), (symbol, rv.pspace.domain.set.inf, rv.pspace.domain.set.sup))
        else:
            if rv.pspace.is_Finite:
                raise NotImplementedError
            else:
                return Sum(arg.replace(rv, symbol) * Probability(Eq(rv, symbol), condition), (symbol, rv.pspace.domain.set.inf, rv.pspace.set.sup))

    def _eval_rewrite_as_Integral(self, arg, condition=None, **kwargs):
        return self.func(arg, condition=condition).doit(deep=False, for_rewrite=True)

    _eval_rewrite_as_Sum = _eval_rewrite_as_Integral  # For discrete this will be Sum

    def evaluate_integral(self):
        return self.rewrite(Integral).doit()

    evaluate_sum = evaluate_integral

    def _latex(self, p):
        tex = r'\mathop{\mathbb{E}}'
        limits = self.limits

        if weights := self.weights:
            weights_str = ','.join([p._print(w) for w in weights])
            def _format_ineq(limit):
                if len(limit) == 1:
                    return r"%s \sim %s" % (p._print(limit[0]), weights_str)
                x, cond = limit
                return r"%s \sim %s \mid %s" % (p._print(x), p._print(cond), weights_str)
        else:
            def _format_ineq(limit):
                if len(limit) == 1:
                    return p._print(limit[0])
                x, cond = limit
                return r"%s \sim %s" % (p._print(x), p._print(cond))

        if not limits:
            tex += ' '  
        elif len(limits) == 1:
            limit = limits[0]
            if len(limit) == 1:
                x, = limit
                if weights:
                    tex += r"_{%s \sim %s} " % (p._print(x), weights_str)
                else:
                    if {*self.expr.random_symbols} - {x}:
                        tex += r"_{%s} " % p._print(x)
            else:
                tex += r"\limits_{%s} " % _format_ineq(limit)
        else:
            if all(len(limit) == 1 for limit in limits):
                vars = [limit[0] for limit in limits]
                if {*self.expr.random_symbols} - {*vars}:
                    tex += r"_{%s} " % str.join(', ', [p._print(v) for v in vars])
            else:
                tex += r"\limits_{\begin{subarray}{c}%s\end{subarray}} " % str.join('\\\\', [_format_ineq(l) for l in limits])

        tex += r"\left(%s\right)" % p._print(self.expr)
        return tex

    def _sympystr(self, p):
        if weights := self.weights:
            weights_str = ','.join([p._print(w) for w in weights])
            def _format_ineq(limit):
                if len(limit) == 1:
                    return r"%s ~ %s" % (p._print(limit[0]), weights_str)
                x, cond = limit
                return r"%s ~ %s | %s" % (p._print(x), p._print(cond), weights_str)
        else:
            def _format_ineq(limit):
                if len(limit) == 1:
                    return p._print(limit[0])
                x, cond = limit
                return r"%s ~ %s" % (p._print(x), p._print(cond))

        return 'E[%s](%s)' % (','.join([_format_ineq(limit) for limit in self.limits]), p._print(self.expr))

    def _eval_is_random(self):
        expr = self.expr
        
        variables_set = self.variables_set
        if any(not any(V.index_contains(v) for V in variables_set) for v in expr.random_symbols): 
            return True
                
        if expr.is_Conditioned:
            for v in expr.rhs.yield_random_symbols():
                if v.is_Surrogate:
                    return True

    def _if_new_has_variables(self, old, new):
        return set()
    
    def simplify(self, deep=False):
        [*limits] = self.limits
        expr = self.expr
        if expr.is_Conditioned:
            expr = expr.lhs
            
        if std.deleteIndices(limits, lambda limit: not expr._has(limit[0])):
            if weights := self.weights:
                limits.append(weights)
            self = self.func(self.expr, *limits)
            
        random_symbols = expr.random_symbols
        
        varMapping = defaultdict(list)
        for x, *ab in self.limits:
            if ab:
                continue
            
            for v in random_symbols:
                if x != v and x.index_contains(v):
                    varMapping[x].append(v)
                    
        if varMapping:
            for x, s in varMapping.items():
                if len(s) == 1:
                    s, = s
                    i = self.variables.index(x)
                    limits[i] = (s,)
                
            self = self.func(self.expr, *limits, *self.weights)

        return ExprWithLimits.simplify(self, deep)

    def yield_random_symbols_from_expr(self):
        expr = self.expr
        if expr.is_Conditioned:
            lhs, rhs = expr.args
            yield from lhs.yield_random_symbols()

            for v in rhs.yield_random_symbols():
                if v.is_Surrogate:
                    yield v.arg
        else:
            yield from expr.yield_random_symbols()

    def yield_random_symbols(self):
        variables = self.variables
        for v in self.yield_random_symbols_from_expr():
            if not any(V.index_contains(v) for V in variables):
                yield v

        for x, *ab in self.limits:
            for v in ab:
                yield from v.yield_random_symbols()

    def _has_indexed(self, pattern):
        base = pattern.base
        if base.is_Indexed:
            base = base.base
        
        if not base.is_random:
            for surrogate in self.finditer(Surrogate):
                if surrogate.arg.var._has(pattern):
                    return True

        return ExprWithLimits._has_indexed(self, pattern)

    def __iter__(self):
        raise TypeError
    
    def __getitem__(self, indices, **kw_args):
        return self.func(self.expr[indices], *self.limits, *self.weights)


class Variance(ExprWithLimits):
    """
    Symbolic expression for the variance.

    Examples
    ========

    >>> from sympy import symbols, Integral
    >>> from sympy.stats import Normal, Expectation, Variance, Probability
    >>> mu = symbols("mu", positive=True)
    >>> sigma = symbols("sigma", positive=True)
    >>> X = Normal("X", mu, sigma)
    >>> Variance(X)
    Variance(X)
    >>> Variance(X).evaluate_integral()
    sigma**2

    Integral representation of the underlying calculations:

    >>> Variance(X).rewrite(Integral)
    Integral(sqrt(2)*(X - Integral(sqrt(2)*X*exp(-(X - mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (X, -oo, oo)))**2*exp(-(X - mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (X, -oo, oo))

    Integral representation, without expanding the PDF:

    >>> Variance(X).rewrite(Probability)
    -Integral(x*Probability(Eq(X, x)), (x, -oo, oo))**2 + Integral(x**2*Probability(Eq(X, x)), (x, -oo, oo))

    Rewrite the variance in terms of the expectation

    >>> Variance(X).rewrite(Expectation)
    -Expectation(X)**2 + Expectation(X**2)

    Some transformations based on the properties of the variance may happen:

    >>> from sympy.abc import a
    >>> Y = Normal("Y", 0, 1)
    >>> Variance(a*X)
    Variance(a*X)

    To expand the variance in its expression, use ``expand()``:

    >>> Variance(a*X).expand()
    a**2*Variance(X)
    >>> Variance(X + Y)
    Variance(X + Y)
    >>> Variance(X + Y).expand()
    2*Covariance(X, Y) + Variance(X) + Variance(Y)

    """

    def __new__(cls, expr, *limits, **kwargs):
        expr = _sympify(expr)
        if not expr.is_random:
            from sympy import ZeroMatrix
            return ZeroMatrix(*expr.shape)
        
        if (given := kwargs.get('given')) is not None:
            if given.is_symbol:
                given = Equal(given, given.var)
            expr = Conditioned(expr, given)
        
        return ExprWithLimits.__new__(cls, expr, *limits)

    def expand(self, **hints):
        arg = self.args[0]
        condition = self._condition

        if not is_random(arg):
            return S.Zero

        if isinstance(arg, RandomSymbol):
            return self
        elif isinstance(arg, Add):
            rv = []
            for a in arg.args:
                if is_random(a):
                    rv.append(a)
            variances = Add(*map(lambda xv: Variance(xv, condition).expand(), rv))
            map_to_covar = lambda x: 2 * Covariance(*x, condition=condition).expand()
            covariances = Add(*map(map_to_covar, itertools.combinations(rv, 2)))
            return variances + covariances
        elif isinstance(arg, Mul):
            nonrv = []
            rv = []
            for a in arg.args:
                if is_random(a):
                    rv.append(a)
                else:
                    nonrv.append(a ** 2)
            if len(rv) == 0:
                return S.Zero
            return Mul.fromiter(nonrv) * Variance(Mul.fromiter(rv), condition)

        # this expression contains a RandomSymbol somehow:
        return self

    def _eval_rewrite_as_Expectation(self, arg, condition=None, **kwargs):
            e1 = Expectation(arg ** 2, condition)
            e2 = Expectation(arg, condition) ** 2
            return e1 - e2

    def _eval_rewrite_as_Probability(self, arg, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Probability)

    def _eval_rewrite_as_Integral(self, arg, condition=None, **kwargs):
        return variance(self.args[0], self._condition, evaluate=False)

    _eval_rewrite_as_Sum = _eval_rewrite_as_Integral

    def evaluate_integral(self):
        return self.rewrite(Integral).doit()

    def _latex(self, p):
        tex = r'\mathop{\mathbb{Var}}'
        limits = self.limits
        
        def _format_ineq(limit):
            if len(limit) == 1:
                return p._print(limit[0])
            x, cond = limit
            return r"%s \sim %s" % (p._print(x), p._print(cond))
        
        if not limits:
            tex += ' '  
        elif len(limits) == 1:
            limit = limits[0]
            if len(limit) == 1:
                x, = limit
                if {*self.expr.random_symbols} - {x}:
                    tex += r"_{%s} " % p._print(x)
            else:
                tex += r"\limits_{%s} " % _format_ineq(limit)
        else:
            if all(len(limit) == 1 for limit in limits):
                vars = [limit[0] for limit in limits]
                if {*self.expr.random_symbols} - {*vars}:
                    tex += r"_{%s} " % str.join(', ', [p._print(v) for v in vars])
            else:
                tex += r"\limits_{\begin{subarray}{c}%s\end{subarray}} " % str.join('\\\\', [_format_ineq(l) for l in limits])

        tex += r"\left(%s\right)" % p._print(self.expr)
        return tex

    def _sympystr(self, p):
        expr, *limits = self.args
        if limits:
            def _format_ineq(limit):
                if len(limit) == 1:
                    return p._print(limit[0])
                x, cond = limit
                return r"%s ~ %s" % (p._print(x), p._print(cond))
            
            return 'Var[%s](%s)' % (','.join([_format_ineq(limit) for limit in limits]), p._print(expr))
        else:
            return 'Var(%s)' % p._print(expr)

    def _eval_is_random(self):
        if {*self.expr.random_symbols} - {*self.variables}:
            return True
        
        return False


class KL(Expr):
    """
    Symbolic expression for the Kullback-Leibler divergence.
    """

    def __new__(cls, lhs, rhs, **kwargs):
        assert lhs.is_Probability and rhs.is_Probability
        return Expr.__new__(cls, lhs, rhs)

    def _latex(self, p):
        tex = r'\mathop{\mathbb{KL}}'
        lhs, rhs = self.args
        limits = []
        
        def _format_ineq(limit):
            if len(limit) == 1:
                return p._print(limit[0])
            x, cond = limit
            return r"%s \sim %s" % (p._print(x), p._print(cond))
        
        if not limits:
            tex += ' '  
        elif len(limits) == 1:
            limit = limits[0]
            if len(limit) == 1:
                x, = limit
                if {*self.expr.random_symbols} - {x}:
                    tex += r"_{%s} " % p._print(x)
            else:
                tex += r"\limits_{%s} " % _format_ineq(limit)
        else:
            if all(len(limit) == 1 for limit in limits):
                vars = [limit[0] for limit in limits]
                if {*self.expr.random_symbols} - {*vars}:
                    tex += r"_{%s} " % str.join(', ', [p._print(v) for v in vars])
            else:
                tex += r"\limits_{\begin{subarray}{c}%s\end{subarray}} " % str.join('\\\\', [_format_ineq(l) for l in limits])
        #\bigg/
        tex += r"\left(%s\middle/%s\right)" % (p._print(lhs), p._print(rhs))
        return tex

    @property
    def shape(self):
        return ()
    
    @property
    def dtype(self):
        from sympy import dtype
        return dtype.real

    def _eval_is_extended_nonnegative(self):
        return True

    def _sympystr(self, p):
        lhs, rhs = self.args
        limits = []

        if limits:
            def _format_ineq(limit):
                if len(limit) == 1:
                    return p._print(limit[0])
                x, cond = limit
                return r"%s ~ %s" % (p._print(x), p._print(cond))
            
            return 'KL[%s](%s, %s)' % (','.join([_format_ineq(limit) for limit in limits]), p._print(lhs), p._print(rhs))
        else:
            return 'KL(%s, %s)' % (p._print(lhs), p._print(rhs))

    def _eval_is_random(self):
        return any(arg.is_random for arg in self.args)


class Covariance(ExprWithLimits):
    """
    Symbolic expression for the covariance.

    Examples
    ========

    >>> from sympy.stats import Covariance
    >>> from sympy.stats import Normal
    >>> X = Normal("X", 3, 2)
    >>> Y = Normal("Y", 0, 1)
    >>> Z = Normal("Z", 0, 1)
    >>> W = Normal("W", 0, 1)
    >>> cexpr = Covariance(X, Y)
    >>> cexpr
    Covariance(X, Y)

    Evaluate the covariance, `X` and `Y` are independent,
    therefore zero is the result:

    >>> cexpr.evaluate_integral()
    0

    Rewrite the covariance expression in terms of expectations:

    >>> from sympy.stats import Expectation
    >>> cexpr.rewrite(Expectation)
    Expectation(X*Y) - Expectation(X)*Expectation(Y)

    In order to expand the argument, use ``expand()``:

    >>> from sympy.abc import a, b, c, d
    >>> Covariance(a*X + b*Y, c*Z + d*W)
    Covariance(a*X + b*Y, c*Z + d*W)
    >>> Covariance(a*X + b*Y, c*Z + d*W).expand()
    a*c*Covariance(X, Z) + a*d*Covariance(W, X) + b*c*Covariance(Y, Z) + b*d*Covariance(W, Y)

    This class is aware of some properties of the covariance:

    >>> Covariance(X, X).expand()
    Variance(X)
    >>> Covariance(a*X, b*Y).expand()
    a*b*Covariance(X, Y)
    """

    def __new__(cls, *args, **kwargs):
        if args[0].is_Tuple:
            arg1, arg2 = args[0]
            limits = args[1:]
        else:
            arg1, arg2, *limits = args
        arg1 = _sympify(arg1)
        arg2 = _sympify(arg2)

        if kwargs.pop('evaluate', global_parameters.evaluate):
            arg1, arg2 = sorted([arg1, arg2], key=default_sort_key)
            
        from sympy import Tuple
        expr = Tuple(arg1, arg2)
        if (given := kwargs.get('given')) is not None:
            if given.is_symbol:
                given = Equal(given, given.var)
                
            expr = Conditioned(expr, given)

        obj = ExprWithLimits.__new__(cls, expr, *limits)
        return obj

    def expand(self, **hints):
        arg1 = self.args[0]
        arg2 = self.args[1]
        condition = self._condition

        if arg1 == arg2:
            return Variance(arg1, condition).expand()

        if not is_random(arg1):
            return S.Zero
        if not is_random(arg2):
            return S.Zero

        arg1, arg2 = sorted([arg1, arg2], key=default_sort_key)

        if isinstance(arg1, RandomSymbol) and isinstance(arg2, RandomSymbol):
            return Covariance(arg1, arg2, condition)

        coeff_rv_list1 = self._expand_single_argument(arg1.expand())
        coeff_rv_list2 = self._expand_single_argument(arg2.expand())

        addends = [a * b * Covariance(*sorted([r1, r2], key=default_sort_key), condition=condition)
                   for (a, r1) in coeff_rv_list1 for (b, r2) in coeff_rv_list2]
        return Add.fromiter(addends)

    @classmethod
    def _expand_single_argument(cls, expr):
        # return (coefficient, random_symbol) pairs:
        if isinstance(expr, RandomSymbol):
            return [(S.One, expr)]
        elif isinstance(expr, Add):
            outval = []
            for a in expr.args:
                if isinstance(a, Mul):
                    outval.append(cls._get_mul_nonrv_rv_tuple(a))
                elif is_random(a):
                    outval.append((S.One, a))

            return outval
        elif isinstance(expr, Mul):
            return [cls._get_mul_nonrv_rv_tuple(expr)]
        elif is_random(expr):
            return [(S.One, expr)]

    @classmethod
    def _get_mul_nonrv_rv_tuple(cls, m):
        rv = []
        nonrv = []
        for a in m.args:
            if is_random(a):
                rv.append(a)
            else:
                nonrv.append(a)
        return (Mul.fromiter(nonrv), Mul.fromiter(rv))

    def _eval_rewrite_as_Expectation(self, arg1, arg2, condition=None, **kwargs):
        e1 = Expectation(arg1 * arg2, condition)
        e2 = Expectation(arg1, condition) * Expectation(arg2, condition)
        return e1 - e2

    def _eval_rewrite_as_Probability(self, arg1, arg2, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Probability)

    def _eval_rewrite_as_Integral(self, arg1, arg2, condition=None, **kwargs):
        return covariance(self.args[0], self.args[1], self._condition, evaluate=False)

    _eval_rewrite_as_Sum = _eval_rewrite_as_Integral

    def evaluate_integral(self):
        return self.rewrite(Integral).doit()

    def _latex(self, p):
        (arg1, arg2), *limits = self.args
        tex = r'\mathop{\mathbb{Cov}}'
        def _format_ineq(limit):
            if len(limit) == 1:
                return p._print(limit[0])
            x, cond = limit
            return r"%s \sim %s" % (p._print(x), p._print(cond))
        
        if not limits:
            tex += ' '  
        elif len(limits) == 1:
            limit = limits[0]
            if len(limit) == 1:
                tex += r"_{%s} " % p._print(limit[0])
            else:
                tex += r"\limits_{%s} " % _format_ineq(limit)
        else:
            if all(len(limit) == 1 for limit in limits):
                tex += r"_{%s} " % str.join(', ', [p._print(l[0]) for l in limits])
            else:
                tex += r"\limits_{\begin{subarray}{c}%s\end{subarray}} " % str.join('\\\\', [_format_ineq(l) for l in limits])

        tex += r"\left(%s,%s\right)" % (p._print(arg1), p._print(arg2))
        return tex

    def _sympystr(self, p):
        expr, *limits = self.args
        if limits:
            def _format_ineq(limit):
                if len(limit) == 1:
                    return p._print(limit[0])
                x, cond = limit
                return r"%s ~ %s" % (p._print(x), p._print(cond))
            
            return 'Cov[%s]%s' % (','.join([_format_ineq(limit) for limit in limits]), p._print(expr))
        else:
            return 'Cov%s' % p._print(expr)

    @property
    def dtype(self):
        return self.expr[0].dtype
    
    def _eval_is_random(self):
        if {*self.expr.random_symbols} - {*self.variables}:
            return True
        
        return False


class Moment(Expr):
    """
    Symbolic class for Moment

    Examples
    ========

    >>> from sympy import Symbol, Integral
    >>> from sympy.stats import Normal, Expectation, Probability, Moment
    >>> mu = Symbol('mu', real=True)
    >>> sigma = Symbol('sigma', real=True, positive=True)
    >>> X = Normal('X', mu, sigma)
    >>> M = Moment(X, 3, 1)

    To evaluate the result of Moment use `doit`:

    >>> M.doit()
    mu**3 - 3*mu**2 + 3*mu*sigma**2 + 3*mu - 3*sigma**2 - 1

    Rewrite the Moment expression in terms of Expectation:

    >>> M.rewrite(Expectation)
    Expectation((X - 1)**3)

    Rewrite the Moment expression in terms of Probability:

    >>> M.rewrite(Probability)
    Integral((x - 1)**3*Probability(Eq(X, x)), (x, -oo, oo))

    Rewrite the Moment expression in terms of Integral:

    >>> M.rewrite(Integral)
    Integral(sqrt(2)*(X - 1)**3*exp(-(X - mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (X, -oo, oo))

    """

    def __new__(cls, X, n, c=0, condition=None, **kwargs):
        X = _sympify(X)
        n = _sympify(n)
        c = _sympify(c)
        if condition is not None:
            condition = _sympify(condition)
        return Expr.__new__(cls, X, n, c, condition)

    def doit(self, **hints):
        if not is_random(self.args[0]):
            return self.args[0]
        return self.rewrite(Expectation).doit(**hints)

    def _eval_rewrite_as_Expectation(self, X, n, c=0, condition=None, **kwargs):
        return Expectation((X - c) ** n, condition)

    def _eval_rewrite_as_Probability(self, X, n, c=0, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Probability)

    def _eval_rewrite_as_Integral(self, X, n, c=0, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Integral)


class CentralMoment(Expr):
    """
    Symbolic class Central Moment

    Examples
    ========

    >>> from sympy import Symbol, Integral
    >>> from sympy.stats import Normal, Expectation, Probability, CentralMoment
    >>> mu = Symbol('mu', real=True)
    >>> sigma = Symbol('sigma', real=True, positive=True)
    >>> X = Normal('X', mu, sigma)
    >>> CM = CentralMoment(X, 4)

    To evaluate the result of CentralMoment use `doit`:

    >>> CM.doit().simplify()
    3*sigma**4

    Rewrite the CentralMoment expression in terms of Expectation:

    >>> CM.rewrite(Expectation)
    Expectation((X - Expectation(X))**4)

    Rewrite the CentralMoment expression in terms of Probability:

    >>> CM.rewrite(Probability)
    Integral((x - Integral(x*Probability(True), (x, -oo, oo)))**4*Probability(Eq(X, x)), (x, -oo, oo))

    Rewrite the CentralMoment expression in terms of Integral:

    >>> CM.rewrite(Integral)
    Integral(sqrt(2)*(X - Integral(sqrt(2)*X*exp(-(X - mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (X, -oo, oo)))**4*exp(-(X - mu)**2/(2*sigma**2))/(2*sqrt(pi)*sigma), (X, -oo, oo))

    """

    def __new__(cls, X, n, condition=None, **kwargs):
        X = _sympify(X)
        n = _sympify(n)
        if condition is not None:
            condition = _sympify(condition)
        return Expr.__new__(cls, X, n, condition)

    def doit(self, **hints):
        if not is_random(self.args[0]):
            return self.args[0]
        return self.rewrite(Expectation).doit(**hints)

    def _eval_rewrite_as_Expectation(self, X, n, condition=None, **kwargs):
        mu = Expectation(X, condition, **kwargs)
        return Moment(X, n, mu, condition, **kwargs).rewrite(Expectation)

    def _eval_rewrite_as_Probability(self, X, n, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Probability)

    def _eval_rewrite_as_Integral(self, X, n, condition=None, **kwargs):
        return self.rewrite(Expectation).rewrite(Integral)
