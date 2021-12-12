import random
from math import sqrt


class Vector(object):

    def __init__(self, x, y):
        super(Vector, self).__init__()
        self.x, self.y = x, y

    def __add__(self, vector):
        if isinstance(vector, self.__class__):
            return self.__class__(self.x + vector.x, self.y + vector.y)
        return super(Vector, self).__add__(vector)

    def __mul__(self, vector):
        if isinstance(vector, self.__class__):
            return self.__class__(self.x * vector.x, self.y * vector.y)
        return self.__class__(self.x * vector, self.y * vector)

    def __repr__(self):
        return "{0}, {1}".format(self.x, self.y)

    @property
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        _length = self.length
        self.x = self.x / _length
        self.y = self.y / _length


class Bird(object):
    size = 3
    max_speed = 25

    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0)
        super(Bird, self).__init__()

    def step(self, force, keep):
        if keep:
            self.vel = self.vel + force
        else:
            self.vel = force
        if self.vel.length > self.max_speed:
            self.vel.normalize()
            self.vel = self.vel * self.max_speed
        self.pos = self.pos + self.vel

    def check_collide(self, tubes, eagles):
        if (self.pos.y < 0) or (self.pos.y + self.size > Environment.map_size.y):
            return True
        for tube in tubes:
            if self.pos.x + self.size > tube.pos.x and self.pos.x < tube.pos.x + Tube.width:
                if self.pos.y < tube.height or self.pos.y + self.size > tube.height + Tube.gap_size:
                    return True
        for eagle in eagles:
            if eagle.is_alive and (eagle.pos.x < self.pos.x):
                return True
        return False


class Tube(object):
    gap_size = 20
    tube_speed = Vector(-2, 0)
    width = 10
    height_range = (8, 12)

    def __init__(self, pos, height):
        self.pos = pos
        self.height = height
        self.scored = False
        super(Tube, self).__init__()

    def step(self):
        self.pos = self.pos + self.tube_speed

    def distance_to_bird(self, bird):
        return self.pos.x - bird.pos.x


class Eagle(object):
    size = 5
    eagle_speed = Vector(-2, 0)
    height_range = (12, 18)

    def __init__(self, pos, height):
        self.pos = pos
        self.height = height
        self.is_alive = True
        super(Eagle, self).__init__()

    def step(self):
        self.pos = self.pos + self.eagle_speed

    def distance_to_bird(self, bird):
        return self.pos.x - bird.pos.x


class Environment(object):
    map_size = Vector(80, 40)
    object_interval = 30
    gravity = Vector(0, 1)
    jumpforce = Vector(0, -5)
    eagle_probability = 0.5

    def __init__(self, seed=None):
        if seed is None:
            self.random_seed = random.randint(0, 200)
        else:
            self.random_seed = seed

        self.tube_heights = []
        self.eagle_heights = []
        self.reset()
        super(Environment, self).__init__()

    @property
    def action_space(self):
        return [0, 1, 2]

    @property
    def observation_space(self):
        return [
            [-1, Environment.map_size.y - Bird.size + 1],
            [-Bird.max_speed, Bird.max_speed],
            [0, 1],
            [min((-(Tube.width + 1), -(Eagle.size + 1))), Environment.map_size.x],
            [min((Tube.height_range[0], Eagle.height_range[0])), max((Tube.height_range[1], Eagle.height_range[1]))]
        ]

    @property
    def observation_space_size(self):
        return [s[1] - s[0] + 1 for s in self.observation_space]

    @property
    def state(self):
        tubes_sorted = sorted(self.tubes, key=lambda p: p.distance_to_bird(self.bird))
        eagles_sorted = sorted(self.eagles, key=lambda p: p.distance_to_bird(self.bird))

        if (len(self.tubes) == 0) and (len(self.eagles) == 0):
            closest_object_type = None
        elif len(self.tubes) == 0:
            closest_object_type = 'eagle'
        elif len(self.eagles) == 0:
            closest_object_type = 'tube'
        elif eagles_sorted[0].distance_to_bird(self.bird) < tubes_sorted[0].distance_to_bird(self.bird):
            closest_object_type = 'eagle'
        else:
            closest_object_type = 'tube'

        if self.bird.pos.y < 0:
            current_bird_pos = -1
        elif self.bird.pos.y > Environment.map_size.y - Bird.size:
            current_bird_pos = Environment.map_size.y - Bird.size + 1
        else:
            current_bird_pos = self.bird.pos.y

        current_bird_pos = current_bird_pos + 1
        current_bird_vel = self.bird.vel.y + Bird.max_speed

        if closest_object_type == 'tube':
            current_object_dst = tubes_sorted[0].distance_to_bird(self.bird) + Tube.width + 1
            current_object_hgt = tubes_sorted[0].height - Tube.height_range[0]
        elif closest_object_type == 'eagle':
            current_object_dst = eagles_sorted[0].distance_to_bird(self.bird) + (Eagle.size // 2) + 1
            current_object_hgt = eagles_sorted[0].height - Eagle.height_range[0]
        else:
            current_object_dst = Environment.map_size.x
            current_object_hgt = 0

        return current_bird_pos, current_bird_vel, (1 if closest_object_type == 'bird' else 0), \
               current_object_dst, current_object_hgt

    def is_valid_state(self, value):
        ret = True
        for i, v in enumerate(value):
            ret = ret and (v >= self.observation_space[i][0] and v <= self.observation_space[i][1])
        return ret

    def spawn_object(self):
        if random.random() < Environment.eagle_probability:
            eagle_height = self.rnd.randint(*Eagle.height_range)
            self.eagles.append(Eagle(Vector(Environment.map_size.x, 0), eagle_height))
        else:
            tube_height = self.rnd.randint(*Tube.height_range)
            self.tubes.append(Tube(Vector(Environment.map_size.x, 0), tube_height))

    def step(self, action):
        assert action in self.action_space

        reward = 0
        shot_height = None

        if not self.done:
            self.step_counter += 1

            if action == 0:
                self.bird.step(Environment.gravity, keep=True)
            elif action == 1:
                self.bird.step(Environment.jumpforce, keep=False)
            elif action == 2:
                shot_height = self.bird.pos.y
                self.bird.step(Environment.gravity, keep=True)

            if self.step_counter % Environment.object_interval == 0:
                self.spawn_object()

            for tube in self.tubes:
                tube.step()

                if tube.pos.x + Tube.width < self.bird.pos.x and not tube.scored:
                    tube.scored = True
                    reward = 1.0

            self.tubes = list(filter(lambda tube: not tube.scored, self.tubes))

            if shot_height is not None:
                hit = False
                if len(self.eagles) > 0:
                    eagles_sorted = sorted(self.eagles, key=lambda p: p.distance_to_bird(self.bird))
                    if (shot_height < (eagles_sorted[0].height + Bird.size)) and \
                            (shot_height > (eagles_sorted[0].height - (Eagle.size + Bird.size))):
                        eagles_sorted[0].is_alive = False
                        hit = True
                        reward = 1.0
                # for eagle in self.eagles:
                #     if abs(shot_height - eagle.height) < Eagle.size:
                #         eagle.is_alive = False
                #         hit = True
                #         reward = 1.0
                if not hit:
                    reward = -0.25

            for eagle in self.eagles:
                eagle.step()

            self.eagles = list(filter(lambda eagle: eagle.is_alive, self.eagles))

            if self.bird.check_collide(self.tubes, self.eagles):
                reward = -1.0
                self.done = True

        return (self.state, reward, self.done,
                {
                    'bird': {
                        'pos': self.bird.pos,
                        'size': Bird.size
                    },
                    'tubes': {
                        'list': list(map(lambda tube: (tube.pos.x, tube.height), self.tubes)),
                        'width': Tube.width,
                        'gapsize': Tube.gap_size
                    },
                    'eagles': {
                        'list': list(map(lambda eagle: (eagle.pos.x, eagle.height), self.eagles)),
                        'size': Eagle.size
                    },
                    'shot_fired': shot_height is not None
                })

    def reset(self):
        self.rnd = random.Random(self.random_seed)
        self.bird = Bird(Vector(10, Environment.map_size.y // 2))
        self.step_counter = 0
        self.tubes = []
        self.eagles = []
        self.spawn_object()
        self.done = False

        return self.state
