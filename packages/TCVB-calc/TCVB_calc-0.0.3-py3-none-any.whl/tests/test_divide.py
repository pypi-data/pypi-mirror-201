import TCVB_calc.calc_main as cc

def test_divide():
    test_var=cc.Calculator(12)
    test_var.divide(3)
    assert test_var.result==4
    
