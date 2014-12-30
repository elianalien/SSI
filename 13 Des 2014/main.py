import os, sys, random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.moretransitions import BlurTransition
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.input.motionevent import MotionEvent

class Page(Screen):
	fullscreen = BooleanProperty(True)
	source = StringProperty()
	tX = 0
	tY = 0
	minDist = 80

	#untuk swap atau klik tombol
	def on_touch_down(self, touch):
		self.tX = touch.x
		self.tY = touch.y 
		if (0 < self.tX < (self.width/10)) and (((self.height/2)-80) < self.tY < ((self.height/2)+80)):
			self.manager.current = self.manager.previous()
		if ((self.width-(self.width/10)) < self.tX < self.width) and (((self.height/2)-80) < self.tY < ((self.height/2)+80)):
			self.manager.current = self.manager.next()
		print 'x: ',self.tX, '   y:', self.tY

	def on_touch_up(self, touch):
		if self.tX - touch.x > self.minDist:
			self.manager.current = self.manager.next()
			print "left"
		if self.tX - touch.x < -self.minDist:
			self.manager.current = self.manager.previous()
			print "right"

class SlideShow(App):
	def build(self):
		#ini judul
		self.title = 'Sadang Serang Interaktif'
		
		#variabel buat nampung path
		rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))
		
		#array photo
		self.photos = []
		for image in os.listdir(rootPath + '/Photos'):
			self.photos.append(rootPath + '/Photos/' + image)

		#untuk kelas screen manager
		self.screenManager = ScreenManager(transition=BlurTransition(duration=1.0))

		#untuk iterasi ngambil source file
		for i in range(1,len(self.photos)):
			page = 'page'
			page = page + str(i)
			self.page = Page(name=page, source = self.photos[i])
			self.screenManager.add_widget(self.page)

		#untuk nampilin
		return self.screenManager
	
if __name__ in '__main__':
	SlideShow().run()

 