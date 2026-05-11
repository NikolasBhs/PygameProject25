from gamelib import *

def hero_update():
    old_bottom = hero.y + hero.height / 2

    if keys.Pressed[K_w] and hero.on_ground:
        hero.vy = jump_strength
        hero.on_ground = False

    hero.vy += gravity
    hero.y += hero.vy
    hero.on_ground = False

    if hero.y >= ground_y:
        hero.y = ground_y
        hero.vy = 0
        hero.on_ground = True

    for p in platforms:
        hero_left = hero.x - hero.width / 2
        hero_right = hero.x + hero.width / 2
        hero_bottom = hero.y + hero.height / 2

        p_left = p.x - p.width / 2 + 10
        p_right = p.x + p.width / 2 - 10
        p_top = p.y - p.height / 2 + 50

        if hero_right > p_left and hero_left < p_right:
            if hero.vy >= 0 and old_bottom <= p_top + 15 and hero_bottom >= p_top:
                hero.y = p_top - hero.height / 2
                hero.vy = 0
                hero.on_ground = True

    if hero.x < 20:
        hero.x = 20
    if hero.x > game.width - 20:
        hero.x = game.width - 20

    if keys.Pressed[K_a]:
        hero.x -= 5
    if keys.Pressed[K_d]:
        hero.x += 5

    hero.draw()

    healthbar.moveTo(hero.x - 25, hero.y - 105)
    healthbar.width = hero.health / 2

    ammobar.moveTo(hero.x - 15, hero.y - 90)
    ammobar.width = hero.ammo * 3


def power_update():
    for v in vests:
        if v.visible:
            v.move()

            if v.y >= ground_y:
                v.y = ground_y
                v.setSpeed(0, 180)

            if hero.collidedWith(v):
                hero.health += 5
                if hero.health > 100:
                    hero.health = 100
                v.visible = False

    for c in cammo:
        if c.visible:
            c.move()

            if c.y >= ground_y:
                c.y = ground_y
                c.setSpeed(0, 180)

            for p in platforms:
                c_left = c.x - c.width / 2
                c_right = c.x + c.width / 2
                c_bottom = c.y + c.height / 2

                p_left = p.x - p.width / 2 + 10
                p_right = p.x + p.width / 2 - 10
                p_top = p.y - p.height / 2 + 30

                if c_right > p_left and c_left < p_right:
                    if c_bottom >= p_top - 5 and c.y < p.y:
                        c.y = p_top - c.height / 2
                        c.setSpeed(0, 180)

            if hero.collidedWith(c):
                hero.ammo += 1
                c.visible = False

    for robot in evilrobots:
        if robot.visible and hero.collidedWith(robot):
            hero.health -= 20
            robot.visible = False


def drop_ammo(x, y):
    dropped = 0
    for c in cammo:
        if not c.visible:
            c.moveTo(x + dropped * 20, y)
            c.setSpeed(3, 180)
            c.visible = True
            dropped += 1
            if dropped == 2:
                break


def reset_level2_robots():
    for i in range(len(platforms_robot_positions)):
        evilrobots[i].moveTo(platforms_robot_positions[i][0], platforms_robot_positions[i][1])
        evilrobots[i].visible = True
        evilrobots[i].shoot_timer = 0
        evilrobots[i].fixed = False

    evilrobots[-1].moveTo(700, 500)
    evilrobots[-1].visible = True
    evilrobots[-1].shoot_timer = 0
    evilrobots[-1].fixed = True


def reset_level_objects():
    bullet.visible = False

    for b in enemy_bullets:
        b.visible = False

    for v in vests:
        v.visible = False

    for c in cammo:
        c.visible = False


def all_robots_dead():
    for robot in evilrobots:
        if robot.visible:
            return False
    return True


def show_end_screen(img):
    mouse.visible = False
    menu_pointer.visible = True
    img.visible = True

    while True:
        game.processInput()
        game.scrollBackground("left", 1)

        img.draw()
        menu_pointer.moveTo(mouse.x, mouse.y)
        menu_pointer.draw()

        game.drawText("Press Q to quit", 550, 450)
        game.drawText("Press ESC to go back to menu", 500, 500)

        if keys.Pressed[K_q]:
            img.visible = False
            return "quit"

        if keys.Pressed[K_ESCAPE]:
            img.visible = False
            return "menu"

        game.update(45)


def reset_game_state():
    hero.moveTo(80, 480)
    hero.vy = 0
    hero.on_ground = False
    hero.health = 100
    hero.ammo = 2

    bullet.visible = False

    tank.health = 30
    tank.moveTo(1000, 465)
    tank.shoot_timer = 0

    for b in enemy_bullets:
        b.visible = False

    for v in vests:
        v.visible = False

    for c in cammo:
        c.visible = False

    for i in range(len(platforms_robot_positions)):
        evilrobots[i].moveTo(platforms_robot_positions[i][0], platforms_robot_positions[i][1])
        evilrobots[i].visible = True
        evilrobots[i].shoot_timer = 0
        evilrobots[i].fixed = False

    evilrobots[-1].moveTo(700, 500)
    evilrobots[-1].visible = True
    evilrobots[-1].shoot_timer = 0
    evilrobots[-1].fixed = True


game = Game(1200, 600, "Mr Superfire")

bk = Image("images/background.png", game)
game.setBackground(bk)
bk.resizeBy(25)

hero = Animation("images/character.png", 3, game, 387/3, 400/2, 8)
hero.resizeBy(-30)
hero.moveTo(80, 480)
hero.vy = 0
hero.on_ground = False
hero.health = 100
hero.ammo = 2

ground_y = 485
gravity = 0.8
jump_strength = -22

ammobar = Shape("bar", game, hero.ammo, 10, blue)
healthbar = Shape("bar", game, hero.health, 10, green)

tank = Animation("images/tank.png", 2, game, 408/1, 352/2, 1)
tank.health = 30
tank_bar = Shape("bar", game, 30, 10, green)
tank.moveTo(1000, 465)
tank.flipV = True
tank.shoot_timer = 0
tank_shoot_delay = 90

platforms = []

p1 = Image("images/platform.png", game)
p1.resizeBy(-85)
p1.moveTo(250, 360)
platforms.append(p1)

p2 = Image("images/platform.png", game)
p2.resizeBy(-85)
p2.moveTo(500, 260)
platforms.append(p2)

p3 = Image("images/platform.png", game)
p3.resizeBy(-85)
p3.moveTo(760, 190)
platforms.append(p3)

p4 = Image("images/platform.png", game)
p4.resizeBy(-85)
p4.moveTo(980, 300)
platforms.append(p4)

p5 = Image("images/platform.png", game)
p5.resizeBy(-85)
p5.moveTo(1080, 160)
platforms.append(p5)

evilrobots = []
platforms_robot_positions = []

for i in range(4):
    e = Animation("images/evilrobot.png", 7, game, 960/3, 960/3, 5)
    e.resizeBy(-70)
    e.moveTo(platforms[i].x, platforms[i].y - 68)
    e.shoot_timer = 0
    e.fixed = False
    evilrobots.append(e)
    platforms_robot_positions.append((platforms[i].x, platforms[i].y - 68))

e = Animation("images/evilrobot.png", 7, game, 960/3, 960/3, 5)
e.resizeBy(-70)
e.moveTo(700, 500)
e.shoot_timer = 0
e.fixed = True
evilrobots.append(e)

bullet = Image("images/bullet.png", game)
bullet.resizeBy(-76)
bullet.moveTo(hero.x, hero.y)
bullet.visible = False

enemy_bullets = []
for i in range(12):
    b = Image("images/robotbullet.png", game)
    b.resizeBy(-94)
    b.visible = False
    enemy_bullets.append(b)

enemy_shoot_delay = 140

vests = []
for i in range(5):
    v = Image("images/vest.png", game)
    v.resizeBy(-50)
    v.visible = False
    vests.append(v)

cammo = []
for i in range(12):
    c = Image("images/Collect_ammo.png", game)
    c.resizeBy(-90)
    c.visible = False
    cammo.append(c)

title = Image("images/title.png", game)
title.moveTo(game.width / 2, 110)

start_btn = Image("images/start.png", game)
start_btn.moveTo(game.width / 2, 250)
start_btn.resizeBy(-80)

howto_btn = Image("images/howtoplay.png", game)
howto_btn.moveTo(game.width / 2, 360)
howto_btn.resizeBy(-80)

story_btn = Image("images/story.png", game)
story_btn.moveTo(game.width / 2, 470)
story_btn.resizeBy(-80)

howto_text = Image("images/howtotext.png", game)
howto_text.moveTo(game.width / 2, game.height / 2 + 10)
howto_text.visible = False

story_text = Image("images/storytext.png", game)
story_text.moveTo(game.width / 2, game.height / 2 + 10)
story_text.visible = False
story_text.resizeBy(-30)

win_img = Image("images/youwin.png", game)
win_img.moveTo(game.width / 2, game.height / 2)
win_img.resizeBy(-50)
win_img.visible = False

gameover_img = Image("images/gameover.png", game)
gameover_img.moveTo(game.width / 2, game.height / 2)
gameover_img.resizeBy(-50)
gameover_img.visible = False

menu_pointer = Image("images/bullet.png", game)
menu_pointer.resizeBy(-76)
menu_pointer.visible = True

app_running = True

while app_running:
    reset_game_state()

    mouse.visible = False
    menu_pointer.visible = True

    hero.moveTo(220, 430)

    in_menu = True
    show_howto = False
    show_story = False

    while in_menu:
        game.processInput()
        game.scrollBackground("left", 1)

        title.draw()
        hero.draw()
        start_btn.draw()
        howto_btn.draw()
        story_btn.draw()

        menu_pointer.moveTo(mouse.x, mouse.y)
        menu_pointer.draw()

        if menu_pointer.collidedWith(howto_btn, "rectangle") and mouse.LeftClick:
            show_howto = True
            show_story = False

        if menu_pointer.collidedWith(story_btn, "rectangle") and mouse.LeftClick:
            show_story = True
            show_howto = False

        if menu_pointer.collidedWith(start_btn, "rectangle") and mouse.LeftClick:
            in_menu = False
            show_howto = False
            show_story = False

        if keys.Pressed[K_SPACE] or keys.Pressed[K_ESCAPE]:
            show_howto = False
            show_story = False

        if show_howto:
            howto_text.visible = True
            howto_text.draw()
        else:
            howto_text.visible = False

        if show_story:
            story_text.visible = True
            story_text.draw()
        else:
            story_text.visible = False

        game.update(45)

    mouse.visible = True
    menu_pointer.visible = False

    hero.moveTo(80, 480)
    hero.vy = 0
    hero.on_ground = False
    hero.health = 100
    hero.ammo = 2
    bullet.visible = False

    result = ""

    while result == "":
        game.processInput()
        game.scrollBackground("left", 1)

        for robot in evilrobots:
            if robot.visible:
                robot.shoot_timer += 1

                if robot.shoot_timer >= enemy_shoot_delay:
                    robot.shoot_timer = 0

                    for b in enemy_bullets:
                        if not b.visible:
                            b.moveTo(robot.x, robot.y)
                            b.setSpeed(4, b.angleTo(hero))
                            b.visible = True
                            break

        for b in enemy_bullets:
            if b.visible:
                b.move()

                if b.collidedWith(hero):
                    hero.health -= 10
                    b.visible = False

                elif b.isOffScreen():
                    b.visible = False

        hero_update()
        power_update()

        if bullet.visible:
            bullet.move()

            if bullet.isOffScreen():
                bullet.visible = False

        for robot in evilrobots:
            if robot.visible:
                if robot.fixed:
                    robot.draw()
                else:
                    robot.move()

                if bullet.visible and bullet.collidedWith(robot):
                    robot.visible = False
                    bullet.visible = False
                    drop_ammo(robot.x, robot.y)

        for p in platforms:
            p.draw()

        if keys.Pressed[K_SPACE] and hero.ammo > 0 and bullet.visible == False:
            bullet.moveTo(hero.x, hero.y)
            bullet.setSpeed(8, bullet.angleTo(mouse))
            hero.ammo -= 1
            bullet.visible = True

        if hero.health <= 0:
            result = "lose"

        if all_robots_dead() and hero.x > game.width - 50:
            break

        game.update(45)

    if result == "":
        hero.moveTo(80, 480)
        hero.vy = 0
        hero.on_ground = False
        bullet.visible = False
        hero.ammo += 4

        reset_level_objects()
        reset_level2_robots()

        while result == "":
            game.processInput()
            game.scrollBackground("left", 2)

            for robot in evilrobots:
                if robot.visible:
                    robot.shoot_timer += 1

                    if robot.shoot_timer >= enemy_shoot_delay:
                        robot.shoot_timer = 0

                        for b in enemy_bullets:
                            if not b.visible:
                                b.moveTo(robot.x, robot.y)
                                b.setSpeed(4, b.angleTo(hero))
                                b.visible = True
                                break

            tank.shoot_timer += 1
            if tank.shoot_timer >= tank_shoot_delay:
                tank.shoot_timer = 0

                for b in enemy_bullets:
                    if not b.visible:
                        b.moveTo(tank.x, tank.y)
                        b.setSpeed(5, b.angleTo(hero))
                        b.visible = True
                        break

            for b in enemy_bullets:
                if b.visible:
                    b.move()

                    if b.collidedWith(hero):
                        hero.health -= 10
                        b.visible = False

                    elif b.isOffScreen():
                        b.visible = False

            hero_update()
            power_update()

            if bullet.visible:
                bullet.move()

                if bullet.isOffScreen():
                    bullet.visible = False

            tank.move()
            tank.draw()

            for robot in evilrobots:
                if robot.visible:
                    if robot.fixed:
                        robot.draw()
                    else:
                        robot.move()

                    if bullet.visible and bullet.collidedWith(robot):
                        robot.visible = False
                        bullet.visible = False
                        drop_ammo(robot.x, robot.y)

            for p in platforms:
                p.draw()

            tank_bar.width = tank.health
            tank_bar.x = tank.x - tank_bar.width / 2
            tank_bar.y = tank.bottom
            tank_bar.draw()

            if bullet.visible and bullet.collidedWith(tank):
                tank.health -= 5
                bullet.visible = False

            if keys.Pressed[K_SPACE] and hero.ammo > 0 and bullet.visible == False:
                bullet.moveTo(hero.x, hero.y)
                bullet.setSpeed(8, bullet.angleTo(mouse))
                hero.ammo -= 1
                bullet.visible = True

            if hero.health <= 0:
                result = "lose"

            if tank.health <= 0:
                result = "win"

            game.update(45)

    if result == "win":
        action = show_end_screen(win_img)
        if action == "quit":
            app_running = False

    if result == "lose":
        action = show_end_screen(gameover_img)
        if action == "quit":
            app_running = False
