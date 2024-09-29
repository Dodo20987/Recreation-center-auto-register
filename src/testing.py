import main
import datetime

def test_press_register():
    for i in range(0, 50):
        e1 = main.registerEvent()
        if e1.clickRegister():
            e1.completeRegister()

def test_info_input():
    for i in range(0, 25):
        e1 = main.registerEvent()
        e1.click_register()
        if e1.login_page():
            e1.complete_register()

if __name__ == "__main__":
    #test_press_register()
#    test_info_input()
    # Get the current day of the week
    current_day = datetime.datetime.now().strftime("%A")
    print(current_day)