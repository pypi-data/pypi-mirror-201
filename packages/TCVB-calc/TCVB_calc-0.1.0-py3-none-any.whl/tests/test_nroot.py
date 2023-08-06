import TCVB_calc.calc_main as cc


def test_root():
    test_var=cc.Calculator(81)
    test_var.n_root(2)
    assert test_var.result==9
    
def test_root2():
    test_var=cc.Calculator()
    test_var.n_root(0)
    assert TypeError