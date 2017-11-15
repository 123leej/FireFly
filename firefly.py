import pygame
import sys
import math
import random
import time
from pygame.locals import*

VISUALIZE = False
AGENT_A_X = 200
AGENT_B_X = 400
AGENT_Y = 200

if VISUALIZE:
    pygame.init()
    screen = pygame.display.set_mode((600, 400), 0, 32)
ff_list = []


class Firefly:

    def __init__(self, x, y, _brightness):
        self.x = x
        self.y = y
        self.brightness = _brightness
        self.current_len = 0
        self.r = int(math.sqrt(self.brightness / math.pi))
        self.is_agent = False
        if self.r < 1:
            self.r = 1  

    def DrawOnScreen(self):
        if VISUALIZE:
            pygame.draw.circle(screen, pygame.Color(131, 245, 44, 255), (self.x, self.y), self.r, 0)
        else:
            pass

    def Calculations(self):
        delta_x = 0
        delta_y = 0

        for f in ff_list:
            if f != self:
                vector_x = (f.x - self.x)
                vector_y = (f.y - self.y)
                self.current_len = math.sqrt(vector_x**2 + vector_y**2)

                effect_range = 150
                # ?????
                if self.current_len > effect_range:
                    rel_brightness = (f.brightness/self.current_len)
                    vector_x = vector_x/self.current_len
                    vector_y = vector_y/self.current_len
                    delta_x += rel_brightness * vector_x
                    delta_y += rel_brightness * vector_y
                else:
                    delta_x = random.randrange(-2, 3)
                    delta_y = random.randrange(-2, 3)

        if abs(delta_x) < 4 and abs(delta_y) < 4:
            self.x += random.randrange(-3, 4)
            self.y += random.randrange(-3, 4)
        else:
            self.x += int(delta_x) + random.randrange(-1, 2)
            self.y += int(delta_y) + random.randrange(-1, 2)

        if self.x > 600:
            self.x = 600
        if self.x < 0:
            self.x = 0
        if self.y > 400:
            self.y = 400
        if self.y < 0:
            self.y = 0


def find_agent(_ff_list):
    temp = []

    for ff_idx, firefly in enumerate(_ff_list):
        temp.append(firefly.brightness)

    agent_a = temp.index(max(temp))
    temp.remove(max(temp))
    agent_b = temp.index(max(temp))

    if agent_b < agent_a:
        result = [agent_a, agent_b]
    else:
        result = [agent_a, agent_b+1]

    _ff_list[result[0]].is_agent = True
    _ff_list[result[0]].x = AGENT_A_X
    _ff_list[result[0]].y = AGENT_Y

    _ff_list[result[1]].is_agent = True
    _ff_list[result[1]].x = AGENT_B_X
    _ff_list[result[1]].y = AGENT_Y

    return result


def cal_length_from_agent(datas):
    for data in datas:
        x = data[1]
        y = data[2]

        len_from_agentA = int(math.sqrt((x-200)**2 + (y-200)**2))
        len_from_agentB = int(math.sqrt((x-400)**2 + (y-200)**2))

        data.append(len_from_agentA)
        data.append(len_from_agentB)


def set_algorithm(num_node):
    init_data = []

    for i in range(num_node):
        x = int(random.randrange(0, 600))
        y = int(random.randrange(0, 400))

        if i < 2:
            brightness = 100
        else:
            brightness = random.randrange(10, 20)

        ff_list.append(Firefly(x, y, brightness*10))
        init_data.append([i, x, y])

    init_data = find_agent(ff_list) + init_data

    init_data[init_data[0] + 2][1] = AGENT_A_X
    init_data[init_data[0] + 2][2] = AGENT_Y
    init_data[init_data[1] + 2][1] = AGENT_B_X
    init_data[init_data[1] + 2][2] = AGENT_Y

    cal_length_from_agent(init_data[2:])

    return init_data


def run_algorithm():
    data = []
    if VISUALIZE:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color(0, 0, 0, 255))

    for idx, g in enumerate(ff_list):
        if g.is_agent:
            g.DrawOnScreen()
        else:
            g.Calculations()
            g.DrawOnScreen()

        data.append([idx, g.x, g.y])
    time.sleep(0.005)
    cal_length_from_agent(data)
    if VISUALIZE:
        pygame.draw.ellipse(screen, pygame.Color(230, 0, 0), [50, 50, 300, 300], 2)
        pygame.draw.ellipse(screen, pygame.Color(230, 0, 0), [250, 50, 300, 300], 2)

        pygame.display.update()
    return data


if __name__ == "__main__":
    port = int(sys.argv[2])
    init_data = set_algorithm(int(sys.argv[1]))
    # TODO tcp send init_data
    print(init_data)
    # TODO receive ok signal
    while True:
        # TODO udp send to port run_algorithm()
        print(run_algorithm())

# args = node 갯수 , 값 전달할 포트
# 초기 설정해줘야 할 항목 : [[에이전트 노드A_index, 에이전트 노드 B_index], [노드_idx, x, y, agent_A까지 거리, agent_B까지 거리], [노드_idx, x, y, agent_A까지 거리, agent_B까지 거리], ...]
# 이후 계속 업데이트 해줘야 할 항목 : [[노드_idx, x, y, agent_A까지 거리, agent_B까지 거리],[노드_idx, x, y, agent_A까지 거리, agent_B까지 거리],...]
# 초기데이터 인자로 받은 포트로 tcp 전송 후 설정 완료 signal 대기, 업데이트 데이터 인자로 받은 포트로 udp 전송
