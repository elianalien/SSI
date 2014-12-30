from threading import Timer

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.clock import Clock
from os.path import join

#from PIL import Image
#from PIL.ExifTags import TAGS


__author__ = 'Chairun R Siregar'

import random

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.lang import Builder
from kivy.loader import Loader
from kivy.graphics.transformation import Matrix
from kivy.animation import Animation

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.accordion import AccordionItem
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

import json

import unicodedata, re
from filter import *
from utils import *
from tweet_fetcher import *
from friendly_time import *
from web_browser import *

Window.clearcolor = (1, 1, 1, 1)
finalSize = (1920, 1080)

photo_rumahKita = []
rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))       
for image in os.listdir(rootPath + '/PhotosRumahKita'):
    if image.lower().endswith(".jpg"):
        photo_rumahKita.append(rootPath + '/PhotosRumahKita/' + image)

img_airtanah=[]
rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))       
for image in os.listdir(rootPath + '\\ebooksRumahKita\\AirTanah'):
    img_airtanah.append(rootPath + '\\ebooksRumahKita\\AirTanah\\' + image)

img_hidroponik=[]
rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))       
for image in os.listdir(rootPath + '\\ebooksRumahKita\\Hidroponik'):
    img_hidroponik.append(rootPath + '\\ebooksRumahKita\\Hidroponik\\' + image)

img_berkebun=[]
rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))       
for image in os.listdir(rootPath + '\\ebooksRumahKita\\KampungBerkebun'):
    img_berkebun.append(rootPath + '\\ebooksRumahKita\\KampungBerkebun\\' + image)   

class SmartCityApp(App):
    def build(self):
        #Window.size = (finalSize[0] / 2, finalSize[1] / 2)
        #Window.fullscreen = 'fake'
        Window.size = (finalSize[0], finalSize[1])
        Window.fullscreen = True

        Builder.load_file('app.kv')
        Builder.load_file('menu_utama.kv')
        Builder.load_file('info_bdg.kv')
        Builder.load_file('slideshow.kv')
        Builder.load_file('pdfGallery.kv') 
        Builder.load_file('rumah-kita.kv')
        #Builder.load_file('rumahKita.kv')

        global app
        app = MainContainer()
        self.mc = app
        app.start()


        return app

class MainContainer(FloatLayout):
#class MainContainer(ScatterLayout):
    def __init__(self, **kwargs):
        super(MainContainer, self).__init__(**kwargs)

    def start(self):
        self.sm = self.ids['screen_manager']

        self.sm.add_widget(MenuUtama(sm = self.sm))

        self.infoNgabandungan = InfoNgabandungan()
        self.sm.add_widget(self.infoNgabandungan)

        self.sm.add_widget(SadangSerangInteraktif())
        self.sm.add_widget(RumahKita())

        self.sm.current = "Menu Utama"

        # nanti scaling dimatiin dan scatternya diganti FlowLayout
        #mat = Matrix().scale(0.5, 0.5, 1)
        #self.apply_transform(mat)
        #---------------------------------------------------

# ------------- MENU UTAMA ---------------------

class MenuUtama(Screen):
    def __init__(self, **kwargs):
        super(MenuUtama, self).__init__(**kwargs)
        self.sm = kwargs['sm']

        btnCont = self.ids['btn_menu_utama_cont']

        btnCont.add_widget(BtnMenuUtama(sm = self.sm,
                                        background_normal = 'lib/btn e-kelurahan.png',
                                        background_down = 'lib/btn e-kelurahan down.png',
                                        screen = ''
                                        ))
        btnCont.add_widget(BtnMenuUtama(sm = self.sm,
                                        background_normal = 'lib/btn info bdg.png',
                                        background_down = 'lib/btn info bdg down.png',
                                        screen = 'Info Ngabandungan'
                                        ))
        btnCont.add_widget(BtnMenuUtama(sm = self.sm,
                                        background_normal = 'lib/btn sadang serang.png',
                                        background_down = 'lib/btn sadang serang down.png',
                                        screen = 'Sadang Serang Interaktif'
                                        ))
        btnCont.add_widget(BtnMenuUtama(sm = self.sm,
                                        background_normal = 'lib/btn rumah kita.png',
                                        background_down = 'lib/btn rumah kita down.png',
                                        screen = 'Rumah Kita'
                                        ))

    def reset(self):
        pass
        #reset size dan top nav bar
        # app.topBar.height = 0
        # app.sm.height = 1080

# --- additional widgets ---

class BtnMenuUtama(Button):
    def __init__(self, **kwargs):
        super(BtnMenuUtama, self).__init__(**kwargs)

        self.sm = kwargs["sm"]

        self.background_normal = kwargs["background_normal"]
        self.background_down = kwargs["background_down"]

        self.screen = kwargs["screen"]

    def on_press(self):
        if len(self.screen)>0:
            self.sm.transition.direction = 'down'
            self.sm.current =  self.screen

# ------------- INFO NGABANDUNGAN ---------------------

class InfoNgabandungan(Screen):

    crntName = "_home_"
    lastTweetId = 1
    animDur = 0.5
    trgHeight = 0
    maxTweet = 30

    def __init__(self, **kwargs):
        super(InfoNgabandungan, self).__init__(**kwargs)
        self.add_widget(TopBar())

        self.size = finalSize

        self.tweetScroll = self.ids['tweet_scroll']
        self.tweetContainer = self.ids['tweet_container']

        # upButton = self.ids['up_button']
        # upButton.on_press = self.scroll_up
        # downButton = self.ids['down_button']
        # downButton.on_press = self.scroll_down

        #full sized image and website
        self.fullSizedImageFilter = self.ids['full_sized_image_filter']
        self.fullSizedImage = self.ids['full_sized_image']

        self.fullSizedImageFilter.bind(on_press = self.close_full_image)


        #tweets and filters
        TweetFetcher(self)
        Clock.schedule_interval(self.add_tweet, self.animDur)
        self.disp_tweets('_home_')

        self.filters = self.ids['filters']


        #add group of group of filters (AKUN TWITTER and KATA KUNCI / HASHTAG)
        for i in xrange(len(filterSuperGroups)):
            superGroup = FilterSuperGroup(title = filterSuperGroups[i])
            self.filters.add_widget(superGroup, 1)

            #add group of filters ('Pemkot Bandung', 'Persib Bandung', 'Info Lain', etc)
            for j in xrange(len(filterGroups[i])):
                group = FilterGroup()
                group.background_normal = "lib/filter " + filterGroupsFiles[i][j] + ".png"
                group.background_selected = "lib/filter " + filterGroupsFiles[i][j] + " slct.png"

                superGroup.accordion.add_widget(group)

                #add filters ('@ridwankamil','@odedmd','@2Serang','@diskominfobdg', etc)
                for k in xrange(len(filters[i][j])):
                    filter = BtnFilter(name = filters[i][j][k])
                    group.filters.add_widget(filter)

        self.btnSemua = self.ids['semua']
        self.btnSemua.bind(on_press = self.disp_all)

        self.base = self.ids['base']

        self.webPageBase = Button()
        self.webPageBase.size_hint = (None, None)
        self.webPageBase.size = (1140, 900)
        self.webPageBase.pos = (405,42.5)
        self.webPageBase.opacity = 0

        self.webPage = CefBrowser()
        self.web_page_width = 1110
        self.web_page_height = 900

    def update(self):
        self.disp_tweets()
        print "update display"

    def disp_all(self, button, **args):
        self.disp_tweets('_home_')

    # Clear current tweets and parse new text file
    def disp_tweets(self, name = ""):

        if name == "":
            #if refreshing
            self.newToOld = False
            name = self.crntName
        else:
            #if displaying from new source
            self.crntName = name
            self.newToOld = True
            self.trgHeight = 0
            self.tweetContainer.height = 0
            self.tweetContainer.clear_widgets()


        # open the file, or create one if none exists
        try:
            tweetsJSONFile = open("./feed/" + name + ".txt")
            tweetsJSON = tweetsJSONFile.read()
            tweetsJSONFile.close()
        except:
            open("./feed/" + name + ".txt", "w")
            print name + ".txt file created"
            tweetsJSON = "[]"

        # load JSON form file, or create an empty one of none exists
        try:
            tweetDatas = json.loads(tweetsJSON)
        except:
            tweetDatas = json.loads("[]")

        tweetDatas = byteify(tweetDatas)

        #if refreshing
        if self.newToOld == False:
            #remove already displayed tweets
            newTweetDatas = []
            for i in xrange(len(tweetDatas)):
                if int(tweetDatas[i]["tweet_id"]) > self.lastTweetId:
                    newTweetDatas.append(tweetDatas[i])
                else:
                    break
            tweetDatas = newTweetDatas

        # save newest id, remove >50 tweets, reverse last newTweets idx
        if len(tweetDatas) > 0:
            self.lastTweetId = int(tweetDatas[0]["tweet_id"])
            if len(tweetDatas) > 50:
                del tweetDatas[50:]
            self.lastNewTweetIdx = 0

        #if refreshing, reverse the order so the older ones appear first
        if self.newToOld == False:
            tweetDatas.reverse()

        #add to newTweets to trigger the actual display via add_tweet()
        self.newTweets = tweetDatas


    def scroll_down(self):
        pass
        # if(self.tweetScroll.scroll_y - self.dy >= 0):
        #     anim = Animation(scroll_y = self.tweetScroll.scroll_y - self.dy, duration = 1, t='in_out_sine')
        #     anim.start(self.tweetScroll)
        #     self.tweetScroll.update_from_scroll()

    def scroll_up(self):
        pass
        # if(self.tweetScroll.scroll_y + self.dy <= 1):
        #     anim = Animation(scroll_y = self.tweetScroll.scroll_y + self.dy, duration = 1, t='in_out_sine')
        #     anim.start(self.tweetScroll)
        #     self.tweetScroll.update_from_scroll()

    #full sized image and website
    def disp_full_image(self, texture, srcHeight, trgHeight):
        self.fullSizedImage.texture = texture
        self.fullSizedImage.height = srcHeight
        self.fullSizedImage.opacity = 0

        anim1 = Animation(height = trgHeight, opacity = 1, duration = 0.3)
        anim1.start(self.fullSizedImage)

        self.fullSizedImageFilter.active = True
        self.fullSizedImageFilter.width = 2000
        self.fullSizedImageFilter.height = 2000

        anim = Animation(opacity = 1, duration = 0.3)
        anim.start(self.fullSizedImageFilter)

    def disp_web_page(self, url):
        self.base.add_widget(self.webPageBase)
        self.base.add_widget(self.webPage)

        self.webPage.start_cef(url)
        self.webPage.displaying = True

        self.fullSizedImageFilter.active = True
        self.fullSizedImageFilter.width = 2000
        self.fullSizedImageFilter.height = 2000

        anim = Animation(opacity = 1, duration = 0.3)
        anim.start(self.webPage)
        anim.start(self.fullSizedImageFilter)

    def close_full_image(self, button = None, **args):
        self.base.remove_widget(self.webPageBase)
        self.base.remove_widget(self.webPage)

        anim1 = Animation(opacity = 0, duration = 0.3)
        anim1.start(self.fullSizedImage)

        self.fullSizedImageFilter.active = False

        anim = Animation(opacity = 0, duration = 0.3) + Animation(height = 0, duration = 0)
        anim.start(self.fullSizedImageFilter)
        self.webPage.start_cef("")
        self.webPage.displaying = False

    def reset(self):

        #reset tampilan awal
        self.disp_tweets('_home_')
        self.close_full_image()

    newTweets = []
    lastNewTweetIdx = 99999
    newToOld = True

    def add_tweet(self, *largs):
        # reverse so the older ones will be displayed first
        if self.lastNewTweetIdx < len(self.newTweets):
            tweetData = self.newTweets[self.lastNewTweetIdx]
            tweet = Tweet(**tweetData)
            #if displaying new account
            if self.newToOld:
                # add the tweet at the beginning (bottom) of the stack
                self.tweetContainer.add_widget(tweet)
            #if refreshing
            else:
                # add the tweet at the end (top) of the stack
                self.tweetContainer.add_widget(tweet, len(self.tweetContainer.children))

            # set target height for tweet container
            self.trgHeight += tweet.trgHeight + self.tweetContainer.spacing[1]

            # remove >50 tweets
            if len(self.tweetContainer.children) > self.maxTweet:
                self.trgHeight -= self.tweetContainer.children[0].height + self.tweetContainer.spacing[1]
                self.tweetContainer.children[0].delete()

            # start anim to change tweet container height to target height
            anim = Animation(height = self.trgHeight, duration = self.animDur)
            anim.start( self.tweetContainer)
            self.lastNewTweetIdx += 1
        else:
            self.lastNewTweetIdx = 99999

# --- additional widgets ---

# Tweet display
class Tweet(BoxLayout, StencilView):
    trgHeight = 0;
    animDur = 0.5

    def __init__(self, **kwargs):
        super(Tweet, self).__init__(**kwargs)

        contentContainer = self.ids['content_container']

        self.profPic = self.ids['profile_image']
        profPicLoader = Loader.image(kwargs["profile_image"])
        profPicLoader.bind(on_load=self._image_loaded)

        userName = self.ids['user_name']
        userName.text = kwargs["user_name"] + " " + "[size=19][color=075981]" + " @"+kwargs["screen_name"] + " - " + to_friendly_time(kwargs["created_at"]) + "[/color][/size]"
        userName.markup = True


        tweetText = self.ids['tweet_text']
        tweetText.text = kwargs["text"]

        self.linkButton = self.ids['link_button']

        urls = kwargs['urls']
        if len(urls)>0:
            self.link = urls[0]["url"]
            if self.link[:15] != "http://youtu.be":
                self.add_hyperlinks(tweetText, urls)
                self.linkButton.bind(on_release = self.on_ref_pressed_btn)

        # hashtag = self.ids['hashtag']

        self.trgHeight = self.height

        if len(kwargs["media"]) > 0:
            pass
            self.addImageCont = self.ids['additional_image_cont']
            self.addImage = self.ids['additional_image']
            self.addImageBtn = self.ids['additional_image_button']

            addImageLoader = Loader.image(kwargs["media"][0]['url'])
            addImageLoader.bind(on_load=self._add_image_loaded)

            self.addImageCont.height = 300
            self.fullHeight = int(kwargs["media"][0]['lrg_height'])

            self.trgHeight += self.addImageCont.height

        self.height = 0
        self.opacity = 0
        anim = Animation(height = self.trgHeight, opacity = 1, duration = self.animDur)
        anim.start(self)

    hypStart = '[b][color=075981][ref='
    hypEnd = '[/ref][/color][/b]'

    def add_hyperlinks(self, label, urls):
            #apply in reverse so the char idx doesn't get mixed up
            for i in xrange(len(urls) - 1, -1, -1):
                url = urls[i]
                label.text = label.text[:url["start"]] + self.hypStart + url["url"] + ']' + label.text[url["start"]:url["end"]] + self.hypEnd + label.text[url["end"]:]

            label.markup = True
            label.bind(on_ref_press = self.on_ref_pressed)

    def _image_loaded(self, proxyImage):
        if proxyImage.image.texture:
            self.profPic.texture = proxyImage.image.texture

    def _add_image_loaded(self, proxyImage):
        if proxyImage.image.texture:
            self.addImage.texture = proxyImage.image.texture

            self.addImage.opacity = 0
            anim = Animation(opacity = 1, duration = self.animDur)
            anim.start(self.addImage)

            self.addImageBtn.bind(on_press = self.on_image_pressed)

    def on_image_pressed(self, button, **args):
        app.infoNgabandungan.disp_full_image(self.addImage.texture, self.addImage.height, self.fullHeight)

    def on_ref_pressed_btn(self, btn, *largs):
        app.infoNgabandungan.disp_web_page(self.link)

    def on_ref_pressed(self, *largs):
        #largs[1] = url
        app.infoNgabandungan.disp_web_page(largs[1])

    def delete(self):
        # anim = Animation(height = 1, duration = 0.3)
        # anim.start(self)
        self.parent.remove_widget(self)
        # Clock.schedule_once(self.really_delete, self.animDur)

    def really_delete(self):
        self.parent.remove_widget(self)

# Filter display
class FilterSuperGroup(StackLayout):
    def __init__(self, **kwargs):
        super(FilterSuperGroup, self).__init__(**kwargs)

        title = self.ids['title']
        title.text = kwargs["title"]

        self.accordion = self.ids['accordion']

class FilterGroup(AccordionItem):
    def __init__(self, **kwargs):
        super(FilterGroup, self).__init__(**kwargs)

        self.filters = self.ids['filters']


class BtnFilter(ToggleButton):
    def __init__(self, **kwargs):
        super(BtnFilter, self).__init__(**kwargs)

        self.text = kwargs["name"]
    def on_press(self):
        app.infoNgabandungan.disp_tweets(self.text)


# ------------- SADANG SERANG INTERAKTIF ---------------------

class SadangSerangInteraktif(Screen):
    def __init__(self, **kwargs):
        super(SadangSerangInteraktif, self).__init__(**kwargs)
        self.add_widget(TopBar())

        #ini judul
        #self.title = 'Sadang Serang Interaktif'

        #variabel buat nampung path
        rootPath = os.path.dirname(os.path.realpath(sys.argv[0]))

        #array photo
        self.photos = []
        for image in os.listdir(rootPath + '/Photos'):
            self.photos.append(rootPath + '/Photos/' + image)

        #untuk kelas screen manager
        self.screenManager = self.ids['screenManager']
        self.screenManager.transition = FadeTransition(duration=1.0)

        self.btnNext = self.ids['btn_next']
        self.btnPrev = self.ids['btn_prev']

        self.btnNext.bind(on_release = self.on_next)
        self.btnPrev.bind(on_release = self.on_prev)

        self.pages = []
        self.crntPage = 0

        #untuk iterasi ngambil source file
        for i in range(0,len(self.photos)):
            page = 'page'
            page = page + str(i)
            self.page = Page(name=page, source = self.photos[i])
            self.screenManager.add_widget(self.page)
            self.pages.append(page)

        self.bind(on_touch_down = self.on_td)
        self.bind(on_touch_up = self.on_tu)

    def on_next(self, btn = None, **args):
        if self.crntPage < (len(self.pages) - 1):
            self.crntPage += 1
        else:
            self.crntPage -= len(self.pages)

        self.screenManager.current = self.pages[self.crntPage]

    def on_prev(self, btn = None, **args):
        if self.crntPage > 0:
            self.crntPage -= 1
        else:
            self.crntPage = len(self.pages) - 1

        self.screenManager.current = self.pages[self.crntPage]

    tX = 0
    tY = 0
    minDist = 80

    def on_td(self, widget, touch):
        self.tX = touch.x


    def on_tu(self, widget, touch):
        if self.tX - touch.x > self.minDist:
            self.on_next()

        if self.tX - touch.x < -self.minDist:
            self.on_prev()

    def reset(self):
        self.crntPage = 0
        self.screenManager.current = self.pages[self.crntPage]

class Page(Screen):
    source = StringProperty()

    def __init__(self, **kwargs):
        super(Page, self).__init__(**kwargs)

    def reset(self):
        pass

# ------------- RUMAH KITA ---------------------

class RumahKita(Screen):    

    def __init__(self,**kwargs):
        super(RumahKita,self).__init__(**kwargs)     
        self.add_widget(TopBar())     
        ###### popup as instance of ViewerScreen    
        gallery=ToggleGallery()
        self.add_widget(gallery)

    def reset(self):
        pass
class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.pageTitle = self.ids['page_title']

    def on_parent(self, a, b):
        if self.parent:
            self.pageTitle.text = self.parent.name.upper()

            
class ThumbnailPhotos(FloatLayout):
    popup=ObjectProperty(0)
    isPopup=BooleanProperty()

    def __init__(self,**kwargs):
        super(ThumbnailPhotos,self).__init__(**kwargs)          
        ###### popup as instance of ViewerScreen    
        self.popup=ViewerPhotos()
        # self.isPopup=self.popup.isPopup
        layout = GridLayout(cols=3, padding=10, spacing=20,size_hint=(None, None), width=800)
        layout.bind(minimum_height=layout.setter('height'))     
        ###### make thumbnail base on length/sum of image list
        for i in range(len(photo_rumahKita)):
            btn = Button(id='btn'+str(i), size=(300,300),size_hint=(None, None),background_normal=photo_rumahKita[i])
            layout.add_widget(btn)
            btn.bind(on_press=self.popup.open_popup)
            btn.bind(on_press=self.printer)
        root = ScrollView(size_hint=(None, None), size=(1080, 720),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        self.add_widget(root)

        ###### add popup to thumbnailscreen widget
        self.add_widget(self.popup)

    def thumbnail_hide(self):
        self.pos_hint={'x':1,'y':1}
        self.popup.close_popup()

    def thumbnail_unhide(self):
        self.pos_hint={'x':0,'y':0}

    def printer(self,b,**kwargs):
        print self.isPopup

class ViewerPhotos(FloatLayout):
    ####  list of image and index variable
    photos = photo_rumahKita
    idx=0
    isPopup=False
    def __init__(self, **kwargs):
        super(ViewerPhotos, self).__init__(**kwargs)
        self.img=self.ids['img_display']

    # def get_exif_data(fname):
    #     """Get embedded EXIF data from image file."""
    #     ret = {}
    #     try:
    #         img = Image.open(fname)
    #         if hasattr( img, '_getexif' ):
    #             # raw data
    #             exifinfo = img._getexif()
    #             if exifinfo != None:
    #                 for tag, value in exifinfo.items():
    #                     decoded = TAGS.get(tag, tag)
    #                     ret[decoded] = value
    #                     # fo.write(ret[decoded]+"\n")
    #     except IOError:
    #         print 'IOERROR ' + fname
    #     # fo.close()    
    #     return ret


    def next_image(self):       
        if(self.idx==len(self.photos)-1):
            self.idx=0
        else:
            self.idx+=1     
        print self.idx

    def prev_image(self):
        if(self.idx==0):
            self.idx=len(self.photos)-1
        else:
            self.idx-=1

    def change_image(self,*args):
        filename=join(self.photos[self.idx])
        self.img.source=filename      
        #self.exifdata  = get_exif_data(filename)
        #print self.exifdata['ImageDescription']
        caption =  filename.split("/")[2][:-4]                
        self.caps=self.ids['caption']
        self.caps.text = caption

        print self.caps.text


    #### method to move popup into front of screen
    def open_popup(self,b,**kwargs):
        self.img.source=self.photos[int(b.id[3:])]
        pop=self.ids['img_display']
        bgBtn=self.ids['bgButton']
        bgBtn.pos_hint={'x':0, 'y':0}
        pop.pos_hint={'x':0, 'y':0}
        self.pos_hint={'x':0, 'y':0}
        self.isPopup=True
        #self.change_image()
        filename=join(self.photos[int(b.id[3:])])
        self.img.source=filename
        caption =  filename.split("/")[2][:-4]                
        self.caps=self.ids['caption']
        self.caps.text = caption

        print self.caps.text
        # print self.isPopup

    #### method to move popup out of screen
    def close_popup(self):
        pop=self.ids['img_display']
        bgBtn=self.ids['bgButton']
        bgBtn.pos_hint={'x':1, 'y':1}
        pop.pos_hint={'x':1, 'y':1}
        self.pos_hint={'x':1, 'y':1}
        self.isPopup=False
        # print self.isPopup

#### class of scrollview thumbnail              
class ThumbnailPDF(FloatLayout):
    popup=ObjectProperty(0)
    isPopup=BooleanProperty

    def __init__(self,**kwargs):
        super(ThumbnailPDF,self).__init__(**kwargs)         
        ###### popup as instance of ViewerScreen    
        self.popup=ViewerPDF()
        self.isPopup=self.popup.isPopup
        layout = GridLayout(cols=3, padding=10, spacing=20,size_hint=(None, None), width=800)
        layout.bind(minimum_height=layout.setter('height'))
        ###### make thumbnail base on length/sum of image list
        
        btn1 = Button(id='btn1', size=(300,300),size_hint=(None, None),background_normal=img_airtanah[0])
        layout.add_widget(btn1)
        btn1.bind(on_press=self.popup.open_popup)

        btn2 = Button(id='btn2', size=(300,300),size_hint=(None, None),background_normal=img_hidroponik[0])
        layout.add_widget(btn2)
        btn2.bind(on_press=self.popup.open_popup)

        btn3 = Button(id='btn3', size=(300,300),size_hint=(None, None),background_normal=img_berkebun[0])
        layout.add_widget(btn3)
        btn3.bind(on_press=self.popup.open_popup)

        root = ScrollView(size_hint=(None, None), size=(1080, 720),pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        root.add_widget(layout)
        self.add_widget(root)

        ###### add popup to thumbnailscreen widget
        self.add_widget(self.popup)

    def thumbnail_hide(self):
        self.pos_hint={'x':1,'y':1}
        self.popup.close_popup()

    def thumbnail_unhide(self):
        self.pos_hint={'x':0,'y':0}

class ViewerPDF(FloatLayout):
    ####  list of image and index variable
    list_airtanah=img_airtanah
    list_hidroponik=img_hidroponik
    list_berkebun=img_berkebun
    idx=0
    bool_airtanah=False
    bool_hidroponik=False
    bool_berkebun=False
    isPopup=False

    def __init__(self, **kwargs):
        super(ViewerPDF, self).__init__(**kwargs)
        self.img=self.ids['img_display']

    def next_image(self):
        pop=self.ids['img_display'] 
        length=0    
        if self.bool_airtanah:
            length=len(self.list_airtanah)
        elif self.bool_hidroponik:
            length=len(self.list_hidroponik)
        elif self.bool_berkebun:
            length=len(self.list_berkebun)

        if(self.idx==length-1):
            self.idx=0
        else:
            self.idx+=1     
        print self.idx
        print length

    def prev_image(self):
        pop=self.ids['img_display'] 
        length=0    
        if self.bool_airtanah:
            length=len(self.list_airtanah)
        elif self.bool_hidroponik:
            length=len(self.list_hidroponik)
        elif self.bool_berkebun:
            length=len(self.list_berkebun)

        if(self.idx==0):
            self.idx=length-1
        else:
            self.idx-=1

    def change_image(self,*args):
        pop=self.ids['img_display'] 
        if self.bool_airtanah:
            filename=join(self.list_airtanah[self.idx]) 
            pop.source=filename     
        elif self.bool_hidroponik:
            filename=join(self.list_hidroponik[self.idx])
            pop.source=filename
        elif self.bool_berkebun :
            filename=join(self.list_berkebun[self.idx]) 
            pop.source=filename

                
    #### method to move popup into front of screen
    def open_popup(self,b,**kwargs):
        if int(b.id[3:])==1:
            self.img.source=self.list_airtanah[0]
            self.bool_airtanah=True
            self.bool_hidroponik=False
            self.bool_berkebun=False
        elif int(b.id[3:])==2:
            self.img.source=self.list_hidroponik[0]
            self.bool_airtanah=False
            self.bool_hidroponik=True
            self.bool_berkebun=False
        else :
            self.img.source=self.list_berkebun[0]
            self.bool_airtanah=False
            self.bool_hidroponik=False
            self.bool_berkebun=True

        pop=self.ids['img_display']
        bgBtn=self.ids['bgButton']
        bgBtn.pos_hint={'x':0, 'y':0}
        pop.pos_hint={'x':0, 'y':0}
        self.idx=0
        self.pos_hint={'x':0, 'y':0}
        self.isPopup=True

    #### method to move popup out of screen
    def close_popup(self):
        pop=self.ids['img_display']
        bgBtn=self.ids['bgButton']
        bgBtn.pos_hint={'x':1, 'y':1}
        pop.pos_hint={'x':1, 'y':1}
        self.pos_hint={'x':1, 'y':1}    
        self.isPopup=False   
           
class ToggleGallery(FloatLayout):
    """docstring for ClassName"""
    photosScreen=ObjectProperty(0)
    pdfScreen=ObjectProperty(0)
    btn1=ObjectProperty(0)
    btn2=ObjectProperty(0)

    def __init__(self, **kwargs):
        super(ToggleGallery, self).__init__(**kwargs)   
        self.photosScreen=ThumbnailPhotos()
        self.pdfScreen=ThumbnailPDF()   
        self.btn1 = ToggleButton(group='rumah-kita', size_hint=[.15,.10], pos_hint={'x':0.85, 'y':0.3}, #text='Photos', 
                                    background_color=(0.8,0.8,0.8,0.8),
                                    background_normal='assets-rumah-kita/info-perkembangan-button.png',
                                    background_down='assets-rumah-kita/info-perkembangan-button-hit.png')
        self.btn2 = ToggleButton(group='rumah-kita', state='down', size_hint=[.15,.10], y=100, pos_hint={'x':0.85, 'y':0.4}, #text='Ebooks', 
                                    background_color=(0.8,0.8,0.8,0.8),
                                    background_normal='assets-rumah-kita/info-tematik-button.png',
                                    background_down='assets-rumah-kita/info-tematik-button-hit.png')
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.photosScreen)
        self.add_widget(self.pdfScreen)        
        self.photosScreen.thumbnail_hide()
        # self.pdfScreen.thumbnail_hide()
        # print "abbcbcackjasjkcbas"+btn1.state
        if self.photosScreen.isPopup or self.pdfScreen.isPopup :
            self.button_hide
        else:
            self.button_unhide

        self.btn1.bind(on_press=self.on_press_photo)
        self.btn2.bind(on_press=self.on_press_pdf)

    def button_hide(self):
        self.btn1.pos_hint={'x':1,'y':1}
        self.btn2.pos_hint={'x':1,'y':1}

    def button_unhide(self):
        self.btn1.pos_hint={'x':0,'y':0}
        self.btn2.pos_hint={'x':0,'y':0}        

    def on_press_photo(self,b,**kwargs):
        if b.state=='down':
            self.photosScreen.thumbnail_unhide()
            self.pdfScreen.thumbnail_hide()
            self.btn2.state='normal'
            print "photo down"
        elif b.state=='normal' :
            self.pdfScreen.thumbnail_unhide()
            self.photosScreen.thumbnail_hide()
            print "photo normal"

    def on_press_pdf(self,b,**kwargs):
        if b.state=='down':
            self.pdfScreen.thumbnail_unhide()
            self.photosScreen.thumbnail_hide()
            self.btn1.state='normal'
            print "pdf down"
        elif b.state=='normal' :
            self.photosScreen.thumbnail_unhide()
            self.pdfScreen.thumbnail_hide()
            print "pdf normal"

if __name__ == '__main__':
    # app = SmartCityApp().run(
    SmartCityApp().run()
