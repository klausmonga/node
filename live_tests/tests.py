# python 3.11
from live_tests.tests_lib import send_report
from live_tests.tests_lib import init_test



def test_1():
    send_report({'status':1,'test_name':'test001','message':'error ...', 'flag':False})
    return True

def test_2():
    send_report({'status':1,'test_name':'test002','message':'ok ...', 'flag':False})
    return True
def test_3():
    send_report({'status':1,'test_name':'test003','message':'ok ...', 'flag':False})
    return True
def test_4():
    send_report({'status':1,'test_name':'test004','message':'tty/usb0 error ...', 'flag': True})
    return True
if __name__ == '__main__':
    if test_1():
        if test_2():
            if test_3():
                if test_4():
                    print("DONE TEST !!!")