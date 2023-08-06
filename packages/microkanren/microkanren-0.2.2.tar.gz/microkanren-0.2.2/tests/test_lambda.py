from microkanren import (
    Constraint,
    Var,
    conj,
    disj,
    eq,
    extend_constraint_store,
    fresh,
    goal_from_constraint,
    run_constraints,
    set_process_prefix,
    walk,
)
from microkanren.cons import cons


def vcons(*args):
    return cons.from_xs(args)


_ = vcons


class SymbolMeta(type):
    _symbols = {}

    def __new__(cls, name, bases, _dict):
        new_cls = super().__new__(cls, name, bases, _dict)

        cls._symbols[new_cls] = name
        return new_cls

    def __repr__(self):
        return self._symbols[self]


class λ(metaclass=SymbolMeta):
    def __new__(cls, arg, body, out):
        return eq(_(λ, _(arg), body), out) & variable(arg)


def typeo(x, typ):
    return goal_from_constraint(typeoc(x, typ))


def typeoc(value, typ):
    def _typeoc(state):
        v = walk(value, state.sub)
        if isinstance(v, Var):
            return state.set(
                constraints=extend_constraint_store(
                    Constraint(typeoc, [value, typ]),
                    state.constraints,
                )
            )
        elif type(v) == typ:
            return state
        else:
            return None

    return _typeoc


def process_prefix_typeo(prefix, constraints):
    return run_constraints(prefix.keys(), constraints)


set_process_prefix(process_prefix_typeo)


def lambda_term(term):
    return disj(
        variable(term),
        fresh(
            lambda arg, body: conj(
                λ(arg, body, term),
                lambda_term(arg),
                lambda_term(body),
            )
        ),
        fresh(
            lambda rand, rator: conj(
                apply(rand, rator, term),
                lambda_term(rand),
                lambda_term(rator),
            )
        ),
    )


def variable(term):
    return typeo(term, int)


def apply(rand, rator, term):
    return eq(_(rand, rator), term)


def evalo(term, out):
    return disj(
        variable(term) & eq(term, out),
        fresh(lambda arg, body: λ(arg, body, term) & eq(term, out)),
        fresh(
            lambda rand, rator: apply(rand, rator, term) & eval_app(rand, rator, out)
        ),
    )


def eval_app(rand, rator, out):
    return fresh(
        lambda arg, body, rand1, rator1: conj(
            evalo(rand, rand1),
            evalo(rator, rator1),
            λ(arg, body, rand),
            eq(arg, rator1),
            evalo(body, out),
        )
    )


def true(term):
    return fresh(lambda x, y: eq(term, _(λ, _(x), _(λ, _(y), x))))


def false(term):
    return fresh(lambda x, y: eq(term, _(λ, _(x), _(λ, _(y), y))))
