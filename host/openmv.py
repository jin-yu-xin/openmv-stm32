import sensor
import image
import time
import math
from pid import PID
from pyb import Servo
from pyb import UART
from pyb import Pin
uart = UART(3, 19200)
pan_servo = Servo(1)
tilt_servo = Servo(2)
p_in1 = Pin('P1', Pin.IN, Pin.PULL_UP)
Det_Mode = 1
target = 0
target_ball = 0
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 图像分辨率160x120
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()
change_times = 0
def get_uart_data(uart):
    str_1 = uart.read()
    str_1 = str(str_1)
    str_1 = list(str_1)
    str_1 = str_1[2:5]
    s = "".join(str_1)
    s_1 = 0.0
    if(s != "ne"):
        s_1 = float(s)
    return s_1
def grade_mode(list):
    list_set = set(list)
    frequency_dict = {}
    for i in list_set:
        frequency_dict[i] = list.count(i)
    grade_mode = []
    for key, value in frequency_dict.items():
        if value == max(frequency_dict.values()):
            grade_mode.append(key)
    return grade_mode
grade_list = [100, 98, 87, 65, 82, 99, 92, 99, 100]
grade_mode(grade_list)
def Key_Down(p_in):
    global change_times
    key = p_in.value()
    if key == 1 and change_times != 1:
        change_times += 1
    if change_times == 1:
        key = p_in.value()
        if key == 0:
            change_times += 1
    if change_times == 2:
        change_times = 0
        print('！！！！！！！！domn!!!!!')
        return 1
center_in_canvas = [0, 0]
def Mode_Control(pin1):
    global Det_Mode
    key1_down = 0
    key1_down = Key_Down(pin1)
    if key1_down:
        Det_Mode += 1
        if Det_Mode == 3:
            Det_Mode = 0
    key2_down = Key_Down(pin2)
    key3_down = Key_Down(pin3)
    if (Det_Mode == 3):
        if key2_down:
            oringin[0] = oringin[0] + 1
        if key3_down:
            oringin[0] = oringin[0] - 1
def get_suit_window(d_0, l_0, dalta_d, orignal):
    pixel_length = d_0 * l_0 / (d_0 + dalta_d)
    h = (pixel_length / l_0) * orignal[1]
    orignal = [orignal[0] - (pixel_length) / 2, orignal[1] - h/2]
    rec_owm = [int(orignal[0]), int(orignal[1]),
               int(pixel_length), int(h)]
    return rec_owm
def get_triangle_pixel(d_0, l_0, dalta_d):
    pixelm = d_0*l_0 / (d_0 + dalta_d)  # 白板移动dalta_d后再图像中的像素长度
    tri_pixel = pixelm * 0.354
    return tri_pixel
def is_triangle(line_list, l_triangle):
    tolorence = 4
    candinate_list = []
    for i in line_list:
        if(i[4] > (l_triangle - tolorence) and i[4] < (l_triangle + tolorence)):
            candinate_list.append(i)
        else:
            pass
    better_candinate_line = []
    # 所有检测到的直线进行两两配对 判断是否为同一个三角形的两个边
    for i in range(0, len(candinate_list)):
        for j in range(i+1, len(candinate_list)):
            x_0 = (candinate_list[i][0] + candinate_list[i][2])/2.0
            y_0 = (candinate_list[i][1] + candinate_list[i][3])/2.0
            x_1 = (candinate_list[j][0] + candinate_list[j][2])/2.0
            y_1 = (candinate_list[j][1] + candinate_list[j][3])/2.0
            distance = math.sqrt((x_1 - x_0)*(x_1 - x_0) +
                                 (y_1 - y_0)*(y_1 - y_0))
            # 根据两边中点的距离是否在规定范围内判断是否为同一个等边三角形的两边
            if(distance > (l_triangle - tolorence)/2.0 and distance < (l_triangle + tolorence)/2.0):
                better_candinate_line.append(candinate_list[i])
                better_candinate_line.append(candinate_list[j])
    return better_candinate_line
def choose_correct_line(d_0, l_0, dalta_d, checked_line):
    l_triangle = get_triangle_pixel(d_0, l_0, dalta_d)
    line_first_check = is_triangle(checked_line, l_triangle)
    return line_first_check
def calculate_triangle_center(ideal_line):
    center = []
    center_point = []
    real_center = []
    dis_tolorance = 3
    if(len(ideal_line) >= 3):
        for i in ideal_line:
            x_0 = (i[0] + i[2])/2.0
            y_0 = (i[1] + i[3])/2.0
            linshi = [x_0, y_0]
            center.append(linshi)
    print(center)
    if(len(center) >= 3):
        for i in range(0, len(center)):
            for j in range(i+1, len(center)):
                # 两边中点横坐标的距离或纵坐标的距离要满足大于dis_tolorance 两点横纵坐标距离太近认为无法构成等边三角形
                if(abs(center[i][0]-center[j][0]) > dis_tolorance or abs(center[i][1]-center[j][1]) > dis_tolorance):
                    if(len(real_center) != 2):
                        real_center.append(center[i])
                        real_center.append(center[j])
    # real_center 存储等边三角形其中两条边的中点坐标
    print(real_center)
    if(len(real_center) == 2):
        # 根据两条边的中点坐标求等边三角形的中心点坐标
        center_point = [(real_center[0][0]+real_center[1][0]) /
                        2.0, (real_center[0][1]+real_center[1][1])/2.0]
        center_point = [int(center_point[0]), int(center_point[1])]
    return center_point
circle_1 = 0
def cir_det(img):
    global circle_1
    global target_ball
    global Det_Mode
    circle_1 = img.find_circles(threshold=3000, x_margin=10,
                                y_margin=10, r_margin=10, r_min=2, r_max=100, r_step=2)
    if circle_1:
        circle_1 = circle_1[0]
        img.draw_circle(circle_1.x(), circle_1.y(), circle_1.r(),
                        color=(255, 0, 0))
        img.draw_cross(circle_1.x(), circle_1.y())
    if circle_1 and Det_Mode == 1:  # 检测平面标准圆
        print('circle_1 done')
        return 1
    elif circle_1 and Det_Mode == 2: # 检测球体
        target_ball = ball_det(circle_1)
        return 1
rectangle_1 = 0
def rec_det(img, rec):
    global target
    global rectangle_1
    thresholds = (80, 100, -6, 5, -9, 4)
    img = img.binary([thresholds], invert=False, zero=True)
    rectangle_1 = img.find_rects(
        rec, threshold=10000)
    if rectangle_1 and Det_Mode == 1:
        return 3
ideal_line = []
center_point = 0
def tri_det(img, rec):
    img.draw_rectangle(rec)
    rec = [rec[0]-2, rec[1]-2, rec[2]-4, rec[3]-4]
    checked_line = img.find_line_segments(
        rec, merge_distance=10, max_theta_diff=20)  # 在感兴趣的rec范围内使用霍夫变换来查找线段
    line_first_check = choose_correct_line(d_0, l_0, dalta_d, checked_line)
    if(len(line_first_check) >= 1 and len(ideal_line) < 3):
        for i in line_first_check:
            ideal_line.append(i)
    if(len(ideal_line) > 6):
        ideal_line.clear()
    global center_point
    center_point = calculate_triangle_center(ideal_line)
    if(len(ideal_line) >= 1):
        return 2
def ball_det(circle_1):
    if circle_1 != 0:
        print('circle_1 done', circle_1)
        return 1
def key_scan(key):
    return key
def target_choose(key, img, rec):
    t = 0
    t = cir_det(img)
    if t:
        return t
    t = tri_det(img, rec)
    if t:
        return t
    t = rec_det(img, rec)
    if t:
        return t
def target_choose2(key, img, rec):
    t = 0
    t = cir_det(img)
    threshold = (20,50) # Lab 这里只设置L（明度）的范围20~50
    if t:
        uart.write("A"+str(get_uart_data(uart)-30)+",C"+str(0)+",BBasketBall,D"+str(0)+\
                   ",E" + str(0) + ",\r\n")
        return t
    sensor.set_pixformat(sensor.GRAYSCALE)
    for blob in img.find_blobs([threshold],roi=[43,22,57,40] ,pixels_threshold=1, area_threshold=1, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        if blob :
            uart.write("A"+str(get_uart_data(uart)-20)+",C"+str(0)+",BFootBall,D"+str(0)+\
                       ",E" + str(0) + ",\r\n")
            return 2
        else :
            uart.write("A"+str(get_uart_data(uart)-20)+",C"+str(0)+",BVolliBall,D"+str(0)+\
                       ",E" + str(0) + ",\r\n")
            return 3
def matrix_mul(mid_point):
    global matrix_homography
    real_mid_point = [0, 0, 0]
    real_mid_point[0] = matrix_homography[0][0]*mid_point[0] + \
        matrix_homography[0][1]*mid_point[1] + \
        matrix_homography[0][2]*mid_point[2]
    real_mid_point[1] = matrix_homography[1][0]*mid_point[0] + \
        matrix_homography[1][1]*mid_point[1] + \
        matrix_homography[1][2]*mid_point[2]
    real_mid_point[2] = matrix_homography[2][0]*mid_point[0] + \
        matrix_homography[2][1]*mid_point[1] + \
        matrix_homography[2][2] * mid_point[2]
    return real_mid_point
def angle_cal_pixel_to_m(k, d_0, l_0, dalta_d, oringin, center):
    pixel_length = k * d_0 * l_0 / (d_0 )
    if center and oringin:
        dlta = [center[0] - oringin[0], center[1] - oringin[1]]
        real_point = [dlta[0]/pixel_length, -dlta[1]/pixel_length]
        return real_point
    else:
        k = [0,0]
        return k
def calibration_laser_light(d_0, l_0, dalta_d, oringin):
    L = d_0
    x_0 = 0.035
    y_0 = -0.240
    pixel_length = d_0 * l_0 / (d_0 + dalta_d)
    p_x = -0 * x_0 / d_0 * pixel_length
    p_y = 0 * y_0 / d_0 * pixel_length
    dynamic_laser_oringin = [oringin[0] + p_x, oringin[1] + p_y]
    dlta = [oringin[0]-dynamic_laser_oringin[0], oringin[1] -
            dynamic_laser_oringin[1]]
    real_point = [dlta[0]/pixel_length, -dlta[1] /
                  pixel_length]
    xr = real_point[0]
    yr = real_point[1]
    angle_x = math.atan(xr / L) / 3.1415 * 180
    angle_y = math.atan(yr / math.sqrt(L * L + xr * xr)) / 3.1415 * 180
    angle = [angle_x, angle_y]
    return angle
# 用于标定
oringin = [80, 50]
d_0 = 1.905 # 最初将白板放置在距离摄像头d_0的距离处  
l_0 = 66 # 白板距摄像头d_0时 在图像中的像素长度
dalta_d = 0 # 白板前后移动的距离
# 假设白板实际长度为H米 摄像头的焦距为f 则：
# l_0/H = f/d_0
# 白板移动dalta_d后：l_1/H = f/(d_0 + dalta_d)
# 两等式相处得到：
# l_1 = l_0 * d_0 / (d_0 + dalta_d) 即可计算出白板移动后在图像中的像素长度
def angle_cal(k, shape):
    global d_0
    global oringin
    global l_0
    global dalta_d
    print('shape', shape)
    if shape != 0:
        angle = []
        point = []
        if not shape:
            return[[0,0],[0,0]]
        else:
            x = shape[0]
            y = shape[1]
            point = [x, y]
        real_point = angle_cal_pixel_to_m(k ,d_0, l_0, dalta_d, oringin, point)
        xr = real_point[0]
        yr = real_point[1]
        angle_x = math.atan(xr / d_0) / 3.1415 * 180
        angle_y = math.atan(yr / math.sqrt(d_0 * d_0 + xr * xr)) / 3.1415 * 180
        angle = [angle_x, angle_y]
        angle_calibration = calibration_laser_light(d_0, l_0, dalta_d, oringin)
        angle_all = [angle, angle_calibration]
        return angle_all
def auto_get_orignal(d_0, l_0, dalta_d, orignal, dalta_hor):
    pixel_length = d_0 * l_0 / (d_0 + dalta_d)
    dalta_x_y = (-0.057*dalta_d, 0.028*dalta_d)
    print('dalta_x_ys', dalta_x_y)
    orignal = [orignal[0] + dalta_hor +
               dalta_x_y[0], orignal[1] + dalta_x_y[1]]
    return orignal
def get_suit_window(d_0, l_0, dalta_d, orignal):
    pixel_length = d_0 * l_0 / (d_0 + dalta_d)
    h = (pixel_length / l_0) * orignal[1]
    orignal = [orignal[0] - (pixel_length) / 2, orignal[1] - h/2]
    rec_owm = [int(orignal[0]-2), int(orignal[1]-2),
               int(pixel_length-4), int(h-4)]
    return rec_owm
def get_real_mess(d_0, l_0, dalta_d, oringin, shape):
    real_mess = [0, 0, 0, 0]
    pixel_length = d_0 * l_0 / (d_0 + dalta_d)
    h = (pixel_length / l_0) * oringin[1]
    oringin = auto_get_orignal(d_0, l_0, dalta_d, oringin, 0)
    real_point = angle_cal_pixel_to_m(d_0, l_0, dalta_d, oringin, shape)
    real_mess[0] = real_point[0]
    real_mess[1] = real_point[1]
    real_mess[2] = shape.w() / pixel_length
    real_mess[3] = shape.r() / pixel_length
    if shape.w():
        real_mess[2] = shape.w() / pixel_length
    elif shape.r():
        real_mess[2] = shape.r() / pixel_length
    if shape.h():
        real_mess[3] = shape.h() / pixel_length
    elif shape.r():
        real_mess[3] = shape.r() / pixel_length
dalta_d = 0
rec = get_suit_window(d_0, l_0, dalta_d, oringin)
rec = [10, 10, 140, 80]
dalta_d = 0
target_list = []
final_target = 0
count = 0
while (True):
    if Key_Down(p_in1) :
        Det_Mode = Det_Mode + 1
        if Det_Mode == 3:
            Det_Mode = 0
    u_data = 0
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8) # 畸变矫正 去除图像鱼眼效果
    target_x = 0
    if Det_Mode == 1: # 检测平面几何
        target_x = target_choose(1, img, rec) # 按照圆、三角形、矩形的顺序进行检测（按照检测的难易程度）
        if target_x != None:
            target_list.append(target_x)
    elif Det_Mode == 2: # 检测球体 篮球、足球、排球
        target_x = target_choose2(1, img, rec)
        if target_x:
            final_target = 0
    if len(target_list) > 14:
        target_list.clear()
    if len(target_list) > 7:
        final_target = grade_mode(target_list)
        final_target = final_target[0]
    if final_target == 1:  # 被检测出数量最多的物体形状 1：圆形
        if circle_1:
            k = circle_1[2]*2/24.0
            if(circle_1[2]*2 < 12):
                k = 55/66.0
            pixel_length = k*  d_0 * l_0 / (d_0 + dalta_d)
            angle = angle_cal(k, circle_1)
            real_point = angle_cal_pixel_to_m(
                k, d_0, l_0, dalta_d, oringin, circle_1)
            d = d_0/k
            s = real_point[0]*real_point[0] + real_point[1]*real_point[1]
            distance = math.sqrt(s + d*d)
            real_mess = [0, 0, 0, 0, 0]
            real_mess[0] = real_point[0]
            real_mess[1] = real_point[1] - 0.1
            real_mess[2] = 2*circle_1.r() / pixel_length
            real_mess[3] = 2*circle_1.r() / pixel_length
            real_mess[4] = distance
            pan_angle = angle[1][0] + angle[0][0]
            if(pan_angle > 0):
                pan_angle = pan_angle - 1
            if(pan_angle < 0):
                pan_angle = pan_angle
            pan_servo.angle(-0.5 - pan_angle)
            time.sleep(500)
            tile_degree = angle[1][1] + angle[0][1]
            if(tile_degree < 0):
                tile_degree = tile_degree + 0.6
            if(tile_degree > 0):
                tile_degree = tile_degree + 0.4
            tilt_servo.angle(2.1 - tile_degree)
            print("circle_done", angle)
            print("ertsdghhkl",real_mess)
            uart = UART(3, 19200)
            uart.write("A"+str(real_mess[2]*100)+",C"+str(real_mess[4]*100)+",Bcircle,D"+str(real_mess[0]*100) +
                       ",E" + str(real_mess[1]*100) + ",\r\n")
    elif final_target == 3: # 矩形
        if rectangle_1:
            if(isinstance(rectangle_1 ,int)):
                pass
            else:
                rectangle_1 = rectangle_1[0]
            list_rec = []
            if not rectangle_1 or isinstance(rectangle_1 ,int):
                list_rec = [0, 0]
            else:
                list_rec = [rectangle_1[0] + int(rectangle_1[3]/2), rectangle_1[1] + int(rectangle_1[3]/2)]
                k = rectangle_1[3]/24
                if(rectangle_1[3] < 10):
                    k = 55/66.0
                pixel_length = k* d_0 * l_0 / (d_0 + dalta_d)
                angle = angle_cal(k, list_rec)
                real_mess = [0, 0, 0, 0, 0]
                real_point = angle_cal_pixel_to_m(
                    k, d_0, l_0, dalta_d, oringin, list_rec)
                d = d_0/k
                s = real_point[0]*real_point[0] + real_point[1]*real_point[1]
                distance = math.sqrt(s + d*d)
                real_mess[0] = real_point[0]
                real_mess[1] = real_point[1] - 0.1
                real_mess[2] = 2*rectangle_1.w() / pixel_length
                real_mess[3] = 2*rectangle_1.h() / pixel_length
                real_mess[4] = distance
                pan_angle = angle[1][0] + angle[0][0]
                if(pan_angle > 0):
                    pan_angle = pan_angle - 1
                if(pan_angle < 0):
                    pan_angle = pan_angle
                pan_servo.angle(-0.5 - pan_angle)
                time.sleep(500)
                tile_degree = angle[1][1] + angle[0][1]
                if(tile_degree < 0):
                    tile_degree = tile_degree + 0.6
                if(tile_degree > 0):
                    tile_degree = tile_degree + 0.4
                tilt_servo.angle(2.1 - tile_degree)
                img.draw_rectangle(rectangle_1.rect(), color=(0, 255, 0))
                uart.write("A"+str(real_mess[2]*100)+",C"+str(real_mess[4]*100)+",Brectangle,D"+str(real_mess[0]*100) +
                           ",E" + str(real_mess[1]*100) + ",\r\n")
    elif final_target == 2: # 三角形
        real_mess = [0, 0, 0, 0, 0]
        k = 1
        if  len(ideal_line)>=3 :
            k_len = ideal_line[2][4]
            k = k_len/24
            if k_len<10:
                k = 55/66.0
        pixel_length = k*  d_0 * l_0 / (d_0 + dalta_d)
        angle = angle_cal(k, center_point)
        real_point = angle_cal_pixel_to_m(
            k, d_0, l_0, dalta_d, oringin, center_point)
        d = d_0/k
        s = real_point[0]*real_point[0] + real_point[1]*real_point[1]
        distance = math.sqrt(s + d*d)
        if real_point and len(ideal_line)>=3 :
            real_mess[0] = real_point[0]
            real_mess[1] = real_point[1] - 0.1
            real_mess[2] = 2*ideal_line[1].length() / pixel_length
            real_mess[3] = 2*ideal_line[2].length() / pixel_length
            real_mess[4] = distance
        pan_angle = angle[1][0] + angle[0][0]
        if(pan_angle > 0):
            pan_angle = pan_angle - 1
        if(pan_angle < 0):
            pan_angle = pan_angle
        pan_servo.angle(-0.5 - pan_angle)
        time.sleep(500)
        tile_degree = angle[1][1] + angle[0][1]
        if(tile_degree < 0):
            tile_degree = tile_degree + 0.6
        if(tile_degree > 0):
            tile_degree = tile_degree + 0.4
        tilt_servo.angle(2.1 - tile_degree)
        for i in ideal_line:
            img.draw_line(i.line(), color=(255, 0, 0))
        uart.write("A"+str(real_mess[2]*100)+",C"+str(real_mess[4]*100)+",Btriangle,D"+str(real_mess[0]*100) +
                   ",E" + str(real_mess[1]*100) + ",\r\n")
    else:
        pass
