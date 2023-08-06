import TCVB_calc.calc_main as cc


def test_multiply():
    test_var=cc.Calculator(12.5)
    test_var.multiply(4)
    assert test_var.result==50
    