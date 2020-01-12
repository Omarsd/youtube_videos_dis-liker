# youtube_videos_dis-liker

This script allows you to like or dislike all videos of a channel, and also report them. You can use it to support your favourite youtuber or screw a brand. Up to you! 

It is written on Python 3.8 and it uses Selenium.

All code is commented, so it is self-explanatory.

## Setup

1. **Download Google Chrome**

     *You can skip this step if you have it already.*

     This script uses Google Chrome as its web browsers, you download it and installing if you don't have it.

     You could use another one like Firefox, it would be downloading geckodriver instead of chromedriver and changing a couple lines of code. Currently I don't have time for it.

     https://www.google.com/intl/en/chrome/

2. **Download Python**

     This was tested using Python 3.8, although it should work in previous Python 3 versions.

     https://www.python.org/downloads/

 3. **Download Chromedriver** 

      ChromeDriver is a separate executable that Selenium WebDriver uses to control Chrome. The version you use depends on the version of your Google Chrome. So download the version of ChromeDriver that match your version of Chrome and place it in the same folder as the script.

      https://chromedriver.chromium.org

4. **Installing Selenium**

     Install python's package selenium (library that manages every automatic process of the web) writing this command into cmd, powershell or terminal:

  ```
  pip3 install selenium
  ```

## Features

- Currently you can dislike or like all videos of a channel. 

- There is also the posibility to report every video of the channel, but youtube prevents you from doing it to many. I don't know the implications it could have in someone's account; maybe youtube sees you as a bot and do something about it. After reporting an account while testing it, it just prevented the script to pass the 50-ish mark. Use it under your own risk.

## Inputs for the script

  - SCROLL_PAUSE_TIME
  
    Integer. Pause time between scrolls. It uses this time to let the browser refresh everything in order to calculate if it has scrolled to the bottom of the page already. For me is 1 second, but maybe you need more time. You will see when you use it.
  
- LIKE_DISLIKE

    String. Either you want to like or dislike videos.
  
- CHANNEL_URL

    String. Url of the channel you want to apply the algorithm. Keep in mind this url is the one that appears when you search for all uploaded videos of a channel. https://www.youtube.com/user/CHANNEL/videos or https://www.youtube.com/channel/CHANNEL/videos
  
- REPORT

    String (yes or no). If you hit on Dislike, you will be asked if you want to report videos also.
  
- THIS_APPLIES

    String (yes or no). If you hit on Report, you will be asked if you wan to turn the flag on youtube's report that tells them to also check the description of the video, since there is something that they don't allow.
  
- CHROME_PROFILE_PATH

    String. This is the path to your profile of Chrome. If you don't supply it, Selenium won't open Chrome with your Google account, so you won't be able to like or dislike videos. In windows it is:

  ```
  C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data
  ```
  
## Things to have in mind

- You can't minimize Chrome while it is working. Honestly I don't know why, but I guess it is something from Selenium. Also I tried to run it in the background, but it stops mid-way. So when it opens a video mute it and place something on top, or leave it.

- I recomend to use adblock if you want to dislike someone's channel. We wouldn't like to give revenue, would we? Also there is an extension called Audio Only Youtube for Chrome that prevents youtube from stream video, just the audio. That would ease your CPU and network while the script do its job.

- When it reports, it picks a random timestamp, a random category and subcategory (excepts "Infringes my rights", sinces you get redirected to another tab and I don't have time to implement it) and picks a line from "report_messages.txt" file. Lines of that file is what it writes into the report textbox. I created it using synonyms of words like "disgusting", whatever you place there, it will pick. You only need that file if you plan on report and it has to be placed in the same directory as the script.

- The method that scrolls to the bottom of the channel video section uses a wait time in seconds that is input into the program at the beginning of the execution. I found that 1 second is good for me, it could be more for you. The first time you open it, you will see if it reaches the bottom.

- Currently everything is input to the program via console, feel free to change the code or do whatever you please with it!
