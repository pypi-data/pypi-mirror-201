from time import sleep
import subprocess
import tkinter
import tkinter.messagebox
import pygame
from enum import Enum, unique
from math import sqrt
from random import randint


@unique
class Color(Enum):
    """颜色"""

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod
    def random_color():
        """获得随机颜色"""
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)


class Ball(object):
    """球"""

    def __init__(self, x, y, radius, sx, sy, color=Color.RED):
        """初始化方法"""
        self.x = x
        self.y = y
        self.radius = radius
        self.sx = sx
        self.sy = sy
        self.color = color
        self.alive = True

    def move(self, screen):
        """移动"""
        self.x += self.sx
        self.y += self.sy
        if self.x - self.radius <= 0 or \
                self.x + self.radius >= screen.get_width():
            self.sx = -self.sx
        if self.y - self.radius <= 0 or \
                self.y + self.radius >= screen.get_height():
            self.sy = -self.sy

    def eat(self, other):
        """吃其他球"""
        if self.alive and other.alive and self != other:
            dx, dy = self.x - other.x, self.y - other.y
            distance = sqrt(dx ** 2 + dy ** 2)
            if distance < self.radius + other.radius \
                    and self.radius > other.radius:
                other.alive = False
                self.radius = self.radius + int(other.radius * 0.146)

    def draw(self, screen):
        """在窗口上绘制球"""
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.radius, 0)


class Test(object):

    def __init__(self, firstname):
        self.__firstname = firstname

    def __test(self):
        print(f'测试了, 打印名字 {self.__firstname}')
        print('__test')

    def __bar(self):
        print(self.__firstname)
        print('方法名字', '__bar')

    def say(self):
        print('公共方法', 'say')


class Clock(object):
    def __init__(self, second, minute, hour):
        self.second = second
        self.minute = minute
        self.hour = hour
        self.check()

    def run(self):
        self.check()

    def check(self):
        self.second += 1
        if self.second == 60:
            self.second = 0
            self.minute += 1
            if self.minute == 60:
                self.minute = 0
                self.hour += 1

    def show(self):
        """显示时间"""
        return '%02d:%02d:%02d' % (self.hour, self.minute, self.second)


class Person(object):
    # __slots__ = ("_age", "gender")

    def __init__(self, age, gender):
        self._age = age
        self._gender = gender

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    @staticmethod
    def personFor():
        return Person(10, 1)


class RubyTool(object):

    @staticmethod
    def readPodfile():
        """
        读取podfile中的依赖库，返回字符串
        """
        ruby_script = """
        require 'cocoapods-core'
        podfile = Pod::Podfile.from_file('Podfile')
        puts podfile.dependencies.map(&:name)
        """
        dependencies = subprocess.check_output(['ruby', '-e', ruby_script]).decode('utf-8').splitlines()
        return dependencies


def main():
    flag = True

    def change_label_test():
        nonlocal flag
        flag = not flag
        (color, msg) = ('red', 'Hello, world!') \
            if flag else ('blue', 'Goodbye, world!')
        label.config(text=msg, fg=color)

    def confirm_to_quit():
        if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗'):
            top.quit()

    # test = Test("你好")
    # test._Test__test()
    # test._Test__bar()
    # test.say()
    # print(test._Test__firstname)
    # person = Person('2',10)
    #
    # person1 = Person.personFor()
    # person1.age = 99
    #
    # person.age = 100
    # print(f'{person.age}')
    # print(f'{person1.age}')
    #
    # print("开始执行了")
    # clock = Clock(59, 59, 23)
    # print(clock.second)
    # while True:
    #     print("开始执行了1111")
    #     clock.show()
    #     sleep(1)
    #     clock.run()
    # dependencies = RubyTool.readPodfile()
    # print(dependencies)
    # 创建顶层窗口
    top = tkinter.Tk()
    # 设置窗口大小
    top.geometry('500x500')
    # 设置窗口标题
    top.title('小游戏')
    # 创建标签对象并添加到顶层窗口
    label = tkinter.Label(top, text='Hello, World', font='Arial -32', fg='red')
    label.pack(expand=1)
    # 创建一个装按钮的容器
    panel = tkinter.Frame(top)
    # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定回调函数
    button1 = tkinter.Button(panel, text='修改', command=change_label_test())
    button1.pack(side='left')
    button2 = tkinter.Button(panel, text='退出', command=confirm_to_quit())
    button2.pack(side='right')
    panel.pack(side='bottom')

    panel2 = tkinter.Frame(top)
    # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定回调函数
    button11 = tkinter.Button(panel2, text='修改', command=change_label_test())
    button11.pack(side='left')
    button21 = tkinter.Button(panel2, text='退出', command=confirm_to_quit())
    button21.pack(side='right')
    panel.pack(side='top')

    tkinter.mainloop()


def main1():
    # 定义用来装所有球的容器
    balls = []
    # 初始化导入的pygame中的模块
    pygame.init()
    # 初始化用于显示的窗口并设置窗口尺寸
    screen = pygame.display.set_mode((800, 600))
    # 设置当前窗口的标题
    pygame.display.set_caption('大球吃小球')
    running = True
    # 开启一个事件循环处理发生的事件
    while running:
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 处理鼠标事件的代码
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 获得点击鼠标的位置
                x, y = event.pos
                radius = randint(10, 100)
                sx, sy = randint(-10, 10), randint(-10, 10)
                color = Color.random_color()
                # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                ball = Ball(x, y, radius, sx, sy, color)
                # 将球添加到列表容器中
                balls.append(ball)
        screen.fill((255, 255, 255))
        # 取出容器中的球 如果没被吃掉就绘制 被吃掉了就移除
        for ball in balls:
            if ball.alive:
                ball.draw(screen)
            else:
                balls.remove(ball)
        pygame.display.flip()
        # 每隔50毫秒就改变球的位置再刷新窗口
        pygame.time.delay(50)
        for ball in balls:
            ball.move(screen)
            # 检查球有没有吃到其他的球
            for other in balls:
                ball.eat(other)


@unique
class Color(Enum):
    """
    颜色
    """
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod
    def random_color():
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)


class Ball(object):
    """球"""

    def __init__(self, x, y, radius, sx, sy, color=Color.RED):
        self.x = x
        self.y = y
        self.radius = radius
        self.sx = sx
        self.sy = sy
        self.color = color
        self.alive = True

    def move(self, screen):
        self.x += self.sx
        self.y += self.sy
        if not self.judgeTheX(screen):
            self.sx = -self.sx
        if not self.judgeTheY(screen):
            self.sy = -self.sy

    def judgeTheX(self, screen):
        """判断开始点的坐标是否合法"""
        return not (self.x - self.radius <= 0 or self.x + self.radius >= screen.get_width())

    def judgeTheY(self, screen):
        """判断开始点的坐标是否合法"""
        return not (self.y - self.radius <= 0 or self.y + self.radius >= screen.get_width())
    #
    # def adjustTheXAndY(self, screen):
    #     offsetx = self.x - self.radius
    #     offsety = self.x + self.radius - screen.get_width()
    #     if offsetx < 0 :
    #         self.x -= offsetx
    #     if offsetx == 0 and self.sx < 0:
    #         self.sx = -self.sx
    #
    #     if offsetx < 0 :
    #         self.x -= offsetx
    #     if offsetx == 0 and self.sx < 0:
    #         self.sx = -self.sx
    #     if not self.judgeTheY(screen):
    #         self.sy = -self.sy

    def eat(self, other: Ball):
        """吃其他球"""
        if self.alive and other.alive and self != other:
            dx, dy = self.x - other.x, self.y - other.y
        distance = sqrt(dx ** 2 + dy ** 2)
        if distance < self.radius + other.radius:
            other.alive = False
            self.radius = self.radius + other.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


def main2():
    pygame.init()
    screeen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('打球吃小球')
    x, y = 50, 50
    running = True
    balls = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.quit():
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                radius = randint(10, 100)
                sx, sy = randint(-10, 10), randint(-10, 10)
                color = Color.random_color()
                ball = Ball(x, y, radius, sx, sy, color)
                balls.append(ball)
        screeen.fill((255, 255, 255))
        # 取出容器中的球 如果没被吃掉就绘制 被吃掉了就移除
        for ball in balls:
            if ball.alive:
                ball.draw(screeen)
            else:
                balls.remove(ball)
        for ball in balls:
            ball.move(screeen)
            # 检查球有没有吃到其他的球
            for other in balls:
                ball.eat(other)

        pygame.display.flip()
        pygame.time.delay(50)
        x, y = x + 5, y + 5


if __name__ == '__main__':
    # main1()
    main2()
