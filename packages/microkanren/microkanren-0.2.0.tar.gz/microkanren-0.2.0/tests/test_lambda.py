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
        abstraction(term),
        application(term),
    )


def abstraction(term):
    return fresh(
        lambda var, body: eq(term, ("λ", var, body))
        & variable(var)
        & lambda_term(body),
    )


def variable(term):
    return typeo(term, str)


def application(term):
    return fresh(lambda m, n: eq(term, (m, n)) & lambda_term(m) & lambda_term(n))


def true(term):
    return fresh(lambda x, y: eq(term, ("λ", x, ("λ", y, x))))


def false(term):
    return fresh(lambda x, y: eq(term, ("λ", x, ("λ", y, y))))


def eval(term, env, out):
    return disj(
        variable(term) & lookup(term, env, out),
        abstraction(term) & eq(term, out),
        conj(
            application(term),
            fresh(
                lambda m, n: conj(
                    eq((m, n), term),
                    fresh(
                        lambda m1: conj(
                            eval(m, env, m1),
                            fresh(
                                lambda var, body, next_env: disj(
                                    conj(
                                        eq(m1, ("λ", var, body)),
					abstraction(("λ", var, body)),
                                        eq(next_env, cons((var, n), env)),
                                        eval(body, next_env, out),
                                    ),
                                    eq(term, out),
                                )
                            ),
                        )
                    ),
                ),
            ),
        ),
    )


def lookup(var, env, out):
    return fresh(
        lambda a, d, rest: conj(
            eq(cons((a, d), rest), env),
            disj(
                eq(a, var) & eq(d, out),
                lookup(var, rest, out),
            ),
        )
    )
