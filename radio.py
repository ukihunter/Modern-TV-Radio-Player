import customtkinter as ctk 
import requests
import vlc
from PIL import Image, ImageTk

class ModernRadioPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        

        self.title("Modern Radio By UKI")
        self.geometry("800x500")
        self.overrideredirect(True)
        self.minsize(800, 500)

        self.bg_image = Image.open("img/image3.png") 
        self.bg_image = self.bg_image.resize((800, 500))  
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1) 
        
 
        self.button_hover_color = "#dda15e"
        self.active_station_color = "#a3b18a"
        self.default_button_color = "#2f3e46"
        self.progress_bar_color = "#f4e285"
        
       
        self.player = None
        self.current_station = None
        self.is_playing = True
        self.volume = 0.5

        self.create_widgets()
        self.load_stations()
        
        self.header = ctk.CTkLabel(self.main_frame, text="Modern Radio By UKI",
                                 font=("Fixedsys", 44, "bold"))
        self.header.place(x=200 ,y= 10)


  
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_widgets(self):
     
        self.main_frame = ctk.CTkFrame(self, corner_radius=70, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)  


        self.volume_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.volume_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.stations_frame = ctk.CTkFrame(self.main_frame)
        self.stations_frame.place(x=140 , y=55)



        self.volume_slider = ctk.CTkSlider(
            self.volume_frame,
            from_=0,  
            to=1,
            orientation="vertical",
            command=self.set_volume,
            height=200,
            width=20,
            button_color=self.active_station_color,
            progress_color=self.active_station_color
        )
        self.volume_slider.set(self.volume)
        self.volume_slider.pack(padx=20, pady=10)


        # Control panel
        self.control_frame = ctk.CTkFrame(
            self.main_frame,
            height=80,
            corner_radius=15,
            fg_color=("#4E3629", "#6F4F25")
        )
        self.control_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
                
           
        self.status_label = ctk.CTkLabel(self.control_frame, text="Select a station",text_color="white", font=("Terminal",5))
        self.status_label.place(x=250, y=10)  

 # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.control_frame, height=6, width=250, progress_color=self.progress_bar_color)
        self.progress_bar.set(0.2)
        self.progress_bar.place(x=240, y=40)
        self.update_progress()

        # Exit button
        exit_image = ctk.CTkImage(Image.open("img/image.png").resize((30, 30)))
        self.exit_button = ctk.CTkButton(
            self.control_frame,
            image=exit_image,
            width=10,
            height=40,
            text="off",
            corner_radius=50,
            command=self.destroy,
            fg_color="#B17457",
            hover_color="#CC0000",
            font=("Arial", 18, "bold")
        )
        self.exit_button.place( x= 520 ,y=25)

        # Play button
        play_icon = ctk.CTkImage(Image.open("img/image2.png"), size=(60, 60))
        self.play_button = ctk.CTkButton(
            self.control_frame,
            image=play_icon,
            width=5,
            height=5,
            text="",
            corner_radius=80,
            command=self.toggle_play,
            fg_color="transparent",
            hover_color=("#4E3629", "#6F4F25"),
            border_width=0
        )
        self.play_button.pack(side="left", padx=150, pady=10)  

     
    def load_stations(self):
            # Sample stations
            self.stations = {
                "Radio Paradise": "http://stream.radioparadise.com/flacm",
                "Classic FM": "http://media-ice.musicradio.com/ClassicFMMP3",
                "BBC Radio ": "http://icecast.ndr.de/ndr/ndr2/hamburg/mp3/128/stream.mp3",
                "hip hop":"http://streams.90s90s.de/hiphop/mp3-192/",
                "hip hop and soul ": "http://stream.rtlradio.de/rnb/mp3-192/",
                "WPR News":"https://wpr-ice.streamguys1.com/wpr-ideas-mp3-64",
                "Abc News":"https://live-radio01.mediahubaustralia.com/PBW/mp3/",
                "Heart South Coast":"http://media-sov.musicradio.com/HeartHampshire",
                "Angel Radio":"http://stream.klassikradio.de/movie/mp3-192/www.klassikradio.de/",
                "Aljazeera TV":"http://live-hls-web-aje.getaj.net/AJE/06.m3u8",
                "BBC":"https://vs-hls-push-ww-live.akamaized.net/x=4/i=urn:bbc:pips:service:bbc_news_channel_hd/t=3840/v=pv14/b=5070016/main.m3u8",
               # "lsl":"http://wzstreaming.rai.it/TVlive/liveStream/playlist.m3u8",
             #  "dasd":"http://voa-22.akacast.akamaistream.net/7/48/322034/v1/ibb.akacast.akamaistream.net/voa-22",
                "Movie":"https://mytimefrance-rakuten-samsung.amagi.tv/playlist.m3u8"
                #"uki":"http://stream1.cinerama.uz/1229/tracks-v1a1/mono.m3u8"
                
            }


            for i, (name, url) in enumerate(self.stations.items()):
                            col = i // 4  
                            row = i % 4   
                            btn = ctk.CTkButton(self.stations_frame, text=name,
                                            corner_radius=15, height=60,
                                            fg_color="#273e47",
                                            hover_color=self.button_hover_color,
                                            font=("Arial", 14),
                                            command=lambda u=url, n=name: self.select_station(u, n))
                            btn.grid(row=row, column=col, pady=5, padx=10, sticky="w")
                           
   
    def select_station(self, url, name):
                self.current_station = url
                self.status_label.configure(text=f"Selected: {name}", text_color="white")
                
                # Update button colors
                for child in self.stations_frame.winfo_children():
                    if isinstance(child, ctk.CTkButton):
                        if child.cget("text") == name:
                            child.configure(fg_color=self.active_station_color)
                        else:
                            child.configure(fg_color=self.default_button_color)
    def toggle_play(self):
        if not self.current_station:
            self.status_label.configure(text="select a station first!", 
                                        text_color="#ff5555" ,font=("Terminal",5))
            return
            
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.start_radio()
            self.play_button.configure(text="")
            self.status_label.configure(text="Playing...", text_color="white")
        else:
            self.stop_radio()
            self.play_button.configure(text="")
            self.status_label.configure(text="Paused", text_color="gray")

    
    
    def set_volume(self, value):
        self.volume = float(value)
        print(f"Volume set to: {self.volume * 100}%")  
        if self.player:
            self.player.audio_set_volume(int(self.volume * 100))

    def start_radio(self):
        try:
            if self.player is None:
                instance = vlc.Instance()
                self.player = instance.media_player_new()
                media = instance.media_new(self.current_station)
                self.player.set_media(media)
                self.player.audio_set_volume(int(self.volume * 100))
                self.player.play()
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="#ff5555")
            self.is_playing = False

    def stop_radio(self):
        if self.player:
            self.player.stop()
            self.player = None

    def update_progress(self):
        if self.is_playing:
            current_progress = self.progress_bar.get()
            new_progress = current_progress + 0.001
            if new_progress > 1:
                new_progress = 0
            self.progress_bar.set(new_progress)
            self.after(100, self.update_progress)


      # Drag functionality
    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self._offsetx
        y = self.winfo_y() + event.y - self._offsety
        self.geometry(f"+{x}+{y}")

    def setup_dragging(self):
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

if __name__ == "__main__":
    app = ModernRadioPlayer()
    app.setup_dragging()
    app.mainloop()