import pyautogui as p
import cv2
import pyperclip
import time


def copy_text_into_txt(count):
    try:
        # clip_img = p.locateCenterOnScreen("clip.jpg", confidence=0.8)
        # print(clip_img)
        x, y = 1830,470
        p.rightClick(x, y)
        # print(x,y)
        time.sleep(0.5)
        p.leftClick(x - 30, y + 50)
        p.leftClick(x - 30, y + 50)
        time.sleep(0.5)
        p.rightClick(x + 40, y)
        time.sleep(0.5)
        p.leftClick(x- 30, y+150)
        p.leftClick(x- 30, y+150)
        p.leftClick(1820, 800+160*count)
        p.hotkey('ctrl', 'a')
        time.sleep(0.3)
        p.hotkey('ctrl', 'v')
        time.sleep(0.3)
        p.hotkey('ctrl', 's')
        return True,x,y
    except:
        return False,0,0

def check_new_message():
    with open("betinfo0.txt", "r", encoding='utf-8') as file1:
        with open("betinfo1.txt", "r", encoding='utf-8') as file2:
            txt1=file1.readlines()
            txt2=file2.readlines()
            if txt1==txt2:
                print("No new message")
                return False
            else:
                return True

def delete_message(x,y):
    p.rightClick(x - 5, y - 40)
    p.leftClick(x + 30, y + 120)
    delete_x,delete_y = p.locateCenterOnScreen("delete_text.jpg",confidence=0.9)
    p.leftClick(delete_x,delete_y)

def read_from_txt(count):
    try:
        with open(f"betinfo{count}.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()
            bet_text = ""

            for line in lines:
                print(line)
                if "Max Limit" in line:
                    print("bulundu")
                    print(line)
                    break
            else:
                quit()


            print(lines)
            for line in lines:
                # if line=="\n":
                #     lines.remove(line)
                try:
                    ilk_bosluk = line.find(" ")
                    if ilk_bosluk<3:
                        line=line[line.find(" "):]
                    print(line)
                except:
                    pass
                bet_text += line.rstrip("\n").rstrip(" ") + " /"
                print(bet_text)

                if " Oran " in line:
                    print(line[1:].rstrip("\n"))
                    line = line[1:].rstrip("\n")
                    oran_index = line.find(" Oran ")
                    max_limit_index = line.find(":") + 1
                    tl_index = line.find("TL")

                    oran = line[:oran_index]
                    max_limit = line[max_limit_index:tl_index].strip(" ")
                    max_limit = "".join(max_limit.split("."))
                    info = [oran, max_limit]
                    print(info)

                    if int(max_limit) >= 100:
                        oynanacak_miktar = 90
                    elif int(max_limit) >= 20:
                        oynanacak_miktar = int(int(max_limit) * 0.9)
                    else:
                        oynanacak_miktar = int(max_limit)

                    print(oynanacak_miktar)
            first_occur = bet_text.find("/ /")
            second_occur = bet_text.find("/ /", first_occur + 1)

            print(bet_text[first_occur + 4:second_occur - 1])
            print(lines)
            bet_text = bet_text[first_occur + 4:second_occur - 1]
            pyperclip.copy(bet_text)
            print(bet_text)
            quit()
        return info,oynanacak_miktar,bet_text
    except:
        return False,False,False

def sitede_maci_ara(bet_text,trial_count):
    p.leftClick(944, 0)
    time.sleep(0.3)
    p.hotkey('ctrl', 'f')
    time.sleep(0.3)
    if trial_count==1:
        p.hotkey('ctrl', 'v')
    elif trial_count==2:
        new_text = bet_text.replace("-"," - ")
        p.write(new_text)
    time.sleep(1)

def sitede_beti_ara(refreshed):
    kupa = p.locateCenterOnScreen("kupa.jpg", confidence=0.95)
    kupa_x, kupa_y = kupa
    if refreshed:
        p.leftClick(kupa_x, kupa_y - 75)
    bet_found = False
    for x in range(kupa_x, 1920, 20):
        for y in range(kupa_y + 15, 900, 5):
            if p.pixelMatchesColor(x, y, (255, 255, 0), 20) or p.pixelMatchesColor(x, y, (120, 204, 102), 20):
                p.leftClick(x, y)
                bet_found = True
                break
        if bet_found:
            break
    time.sleep(0.3)
    if bet_found:
        p.leftClick(kupa_x, kupa_y - 75)
    time.sleep(1)
    return bet_found

def bet_bilgilerini_gir_ve_oyna(oynanacak_miktar):
    eksi_sembol_x, eksi_sembol_y = p.locateCenterOnScreen("eksi_sembol.jpg", region=(1110, 170, 1450, 650),
                                                          confidence=0.9)
    p.leftClick(eksi_sembol_x + 30, eksi_sembol_y)
    eksi_sembol_y, eksi_sembol_x = int(eksi_sembol_y), int(eksi_sembol_x)
    time.sleep(0.3)
    p.hotkey('ctrl', 'a')
    p.write(str(oynanacak_miktar))
    while True:
        eksi_sembol_y += 5
        if p.pixelMatchesColor(eksi_sembol_x, eksi_sembol_y, (255, 205, 54), 20):
            p.leftClick(eksi_sembol_x, eksi_sembol_y)
            break

def main():
    count=0
    refresh_count=0
    refreshed=False
    while True:
        if refresh_count==20:
            refresh_count=0
            refreshed=True
            p.press("f5")
            time.sleep(5)
            p.leftClick(1240,140)
            time.sleep(1)
            p.leftClick(650,770)

        count%=2
        copied,x,y = copy_text_into_txt(count)
        if copied:
            new_message = check_new_message()
            if new_message:
                info, oynanacak_miktar,bet_text = read_from_txt(count)
                if oynanacak_miktar:
                    sitede_maci_ara(bet_text,1)
                    bet_found = sitede_beti_ara(refreshed)
                    refreshed=False
                    if not bet_found:
                        sitede_maci_ara(bet_text,2)
                        sitede_beti_ara(refreshed)
                        refreshed=False
                    bet_bilgilerini_gir_ve_oyna(oynanacak_miktar)
                    print("Bet oynandı. Miktar:",oynanacak_miktar)
        time.sleep(10)
        count+=1
        refresh_count+=1

main()