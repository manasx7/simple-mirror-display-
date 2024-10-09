import tkinter as tk
from datetime import datetime, date
import pyjokes
import requests
from bs4 import BeautifulSoup

class SimpleGUI:
    def __init__(self, root):

        self.root = root
        self.weather_visible = False
        self.news_visible = False
        '''self.root.title("Simple Display")
        self.root.attributes('-fullscreen', True)  
        self.root.configure(bg='black')'''        
        self.create_date_time_frame()
        self.create_label()
        self.joke_frame()
        self.neweather_frame()  
        self.create_user_input() 
        self.fetch_datetime()
        self.fetch_joke()



    def create_label(self):

        self.label2 = tk.Label(root, text="Hii..manas", font=("Arial", 36),  fg='black')
        self.label2.pack(pady=20)

    def joke_frame(self):

        joke_frame = tk.Frame(self.root,border=5)
        joke_frame.pack( padx=10, pady=(20, 10))
        self.joke_label = tk.Label(joke_frame, text="joke for you ;)", font=("Arial", 20), fg='black') 
        self.joke_label.pack(pady=10)
        self.joke_display_label = tk.Label(joke_frame, text="", font=("Arial", 20),  fg='black') 
        self.joke_display_label.pack(pady=10)
  

    def create_date_time_frame(self):

       
        date_time_frame = tk.Frame(self.root, border=2)
        date_time_frame.pack(side=tk.TOP, padx=10, pady=10)
        self.time_label = tk.Label(date_time_frame, text="", font=("Arial", 20), fg='black')  
        self.time_label.pack(side=tk.LEFT, padx=10)
        self.day_label = tk.Label(date_time_frame, text="", font=("Arial", 20),  fg='black')  
        self.day_label.pack(side=tk.LEFT, padx=10)
        self.date_label = tk.Label(date_time_frame, text="", font=("Arial", 20),  fg='black') 
        self.date_label.pack(side=tk.LEFT, padx=10)
        
    

    def neweather_frame(self):

        neweather_frame = tk.Frame(self.root,border=5)
        neweather_frame.pack(side=tk.TOP, padx=10, pady=10)   
        self.weather_button = tk.Button(neweather_frame, text="Click to Know Weather", font=("Arial", 15), height=1, width=20, fg='black', bg='white', command=self.toggle_weather_info)
        self.weather_button.pack( padx=10, pady=10)
        self.weather_info_label = tk.Label(neweather_frame, text="", font=("Arial", 15), fg='black') 
        self.weather_info_label.pack(pady=10)
        self.news_button = tk.Button(neweather_frame, text="Click to Know News Headlines", font=("Arial", 15), height=1, width=30, fg='black', bg='white', command=self.toggle_news_info)
        self.news_button.pack(padx=10, pady=10)
        self.news_info_label = tk.Label(neweather_frame, text="", font=("Arial", 15), fg='black') 
        self.news_info_label.pack(pady=10)
        
    def create_user_input(self):

        self.user_input = tk.Entry(root, font=("Arial", 16), fg='white', bg='black', show='*')  
        self.user_input.pack(pady=10,side=tk.BOTTOM)
        self.user_input.focus() 
        
    def fetch_datetime(self):

        today = datetime.today()
        weekday = today.strftime("%A") 
        self.day_label.config(text=weekday)        
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=current_time)        
        day = date.today()
        self.date_label.config(text=day)  
        self.root.after(1000, self.fetch_datetime)
    

    def fetch_joke(self):

        joke = pyjokes.get_joke()
        self.joke_display_label.config(text=joke)
        self.root.after(10000, self.fetch_joke)  
        if self.user_input.get().lower() == 'manas':
            self.root.destroy()
              
    def fetch_weather(self):

        #city = input("Enter City:")
        city = "jaipur"
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=f2b889c6702ad8a68991757ed4c05d3f&units=metric'.format(city)
        res = requests.get(url)
        data = res.json()
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        weather_info = f"Temperature: {temp} °C\nWind: {wind} m/s\nPressure: {pressure} hPa\nHumidity: {humidity} %\nDescription: {description}"
        self.weather_info_label.config(text=weather_info)
        self.weather_visible = True
    
    def toggle_weather_info(self):

        if self.weather_visible:
            self.weather_info_label.config(text="")
            self.weather_visible = False
        else:
            self.fetch_weather()

        
    def fetch_news(self):

        url = 'https://www.thehindu.com/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find('body').find_all('h3')
        news_info = ""  
        count = 0  
        for x in headlines:
            news_info += "👉 " + x.text.strip() + "\n"   
            count += 1
            if count == 5:
                break  
        self.news_info_label.config(text=news_info)
        self.news_visible = True
   

    def toggle_news_info(self):
        if self.news_visible:
            self.news_info_label.config(text="")
            self.news_visible = False
        else:
            self.fetch_news()


    def close_escape(self):
            print('Smart mirror closed')
            self.root.destroy() 

if __name__ == "__main__":

    root = tk.Tk()
    root.title(" Display")
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.7)  
    app = SimpleGUI(root)
    #root.bind("<Escape>", lambda e: app.close_escape())
    root.bind("<`>", lambda e: app.close_escape())
    root.focus_set()
    root.mainloop()