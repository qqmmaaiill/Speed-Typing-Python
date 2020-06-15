# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:30:08 2020

@author: IVAN
"""


import pygame
import random
import sys
import time

#dimentions of the window + bool for when we enter typing box + reset boolean(True)?
width = 800
height = 500
active_for_input = False
reset = True

#parameters for final output - accuracy\wpm\time
time_a = 0
accuracy = 0
wpm = 0

#variables for the input + result + sentence_w
input_t = ''
result = 'Accuracy is 0%,Time is 0s,WPM is '
chosen_w = ''

#variables for time - when we start + total time for results
start_t = 0
total_t = 0

#predefined colors for headline,text box(input) and result text(just for better look)
header_c = (255,200,100)
input_c = (235,235,235)
result_c = (200,70,70)

end = False

#load pygame

pygame.init()

#load open image + background,then resize them according to the window size
open_img = pygame.image.load("opening_img.jpg")
open_img = pygame.transform.scale(open_img,(width,height))

background = pygame.image.load("background_img.jpg")
background = pygame.transform.scale(background,(width,height))

#create display itself and assign it to screen + caption
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Speed typing")


#open the database for retrieving the sentences,the choosing random sentence via random.choice() and return it
def retrieve_sentence():
    
    f = open("database.txt").read()
    list_s = f.split('\n')
    the_chosen_one = random.choice(list_s)
    return the_chosen_one

#create a function for easier visualise different text(we will have parts with different color and size) + y coordinate from where to draw
#can be written in the core code since we will have only title,sentence itself and input box,but it will help with potential additional changes + a bit more clear and organised
def show_text(screen,d_text,y_c,size,color):
    
    font = pygame.font.Font(None,size)
    text = font.render(d_text,1,color)
    text_rect = text.get_rect(center=(width/2,y_c))
    screen.blit(text,text_rect)
    pygame.display.update()
  
#final function,used to show our results in a little more organised way
def results(screen):
    
    #formula for calculating accuracy:
    #(correct_characters/all_characters)*100
    
    #time is total time - start time /60 for minutes(since time is in seconds)
    
    #wpm is 
    
    global total_t
    global start_t
    global chosen_w
    global accuracy
    global result
    
    #for time
    total_t=time.time() - start_t
    #for accuracy??? problem when input is not the same lenght?
    br = 0
    for i,c in enumerate(chosen_w):
        if input_t[i] == c:
            br += 1
    
    accuracy = (br/len(chosen_w))*100
    
    wpm = len(input_t)*60/(5*total_t)
    
    result = 'Time:'+str(round(total_t)) +" secs --- Accuracy:"+ str(round(accuracy)) + "%" + ' --- Wpm: ' + str(round(wpm))
    
    #reset_img = pygame.image.load("reset_img.jpg")
    #reset_img = pygame.transform.scale(reset_img,(160,160))
    
    #screen.blit(reset_img,(width/2 - 80,height - 150))
    show_text(screen,"Reset",height-75,30,(111,111,111))
    
    pygame.display.update()
    
#function for start and then reset the game
#resetting all variables,then choosing random sentence from the database(using random library)

def game_sr():
    
    global time_a,accuracy,wpm
    global reset,active_for_input,end
    global result,input_t,chosen_w
    global start_t,total_t
    global head_c,text_c
    
    screen.blit(open_img,(0,0))
    pygame.display.update()
    time.sleep(2)
      
    active_for_input = False
    reset = False
    end = False
    
    time_a = 0
    accuracy = 0
    wpm = 0
    
    input_t = ''
    result = 'Accuracy is 0%,Time is 0s,WPM is '
    chosen_w = ''
    
    start_t = 0
    total_t = 0
    
    chosen_w = retrieve_sentence()
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    d_text = "Welcome to typing test!!!"
    show_text(screen,d_text,79,80,header_c)
    
    #rectangle for where the input will be so that user will be able to easily recognise 
    #...the box and click that to start typing
    pygame.draw.rect(screen,(255,192,25),(50,250,650,50),2)
    #show the chosen sentence(word)
    show_text(screen,chosen_w,200,30,input_c)
    
    pygame.display.update()
    
def run():
    global head_c,input_c,result_c
    global input_t,start_t
    global active_for_input
    global end
    game_sr()
    
    #in order to cancel while-loop when we press X on the window
    running = True
    
    while(running):
        
        clock = pygame.time.Clock()
        screen.fill((0,0,0),(50,250,650,50))
        pygame.draw.rect(screen,header_c,(50,250,650,50), 2)
        
        show_text(screen,input_t,275,30,(250,250,250))
        
        pygame.display.update()
        #looping trought muse\kb inputs options
        for event in pygame.event.get():
            #if we click X on the window(code QUIT)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                #take position of the cursor via built-in get_pos()
                x,y = pygame.mouse.get_pos()
                #if in input - active = True and time starts
                if(x>=50 and x<=700 and y>=250 and y<= 300):
                    active_for_input = True
                    input_t = ''
                    start_t = time.time()
                #if we have ended the game and click reset 
                if(x>=310 and x<=510 and y>= 350 and end):
                    game_sr()
                    x,y = pygame.mouse.get_pos()
            #if its a keyboard stroke(input)
            elif event.type == pygame.KEYDOWN:
                if active_for_input and not end:
                    #if we press ENTER(code K_RETURN)
                    if event.key == pygame.K_RETURN:
                        results(screen)
                        show_text(screen,result,350,28,result_c)
                        end = True
                    #if we press BACKSPACE to delete a character  
                    elif event.key == pygame.K_BACKSPACE:
                        input_t = input_t[:-1]
                    #just concatanate symbol to the input
                    else:
                        input_t += event.unicode
            
            pygame.display.update()
            
            clock.tick(60)
    
run()
                    
        
        
    
    
    
    
    



