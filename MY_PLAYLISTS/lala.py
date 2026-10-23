import pygame
import random
import webbrowser

class Video:
    def __init__(self , title , link):
        self.title = title
        self.link = link
        self.seen = False

    def open(self):
        webbrowser.open(self.link)
        print("Open " + self.title)
        self.seen = True

class Playlist:
    def __init__(self , name , description  , rating , videos):
        self.name = name
        self.description = description
        self.rating = rating
        self.videos = videos

class TextButton:
    def __init__(self, text , position):
        self.text = text
        self.position = position

    def is_mouse_on_text(self):
        mouse_x , mouse_y = pygame.mouse.get_pos()
        if mouse_x > self.position[0] and mouse_x < self.position[0] + self.text_box[2] and mouse_y > self.position[1] and mouse_y < self.position[1] + self.text_box[3]:
            return True
        return False

    def draw(self):
        font = pygame.font.SysFont('sans', 20)
        text_render = font.render(self.text , True , (0, 0, 255))
        self.text_box = text_render.get_rect() 
        if self.is_mouse_on_text():
            text_render = font.render(self.text , True , (0, 0, 255))
            pygame.draw.line(screen, (0, 0, 255), (self.position[0], self.position[1] + self.text_box[3]), (self.position[0] + self.text_box[2], self.position[1] + self.text_box[3]), 2)
        else:
            text_render = font.render(self.text , True , (0, 0, 0))
        screen.blit(text_render, self.position)

def read_video_from_txt(file):
    title = file.readline() 
    link = file.readline() 
    video = Video(title, link)
    return video

def read_videos_from_txt(file):
    videos = []
    total = file.readline().strip()
    for i in range (int(total)):
        video = read_video_from_txt(file)
        videos.append(video)
    return videos

def read_playlist_from_txt(file):
        playlist_name = file.readline()
        playlist_description = file.readline()
        playlist_rating = file.readline()
        playlist_videos = read_videos_from_txt(file)
        playlist = Playlist(playlist_name,playlist_description,playlist_rating,playlist_videos)
        return playlist

def read_playlists_from_txt():
    playlists = []
    with open("data.txt", "r", encoding="utf-8") as file:
        total = file.readline().strip()
        for i in range(int(total)):
            playlist = read_playlist_from_txt(file)
            playlists.append(playlist)
    return playlists

pygame.init()
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("My Playlists")
running = True
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock() 

playlists = read_playlists_from_txt()
playlist = playlists[1]
videos_btn_list = []
playlists_btn_list = []
margin = 50
for i in range(len(playlists)):   
    playlist_btn = TextButton(str(i+1) + ". " + playlists[i].name.rstrip(), (50, 50 + margin*i))
    playlists_btn_list.append(playlist_btn)

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for playlist_button in playlists_btn_list:
        playlist_button.draw()
    for video_button in videos_btn_list:
        video_button.draw()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event .button == 1:
                for i in range (len(playlists_btn_list)):
                    if playlists_btn_list[i].is_mouse_on_text():
                        videos_btn_list = []
                        playlist = playlists[i]
                        for i in range(len(playlist.videos)):   
                            video_btn = TextButton(str(i+1) + ". " + playlist.videos[i].title.rstrip(), (250, 50 + margin*i))
                            videos_btn_list.append(video_btn)
                for video_button in videos_btn_list:
                    if video_button.is_mouse_on_text():
                        index = videos_btn_list.index(video_button)
                        playlist.videos[index].open()

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()