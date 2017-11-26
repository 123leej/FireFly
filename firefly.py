import sys
import math
import random
import time

AGENT_A_X = 255
AGENT_B_X = 506
AGENT_Y = 205

ff_list = []


class Firefly:

    def __init__(self, x, y, _brightness, _zone_effect_range):
        self.x = x
        self.y = y
        self.brightness = _brightness
        self.zone_effect_range = _zone_effect_range
        self.current_len = 0
        self.r = int(math.sqrt(self.brightness / math.pi))
        self.is_agent = False
        if self.r < 1:
            self.r = 1

    def Calculations(self):
        delta_x = 0
        delta_y = 0

        for f in ff_list:
            if f != self:
                vector_x = (f.x - self.x)
                vector_y = (f.y - self.y)
                self.current_len = math.sqrt(vector_x**2 + vector_y**2)

                if self.is_agent:
                    zone_range = self.zone_effect_range
                else:
                    zone_range = 50

                if self.current_len > zone_range:
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

        if self.x > 761:
            self.x = 761
        if self.x < 0:
            self.x = 0
        if self.y > 411:
            self.y = 411
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

        len_from_agentA = int(math.sqrt((x-AGENT_A_X)**2 + (y-AGENT_Y)**2))
        len_from_agentB = int(math.sqrt((x-AGENT_B_X)**2 + (y-AGENT_Y)**2))

        data.append(len_from_agentA)
        data.append(len_from_agentB)


def set_algorithm(num_node, zone_range):
    init_data = []
    agent_a = random.randrange(0, num_node)
    agent_b = random.randrange(0, num_node)

    while True:
        if agent_a != agent_b:
            break
        agent_b = random.randrange(0, num_node)

    for i in range(num_node):
        x = int(random.randrange(0, 761))
        y = int(random.randrange(0, 411))

        if i is agent_a or i is agent_b:
            brightness = 100
        else:
            brightness = random.randrange(10, 20)

        ff_list.append(Firefly(x, y, brightness*10, zone_range))
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

    for idx, g in enumerate(ff_list):
        if not g.is_agent:
            g.Calculations()

        data.append([idx, g.x, g.y])
    time.sleep(0.005)
    cal_length_from_agent(data)

    return data


if __name__ == "__main__":

    init_data = set_algorithm(int(sys.argv[1]), int(sys.argv[2]))
    print(init_data)

    while True:
        print(run_algorithm())


# args = node 갯수 , zone_range
# node_data = [노드_idx, x, y, agent_A까지 거리, agent_B까지 거리]
# 초기 설정해줘야 할 항목 : [에이전트 노드A_index, 에이전트 노드 B_index, node_data1, node_data2, node_data3, node_data4,....]
# 이후 계속 업데이트 해줘야 할 항목 : [node_data1, node_data2, node_data3, node_data4, ....]
# 초기 설정해줘야 할 항목 및 계속 업데이트 해줘야 할 항목은 터미널에서 실행했을때 값을 print 로 찍어내면 됨
# ex) (에이전트노드가 각각 0, 1 인덱스라고 할때)
# [0, 1, [0, x, y, 0, n], [1, x, y, n, 0], [2, x, y, n, n], [3, x, y, n, n], [4, x, y, n, n], [5, x, y, n, n],...]
# [[0, x, y, 0, n], [1, x, y, n, 0], [2, x, y, n, n], [3, x, y, n, n], [4, x, y, n, n], [5, x, y, n, n],...]
# [[0, x, y, 0, n], [1, x, y, n, 0], [2, x, y, n, n], [3, x, y, n, n], [4, x, y, n, n], [5, x, y, n, n],...]
# [[0, x, y, 0, n], [1, x, y, n, 0], [2, x, y, n, n], [3, x, y, n, n], [4, x, y, n, n], [5, x, y, n, n],...]
# [[0, x, y, 0, n], [1, x, y, n, 0], [2, x, y, n, n], [3, x, y, n, n], [4, x, y, n, n], [5, x, y, n, n],...]
# ...
#
# 화면 크기는 width = 761, height = 411
