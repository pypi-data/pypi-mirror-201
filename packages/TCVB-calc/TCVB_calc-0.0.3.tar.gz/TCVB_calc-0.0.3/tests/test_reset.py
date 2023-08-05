import TCVB_calc.calc_main as cc


def test_reset():
    test_var=cc.Calculator()
    test_var.add(20)
    test_var.reset()
    assert test_var.result==0
    