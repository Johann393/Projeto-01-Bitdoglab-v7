from machine import Pin, ADC, I2C, PWM
import neopixel
import ssd1306
import time
import random

# ===== LED MATRIX =====
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# ===== BUZZER =====
buzzer = PWM(Pin(21))
buzzer.duty_u16(0)

# ===== JOYSTICK =====
joy_x = ADC(Pin(27))
joy_y = ADC(Pin(26))

# ===== BOTÕES =====
btnA = Pin(5, Pin.IN, Pin.PULL_UP)
btnB = Pin(6, Pin.IN, Pin.PULL_UP)
btnC = Pin(10, Pin.IN, Pin.PULL_UP)

# ===== OLED =====
i2c = I2C(1, scl=Pin(3), sda=Pin(2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ===== ESTADOS =====
MENU, PLAYING, GAME_OVER, LEADERBOARD = 0,1,2,3
state = MENU

# ===== SCORE =====
score = 0
high_score = 0

# ===== DIFICULDADE =====
difficulty = 0
fall_speed = [400, 200]

# ===== NOTAS =====
NOTES = {
    "DO":523,"RE":587,"MI":659,
    "FA":698,"SOL":784,"LA":880,"SI":988
}

# ===== MÚSICAS =====
melody_menu = [("DO",200),("MI",200),("SOL",400),("MI",200),("DO",400)]
melody_normal = [("MI",150),("MI",150),("MI",150),("DO",150),("MI",150),("SOL",300),("SOL",300)]
melody_hard = [("MI",80),("SOL",80),("LA",80),("SI",80),("LA",80),("SOL",80),("MI",80),("DO",80)]

current_melody = melody_menu
note_index = 0
last_note_time = time.ticks_ms()

def play_music():
    global note_index, last_note_time

    # proteção contra overflow
    if note_index >= len(current_melody):
        note_index = 0

    note, duration = current_melody[note_index]

    if time.ticks_diff(time.ticks_ms(), last_note_time) >= duration:
        note_index = (note_index + 1) % len(current_melody)
        last_note_time = time.ticks_ms()

        note, duration = current_melody[note_index]
        buzzer.freq(NOTES[note])
        buzzer.duty_u16(8000)

# ===== OLED =====
def show_menu(opt):
    oled.fill(0)
    oled.text("MENU",45,5)
    oled.text("> Jogar" if opt==0 else "  Jogar",15,20)

    diff_text = "Normal" if difficulty == 0 else "Dificil"
    oled.text(("> Dif: "+diff_text) if opt==1 else ("  Dif: "+diff_text),15,35)

    oled.text("> Score" if opt==2 else "  Score",15,50)
    oled.show()

def show_score():
    oled.fill(0)
    oled.text("GAME OVER",20,10)
    oled.text("Score:"+str(score),20,30)
    oled.text("Max:"+str(high_score),20,45)
    oled.show()

def show_leaderboard():
    oled.fill(0)
    oled.text("LEADERBOARD",5,10)
    oled.text("Max Score:",10,30)
    oled.text(str(high_score),50,45)
    oled.show()

# ===== MATRIZ =====
def index(x,y):
    return y*5+x if y%2==0 else y*5+(4-x)

def clear():
    for i in range(NUM_LEDS):
        np[i]=(0,0,0)

def draw(notes, px):
    clear()
    colors=[(50,0,0),(0,0,50),(0,50,0)]

    for n in notes:
        if 0 <= n["x"] < 5 and 0 <= n["y"] < 5:
            np[index(n["x"], n["y"])] = colors[n["color"]]

    if 0 <= px < 5:
        np[index(px,4)] = (50,50,50)

    np.write()

# ===== INPUT =====
def read_joystick_x():
    x = joy_x.read_u16()
    if x < 20000: return -1
    if x > 45000: return 1
    return 0

def read_joystick_y():
    y = joy_y.read_u16()
    if y < 20000: return -1
    if y > 45000: return 1
    return 0

last_btn=[1,1,1]
def read_button():
    global last_btn
    curr=[btnA.value(),btnB.value(),btnC.value()]
    for i in range(3):
        if last_btn[i]==1 and curr[i]==0:
            last_btn=curr
            return i
    last_btn=curr
    return -1

# ===== EFEITO =====
def ripple(cx,cy):
    for d in range(5):
        clear()
        for x in range(5):
            for y in range(5):
                if abs(x-cx)+abs(y-cy)==d:
                    np[index(x,y)] = (50,0,50)
        np.write()
        time.sleep(0.03)

# ===== SPAWN =====
def spawn_note(notes):
    occupied_rows = [n["y"] for n in notes]
    if 0 in occupied_rows:
        return

    notes.append({
        "x": random.randint(0,4),
        "y": 0,
        "color": random.randint(0,2)
    })

# ===== LOOP =====
menu_option = 0

while True:

    play_music()

    if time.ticks_diff(time.ticks_ms(), last_note_time) > current_melody[note_index][1] * 0.7:
        buzzer.duty_u16(0)

    if state == MENU:
        current_melody = melody_menu
        note_index = 0   # <-- FIX
        show_menu(menu_option)

        move = read_joystick_y()
        if move == 1:
            menu_option = (menu_option + 1) % 3
            time.sleep(0.2)
        elif move == -1:
            menu_option = (menu_option - 1) % 3
            time.sleep(0.2)

        btn = read_button()
        if btn != -1:
            if menu_option == 0:
                state = PLAYING
                score = 0
                player_x = 2
                notes = []
                spawn_note(notes)
                last_move = time.ticks_ms()

                current_melody = melody_hard if difficulty else melody_normal
                note_index = 0   # <-- FIX

            elif menu_option == 1:
                difficulty = 1 - difficulty

            elif menu_option == 2:
                state = LEADERBOARD

    elif state == PLAYING:

        move = read_joystick_x()
        if move == -1 and player_x > 0:
            player_x -= 1
        elif move == 1 and player_x < 4:
            player_x += 1

        btn = read_button()

        if btn != -1:
            hit = False
            for n in notes:
                if n["x"] == player_x and n["color"] == btn and n["y"] >= 3:
                    score += 1
                    ripple(player_x,4)
                    notes.remove(n)
                    hit = True
                    break

            if not hit:
                state = GAME_OVER
                continue  # <-- FIX

        if time.ticks_diff(time.ticks_ms(), last_move) > fall_speed[difficulty]:

            for n in notes:
                n["y"] += 1

            for n in notes:
                if n["y"] > 4:
                    state = GAME_OVER
                    break  # <-- FIX

            if state == GAME_OVER:
                continue  # <-- FIX

            if difficulty == 1:
                if len(notes) < 2 and random.random() < 0.25:
                    spawn_note(notes)
            else:
                if len(notes) == 0:
                    spawn_note(notes)

            last_move = time.ticks_ms()

        draw(notes, player_x)

    elif state == GAME_OVER:

        if score > high_score:
            high_score = score

        current_melody = melody_menu
        note_index = 0   # <-- FIX
        show_score()
        time.sleep(2)
        state = MENU

    elif state == LEADERBOARD:
        show_leaderboard()
        if read_button() != -1:
            state = MENU

    time.sleep(0.05)
