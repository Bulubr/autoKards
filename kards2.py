import pyautogui
import cv2
import numpy as np
import time
import os

# 截图函数，捕捉指定区域的图像
def take_screenshot(region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

# 检测按钮并返回是否找到按钮（不点击）
def detect_button(image_path, threshold=0.8):
    screenshot = take_screenshot()
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        button_x, button_y = max_loc
        button_w, button_h = template.shape[1], template.shape[0]
        center_x, center_y = button_x + button_w // 2, button_y + button_h // 2
        print(f"Button detected at ({center_x}, {center_y})")
        return (center_x, center_y)
    return None

# 检测按钮并移动鼠标点击
def detect_and_click_button(image_path, threshold=0.8):
    button_pos = detect_button(image_path, threshold)
    if button_pos:
        pyautogui.moveTo(button_pos[0], button_pos[1])
        time.sleep(0.5)  # 稍作等待
        pyautogui.click()
        return True
    return False

# 拖动鼠标操作
def drag_mouse(start_x, start_y, drag_x, drag_y):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.move(drag_x, drag_y)  # 按住左键并拖动
    pyautogui.mouseUp()

def drag_mouse(start_x, start_y, drag_x, drag_y, duration=0.3):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.move(drag_x, drag_y, duration=duration)  # 按住左键并拖动，duration 参数控制滑动速度
    pyautogui.mouseUp()

# 检测并处理 Setting 图标操作
def handle_setting_and_drag(setting_image_path):
        for i in range(1):  # 重复1次拖动操作
            button_pos = detect_button(setting_image_path)
            if button_pos:
                center_x, center_y = button_pos
                # 移动鼠标至 setting 图标中央
                pyautogui.moveTo(center_x, center_y)
                time.sleep(1)  # 稍作等待

                # 向左移动400像素，向下移动400像素
                pyautogui.move(-580, 630)
                time.sleep(1)  # 稍作等待

                # 按住左键向上移动100像素后松开
                drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                time.sleep(1)
                drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                time.sleep(1)
                drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
            else:
                print("Setting button not found.")

            time.sleep(1)  # 每次操作后等待7秒

        for i in range(1):  # 重复1次拖动操作
            button_pos = detect_button(setting_image_path)
            if button_pos:
                center_x, center_y = button_pos
                # 移动鼠标至 setting 图标中央
                pyautogui.moveTo(center_x, center_y)
                time.sleep(0.5)  # 稍作等待

                # 向左移动400像素，向下移动400像素
                pyautogui.move(-500, 630)
                time.sleep(1)  # 稍作等待

                # 按住左键向上移动100像素后松开
                drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                time.sleep(1)
                drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                time.sleep(1)
                drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
            else:
                print("Setting button not found.")

            time.sleep(1)  # 每次操作后等待7秒
# 主程序
def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    start_image_path = os.path.join(current_dir, 'start.png')  
    confirm_image_path = os.path.join(current_dir, 'confirm.png')  
    endturn_image_path = os.path.join(current_dir, 'endturn.png')  
    setting_image_path = os.path.join(current_dir, 'setting.png')  # Setting 图标路径
    continue_image_path = os.path.join(current_dir, 'continue.png')  # Continue 按钮路径
    surrender_image_path = os.path.join(current_dir, 'surrender.png')

    # 检测并点击 Start 按钮
    while True:
        if detect_and_click_button(start_image_path):
            print("Start button clicked, waiting for 10 seconds...")
            time.sleep(2)
            break
    
    # 检测并点击 Confirm 按钮
    while True:
        if detect_and_click_button(confirm_image_path):
            print("Confirm button clicked, starting 4-minute countdown...")
            break
        time.sleep(1)
        pyautogui.click()

    # 进入4分钟倒计时
    countdown_time = 4 * 60  # 4分钟
    start_time = time.time()

    while time.time() - start_time < countdown_time:
        print("Checking for Endturn or Continue button...")
        
        endturn_pos = detect_button(endturn_image_path)
        continue_pos = detect_button(continue_image_path)

        if continue_pos:
            while True:
                if detect_and_click_button(continue_image_path):
                    time.sleep(3)
                    detect_and_click_button(continue_image_path)
                    time.sleep(3)
                    detect_and_click_button(continue_image_path)
                    time.sleep(3)
                    detect_and_click_button(continue_image_path)
                    time.sleep(3)
                    detect_and_click_button(continue_image_path)
                    time.sleep(3)
                    break

            print("Restarting main process...")
            return  # 结束当前循环并重新开始程序
        
        if endturn_pos:
            print("Endturn button detected, waiting 5 seconds...")
            time.sleep(3)  # 探测到endturn按钮后等待5秒

            for i in range(1):  # 重复1次拖动操作
                button_pos = detect_button(setting_image_path)
                if button_pos:
                    center_x, center_y = button_pos
                    # 移动鼠标至 setting 图标中央
                    pyautogui.moveTo(center_x, center_y)
                    time.sleep(1)  # 稍作等待

                    # 向左移动400像素，向下移动400像素
                    pyautogui.move(-580, 630)
                    time.sleep(1)  # 稍作等待

                    # 按住左键向上移动100像素后松开
                    drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                    time.sleep(1)
                    drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                    time.sleep(1)
                    drag_mouse(pyautogui.position()[0], pyautogui.position()[1], 0, -165)
                else:
                    print("Setting button not found.")

                time.sleep(1)  # 每次操作后等待7秒

            # 等待25秒后点击endturn按钮
            print("Waiting 25 seconds before clicking Endturn...")
            time.sleep(30)  # 等待25秒

            # 点击endturn按钮
            detect_and_click_button(endturn_image_path)
            print("Endturn button clicked after Setting operations.")

        time.sleep(1)  # 每秒检测一次endturn按钮
    detect_and_click_button(setting_image_path)
    time.sleep(2)  # 等待2秒
    detect_and_click_button(surrender_image_path)
    pyautogui.move(-580, 0)
    time.sleep(6)  # 等待10秒
    while True:
        if detect_and_click_button(continue_image_path):
            time.sleep(3)
            detect_and_click_button(continue_image_path)
            time.sleep(3)
            detect_and_click_button(continue_image_path)
            time.sleep(3)
            detect_and_click_button(continue_image_path)
            time.sleep(3)
            detect_and_click_button(continue_image_path)
            time.sleep(3)
            break
if __name__ == '__main__':
    while True:
        main()

