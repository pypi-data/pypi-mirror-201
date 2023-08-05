import TCVB_calc.calc_main as cc


def root_test():
    test_var=cc.Calculator(81)
    test_var.n_root(2)
    assert test_var.result==9
    