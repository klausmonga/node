# python 3.11
from live_tests.tests_lib import send_report
from live_tests.tests_lib import init_test



def test_1():
    send_report({'status':1,'test_name':'test001','message':'error ...'})
    return True

def test_2():
    send_report({'status':1,'test_name':'test002','message':'ok ...'})
    return True
def test_3():
    send_report({'status':1,'test_name':'test003','message':'ok ...'})
    return True
def test_4():
    send_report({'status':1,'test_name':'test004','message':'tty/usb0 error ...'})
    return True
if __name__ == '__main__':
    init_test(
    test_1() and
    test_2() and
    test_3() and
    test_4()
    )