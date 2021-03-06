#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Randall Balestriero"

import numpy as np

import symjax as sj
import symjax.tensor as T
import networkx as nx


def test_map():
    sj.current_graph().reset()
    w = T.Variable(1.0, dtype="float32")
    u = T.Placeholder((), "float32")
    out = T.map(lambda a, w, u: (u - w) * a, [T.range(3)], non_sequences=[w, u])
    f = sj.function(u, outputs=out, updates={w: w + 1})
    assert np.array_equal(f(2), np.arange(3))
    assert np.array_equal(f(2), np.zeros(3))
    assert np.array_equal(f(0), -np.arange(3) * 3)


def test_grad_map():
    sj.current_graph().reset()
    w = T.Variable(1.0, dtype="float32")
    u = T.Placeholder((), "float32", name="u")
    out = T.map(lambda a, w, u: w * a * u, (T.range(3),), non_sequences=(w, u))
    g = sj.gradients(out.sum(), w)
    f = sj.function(u, outputs=g)

    assert np.array_equal(f(0), 0)
    assert np.array_equal(f(1), 3)


def test_grad_map_v2():
    sj.current_graph().reset()
    out = T.map(lambda a, b: a * b, (T.range(3), T.range(3)))
    f = sj.function(outputs=out)

    assert np.array_equal(f(), np.arange(3) * np.arange(3))


def test_while():
    sj.current_graph().reset()
    w = T.Variable(1.0, dtype="float32")
    v = T.Placeholder((), "float32")
    out = T.while_loop(
        lambda i, u: i[0] + u < 5,
        lambda i: (i[0] + 1.0, i[0] ** 2),
        (w, 1.0),
        non_sequences_cond=(v,),
    )
    f = sj.function(v, outputs=out)
    assert np.array_equal(np.array(f(0)), [5, 16])
    assert np.array_equal(f(2), [3, 4])


if __name__ == "__main__":
    test_while()
    test_map()
    test_grad_map()
