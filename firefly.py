import pygame
import sys
import math
import random
# from pygame.locals import*


AGENT_A_X = 200
AGENT_B_X = 400
AGENT_Y = 200

# pygame.init()
# screen = pygame.display.set_mode((600, 400), 0, 32)
ff_list = []


class Firefly:

    def __init__(self, x, y, _brightness, _zone_range):
        self.x = x
        self.y = y
        self.brightness = _brightness
        self.current_len = 0
        self.zone_range = _zone_range
        self.r = int(math.sqrt(self.brightness / math.pi))
        self.is_agent = False
        if self.r < 1:
            self.r = 1  

#    def DrawOnScreen(self):
#        pygame.draw.circle(screen, pygame.Color(131, 245, 44, 255), (self.x, self.y), self.r, 0)

    def Calculations(self):
        delta_x = 0
        delta_y = 0

        for f in ff_list:
            if f != self:
                vector_x = (f.x - self.x)
                vector_y = (f.y - self.y)
                self.current_len = math.sqrt(vector_x**2 + vector_y**2)

                if f.is_agent:
                    effect_range = self.zone_range
                else:
                    effect_range = 50

                if self.current_len > effect_range:
                    rel_brightness = (f.brightness/self.current_len)
                    vector_x = vector_x/self.current_len
                    vector_y = vector_y/self.current_len
                    delta_x += rel_brightness * vector_x
                    delta_y += rel_brightness * vector_y
                else:
                    delta_x = random.randrange(-3, 4)
                    delta_y = random.randrange(-3, 4)

        if abs(delta_x) < 5 and abs(delta_y) < 5:
            self.x += random.randrange(-4, 5)
            self.y += random.randrange(-4, 5)
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
    brightness = [0, 0]
    result = [0, 0]

    for ff_idx, firefly in enumerate(_ff_list):
        for idx, agent in enumerate(brightness):
            if firefly.brightness > agent:
                brightness[idx] = firefly.brightness
                result[idx] = ff_idx
                break

    _ff_list[result[0]].is_agent = True
    _ff_list[result[0]].x = AGENT_A_X
    _ff_list[result[0]].y = AGENT_Y

    _ff_list[result[1]].is_agent = True
    _ff_list[result[1]].x = AGENT_B_X
    _ff_list[result[1]].y = AGENT_Y

    return result


def set_algorithm(num_node, zone_range):
    init_data = []

    for i in range(num_node):
        x = int(random.randrange(0, 600))
        y = int(random.randrange(0, 400))
        brightness = random.randrange(10, 50)
        ff_list.append(Firefly(x, y, brightness*10, zone_range))
        init_data.append([i+1, x, y])

    init_data = find_agent(ff_list) + init_data

    for i in range(1):
        if i == 0:
            init_data[init_data[i]+1][1] = AGENT_A_X
        else:
            init_data[init_data[i]+1][1] = AGENT_B_X
        init_data[init_data[i]+1][2] = AGENT_Y

    return init_data


def run_algorithm():
    while True:
        data = []

        # for event in pygame.event.get():
        #    if event.type == QUIT:
        #        pygame.quit()
        #        sys.exit()

        # screen.fill(pygame.Color(0, 0, 0, 255))

        for idx, g in enumerate(ff_list):
            # if g.is_agent:
                # g.DrawOnScreen()
            # else:
            g.Calculations()
            # g.DrawOnScreen()
            data.append([idx, g.x, g.y])

        print(data)

        # pygame.draw.ellipse(screen, pygame.Color(230, 0, 0), [50, 50, 300, 300], 2)
        # pygame.draw.ellipse(screen, pygame.Color(230, 0, 0), [250, 50, 300, 300], 2)

        # pygame.display.update()


if __name__ == "__main__":
    print(set_algorithm(int(sys.argv[1]), int(sys.argv[2])))

    run_algorithm()

# args = node 갯수 , zone 영향 범위
# 초기 설정해줘야 할 항목 : [[에이전트 노드A_index, 에이전트 노드 B_index], [노드_idx, x, y], [노드_idx, x, y], ...]
# 이후 계속 업데이트 해줘야 할 항목 : [[노드_idx, x, y],[노드_idx, x, y],...]

