# Краткий обзор класса KUKA (Python)/(User manual):
____
Класс KUKA написан для удобной работы с роботом KUKA youbot с помощью языка программирования Python. В классе есть несколько основных методов для управления роботом.

source: https://github.com/MarkT5/KUKAyoubot_lib
____
## Параметры при создании элемента класса
___ip___ _(str)_: robot ip

___pwd___ _(str)_: password for ssh connection

___ssh___ _(bool)_: whether to connect to SSH or not

___ros___ _(bool)_: force restart of youbot_tl_test on KUKA if true

___offline___ _(bool)_: toggles offline mode (doesn't try to connect to robot)

___read_depth___ _(bool)_: if false doesn't start depth client

___camera_enable___ _(bool)_: enables mjpeg client if True

___advanced___ _(bool)_: disables all safety checks in the sake of time saving

___log___ _[(str), (int)]_: [path, freq] logs odometry and lidar data to set path with set frequency

___read_from_log___ _[(str), (int)]_: [path, freq] streams odometry and lidar data from set log path with set frequency
___
## Основные Методы

___move_arm(...)___ — Sets arm position\n
        ways to set arm position:\n
        array of values: (joint 1, joint 2, joint 3, joint 4, joint 5, grip)\n
        
by keywords:

1. ___m1, m2, m3, m4, m5___ - for joints __(all joint parameters are relative and in degrees from upright position)__
2.    ___grip___ - (0 - 2) for grip
3.    target - ((x, y), ang) to set arm position in cylindrical coordinates (ang - angle from last joint to horizon)
        

___move_base(f, s, ang)___ — принимает:

1. ___f___ — скорость движения вдоль оси по которой направлен робот, если положительное — движение вперёд, если отрицательное — назад,
2. ___s___ — скорость движения поперёк оси по которой направлен робот
3. ___ang___ — угловая скорость
если вызвать этот метод без указания аргументов, то будет отправлена команда остановки

___go_to(x, y, ang)___ — отправляет робота по координатам x, y и задаёт угол от оси x до направления робота (в метрах)



___post_to_send_data(ind, msg)___ — Записывает сообщение msg в ячейку отправки ind (используется другими методами для общения с роботом, но также может использоваться для отправки пользовательских команд, если вызвана с индексом 3. 0 — скорости платформы, 1 — положения манипулятора, 2 — положение захвата)


___arm___ (float[6]) — arm_id, joint 1 - joint 5 

___wheels___ (float[4]) — wheel 1 - wheel 4

___lidar___ _([float[3], float[lidar_resolution]])_— возвращает массив длиной 623 с расстояниями до точек равномерно распределённых от 0 до 240 градусов и данные одометрии скрепленные с этим измерением

___increment___ _(float[3])_ — возвращает массив с положениями по оси x, y и угла от оси x до направления робота

___camera/camera_BGR()___ _(cv2.Mat)_- возвращает изображение в специальном сжатом формате

___depth_camera()___ _(cv2.Mat)_ — возвращает изображение с depth камеры


___
### подробнее - читай dock-string