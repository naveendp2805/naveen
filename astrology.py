import pygame as py
import cv2
import sys
from datetime import datetime
import random
import prediction as pd
# Initialize Pygame
py.init()

class x:
     count=0
     startbuttonColor = "black"
     starttextColor = "white"
     startButton = py.Rect(545, 500, 200, 60)  # x, y, width, height
     quitbuttonColor = "black"
     quittextcolor = "white"
     quitButton = py.Rect(20, 20, 120, 50)
     backbuttonColor = "black"
     backtextcolor = "white"
     backButton = py.Rect(20, 20, 120, 50)
     yesbuttonColor = "black"
     yestextColor = "white"
     yesButton = py.Rect(500, 370, 120, 70)
     nobuttonColor = "black"
     notextColor = "white"
     noButton = py.Rect(690, 370, 120,70)
     zodiac_box = py.Rect(300, 50, 300, 40)
     occupation_box = py.Rect(300, 120, 300, 40)
     get_prediction_box = py.Rect(240, 200, 240, 40)
     zodiac_button = py.Rect(600, 50, 40, 40)  # Button for selecting zodiac
     occupation_button = py.Rect(600, 120, 40, 40)  # Button for selecting occupation

# Set up the display
screen=py.display.set_mode((1300,700))
py.display.set_caption("astrology")
# images
bgimg = py.image.load("image1.jpg")
bgimg = py.transform.scale(bgimg, (1300,700))
# videos
video1 = cv2.VideoCapture("video2.mp4")
video2 = cv2.VideoCapture("video1.mp4")
# fonts
titleFont = py.font.Font("gxdo3.otf", 40)
atartFont = py.font.Font('Avenir.ttf', 40)
Font = py.font.Font('Avenir.ttf', 30)
dialogboxFont = py.font.Font('Avenir.ttf', 45)
# music
loadingSound = py.mixer.Sound("Loading-audio.mp3")
startbuttonSound = py.mixer.Sound("startbutton-sound.mp3")
backbuttonSound = py.mixer.Sound("backbutton-sound.mp3")
quitbuttonSound = py.mixer.Sound("backbutton-sound.mp3")
buttonSound = py.mixer.Sound("button-sound.mp3")
# Input
birth_date = ""
birth_time = ""
birth_location = ""
active_input1 = None
zodiac_sign = ""
occupation = ""
active_input2 = None
zodiac_index = 0
occupation_index = 0
# Results
result = ""
show_prediction = False
prediction_text = ""

input_boxes = {
    "date": py.Rect(650, 150, 300, 40),
    "time": py.Rect(650, 220, 300, 40),
    "location": py.Rect(650, 290, 300, 40)
}
active_boxes = {key: False for key in input_boxes.keys()}

zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
Occupations = ["Student", "Business", "Politician", "Teacher", "Farmer", "Daily Wage Worker","Employee"]


def LoadingVideo():
     if x.count<1:
        frames=0
        while frames < 270:
            val1,frame1 = video1.read()
            if not val1:
                video1.set(cv2.CAP_PROP_POS_FRAMES,0)
                val1, frame1 = video1.read()
                
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1 = cv2.resize(frame1, (1300, 700))
            frame1 = py.surfarray.make_surface(frame1.swapaxes(0, 1))
            screen.blit(frame1, (0, 0))
            py.display.update()
            frames+=1
            x.count+=1
            py.time.wait(7)
     else:
          BackgroundVideo()

def BackgroundVideo():
    val,frame = video2.read()
    if not val:
         video2.set(cv2.CAP_PROP_POS_FRAMES,0)
         val, frame = video2.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1300, 700))
    frame = py.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))

def titleDisplay():
     title =titleFont.render("CELESTIAL COMPASS", True, 'turquoise')
     subtitle =titleFont.render("Navigate Your Life with Astrology ", True, 'turquoise')
     title_width, title_height = title.get_size()
     
     screen.blit(title, (460, 300))
     screen.blit(subtitle, (360, 350))
     py.time.wait(15)

def textDisplay(txt, font, color, x1, y1):
    Text = font.render(txt, True, color)
    wd, ht = Text.get_size()
    screen.blit(Text, (x1,y1))
    

def createButton(txt, txtclr, btn, btclr, font, x1, y1):
    py.draw.rect(screen, btclr, btn, border_radius=25)
    text = font.render(txt, True, txtclr)
    screen.blit(text, (x1, y1))

def dialogBox():
     confirmBox = py.Rect(443, 250, 425, 230)
     py.draw.rect(screen, "skyblue", confirmBox, border_radius=35)
     confirm_font = dialogboxFont.render("Want to Leave?", True, "black")
     screen.blit(confirm_font, (485,280))
     py.draw.rect(screen, x.yesbuttonColor, x.yesButton, border_radius=25)
     yesbuttonFont = Font.render("YES", True, x.yestextColor)
     screen.blit(yesbuttonFont,(530,385))
     py.draw.rect(screen, x.nobuttonColor, x.noButton, border_radius=25)
     nobuttonFont = Font.render("NO", True, x.notextColor)
     screen.blit(nobuttonFont, (725,385))

#______________zodiac sign's functions______________________________
def calculate_western_zodiac_sign(month, day):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius", "(Kumbha)"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Pisces", "(Meena)"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries", "(Mesha)"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus", "(Vrishabha)"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini", "(Mithuna)"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer", "(Kataka)"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo", "(Simha)"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo", "(Kanya)"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra", "(Tula)"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio", "(Vrishchika)"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius", "(Dhanus)"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn", "(Makara)"

def calculate_chinese_zodiac_sign(year):
    signs = [
        ("Monkey", " (Kuruparamu)"),
        ("Rooster", " (Muthadi)"),
        ("Dog", " (Kukka)"),
        ("Pig", " (Pandi)"),
        ("Rat", " (Eluka)"),
        ("Ox", " (Vasha)"),
        ("Tiger", " (Puli)"),
        ("Rabbit", " (Kundelu)"),
        ("Dragon", " (Dragon)"),
        ("Snake", " (Paamu)"),
        ("Horse", " (Gaja)"),
        ("Goat", " (Pashuvu)")
    ]
    return signs[year % 12]

def get_zodiac_description(sign, zodiac_type):
    descriptions = {
        "Western": {
            "Aquarius": "Aquarius is known for being independent, inventive, and forward-thinking.",
            "Pisces": "Pisces are intuitive, compassionate, and artistic.",
            "Aries": "Aries is known for their energetic, confident, and adventurous nature.",
            "Taurus": "Taurus is practical, reliable, and patient.",
            "Gemini": "Gemini is adaptable, curious, and communicative.",
            "Cancer": "Cancer is nurturing, emotional, and protective.",
            "Leo": "Leo is charismatic, confident, and creative.",
            "Virgo": "Virgo is analytical, meticulous, and practical.",
            "Libra": "Libra is diplomatic, charming, and fair-minded.",
            "Scorpio": "Scorpio is passionate, determined, and resourceful.",
            "Sagittarius": "Sagittarius is adventurous, optimistic, and philosophical.",
            "Capricorn": "Capricorn is disciplined, ambitious, and practical."
        },
        "Chinese": {
            "Monkey": "People born in the Year of the Monkey are intelligent, witty, and energetic.",
            "Rooster": "Roosters are hardworking, confident, and courageous.",
            "Dog": "People born in the Year of the Dog are loyal, honest, and protective.",
            "Pig": "Pigs are compassionate, generous, and diligent.",
            "Rat": "Rats are clever, resourceful, and adaptable.",
            "Ox": "Oxen are reliable, patient, and methodical.",
            "Tiger": "Tigers are brave, competitive, and unpredictable.",
            "Rabbit": "Rabbits are gentle, compassionate, and elegant.",
            "Dragon": "Dragons are ambitious, charismatic, and energetic.",
            "Snake": "Snakes are intelligent, wise, and enigmatic.",
            "Horse": "Horses are energetic, independent, and charismatic.",
            "Goat": "Goats are gentle, creative, and compassionate."
        }
    }
    return descriptions[zodiac_type].get(sign, "No description available.")


def get_astrology_info():
    global result
    try:
        # Parse the date and time
        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%d-%m-%Y %H:%M")
        month = birth_datetime.month
        day = birth_datetime.day
        year = birth_datetime.year

        # Calculate zodiac signs
        western_sign, telugu_western = calculate_western_zodiac_sign(month, day)
        chinese_sign, telugu_chinese = calculate_chinese_zodiac_sign(year)

        # Get descriptions
        western_description = get_zodiac_description(western_sign, "Western")
        chinese_description = get_zodiac_description(chinese_sign, "Chinese")

        # Generate result text
        result = (f"Your Western Zodiac Sign: {western_sign} ({telugu_western})\n"
                       f"Characteristics: {western_description}\n\n"
                       f"Your Chinese Zodiac Sign: {chinese_sign} ({telugu_chinese})\n"
                       f"Characteristics: {chinese_description}\n")
    except ValueError:
        result = "Invalid input! Please enter the input in the correct format."

#____________________prediction function________________
def get_prediction(zodiac, occupation):
    try:
        return random.choice(pd.horoscope_data[zodiac][occupation])
    except KeyError:
        return "Invalid Zodiac or Occupation. Please select valid options."

# pages
PAGE0 = 0
PAGE1 = 1
PAGE2 = 2
PAGE3 = 3
page = PAGE1

while True:
    for event in py.event.get():
        if event.type==py.QUIT:
                py.quit()
        if event.type == py.MOUSEBUTTONDOWN:
             if page == PAGE1:
                if x.startButton.collidepoint(event.pos):
                      startbuttonSound.play()
                      x.startbuttonColor = "white"
                      x.starttextColor = "blue"
                elif x.quitButton.collidepoint(event.pos):
                     quitbuttonSound.play()
                     x.quitbuttonColor = "black"
                     x.quittextcolor = "red"
             elif page == PAGE2:        
                if x.backButton.collidepoint(event.pos):
                     backbuttonSound.play()
                     x.backbuttonColor = "black"
                     x.backtextcolor = "red"
                for key, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                         active_input1 = key
                         active_boxes = {k: False for k in input_boxes.keys()}
                         active_boxes[key] = True
             elif page == PAGE3:
                 if x.zodiac_box.collidepoint(event.pos):
                     active_input2 = "zodiac"
                 elif x.occupation_box.collidepoint(event.pos):
                     active_input2 = "occupation"
                 elif x.get_prediction_box.collidepoint(event.pos):
                     if zodiac_sign and occupation:
                         prediction_text = get_prediction(zodiac_sign, occupation)
                         show_prediction = True
                     else:
                         prediction_text = "Please fill in both fields."
                         show_prediction = True
                 elif x.zodiac_button.collidepoint(event.pos):
                     zodiac_index = (zodiac_index + 1) % len(zodiac_signs)
                     zodiac_sign = zodiac_signs[zodiac_index]
                 elif x.occupation_button.collidepoint(event.pos):
                     occupation_index = (occupation_index + 1) % len(Occupations)
                     occupation = Occupations[occupation_index]
             elif page == PAGE0:
                  if x.yesButton.collidepoint(event.pos):
                     backbuttonSound.play()
                     x.yesbuttonColor = "white"
                     x.yestextColor = "chartreuse"
                  elif x.noButton.collidepoint(event.pos):
                     x.nobuttonColor = "white"
                     x.notextColor = "red"
                     buttonSound.play()
                
        if event.type == py.MOUSEBUTTONUP:
             if page == PAGE1:
                if x.startButton.collidepoint(event.pos):
                      x.startbuttonColor = "black"
                      x.starttextColor = "white" 
                      page = PAGE3
                elif x.quitButton.collidepoint(event.pos):
                     x.quitbuttonColor = "black"
                     x.quittextcolor = "white"
                     page = PAGE0
             elif page == PAGE2:
                if x.backButton.collidepoint(event.pos):
                     x.backbuttonColor = "black"
                     x.backtextcolor = "white"
                     page = PAGE1
             elif page == PAGE0:
                  if x.yesButton.collidepoint(event.pos):
                     x.yesbuttonColor = "black"
                     x.yestextColor = "white"
                     py.time.wait(350)
                     py.quit()
                  elif x.noButton.collidepoint(event.pos):
                     x.nobuttonColor = "black"
                     x.notextColor = "white"
                     page = PAGE1
        elif event.type == py.KEYDOWN:
            if active_input2 == "zodiac":
                 if event.key == py.K_BACKSPACE:
                     zodiac_sign = zodiac_sign[:-1]
                 else:
                     zodiac_sign += event.unicode
            elif active_input2 == "occupation":
                 if event.key == py.K_BACKSPACE:
                     occupation = occupation[:-1]
                 else:
                     occupation += event.unicode
            elif event.key == py.K_BACKSPACE:
                if active_input1 == "date" and len(birth_date) > 0:
                    birth_date = birth_date[:-1]
                elif active_input1 == "time" and len(birth_time) > 0:
                    birth_time = birth_time[:-1]
                elif active_input1 == "location" and len(birth_location) > 0:
                    birth_location = birth_location[:-1]
            elif event.key == py.K_RETURN:
                get_astrology_info()
            else:
                if active_input1 == "date":
                    birth_date += event.unicode
                elif active_input1 == "time":
                    birth_time += event.unicode
                elif active_input1 == "location":
                    birth_location += event.unicode

    if page == PAGE0:
         BackgroundVideo()
         titleDisplay()
         createButton("START", x.starttextColor, x.startButton, x.startbuttonColor, atartFont, 584, 504)
         createButton("QUIT", x.quittextcolor, x.quitButton, x.quitbuttonColor, Font, 40, 25)
         dialogBox()
    elif page == PAGE1:
        '''loadingSound.play()
        LoadingVideo()
        loadingSound.stop()
        LoadingVideo()'''
        BackgroundVideo()
        titleDisplay()
        createButton("START", x.starttextColor, x.startButton, x.startbuttonColor, atartFont, 584, 504)
        createButton("QUIT", x.quittextcolor, x.quitButton, x.quitbuttonColor, Font, 40, 25)
    elif page == PAGE2:
         screen.blit(bgimg,(0,0))
         createButton("BACK", x.backtextcolor, x.backButton, x.backbuttonColor, Font, 37, 25)
         date = textDisplay("Birth Date (DD-MM-YYYY):", Font, 'white', 260, 155)
         py.draw.rect(screen, "chartreuse" if active_boxes["date"] else "white", input_boxes["date"], 2)
         time = textDisplay("Birth Time (HH:MM):", Font, 'white', 337, 225)
         py.draw.rect(screen, "chartreuse" if active_boxes["time"] else "white", input_boxes["time"], 2)
         place = textDisplay("Birth Location:", Font, 'white', 420, 295)
         py.draw.rect(screen, "chartreuse" if active_boxes["location"] else "white", input_boxes["location"], 2)

         date_text = Font.render(birth_date, True, "white")
         screen.blit(date_text, (input_boxes["date"].x + 10, input_boxes["date"].y + 5))
         time_text = Font.render(birth_time, True, "white")
         screen.blit(time_text, (input_boxes["time"].x + 10, input_boxes["time"].y + 5))
         location_text = Font.render(birth_location, True, "white")
         screen.blit(location_text, (input_boxes["location"].x + 10, input_boxes["location"].y + 5))
         if result:
              y_offset = 400
              for line in result.split("\n"):
                   result_display = Font.render(line, True, "WHITE")
                   screen.blit(result_display, (250, y_offset))
                   y_offset += 30
    elif page == PAGE3:
         screen.blit(bgimg,(0,0))
         createButton("BACK", x.backtextcolor, x.backButton, x.backbuttonColor, Font, 37, 25)
         py.draw.rect(screen, "BLUE", x.zodiac_box, 2)
         py.draw.rect(screen, "BLUE", x.occupation_box, 2)
         py.draw.rect(screen, "BLUE", x.get_prediction_box, 2)
         py.draw.rect(screen, "BLUE", x.zodiac_button, 2)
         py.draw.rect(screen, "BLUE", x.occupation_button, 2)
 
         zarrow = textDisplay("^", Font, 'white', x.zodiac_button.x + 10, x.zodiac_button.y + 5)
         oarrow =  textDisplay("^", Font, 'white', x.occupation_button.x + 10, x.occupation_button.y + 5 )
         zodiac = textDisplay("Zodiac Sign:", Font, 'white', 50,55)
         Occupation = textDisplay("Occupation:", Font, 'white', 50,125)
         zodiac_text = textDisplay(zodiac_sign, Font, "white", x.zodiac_box.x + 5, x.zodiac_box.y + 5)
         occupation_text = textDisplay(occupation, Font, 'white', x.occupation_box.x + 5, x.occupation_box.y + 5)
         getprediction = textDisplay("Get Prediction", Font, 'white', 260,200)
         if show_prediction:
             prediction = textDisplay(prediction_text, Font, 'white', 250,250)


    # update the screen everytime
    py.display.update()

# quit pygame
video1.release()
video2.release()
py.quit()
