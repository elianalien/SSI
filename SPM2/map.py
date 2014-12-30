from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.transformation import Matrix
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Ellipse
from kivy.uix.widget import Widget

finalSize = (1920, 1080)
Window.clearcolor = (1,1,1,1)

class Screen(FloatLayout):
#class Screen(ScatterLayout):	
	# baseMap = Image(source='SadangSerangMap.png')
	# rocketMap = Image(source='rocket.png')
	# streetMap = Image(source='jalan.png')
	# miscelMap = Image(source='misc.png')

	def __init__(self, **kwargs):
		super(Screen, self).__init__()

		# blue = InstructionGroup()
		# blue.add(Color(0, 0, 1, 0.2))
		# blue.add(Ellipse(pos=self.pos, size=(500, 500)))
		# green = InstructionGroup()
		# green.add(Color(0, 1, 0, 0.4))
		# green.add(Ellipse(pos=(100, 100), size=(100, 100)))

		# [self.canvas.add(group) for group in [blue, green]]

		self.rocketButton = ToggleButton(text='rocketMap', 
									state='normal', 
									size_hint=(.2,.1))
		self.streetButton = ToggleButton(text='streetMap', 
									state='normal', 
									size_hint=(.2,.1))
		self.miscelButton = ToggleButton(text='miscelMap', 
									state='normal', 
									size_hint=(.2,.1))
		self.resetButton = Button(text='Reset Map', 
							 	  size_hint=(.2,.1))
		self.zoomInButton = Button(text='+',
								   size_hint=(.2,.1))
		self.zoomOutButton = Button(text='-',
								   size_hint=(.2,.1))

		self.rocketButton.bind(on_release=self.addRocket)
		self.streetButton.bind(on_release=self.addStreet)
		self.miscelButton.bind(on_release=self.addMiscel)
		self.resetButton.bind(on_release=self.resetMap)
		self.zoomInButton.bind(on_release=self.zoomIn)
		self.zoomOutButton.bind(on_release=self.zoomOut)

		self.baseMap = Image(source='SadangSerangMap.png', allow_stretch=True, size=(self.width,self.height))
		self.baseMap1 = Image(source='Base Map 1.png', allow_stretch=True, size=(self.width,self.height))
		self.baseMap2 = Image(source='Base Map 2.png', allow_stretch=True, size=(self.width,self.height))
		self.baseMap3 = Image(source='Base Map 3.png', allow_stretch=True, size=(self.width,self.height))
		self.rocketMap = Image(source='rocket.png')
		self.streetMap = Image(source='jalan.png')
		self.miscelMap = Image(source='misc.png')

		self.bLayout = BoxLayout(spacing='20', size_hint=self.size)
		self.bLayout.add_widget(self.rocketButton)
		self.bLayout.add_widget(self.streetButton)
		self.bLayout.add_widget(self.miscelButton)
		self.bLayout.add_widget(self.resetButton)
		self.bLayout.add_widget(self.zoomInButton)
		self.bLayout.add_widget(self.zoomOutButton)

		# self.sLayout = Scatter(do_scale=True, 
		# 					   do_rotation=False,
		# 					   do_translation=False, 
		# 					   auto_bring_to_front=False,
		# 					   scale_min=1.,
		# 					   scale_max=10.)	
		# self.sLayout.add_widget(self.baseMap)
		# mat = Matrix().scale(1,1,1)
		# self.sLayout.apply_transform(mat)

		self.add_widget(self.baseMap)
		self.add_widget(self.bLayout)

	def addRocket(self,b,**kwargs):
		if b.state == 'down':
			self.add_widget(self.rocketMap)
		elif b.state == 'normal':
			self.remove_widget(self.rocketMap)

	def addStreet(self,b,**kwargs):
		if b.state == 'down':
			self.add_widget(self.streetMap)
		elif b.state == 'normal':
			self.remove_widget(self.streetMap)

	def addMiscel(self,b,**kwargs):
		if b.state == 'down':
			self.add_widget(self.miscelMap)
		elif b.state == 'normal':
			self.remove_widget(self.miscelMap)

	def resetMap(self,b,**kwargs):
		self.clear_widgets()
		self.add_widget(self.baseMap)
		self.add_widget(self.bLayout)
		self.rocketButton.state = 'normal'
		self.streetButton.state = 'normal'
		self.miscelButton.state = 'normal'

	def zoomIn(self,b,**kwargs):		
		pass

	def zoomOut(self,b,**kwargs):		
		pass

class MapsApp(App):
	def build(self):
		return Screen()

if __name__ == '__main__':
	MapsApp().run()


