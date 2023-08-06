#! /usr/bin/env python
# Copyright © 2019 Uwe Schitt <uwe.schmitt@id.ethz.ch>


def test_import():
    import emzed_spyder

    assert emzed_spyder.__version__ is not None
