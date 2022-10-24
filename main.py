import sqlite3
import sys
import random
from Button import Button

import pygame as pygame
from pygame.locals import *
from pygame import mixer_music

clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 1, 512)  # prevent sound delay
pygame.init()
pygame.mixer.init()

width, height = 1280, 720

# creating window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Hardcore Hardware")

# loading buttons
play_image = pygame.image.load('play-button.png').convert_alpha()
instructions_image = pygame.image.load('instructions.png').convert_alpha()
leaderboard_image = pygame.image.load('leaderboard.png').convert_alpha()
quit_image = pygame.image.load('quit.png').convert_alpha()

# creating button instances for menu screen
menu_playButton = Button(120, 400, play_image, 0.9)
menu_instructionsButton = Button(410, 400, instructions_image, 0.9)
menu_leaderboardButton = Button(700, 400, leaderboard_image, 0.9)
menu_quitButton = Button(990, 400, quit_image, 0.9)

# creating instances for play button on instructions screen
instructions_playButton = Button(550, 525, play_image, 0.9)

# creating instances for buttons on game over screen
gameover_playButton = Button(200, 450, play_image, 0.9)
gameover_leaderboardButton = Button(590, 450, leaderboard_image, 0.9)
gameover_quitButton = Button(990, 450, quit_image, 0.9)

# loading game over background
game_over_bg = pygame.transform.scale(pygame.image.load('gameover_bg.png'), (width, height))

# game background
game_bg = pygame.image.load('game_bg.jpeg')
game_bg = pygame.transform.scale(game_bg, (width, height))

# menu background
menu_bg = pygame.image.load('menu_bg.jpeg')
menu_bg = pygame.transform.scale(menu_bg, (width, height))
# player image
player = pygame.transform.scale(pygame.image.load('tank.png'), (125, 125))

# shell image
shell = pygame.transform.scale(pygame.image.load('bullet.png'), (50, 70))

# colours
red = pygame.color.Color('#E32671')
white = pygame.color.Color('#FFFFFF')
black = pygame.color.Color('#000000')

# constants
player_health = 3
hardware_kill_count = 0
hardware_width = 50
server_width = 100
cpu_width = 70
phones = []  # empty as it starts off as 0 and is then appended
tvs = []
ipads = []
consoles = []
servers = []
cpus = []
hardware_health = 2
bonusHardware_health = 4

# hardware images
phone_hardware = pygame.transform.scale(pygame.image.load('phone.png'), (hardware_width, hardware_width))
tv_hardware = pygame.transform.scale(pygame.image.load('television.png'), (hardware_width, hardware_width))
ipad_hardware = pygame.transform.scale(pygame.image.load('tablet.png'), (hardware_width, hardware_width))
console_hardware = pygame.transform.scale(pygame.image.load('ps4.png'), (hardware_width, hardware_width))
server_bonus = pygame.transform.scale(pygame.image.load('server.png'), (server_width, server_width))
cpu_bonus = pygame.transform.scale(pygame.image.load('cpu.png'), (cpu_width, cpu_width))


class Game_bg1(pygame.sprite.Sprite):
    """
    Creating a constantly looping background
    """

    def __init__(self, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = game_bg
        self.rect = self.image.get_rect()  # figures out rectangle based on image
        self.rect.center = (640, h / 2)
        self.scrolling_speed = 5
        self.height = 720

    def update(self):
        if self.rect.y > self.height:
            self.rect.y = -self.height
        else:
            self.rect.y += self.scrolling_speed


class Player(pygame.sprite.Sprite):
    """
    Creating the Player class
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = (1280 / 2, 720 / 1.1)
        self.shell_delay = 20
        self.count = 0

    def update(self):
        """
        Updating the class with movement of Player and events that take place when hardware and player collide
        :return:
        """
        global player_health
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.x < 1280 - hardware_width:
            self.rect.x += 15
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 15

        self.count += 1  # adds a delay to the shell if it is held down
        if keys[pygame.K_SPACE] and self.count % self.shell_delay == 0:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('shell.wav'))
            all_sprites.add(Shell())  # space bar adds a shell sprite every time it is pressed

            # when hardware hits the player
            for phone in phones:
                """
                'phones' is a list, same applies for all other hardware in this class
                """
                if pygame.sprite.collide_rect(self, phone):
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('tank_hit.wav'))
                    phones.remove(phone)
                    all_sprites.remove(phone)
                    player_health -= 1

            for tv in tvs:
                if pygame.sprite.collide_rect(self, tv):
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('tank_hit.wav'))
                    tvs.remove(tv)
                    all_sprites.remove(tv)
                    player_health -= 1

            for ipad in ipads:
                if pygame.sprite.collide_rect(self, ipad):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('tank_hit.wav'))
                    ipads.remove(ipad)
                    all_sprites.remove(ipad)
                    player_health -= 1

            for console in consoles:
                if pygame.sprite.collide_rect(self, console):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('tank_hit.wav'))
                    consoles.remove(console)
                    all_sprites.remove(console)
                    player_health -= 1

            for server in servers:
                if pygame.sprite.collide_rect(self, server):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('tank_hit.wav'))
                    servers.remove(server)
                    all_sprites.remove(server)
                    player_health -= 1

            for cpu in cpus:
                if pygame.sprite.collide_rect(self, cpu):
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('tank_hit.wav'))
                    cpus.remove(cpu)
                    all_sprites.remove(cpu)
                    player_health -= 1


class Shell(pygame.sprite.Sprite):
    """
    Creating the shell class
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shell
        self.rect = self.image.get_rect()  # figures out rectangle hit box based on image
        self.rect.center = player.rect.center
        self.shell_vel = 15

    def update(self):
        """
        Updating the class with events that take place when hardware and shell collide
        :return:
        """
        global hardware_kill_count
        self.rect.y -= self.shell_vel

        # if a shell collides with a hardware, the shell will disappear
        for phone in phones:
            """
            'phones' is a list, same applies for all the other hardware in this class
            """
            if pygame.sprite.collide_rect(self, phone):
                phone.health -= 1
                all_sprites.remove(self)  # removes shell after it hits the hardware
                if phone.health < 1:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hardware_destroyed.wav'))
                    phones.remove(phone)
                    all_sprites.remove(phone)
                    phones_Destroyed.append(phone)
                    hardware_kill_count += 1
                else:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('hardware_hit.wav'))

        for tv in tvs:
            if pygame.sprite.collide_rect(self, tv):
                tv.health -= 1
                all_sprites.remove(self)
                if tv.health < 1:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hardware_destroyed.wav'))
                    tvs.remove(tv)
                    all_sprites.remove(tv)
                    tvs_Destroyed.append(tv)
                    hardware_kill_count += 1
                else:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('hardware_hit.wav'))

        for ipad in ipads:
            if pygame.sprite.collide_rect(self, ipad):
                ipad.health -= 1
                all_sprites.remove(self)
                if ipad.health < 1:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hardware_destroyed.wav'))
                    ipads.remove(ipad)
                    all_sprites.remove(ipad)
                    ipads_Destroyed.append(ipad)
                    hardware_kill_count += 1
                else:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('hardware_hit.wav'))

        for console in consoles:
            if pygame.sprite.collide_rect(self, console):
                console.health -= 1
                all_sprites.remove(self)
                if console.health < 1:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hardware_destroyed.wav'))
                    consoles.remove(console)
                    all_sprites.remove(console)
                    consoles_Destroyed.append(console)
                    hardware_kill_count += 1
                else:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('hardware_hit.wav'))

        for server in servers:
            if pygame.sprite.collide_rect(self, server):
                server.health -= 1
                all_sprites.remove(self)
                if server.health < 1:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hardware_destroyed.wav'))
                    servers.remove(server)
                    all_sprites.remove(server)
                    servers_Destroyed.append(server)
                    hardware_kill_count += 5
                else:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('hardware_hit.wav'))

        for cpu in cpus:
            if pygame.sprite.collide_rect(self, cpu):
                cpu.health -= 1
                all_sprites.remove(self)
                if cpu.health < 1:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hardware_destroyed.wav'))
                    cpus.remove(cpu)
                    all_sprites.remove(cpu)
                    cpus_Destroyed.append(cpu)
                    hardware_kill_count += 3
                else:
                    pygame.mixer.Channel(4).play(pygame.mixer.Sound('hardware_hit.wav'))

        if self.rect.y < 0:
            all_sprites.remove(self)


class Hardware(pygame.sprite.Sprite):
    """
    Inheritance - Creating a parent class for all hardware
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()  # figures out rectangle hit box based on image
        self.vel = [random.randrange(-1, 2), random.randrange(2, 12)]
        self.health = hardware_health
        self.rect.center = (random.randrange(0, 1280 - hardware_width), 0)

    def update(self):
        """
        updating the class with movement of the hardware
        :return: None
        """
        # movement (hardware disappear when they hit the edge of the screen)
        self.rect.y += self.vel[1]
        self.rect.x += self.vel[0]


class Phone(Hardware):
    """
    Creating the phone class by using inheritance
    """

    def __init__(self):
        """
        Inheriting properties from parent class
        """
        self.image = phone_hardware
        super().__init__()

    def update(self):
        """
        Using inheritance to update movement and polymorphism - removes phones that hit the edge of the screen
        :return:
        """
        super().update()
        if self.rect.y > 720:
            phones.remove(self)
            all_sprites.remove(self)


class Tv(Hardware):
    """
        Creating the Tv class by using inheritance
        """

    def __init__(self):
        self.image = tv_hardware
        super().__init__()

    def update(self):
        """
                Using inheritance to update movement and polymorphism - removes tvs that hit the edge of the screen
                :return:
                """
        super().update()
        if self.rect.y > 720:
            tvs.remove(self)
            all_sprites.remove(self)


class iPad(Hardware):
    """
        Creating the iPad class by using inheritance
        """

    def __init__(self):
        self.image = ipad_hardware
        super().__init__()

    def update(self):
        """
            Using inhertiance to update movement and polymorphism - removes ipads that hit the edge of the screen
        """

        super().update()
        if self.rect.y > 720:
            ipads.remove(self)
            all_sprites.remove(self)


class Console(Hardware):
    """
        Creating the Console class by using inheritance
        """

    def __init__(self):
        self.image = console_hardware
        super().__init__()

    def update(self):
        """
            Using inhertiance to update movement and polymorphism - removes consoles that hit the edge of the screen
        """

        super().update()
        if self.rect.y > 720:
            consoles.remove(self)
            all_sprites.remove(self)


class Server(Hardware):
    """
        Creating the Sever class by using inheritance
        """

    def __init__(self):
        self.image = server_bonus
        super().__init__()
        self.rect.center = (random.randrange(0, 1280 - server_width), 0)
        self.spawn_time = 75
        self.health = bonusHardware_health  # over-riding health from parent class, Polymorphism

    def update(self):
        """
            Using inhertiance to update movement and polymorphism - removes servers that hit the edge of the screen
        """
        super().update()
        if self.rect.y > 720:
            servers.remove(self)
            all_sprites.remove(self)


class Cpu(Hardware):
    """
    creating the CPU class using inheritance
    """

    def __init__(self):
        self.image = cpu_bonus
        super().__init__()
        self.rect.center = (random.randrange(0, 1280 - cpu_width), 0)
        self.spawn_time = 25
        self.health = bonusHardware_health  # over-riding health from parent class, Polymorphism

    def update(self):
        """
            Using inheritance to update movement and polymorphism - removes cpys that hit the edge of the screen
        """
        super().update()
        if self.rect.y > 720:
            cpus.remove(self)
            all_sprites.remove(self)


# adds hardware at a random location to all_sprites and appends it to the list of hardware
def add_phone():
    """
    spawns phones if there are less than 4 present on the screen
    :return:
    """
    if random.random() < 0.1 and len(phones) < 4:
        phones.append(Phone())
        for phone in phones:
            all_sprites.add(phone)


def add_tv():
    '''
    spawns tvs if there are less than 4 present on the screen
    :return: add tv
    '''
    if random.random() < 0.1 and len(tvs) < 4:
        tvs.append(Tv())
        for tv in tvs:
            all_sprites.add(tv)


def add_ipad():
    '''
    spawns ipads if there are less than 2 present on the screen
    :return: add ipad
    '''
    if random.random() < 0.1 and len(ipads) < 2:
        ipads.append(iPad())
        for ipad in ipads:
            all_sprites.add(ipad)


def add_console():
    '''
    spawns consoles if there is less than 2 present on the screen
    :return: add cpu
    '''
    if random.random() < 0.1 and len(consoles) < 2:
        consoles.append(Console())
        for console in consoles:
            all_sprites.add(console)


def add_server(server):
    '''
    spawns servers to the screen if there is less than 1 present on the screen
    :param server:
    :return: add server
    '''
    if random.random() < 0.05 and len(servers) < 1:
        servers.append(server)
        for server in servers:
            all_sprites.add(server)


def add_cpu(CPU):
    '''
    spawns CPUs to the screen if there is less than one present on the screen
    :param CPU:
    :return: add cpu
    '''
    if random.random() < 0.05 and len(cpus) < 1:
        cpus.append(CPU)
        for cpu in cpus:
            all_sprites.add(cpu)


phones_Destroyed = []
ipads_Destroyed = []
tvs_Destroyed = []
consoles_Destroyed = []
servers_Destroyed = []
cpus_Destroyed = []


class Stack():
    """
    creating stack class to display destroyed hardware onto gameplay screen
    """
    def __init__(self):
        self.items = []

    def push(self, hardware_destroyed):
        """
        Pushes the elements at the Last Index
        """
        self.items.append(hardware_destroyed)

    def pop(self):
        """
        This will remove the last item
        :return:
        """
        if len(self.items) > 0:
            return self.items.pop()
        else:
            return None

    def get_length(self):
        """
        gets length of the list
        :return:  len(self.items)
        """
        return len(self.items)





destroyed_phones = Stack()
destroyed_phones.push(phones_Destroyed)
destroyed_phones.get_length()

destroyed_tvs = Stack()
destroyed_tvs.push(tvs_Destroyed)
destroyed_tvs.get_length()

destroyed_consoles = Stack()
destroyed_consoles.push(consoles_Destroyed)
destroyed_consoles.get_length()

destroyed_ipads = Stack()
destroyed_ipads.push(ipads_Destroyed)
destroyed_ipads.get_length()

destroyed_servers = Stack()
destroyed_servers.push(servers_Destroyed)
destroyed_servers.get_length()

destroyed_cpus = Stack()
destroyed_cpus.push(cpus_Destroyed)
destroyed_cpus.get_length()


# score and health
def draw_labels():
    """
    Draws score and health onto the screen
    :return:
    """
    score = str(hardware_kill_count)
    score_label = drawtitle(25).render("Score: " + score, True, white)
    screen.blit(score_label, (0, 720 / 20))
    health = str(player_health)
    health_label = drawtitle(25).render("Health: " + health, True, red)
    screen.blit(health_label, (0, 0))


def draw_destroyedHardware():
    """
    draws the destroyed hardware count onto gameplay screen
    :return:
    """
    phone_count = str(len(phones_Destroyed))
    phone_label = drawtitle(15).render("x" + phone_count, True, black)
    screen.blit(phone_hardware, (1200, 600))
    screen.blit(phone_label, (1200, 605))

    tv_count = str(len(tvs_Destroyed))
    tv_label = drawtitle(35).render("x" + tv_count, True, black)
    screen.blit(tv_hardware, (1200, 500))
    screen.blit(tv_label, (1200, 505))

    ipad_count = str(len(ipads_Destroyed))
    ipad_label = drawtitle(35).render("x" + ipad_count, True, black)
    screen.blit(ipad_hardware, (1200, 400))
    screen.blit(ipad_label, (1200, 405))

    console_count = str(len(consoles_Destroyed))
    console_label = drawtitle(35).render("x" + console_count, True, black)
    screen.blit(console_hardware, (1200, 300))
    screen.blit(console_label, (1200, 305))

    server_count = str(len(servers_Destroyed))
    server_label = drawtitle(35).render("x" + server_count, True, black)
    screen.blit(server_bonus, (1175, 50))
    screen.blit(server_label, (1200, 80))

    cpu_count = str(len(cpus_Destroyed))
    cpu_label = drawtitle(35).render("x" + cpu_count, True, black)
    screen.blit(cpu_bonus, (1190, 200))
    screen.blit(cpu_label, (1200, 215))


# creating game loop
def main_loop():
    """
    Creating Game
    :return:
    """
    running = True
    while running:
        clock.tick(60)  # keeps the loop running at the right speed, 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('shell.wav'))
                    all_sprites.add(Shell())

        all_sprites.update()
        add_tv()
        add_ipad()
        add_phone()
        add_console()
        new_s = Server()
        new_cpu = Cpu()

        if hardware_kill_count > new_cpu.spawn_time:
            add_cpu(new_cpu)

        if hardware_kill_count > new_s.spawn_time:
            add_server(new_s)

        if player_health < 1:
            game_over()

        # rendering
        all_sprites.draw(screen)
        draw_labels()
        draw_destroyedHardware()
        pygame.display.update()

    pygame.quit()


def quitbutton():
    """
    Creating quitbutton for menu and gameover screen
    """
    quit = pygame.QUIT
    sys.exit(quit)

    # loading fonts


def drawtitle(n):
    """
    loading fonts for score and health
    :param n: Assigned when function is called
    :return:
    """
    return pygame.font.Font("/Users/vivek/Downloads/PixelEmulator-xq08.ttf", n)


def myfont(n):
    return pygame.font.Font("/Users/vivek/Desktop/nea/PublicPixel-0W5Kv.ttf", n)


def game_over():
    """
    creating game over screen
    :return:
    """
    width, height = 1280, 720
    game_overscreen = pygame.display.set_mode((width, height))

    gameisover = True
    pygame.mixer.music.stop()
    pygame.mixer.Channel(3).play(pygame.mixer.Sound('game_over.wav'))

    while gameisover:
        game_overscreen.blit(game_over_bg, (0, 0))

        game_over_text = drawtitle(120).render("GAME OVER", True, red)
        game_overscreen.blit(game_over_text, (225, 150))

        score_text = myfont(30).render("YOUR SCORE WAS " + str(hardware_kill_count), True, white)
        game_overscreen.blit(score_text, (375, 320))

        if gameover_playButton.draw(game_overscreen):
            main_loop()
        if gameover_leaderboardButton.draw(game_overscreen):
            print('LEADERBOARDS')
        if gameover_quitButton.draw(game_overscreen):
            quitbutton()

        for event in pygame.event.get():
            print(event.type)
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()


# sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(Game_bg1(720))
all_sprites.add(Game_bg1(-720))
player = Player()
all_sprites.add(player)


def instructions():
    """
    Creating instructions screen
    :return:
    """
    while True:
        screen.blit(menu_bg, (0, 0))

        instruction_title = drawtitle(40).render("Instructions", False, white)
        screen.blit(instruction_title, (450, 100))

        instruction_set = myfont(25).render("0  Move your tank with left and right keys", False, white)
        screen.blit(instruction_set, (100, 225))

        instruction_set2 = myfont(25).render("0  Press spacebar to shoot shells", False, white)
        screen.blit(instruction_set2, (100, 300))

        instruction_set3 = myfont(25).render("0  Destroy hardware to get points", False, white)
        screen.blit(instruction_set3, (100, 375))

        instruction_set4 = myfont(25).render("0  Avoid getting hit by hardware", False, white)
        screen.blit(instruction_set4, (100, 450))

        if instructions_playButton.draw(screen):
            main_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        pygame.display.update()


def game_menu():
    """
    Creating game menu screen
    :return:
    """
    while True:
        screen.blit(menu_bg, (0, 0))
        screen_text = drawtitle(90).render('Hardcode Hardware', False, red)
        screen.blit(screen_text, (55, 120))

        if menu_playButton.draw(screen):
            main_loop()
        if menu_instructionsButton.draw(screen):
            instructions()
        if menu_leaderboardButton.draw(screen):
            print('LEADERBOARDS')
        if menu_quitButton.draw(screen):
            quitbutton()

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


game_menu()
