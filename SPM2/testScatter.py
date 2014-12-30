from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button


finalSize = (1920, 1080)
#Builder.load_file('maps.kv')

class MapLayout(ScatterLayout):	
	def __init__(self, **kwargs):
		super(MapLayout, self).__init__()
		self.do_rotation = False 
		self.auto_bring_to_front = False
		self.do_collide_after_children = True
		
		#self.image = Image(source = 'Base Map 1.png')
		self.baseMap1 = Image(source='libs/Base Map 3.png', allow_stretch=True, size=(self.width,self.height))
		self.baseMap2 = Image(source='libs/Base Map 2.png', allow_stretch=True, size=(self.width,self.height))
		self.baseMap3 = Image(source='libs/Base Map 1.png', allow_stretch=True, size=(self.width,self.height))
		self.jalanMap = Image(source='libs/peta-jalan.png', allow_stretch=True, size=(self.width,self.height))
		self.airBersihMap = Image(source='libs/peta-air-bersih.png', allow_stretch=True, size=(self.width,self.height))
		self.gorongMap = Image(source='libs/peta-gorong-gorong.png', allow_stretch=True, size=(self.width,self.height))

		self.add_widget(self.baseMap1)
		self.idx = 0

	def addJalan(self):
		self.add_widget(self.jalanMap)
		print 'Jalan added'
	
	def removeJalan(self):
		self.remove_widget(self.jalanMap)
		print 'Jalan remove'

	def addAir(self):
		self.add_widget(self.airBersihMap)
		print 'Air added'
	
	def removeAir(self):
		self.remove_widget(self.airBersihMap)
		print 'Air removed'

	def addGorong(self):
		self.add_widget(self.gorongMap)
		print 'Gorong added'
	
	def removeGorong(self):
		self.remove_widget(self.gorongMap)
		print 'Gorong removed'

	def resetMap(self):
		self.clear_widgets()

	def zoomingIn(self):

		if self.idx == 0:
			self.remove_widget(self.baseMap1)
			self.add_widget(self.baseMap2)
			self.idx = self.idx + 1
			print self.idx
		elif self.idx == 1:
			self.remove_widget(self.baseMap2)
			self.add_widget(self.baseMap3)
			self.idx = self.idx + 1
			print self.idx
		elif self.idx == 2:
			print self.idx
		#	pass

	def zoomingOut(self):
		if self.idx == 2:
			self.remove_widget(self.baseMap3)
			self.add_widget(self.baseMap2)
			self.idx = self.idx - 1
			print self.idx
		elif self.idx == 1:
			self.remove_widget(self.baseMap2)
			self.add_widget(self.baseMap1)
			self.idx = self.idx - 1
			print self.idx
		elif self.idx == 0:
			print self.idx
		#	pass

class filterMap(ScatterLayout):
	def __init__(self, **kwargs):
		super(filterMap, self).__init__()
		pass
		
		

class MainScreenAndButton(FloatLayout):
	def __init__(self, **kwargs):
		super(MainScreenAndButton, self).__init__()

		## TOGGLE BUTTON FUNCTION ##
		self.jaringanJalanButton 		= ToggleButton(background_normal = 'libs/jalan.png',
                                        		background_down = 'libs/jalan-hit.png',
                                         		state='normal', 
                                         		size_hint=(.2,.1))
		self.jaringanAirBersihButton 	= ToggleButton(background_normal = 'libs/air-bersih.png',
                                        		background_down = 'libs/air-bersih-hit.png',
                                         		state='normal', 
                                         		size_hint=(.2,.1))
		self.jaringanGegorongButton 	= ToggleButton(background_normal = 'libs/gorong-gorong.png',
                                        		background_down = 'libs/gorong-gorong-hit.png',
                                         		state='normal', 
                                         		size_hint=(.2,.1))
		self.saranaPublik 				= ToggleButton(background_normal = 'libs/sarana-publik.png',
                                        		background_down = 'libs/sarana-publik-hit.png',
                                         		state='normal', 
                                         		size_hint=(.2,.1))

		## BUTTON FUNCTION ##
		self.zoomInButton	= Button(background_normal = 'libs/zoom-in.png',
                                    	background_down = 'libs/zoom-in-hit.png',
                                        state='normal', 
                                        size_hint=(.2,.1))
		self.zoomOutButton 	= Button(background_normal = 'libs/zoom-out.png',
                                    	background_down = 'libs/zoom-out-hit.png',
                                        state='normal', 
                                        size_hint=(.2,.1))

		self.jaringanJalanButton.bind(on_release=self.jalan)
		self.jaringanAirBersihButton.bind(on_release=self.air)
		self.jaringanGegorongButton.bind(on_release=self.gorong)
		self.saranaPublik.bind(on_release=self.sarana)
		
		self.zoomInButton.bind(on_release=self.zoomIn)
		self.zoomOutButton.bind(on_release=self.zoomOut)

		self.bLayout = BoxLayout(size_hint=(None,None),
									orientation='horizontal', 
									width = 500,
									height= 750,
									pos_hint= {'y':0.1, 'x': 0.1})
		self.bLayout.add_widget(self.jaringanJalanButton)
		self.bLayout.add_widget(self.jaringanAirBersihButton)
		self.bLayout.add_widget(self.jaringanGegorongButton)
		self.bLayout.add_widget(self.saranaPublik)
		
		self.bLayout.add_widget(self.zoomInButton)
		self.bLayout.add_widget(self.zoomOutButton)

		self.mapScreen = MapLayout()

		self.add_widget(self.mapScreen)
		self.add_widget(self.bLayout)
		self.zoomIdx = 0

	def jalan(self,b,**kwargs):
		if b.state == 'down':
			self.mapScreen.addJalan()
		elif b.state == 'normal':
			self.mapScreen.removeJalan()

	def air(self,b,**kwargs):
		if b.state == 'down':
			self.mapScreen.addAir()
		elif b.state == 'normal':
			self.mapScreen.removeAir()

	def gorong(self,b,**kwargs):
		if b.state == 'down':
			self.mapScreen.addGorong()
		elif b.state == 'normal':
			self.mapScreen.removeGorong()

	def sarana(self,b,**kwargs):
		if b.state == 'down':
			pass
		elif b.state == 'normal':
			pass

	def reset(self,b,**kwargs):
		self.mapScreen.resetMap()
		self.jaringanJalanButton.state = 'normal'
		self.jaringanAirBersihButton.state = 'normal'
		self.jaringanGegorongButton.state = 'normal'
		self.saranaPublik.state = 'normal' 

	def zoomIn(self,b,**kwargs):
		self.mapScreen.zoomingIn()

	def zoomOut(self,b,**kwargs):
		self.mapScreen.zoomingOut()
		
class mapApp(App):
	def build(self):
		return MainScreenAndButton()

if __name__ == '__main__':
	mapApp().run()