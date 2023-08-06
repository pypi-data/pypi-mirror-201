import TCVB_calc.calc_main as cc


def test_add():
    test_var=cc.Calculator(10)
    test_var.add(20)
    assert test_var.result==30
    
def test_add2():
    test_var=cc.Calculator()
    test_var.add(20)
    test_var.add(-15)
    assert test_var.result==5

