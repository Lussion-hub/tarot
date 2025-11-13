from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
import os
import random
import time
from PIL import Image as PILImage
import glob
import cv2
import numpy as np
import re
try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    # Android 권한 요청
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    # Android 환경 변수
    Environment = autoclass('android.os.Environment')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    mActivity = PythonActivity.mActivity
    IS_ANDROID = True
except:
    IS_ANDROID = False
    Environment = None

class ColorCardScreen(Screen):
    """색도형카드 선택 화면"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def setup(self, app):
        self.app = app
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 제목
        title = Label(text='색도형카드 선택', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)
        
        # 스크롤 가능한 그리드
        scroll = ScrollView()
        grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        # 카드 이미지 로드 및 표시
        if hasattr(app, 'color_shape_path') and os.path.exists(app.color_shape_path):
            image_files = glob.glob(os.path.join(app.color_shape_path, "*.webp"))
            if not image_files:
                image_files = glob.glob(os.path.join(app.color_shape_path, "*.png"))
            if not image_files:
                image_files = glob.glob(os.path.join(app.color_shape_path, "*.jpg"))
            
            selected_images = random.sample(image_files, min(20, len(image_files)))
            
            for img_path in selected_images:
                btn = Button(size_hint_y=None, height=150)
                try:
                    img = PILImage.open(img_path)
                    img = img.resize((150, 150))
                    
                    # 흐림 효과 적용
                    if app.blur_effect > 0:
                        img_array = np.array(img)
                        if img_array.shape[2] == 4:
                            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
                        blur_amount = int(app.blur_effect * 0.15)
                        if blur_amount > 0:
                            img_array = cv2.GaussianBlur(img_array, (0, 0), blur_amount)
                        img = PILImage.fromarray(img_array)
                    
                    # Kivy Image로 변환
                    img_texture = self.pil_to_texture(img)
                    btn.background_normal = ''
                    btn.background_color = (1, 1, 1, 1)
                    img_widget = Image(texture=img_texture, size_hint=(1, 1))
                    btn.add_widget(img_widget)
                except Exception as e:
                    btn.text = f"Error\n{os.path.basename(img_path)}"
                
                btn.bind(on_press=lambda instance, path=img_path: self.on_card_click(path))
                grid.add_widget(btn)
        
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        
        # 하단 버튼
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_back = Button(text='뒤로', size_hint_x=0.3)
        btn_back.bind(on_press=lambda x: setattr(app.screen_manager, 'current', 'main'))
        btn_layout.add_widget(btn_back)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def pil_to_texture(self, pil_image):
        """PIL Image를 Kivy Texture로 변환"""
        img_data = pil_image.tobytes()
        texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        texture.blit_buffer(img_data, colorfmt='rgb', bufferfmt='ubyte')
        return texture
    
    def on_card_click(self, image_path):
        """카드 클릭 처리"""
        self.app.memory_card1 = image_path
        file_name = os.path.basename(image_path)
        card_number = file_name[3:5] if len(file_name) >= 5 else "00"
        
        if file_name.startswith("CS"):
            self.app.time1 = 31
        else:
            self.app.time1 = None
        
        self.app.load_tarot_front_cards()
        setattr(self.app.screen_manager, 'current', 'sequential_color')
        # 순차 화면 표시 시작
        seq_screen = self.app.screen_manager.get_screen('sequential_color')
        seq_screen.show_sequential()

class SequentialColorScreen(Screen):
    """색도형카드 순차 표시 화면"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.position_times = {}
        
    def setup(self, app):
        self.app = app
        layout = FloatLayout()
        
        # 제목
        title = Label(text='순차 표시', size_hint=(1, None), height=50, 
                     pos_hint={'top': 1}, font_size=20)
        layout.add_widget(title)
        
        # 그리드 영역
        self.grid_layout = GridLayout(cols=3, spacing=5, 
                                      size_hint=(0.9, 0.7),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.45})
        layout.add_widget(self.grid_layout)
        
        # 하단 버튼
        btn_layout = BoxLayout(size_hint=(0.9, None), height=50,
                              pos_hint={'center_x': 0.5, 'y': 0.05}, spacing=10)
        btn_back = Button(text='뒤로')
        btn_back.bind(on_press=lambda x: setattr(app.screen_manager, 'current', 'color_card'))
        btn_layout.add_widget(btn_back)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def show_sequential(self):
        """순차 표시 시작"""
        if not self.app.memory_card1:
            return
        
        self.grid_layout.clear_widgets()
        self.position_times = {}
        
        display_times = [31, 40, 43]
        random.shuffle(display_times)
        
        # 선택된 카드 이미지 로드
        try:
            selected_img = PILImage.open(self.app.memory_card1)
            selected_img = selected_img.resize(self.app.sc_size)
            texture = self.pil_to_texture(selected_img)
        except:
            return
        
        # 3x3 그리드 생성
        for idx in range(9):
            row = idx // 3
            col = idx % 3
            display_time = display_times[idx]
            self.position_times[(row, col)] = display_time
            
            btn = Button(size_hint=(1, 1))
            img_widget = Image(texture=texture, size_hint=(1, 1))
            btn.add_widget(img_widget)
            
            def create_handler(r, c, t, b=btn):
                def handler(instance):
                    self.on_position_click((r, c), t)
                return handler
            
            btn.bind(on_press=create_handler(row, col, display_time, btn))
            self.grid_layout.add_widget(btn)
            
            # 설정된 시간 후 이미지 숨기기
            Clock.schedule_once(lambda dt, b=btn: self.hide_card(b), display_time / 1000.0)
    
    def hide_card(self, button):
        """카드 숨기기"""
        button.clear_widgets()
        button.background_color = (0.2, 0.2, 0.2, 1)
        button.text = ''
    
    def pil_to_texture(self, pil_image):
        """PIL Image를 Kivy Texture로 변환"""
        img_data = pil_image.tobytes()
        texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        texture.blit_buffer(img_data, colorfmt='rgb', bufferfmt='ubyte')
        return texture
    
    def on_position_click(self, position, display_time):
        """위치 클릭 처리"""
        row, col = position
        file_name = os.path.basename(self.app.memory_card1)
        
        if not file_name.startswith("CS"):
            self.app.time1 = display_time
        
        self.app.selected_cards.append((position, display_time))
        setattr(self.app.screen_manager, 'current', 'tarot_back')
        # 타로 뒷면 화면 표시
        tarot_back_screen = self.app.screen_manager.get_screen('tarot_back')
        tarot_back_screen.show_tarot_backs()

class TarotBackScreen(Screen):
    """타로 뒷면 화면"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def setup(self, app):
        self.app = app
        layout = FloatLayout()
        
        # 제목
        title = Label(text='타로 뒷면', size_hint=(1, None), height=50,
                     pos_hint={'top': 1}, font_size=20)
        layout.add_widget(title)
        
        # 스크롤 가능한 그리드
        scroll = ScrollView(size_hint=(1, 0.85), pos_hint={'top': 0.95})
        self.grid_layout = GridLayout(cols=10, spacing=5, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll.add_widget(self.grid_layout)
        layout.add_widget(scroll)
        
        # 하단 버튼
        btn_layout = BoxLayout(size_hint=(0.9, None), height=50,
                              pos_hint={'center_x': 0.5, 'y': 0.02}, spacing=10)
        btn_sequential = Button(text='타로 앞면 순차')
        btn_sequential.bind(on_press=lambda x: self.show_sequential_fronts())
        btn_back = Button(text='뒤로')
        btn_back.bind(on_press=lambda x: setattr(app.screen_manager, 'current', 'sequential_color'))
        btn_layout.add_widget(btn_sequential)
        btn_layout.add_widget(btn_back)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def show_tarot_backs(self):
        """타로 뒷면 표시"""
        self.grid_layout.clear_widgets()
        
        if not os.path.exists(self.app.tarot_back_path):
            return
        
        back_files = glob.glob(os.path.join(self.app.tarot_back_path, "*.webp"))
        if not back_files:
            back_files = glob.glob(os.path.join(self.app.tarot_back_path, "*.png"))
        if not back_files:
            back_files = glob.glob(os.path.join(self.app.tarot_back_path, "*.jpg"))
        
        if not back_files:
            return
        
        selected_back = random.choice(back_files)
        self.app.current_back_file = selected_back
        
        # 앞면 카드 수 확인
        front_files = glob.glob(os.path.join(self.app.tarot_front_path, "*.webp"))
        if not front_files:
            front_files = glob.glob(os.path.join(self.app.tarot_front_path, "*.png"))
        total_cards = len(front_files)
        
        # 뒷면 이미지 로드
        try:
            back_img = PILImage.open(selected_back)
            back_img = back_img.resize(self.app.ts_size)
            back_texture = self.pil_to_texture(back_img)
        except:
            return
        
        # 그리드에 카드 배치
        for i in range(total_cards):
            btn = Button(size_hint_y=None, height=self.app.ts_size[1])
            img_widget = Image(texture=back_texture, size_hint=(1, 1))
            btn.add_widget(img_widget)
            
            def create_handler(idx):
                def handler(instance):
                    self.on_tarot_back_click(idx)
                return handler
            
            btn.bind(on_press=create_handler(i))
            self.grid_layout.add_widget(btn)
    
    def pil_to_texture(self, pil_image):
        """PIL Image를 Kivy Texture로 변환"""
        img_data = pil_image.tobytes()
        texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        texture.blit_buffer(img_data, colorfmt='rgb', bufferfmt='ubyte')
        return texture
    
    def on_tarot_back_click(self, card_index):
        """타로 뒷면 클릭 처리"""
        front_files = glob.glob(os.path.join(self.app.tarot_front_path, "*.webp"))
        if not front_files:
            front_files = glob.glob(os.path.join(self.app.tarot_front_path, "*.png"))
        
        if card_index < len(front_files):
            selected_file = front_files[card_index]
            if selected_file not in self.app.selected_cards:
                self.app.selected_cards.append(selected_file)
    
    def show_sequential_fronts(self):
        """타로 앞면 순차 표시"""
        setattr(self.app.screen_manager, 'current', 'tarot_sequential')
        # 타로 순차 화면 표시
        tarot_seq_screen = self.app.screen_manager.get_screen('tarot_sequential')
        tarot_seq_screen.show_sequential()

class TarotSequentialScreen(Screen):
    """타로 앞면 순차 표시 화면"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def setup(self, app):
        self.app = app
        layout = FloatLayout()
        
        # 제목
        title = Label(text='타로 앞면 순차', size_hint=(1, None), height=50,
                     pos_hint={'top': 1}, font_size=20)
        layout.add_widget(title)
        
        # 스크롤 가능한 그리드
        scroll = ScrollView(size_hint=(1, 0.85), pos_hint={'top': 0.95})
        self.grid_layout = GridLayout(cols=10, spacing=5, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll.add_widget(self.grid_layout)
        layout.add_widget(scroll)
        
        # 하단 버튼
        btn_layout = BoxLayout(size_hint=(0.9, None), height=50,
                              pos_hint={'center_x': 0.5, 'y': 0.02}, spacing=10)
        btn_complete = Button(text='완료')
        btn_complete.bind(on_press=lambda x: self.show_complete())
        btn_back = Button(text='뒤로')
        btn_back.bind(on_press=lambda x: setattr(app.screen_manager, 'current', 'tarot_back'))
        btn_layout.add_widget(btn_complete)
        btn_layout.add_widget(btn_back)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def show_sequential(self):
        """순차 표시 시작"""
        self.grid_layout.clear_widgets()
        
        front_files = glob.glob(os.path.join(self.app.tarot_front_path, "*.webp"))
        if not front_files:
            front_files = glob.glob(os.path.join(self.app.tarot_front_path, "*.png"))
        
        if not front_files:
            return
        
        simultaneous_cards = self.app.simultaneous_cards
        exposure_time = self.app.display_time
        
        # 카드 위치 랜덤 배치
        total_cards = len(front_files)
        card_numbers = list(range(total_cards))
        random.shuffle(card_numbers)
        
        # 앞면 이미지 미리 로드
        front_textures = {}
        for card_num in card_numbers:
            try:
                img = PILImage.open(front_files[card_num])
                img = img.resize(self.app.ts_size)
                
                # 흐림 효과
                if self.app.blur_effect > 0:
                    img_array = np.array(img)
                    if img_array.shape[2] == 4:
                        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
                    blur_amount = int(self.app.blur_effect * 0.15)
                    if blur_amount > 0:
                        img_array = cv2.GaussianBlur(img_array, (0, 0), blur_amount)
                    img = PILImage.fromarray(img_array)
                
                texture = self.pil_to_texture(img)
                front_textures[card_num] = texture
            except:
                continue
        
        # 뒷면 이미지
        back_files = glob.glob(os.path.join(self.app.tarot_back_path, "*.webp"))
        if back_files:
            try:
                back_img = PILImage.open(back_files[0])
                back_img = back_img.resize(self.app.ts_size)
                back_texture = self.pil_to_texture(back_img)
            except:
                back_texture = None
        else:
            back_texture = None
        
        # 초기 뒷면 표시
        for i in range(total_cards):
            btn = Button(size_hint_y=None, height=self.app.ts_size[1])
            if back_texture:
                img_widget = Image(texture=back_texture, size_hint=(1, 1))
                btn.add_widget(img_widget)
            self.grid_layout.add_widget(btn)
        
        # 순차 표시 로직 (간소화)
        self._current_index = 0
        self._front_textures = front_textures
        self._back_texture = back_texture
        self._card_numbers = card_numbers
        self._total_cards = total_cards
        self._exposure_time = exposure_time
        self._simultaneous = simultaneous_cards if simultaneous_cards > 0 else total_cards
        
        Clock.schedule_once(lambda dt: self.show_next_set(), exposure_time / 1000.0)
    
    def show_next_set(self):
        """다음 세트 표시"""
        start = self._current_index
        end = min(start + self._simultaneous, self._total_cards)
        
        # 앞면 표시
        for i in range(start, end):
            if i < len(self.grid_layout.children):
                btn = self.grid_layout.children[self._total_cards - 1 - i]
                btn.clear_widgets()
                card_num = self._card_numbers[i]
                if card_num in self._front_textures:
                    img_widget = Image(texture=self._front_textures[card_num], size_hint=(1, 1))
                    btn.add_widget(img_widget)
        
        self._current_index = end
        
        if end < self._total_cards:
            Clock.schedule_once(lambda dt: self.show_next_set(), self._exposure_time / 1000.0)
    
    def pil_to_texture(self, pil_image):
        """PIL Image를 Kivy Texture로 변환"""
        img_data = pil_image.tobytes()
        texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        texture.blit_buffer(img_data, colorfmt='rgb', bufferfmt='ubyte')
        return texture
    
    def show_complete(self):
        """완료 화면으로 이동"""
        setattr(self.app.screen_manager, 'current', 'complete')

class CompleteScreen(Screen):
    """완료 화면"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def setup(self, app):
        self.app = app
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 제목
        title = Label(text='선택된 카드', size_hint_y=None, height=50, font_size=24)
        layout.add_widget(title)
        
        # 스크롤 가능한 카드 목록
        scroll = ScrollView()
        card_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        card_layout.bind(minimum_height=card_layout.setter('height'))
        
        for i, card_path in enumerate(app.selected_cards):
            if isinstance(card_path, tuple):
                card_path = card_path[0] if isinstance(card_path[0], str) else card_path[1]
            
            try:
                img = PILImage.open(card_path)
                img = img.resize((150, 220))
                texture = self.pil_to_texture(img)
                
                card_box = BoxLayout(orientation='vertical', size_hint_y=None, height=250)
                img_widget = Image(texture=texture, size_hint=(1, 0.8))
                label = Label(text=f"{i+1}. {os.path.basename(card_path)}", 
                             size_hint_y=None, height=50, text_size=(None, None))
                card_box.add_widget(img_widget)
                card_box.add_widget(label)
                card_layout.add_widget(card_box)
            except:
                continue
        
        scroll.add_widget(card_layout)
        layout.add_widget(scroll)
        
        # 하단 버튼
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_new = Button(text='새로 시작')
        btn_new.bind(on_press=lambda x: self.new_session())
        btn_layout.add_widget(btn_new)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def pil_to_texture(self, pil_image):
        """PIL Image를 Kivy Texture로 변환"""
        img_data = pil_image.tobytes()
        texture = Texture.create(size=(pil_image.width, pil_image.height), colorfmt='rgb')
        texture.blit_buffer(img_data, colorfmt='rgb', bufferfmt='ubyte')
        return texture
    
    def new_session(self):
        """새 세션 시작"""
        self.app.selected_cards = []
        self.app.memory_card1 = ""
        self.app.time1 = None
        setattr(self.app.screen_manager, 'current', 'main')

class MainScreen(Screen):
    """메인 화면"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def setup(self, app):
        self.app = app
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 제목
        title = Label(text='타로 카드 선택 프로그램', size_hint_y=None, height=80, font_size=28)
        layout.add_widget(title)
        
        # 설정 영역
        settings = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=300)
        
        # 경로 설정
        path_label = Label(text='이미지 경로 설정', size_hint_y=None, height=30, font_size=18)
        settings.add_widget(path_label)
        
        # 색도형카드 경로
        sc_layout = BoxLayout(size_hint_y=None, height=40)
        sc_layout.add_widget(Label(text='색/도형:', size_hint_x=0.3))
        sc_input = TextInput(text=app.color_shape_path, multiline=False, size_hint_x=0.7)
        app.color_shape_input = sc_input
        sc_layout.add_widget(sc_input)
        settings.add_widget(sc_layout)
        
        # 타로 앞면 경로
        tf_layout = BoxLayout(size_hint_y=None, height=40)
        tf_layout.add_widget(Label(text='타로 앞면:', size_hint_x=0.3))
        tf_input = TextInput(text=app.tarot_front_path, multiline=False, size_hint_x=0.7)
        app.tarot_front_input = tf_input
        tf_layout.add_widget(tf_input)
        settings.add_widget(tf_layout)
        
        # 타로 뒷면 경로
        tb_layout = BoxLayout(size_hint_y=None, height=40)
        tb_layout.add_widget(Label(text='타로 뒷면:', size_hint_x=0.3))
        tb_input = TextInput(text=app.tarot_back_path, multiline=False, size_hint_x=0.7)
        app.tarot_back_input = tb_input
        tb_layout.add_widget(tb_input)
        settings.add_widget(tb_layout)
        
        # 변수 설정
        var_label = Label(text='변수 설정', size_hint_y=None, height=30, font_size=18)
        settings.add_widget(var_label)
        
        # 시간 설정
        time_layout = BoxLayout(size_hint_y=None, height=40)
        time_layout.add_widget(Label(text='시간(ms):', size_hint_x=0.3))
        time_input = TextInput(text=str(app.display_time), multiline=False, size_hint_x=0.7)
        app.time_input = time_input
        time_layout.add_widget(time_input)
        settings.add_widget(time_layout)
        
        # 동시카드수 설정
        sim_layout = BoxLayout(size_hint_y=None, height=40)
        sim_layout.add_widget(Label(text='동시카드수:', size_hint_x=0.3))
        sim_input = TextInput(text=str(app.simultaneous_cards), multiline=False, size_hint_x=0.7)
        app.simultaneous_input = sim_input
        sim_layout.add_widget(sim_input)
        settings.add_widget(sim_layout)
        
        # 흐림효과 설정
        blur_layout = BoxLayout(size_hint_y=None, height=40)
        blur_layout.add_widget(Label(text='흐림효과(%):', size_hint_x=0.3))
        blur_input = TextInput(text=str(app.blur_effect), multiline=False, size_hint_x=0.7)
        app.blur_input = blur_input
        blur_layout.add_widget(blur_input)
        settings.add_widget(blur_layout)
        
        layout.add_widget(settings)
        
        # 버튼 영역
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        
        btn_color = Button(text='색도형카드 선택', size_hint_y=None, height=50)
        btn_color.bind(on_press=lambda x: self.start_color_cards())
        btn_layout.add_widget(btn_color)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def start_color_cards(self):
        """색도형카드 화면으로 이동"""
        # 설정 업데이트
        try:
            self.app.color_shape_path = self.app.color_shape_input.text
            self.app.tarot_front_path = self.app.tarot_front_input.text
            self.app.tarot_back_path = self.app.tarot_back_input.text
            self.app.display_time = int(self.app.time_input.text)
            self.app.simultaneous_cards = int(self.app.simultaneous_input.text)
            self.app.blur_effect = int(self.app.blur_input.text)
        except:
            pass
        
        setattr(self.app.screen_manager, 'current', 'color_card')
        # 색도형카드 화면 새로고침
        color_screen = self.app.screen_manager.get_screen('color_card')
        color_screen.setup(self.app)

class TarotApp(App):
    def build(self):
        # Android 기본 경로 설정
        if IS_ANDROID and Environment:
            try:
                external_storage = Environment.getExternalStorageDirectory().getAbsolutePath()
                base_path = os.path.join(external_storage, "TarotProject")
            except:
                base_path = "/sdcard/TarotProject"
        else:
            # 데스크톱 테스트용 경로
            base_path = os.path.join(os.path.expanduser("~"), "TarotProject")
        
        # 기본 경로 설정
        self.color_shape_path = os.path.join(base_path, "도형_색카드")
        self.tarot_front_path = os.path.join(base_path, "Rider_Waite", "compressed", "AA_tarot")
        self.tarot_back_path = os.path.join(base_path, "Rider_Waite", "compressed", "AB_tarot")
        self.background_path = os.path.join(base_path, "고속노출시배경")
        
        # 변수 초기화
        self.display_time = 31
        self.sc_size = (150, 150)
        self.ts_size = (45, 73)
        self.blur_effect = 17
        self.simultaneous_cards = 4
        self.memory_card1 = ""
        self.time1 = None
        self.selected_cards = []
        self.current_back_file = None
        
        # 이미지 캐시
        self.image_cache = {'sc': {}, 'ts': {}, 'back': {}}
        self.images_loaded = {'sc': False, 'back': False, 'ts': False}
        
        # 화면 관리자
        self.screen_manager = ScreenManager()
        
        # 화면 생성
        main_screen = MainScreen(name='main')
        main_screen.setup(self)
        self.screen_manager.add_widget(main_screen)
        
        color_screen = ColorCardScreen(name='color_card')
        color_screen.setup(self)
        self.screen_manager.add_widget(color_screen)
        
        seq_color_screen = SequentialColorScreen(name='sequential_color')
        seq_color_screen.setup(self)
        self.screen_manager.add_widget(seq_color_screen)
        
        tarot_back_screen = TarotBackScreen(name='tarot_back')
        tarot_back_screen.setup(self)
        self.screen_manager.add_widget(tarot_back_screen)
        
        tarot_seq_screen = TarotSequentialScreen(name='tarot_sequential')
        tarot_seq_screen.setup(self)
        self.screen_manager.add_widget(tarot_seq_screen)
        
        complete_screen = CompleteScreen(name='complete')
        complete_screen.setup(self)
        self.screen_manager.add_widget(complete_screen)
        
        return self.screen_manager
    
    def load_tarot_front_cards(self):
        """타로 앞면 카드 로딩"""
        if self.images_loaded['ts']:
            return
        
        tarot_front_files = glob.glob(os.path.join(self.tarot_front_path, "*.webp"))
        if not tarot_front_files:
            tarot_front_files = glob.glob(os.path.join(self.tarot_front_path, "*.png"))
        
        for file_path in tarot_front_files:
            try:
                img = PILImage.open(file_path)
                img = img.resize(self.ts_size)
                
                if self.blur_effect > 0:
                    img_array = np.array(img)
                    if img_array.shape[2] == 4:
                        img_array = cv2.GaussianBlur(cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB), (0, 0), 
                                                    int(self.blur_effect * 0.15))
                    else:
                        img_array = cv2.GaussianBlur(img_array, (0, 0), int(self.blur_effect * 0.15))
                    img = PILImage.fromarray(img_array)
                
                self.image_cache['ts'][file_path] = img
            except Exception as e:
                print(f"타로 앞면 이미지 로드 실패: {file_path} - {str(e)}")
        
        self.images_loaded['ts'] = True

if __name__ == '__main__':
    TarotApp().run()

