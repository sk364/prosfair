#!/usr/bin/env python

import os
import imp
import sys
import pygame


os.system("export PROSFAIR_PATH=`pwd`")
os.system("g++ ai/minimax_alpha_beta.cpp -o ai/minimax")
gui_basic = imp.load_source('gui_basic','gui/gui_basic.py')
 
pygame.init()
 


 
class MenuItem(pygame.font.Font):
	def __init__(self, text, font=None, font_size=48, font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
    		pygame.font.Font.__init__(self, font, font_size)
        	self.text = text
        	self.font_size = font_size
		self.font_color = font_color
		self.label = self.render(self.text, 1, self.font_color)
		self.width = self.label.get_rect().width
		self.height = self.label.get_rect().height
		self.dimensions = (self.width, self.height)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.position = pos_x, pos_y
 
	def set_position(self, x, y):
        	self.position = (x, y)
        	self.pos_x = x
        	self.pos_y = y
 
  	def set_font_color(self, rgb_tuple):
        	self.font_color = rgb_tuple
        	self.label = self.render(self.text, 1, self.font_color)
 
   	def is_mouse_selection(self, (posx, posy)):
        	if (posx >= self.pos_x and posx <= self.pos_x + self.width) and (posy >= self.pos_y and posy <= self.pos_y + self.height):
                	return True
        	return False
 
 
class GameMenu():
   	def __init__(self, screen, items, funcs, bg_color=(0,0,0), font=None, font_size=30, font_color=(255, 255, 255)):
        	self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.funcs = funcs
	 
		self.bg_color = bg_color
		self.clock = pygame.time.Clock()
	 
		self.items = []
		for index, item in enumerate(items):
			menu_item = MenuItem(item)
	 
		   	t_h = len(items) * menu_item.height
		   	pos_x = (self.scr_width / 2) - (menu_item.width / 2)

		   	pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
	 
		   	menu_item.set_position(pos_x, pos_y)
		    	self.items.append(menu_item)
		self.mouse_is_visible = True
		self.cur_item = None
	 
   	def set_mouse_visibility(self):
        	if self.mouse_is_visible:
            		pygame.mouse.set_visible(True)
        	else:
            		pygame.mouse.set_visible(False)
 
  	def run(self):
        	mainloop = True
        	while mainloop:
            		# Limit frame speed to 50 FPS
            		self.clock.tick(50)
 
            		for event in pygame.event.get():
                		if event.type == pygame.QUIT:
                    			mainloop = False
				if event.type == pygame.MOUSEBUTTONDOWN:
    					mpos = pygame.mouse.get_pos()
					for item in self.items:
						if item.is_mouse_selection(mpos):
							mainloop = False
							if item.text == "Quit":
								self.funcs[item.text]()
							self.funcs[item.text](gui_basic.chessboard,600)

	    	            # Redraw the background
	    		screen.fill([255, 255, 255])
    	    		screen.blit(BackGround.image, BackGround.rect)
   

            		for item in self.items:
                		if item.is_mouse_selection(pygame.mouse.get_pos()):
                    			item.set_font_color((255, 255, 255))
                    			item.set_bold(True)
                		else:
                    			item.set_font_color((255, 255, 255))
                    			item.set_bold(False)
               			self.screen.blit(item.label, item.position)
 
            		pygame.display.flip()
 
class Background(pygame.sprite.Sprite):
   	def __init__(self, image_file, location):
        	pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        	self.image = pygame.image.load(image_file)
        	self.rect = self.image.get_rect()
       		self.rect.left, self.rect.top = location

if __name__ == "__main__":
    	WHITE = [255,255,255]

   	screen = pygame.display.set_mode((600, 600), 0, 32)
    
   	BackGround = Background("res/Background/background_chess_set.jpg", [0,0])

   	screen.fill(WHITE)
   	screen.blit(BackGround.image, BackGround.rect)

   	funcs = { "Play v/s CPU" : gui_basic.looping_cpu_vs_human,
		"2 Player Mode": gui_basic.looping_human_vs_human,
		"Watch the computer": gui_basic.looping_cpu_vs_cpu,
		"Quit" : sys.exit
    	}

   	menu_items = ('Play v/s CPU','2 Player Mode','Watch the computer', 'Quit')
 
   	pygame.display.set_caption('Game Menu')
   	
	gm = GameMenu(screen, menu_items, funcs)
   
	gm.run()
