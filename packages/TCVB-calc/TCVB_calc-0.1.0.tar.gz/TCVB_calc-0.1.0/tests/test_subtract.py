import TCVB_calc.calc_main as cc


def test_subtract():
    test_var=cc.Calculator(81)
    test_var.subtract(21)
    assert test_var.result==60