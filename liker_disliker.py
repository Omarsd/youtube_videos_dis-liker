import os
import time
import random
import platform
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException

#Current path of file
dir_path = os.path.dirname(os.path.realpath(__file__))

#Goes to that directory
os.chdir(dir_path)

#Gobal variables
SCROLL_PAUSE_TIME = int(input("Pause time between scrools in seconds:\n")) #1
LIKE_DISLIKE = input("Like or Dislike?\n")#"Dislike"
CHANNEL_URL = input("Url of channel:\n")
CHROME_PROFILE_PATH = input("Path of your chrome's profile:\n")
REPORT_LIST = {
"Sexual content":   ["Graphic sexual activity",
                    "Nudity",
                    "Suggestive, but without nudity",
                    "Content involving minors",
                    "Abusive title or description",
                    "Other sexual content"],

"Violent or repulsive content": ["Adults fighting",
                                "Physical attack",
                                "Youth violence",
                                "Animal abuse"],

"Hateful or abusive content":   ["Promotes hatred or violence",
	                            "Abusing vulnerable individuals",
	                            "Bullying",
	                            "Abusive title or description"],

"Harmful dangerous acts":   ["Pharmaceutical or drug abuse",
	                        "Abuse of fire or explosives",
	                        "Suicide or self injury",
	                        "Other dangerous acts"],

"Child abuse": None,


"Promotes terrorism": None,


"Spam or misleading":   ["Mass advertising",
	                    "Pharmaceutical drugs for sale",
	                    "Misleading text",
	                    "Misleading thumbnail",
	                    "Scams / fraud"],

#"Infringes my rights":   ["Infringes my copyright",
#	                    "Invades my privacy",
#	                    "Other legal claim"],

"Captions issue":   ["Captions are missing (CVAA)",
	                "Captions are inaccurate",
	                "Captions are abusive"]
}

#Sets boolean variables from input strings
if LIKE_DISLIKE.upper() == "DISLIKE":

    REPORT = input("Do you wanna report too? Yes or No\n")

    if REPORT.upper() == "YES":
        
        REPORT = True
        
        THIS_APPLIES = input("Do you wanna tell youtube to look at the description of the videos you report? Yes or No\n")

        #Opens report messages file and save in a list its content
        with open("report_messages.txt","r") as f:
            report_messages = f.read().split("\n")
        
        if THIS_APPLIES.upper() == "YES": 
            THIS_APPLIES = True
        elif THIS_APPLIES.upper() == "NO":
            THIS_APPLIES = False

    elif REPORT.upper() == "NO":
        REPORT = False


#Initializes ChromeOptions object
options = webdriver.ChromeOptions()

#Passes user-data folder. So it opens the browser with your default google account
options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")

#Use it in the backfround
#options.add_argument("--headless")

#Initializes variable and open Chrome
page = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

#Opens url
page.get(CHANNEL_URL)

# Get scroll height
last_height = page.execute_script("return document.documentElement.scrollHeight")

while True:
    # Scroll down to bottom
    page.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = page.execute_script("return document.documentElement.scrollHeight")
    #print(new_height)
    if new_height == last_height:
        break
    last_height = new_height

#Returns list of Selenium objects that reference to videos
videos = page.find_elements_by_css_selector("a[id='thumbnail']")

#Iterates through Selenium objects (videos) and saves the link values into "link_videos"
link_videos = [video.get_attribute("href") for video in videos]

#Removes the empty ones
link_videos.remove(None)

#print(f"N of videos: {len(link_videos)}")

#Iterates through all videos
for link in link_videos:
    page.get(link)  

    #Finds like and dislike buttons
    like_dislike_buttons = page.find_elements_by_css_selector("a[class='yt-simple-endpoint style-scope ytd-toggle-button-renderer']")

    while len(like_dislike_buttons) == 0:
        like_dislike_buttons = page.find_elements_by_css_selector("a[class='yt-simple-endpoint style-scope ytd-toggle-button-renderer']")

    #print(len(like_dislike_buttons))

    #If LIKE_DISLIKE variable is LIKE
    if LIKE_DISLIKE.upper() == "LIKE":
        
        #Looks for the button with attribute pressed to false. if found, button hasn't been pressed, so we pressed it. This is to avoid removing likes/dislikes
        check_if_pressed = like_dislike_buttons[0].find_elements_by_css_selector("button[aria-pressed='false']")
        
        if check_if_pressed:
            #Clicks first button, the like one
            like_dislike_buttons[0].click()

    elif LIKE_DISLIKE.upper() == "DISLIKE":
        #Looks for the button with attribute pressed to false. if found, button hasn't been pressed, so we pressed it. This is to avoid removing likes/dislikes
        check_if_pressed = like_dislike_buttons[1].find_elements_by_css_selector("button[aria-pressed='false']")
        
        if check_if_pressed:
            #Clicks second button, the dislike one
            like_dislike_buttons[1].click()


    try:
   
        #Starts the report part if selected as true
        if REPORT:

            #clicks in more options
            for button in page.find_elements_by_css_selector("button[aria-label='More actions']"):
                try:
                    button.click()
                    break
                except ElementNotInteractableException:
                    pass

            #Find box of buttons "report", "open transcript", "add translations"
            report_box = page.find_elements_by_css_selector("ytd-menu-service-item-renderer[class='style-scope ytd-menu-popup-renderer']")

            while len(report_box) != 2 and len(report_box) != 1:
                report_box = page.find_elements_by_css_selector("ytd-menu-service-item-renderer[class='style-scope ytd-menu-popup-renderer']")
                print(len(report_box))

            #clicks in "report" button
            report_box[0].click()

            #Gets a random category. If just one was inputed into script, it will retrieve it
            report_string = random.choice(list(REPORT_LIST))
            #print(report_string)

            #Finds all report categories
            categories = page.find_elements_by_css_selector("paper-radio-button[class='radio style-scope yt-options-renderer']")

            while len(categories) != 9:
                categories = page.find_elements_by_css_selector("paper-radio-button[class='radio style-scope yt-options-renderer']")

            #Clicks the one selected previously
            for element in categories:
                if report_string in element.text:
                    element.find_element_by_css_selector("yt-formatted-string[class='style-scope yt-options-renderer']").click()
                    break

            try:
                #All subcategory buttons are in the page, but hidden. this looks for the hiddens (6), and all of them (7, cause we opened one). Substracts them to get the one that is not hidden
                choose_one = set(page.find_elements_by_css_selector("paper-dropdown-menu[aria-label='Choose one']")) - set(page.find_elements_by_css_selector("paper-dropdown-menu[hidden]"))

                while report_string != "Child abuse" and report_string != "Promotes terrorism" and len(choose_one) == 0:
                    choose_one = set(page.find_elements_by_css_selector("paper-dropdown-menu[aria-label='Choose one']")) - set(page.find_elements_by_css_selector("paper-dropdown-menu[hidden]"))
                
                #Pop the element from the set and clicks in "Choose one"
                choose_one.pop().click()

                #finds element of report choice
                subreport_element = page.find_elements_by_css_selector("paper-listbox[aria-expanded='true']")

                while len(subreport_element) == 0:
                    subreport_element = page.find_elements_by_css_selector("paper-listbox[aria-expanded='true']")

                subreport_element = subreport_element[0]
                
                #Selects a subreport string if there is some
                subreport_string = random.choice(REPORT_LIST[report_string])
                #print(subreport_string)


                subreport_elements = subreport_element.find_elements_by_css_selector("paper-item[tabindex='-1']")

                while len(subreport_elements) == 0:
                    subreport_elements = subreport_element.find_elements_by_css_selector("paper-item[tabindex='-1']")

                time.sleep(1)

                #Looks for all subreports category and clicks previously selected subreport
                if subreport_string:
                    for element in subreport_elements:
                        if subreport_string in element.text:
                            element.click()


            except KeyError as err:
                #Set empty cause selected report doesnt have subreport categories
                #traceback.print_tb(err.__traceback__)
                pass
                
            except TypeError as err:
                traceback.print_tb(err.__traceback__)
                print(f"Error: tried to get a subcategory when needed but none were input into script in {report_string}. Check json")

            #Clicks in "This applies to links within the video description" if selected
            if THIS_APPLIES and report_string != "Captions issue" and report_string != "Infringes my rights":
                WebDriverWait(page, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "paper-checkbox[aria-labelledby='yt-boolean-form-field-v2-renderer-label']"))).click()
                #page.find_element_by_css_selector("paper-checkbox[aria-labelledby='yt-boolean-form-field-v2-renderer-label']").click()

            #Clicks in NEXT
            WebDriverWait(page, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "paper-button[aria-label='Next']"))).click()
            #page.find_element_by_css_selector("paper-button[aria-label='Next']").click()


            #Looks for video duration and splits by ":"
            duration = page.find_element_by_css_selector("span[class='ytp-time-duration']").text.split(":")
            
            #If video is more than an hour, convert hours to minutes and add it to minutes
            if(len(duration)>2):
                duration.insert(0, str(int(duration.pop(0))*60+int(duration.pop(0))))

            #Find Timestamp fields
            timestamps = page.find_elements_by_css_selector("paper-input[allowed-pattern='[0-9]']")

            while len(timestamps) != 2:
                timestamps = page.find_elements_by_css_selector("paper-input[allowed-pattern='[0-9]']")

            #Clears timestamps default values
            if platform.system() == "Linux" or platform.system() == "Windows":
                    
                timestamps[0].send_keys(Keys.CONTROL + "a")
                timestamps[0].send_keys(Keys.DELETE)

                timestamps[1].send_keys(Keys.CONTROL + "a")
                timestamps[1].send_keys(Keys.DELETE)

            elif platform.system() == "Darwin":

                timestamps[0].send_keys(Keys.COMMAND + "a")
                timestamps[0].send_keys(Keys.DELETE)

                timestamps[1].send_keys(Keys.COMMAND + "a")
                timestamps[1].send_keys(Keys.DELETE)

            #Picks a random value between duration of video as timestamps and write it in the form
            timestamps[0].send_keys(random.randint(0,int(duration[0])))
            timestamps[1].send_keys(random.randint(0,int(duration[1])))

            #Picks a random message from report_messages and send in to form
            page.find_element_by_css_selector("textarea[id='textarea']").send_keys(report_messages[random.randint(0,len(report_messages)-1)])

            #Clicks in REPORT
            WebDriverWait(page, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "paper-button[aria-label='Report']"))).click()
            #page.find_element_by_css_selector("paper-button[aria-label='Report']").click()
            
            #Clicks in CLOSE
            WebDriverWait(page, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "paper-button[aria-label='Close']"))).click()
            #page.find_element_by_css_selector("paper-button[aria-label='Close']").click()
        
    except NameError as err:
        #traceback.print_tb(err.__traceback__)
        pass

page.quit()