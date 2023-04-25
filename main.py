import os
import sys
if sys.__stdout__ is None or sys.__stderr__ is None:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'
import datetime
import openpyxl
import pygame
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.popup import Popup
from kivy.clock import Clock

# loads the layout file
Builder.load_file('graphics/layout.kv')

# main class of the program
class MainScreen(BoxLayout):

    # starts important variables
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # setting up DATE and TIME variables to automatically update
        self.DATE = datetime.datetime.now().strftime("%d/%m/%Y")
        self.TIME = datetime.datetime.now().strftime("%H:%M:%S")
        # initiating the variables used by the snackbar that counts clicks
        self.snackbar = None
        self.counter = 0
        self.last_button_press_time = None

    # plays a click sound
    def click_sound(self):
        try:
            pygame.mixer.init()
            sound_file = os.path.join(os.getcwd(), 'sounds/click.wav')
            sound = pygame.mixer.Sound(sound_file)
            sound.play()
        except FileNotFoundError:
            sound = None
            print("Erro: O arquivo de som não foi encontrado ou não pôde ser carregado.")

    # erases all the selected buttons and reset their colors
    def eraser(self):
        # make its color blue
        self.ids.auto_button.md_bg_color = 'blue'
        # makes the manual button color grey
        self.ids.manual_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        # makes all the period of the day button grey
        self.ids.morning_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        self.ids.afternoon_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        self.ids.night_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        # keeps all the manual date and period of the day buttons disabled
        self.ids.select_date.disabled = True
        self.ids.calendar_button.disabled = True
        self.ids.select_day_period.disabled = True
        self.ids.morning_button.disabled = True
        self.ids.afternoon_button.disabled = True
        self.ids.night_button.disabled = True
        # makes all the age selection buttons grey again
        self.ids.twelve_yo_button.md_bg_color = (0.35, 0.35, 0.35, 1) 
        self.ids.thirteen_til_seventeen_yo_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        self.ids.eighteen_til_fiftynine_yo_button.md_bg_color = (0.35, 0.35, 0.35, 1) 
        self.ids.sixty_yo_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        # makes all the public selection buttons grey again
        self.ids.cei_button.md_bg_color = (0.35, 0.35, 0.35, 1) 
        self.ids.emei_button.md_bg_color = (0.35, 0.35, 0.35, 1) 
        self.ids.emef_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        self.ids.etec_button.md_bg_color = (0.35, 0.35, 0.35, 1)
        self.ids.community_button.md_bg_color = (0.35, 0.35, 0.35, 1) 
        self.ids.employee_button.md_bg_color = (0.35, 0.35, 0.35, 1)

    # handles what button was clicked between auto and manual
    def toggle_date_and_time(self, button):
        # declares variables associated with the two possible buttons
        auto_button = self.ids.auto_button
        manual_button = self.ids.manual_button
        # if the auto button is clicked
        if button == auto_button:
            # returns the date to the current date
            self.DATE = datetime.datetime.now().strftime("%d/%m/%Y")
            print(self.DATE)
            # returns the time to the current time
            self.TIME = datetime.datetime.now().strftime("%H:%M:%S")
            print(self.TIME)
            # info message
            snackbar = Snackbar(
                            text=f"Data alterada para {self.DATE}.", 
                            duration=4.0,
                            bg_color=(0, 0.5, 0, 1), # green
                            font_size="16sp"
                        )
            snackbar.open()
            # make its color blue
            button.md_bg_color = 'blue'
            # makes the manual button color grey
            manual_button.md_bg_color = (0.35, 0.35, 0.35, 1)
            # makes all the period of the day button grey
            self.ids.morning_button.md_bg_color = (0.35, 0.35, 0.35, 1)
            self.ids.afternoon_button.md_bg_color = (0.35, 0.35, 0.35, 1)
            self.ids.night_button.md_bg_color = (0.35, 0.35, 0.35, 1)
            # keeps all the manual date and period of the day buttons disabled
            self.ids.select_date.disabled = True
            self.ids.calendar_button.disabled = True
            self.ids.select_day_period.disabled = True
            self.ids.morning_button.disabled = True
            self.ids.afternoon_button.disabled = True
            self.ids.night_button.disabled = True
        # if the manual button is clicked    
        elif button == manual_button:
            # make its color blue
            button.md_bg_color = 'blue'
            # makes the auto button color grey
            auto_button.md_bg_color = (0.35, 0.35, 0.35, 1)
            # enable sall the manual date and period of the day buttons
            self.ids.select_date.disabled = False
            self.ids.calendar_button.disabled = False
            self.ids.select_day_period.disabled = False
            self.ids.morning_button.disabled = False
            self.ids.afternoon_button.disabled = False
            self.ids.night_button.disabled = False

    # handles the time of the day buttons
    def on_manual_period(self, instance):
        buttons = [self.ids.morning_button, self.ids.afternoon_button, self.ids.night_button]
        # toggle the selected button's color between blue and grey
        if instance.md_bg_color == [0, 0, 1, 1]:
            instance.md_bg_color = [0.35, 0.35, 0.35, 1]
        else:
            for button in buttons:
                button.md_bg_color = [0.35, 0.35, 0.35, 1]
            instance.md_bg_color = [0, 0, 1, 1]
            self.TIME = instance.text 

    # on save used on date picker function
    def on_save_date(self, instance, value, date_range):
        self.DATE = value.strftime("%d/%m/%Y")
        snackbar = Snackbar(
                            text=f"Data alterada para {self.DATE}.", 
                            duration=4.0,
                            bg_color=(0, 0.5, 0, 1), # green
                            font_size="16sp"
                        )
        snackbar.open()
        print(self.DATE)
        
    # opens the date picker widget
    def show_date_picker(self):
        #self.click_sound()
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    # handles the age selection buttons
    def age_selection(self, instance):
        buttons = [self.ids.twelve_yo_button, self.ids.thirteen_til_seventeen_yo_button,
                self.ids.eighteen_til_fiftynine_yo_button, self.ids.sixty_yo_button]
        # toggle the selected button's color between blue and grey
        if instance.md_bg_color == [0, 0, 1, 1]:
            instance.md_bg_color = [0.35, 0.35, 0.35, 1]
        else:
            for button in buttons:
                button.md_bg_color = [0.35, 0.35, 0.35, 1]
            instance.md_bg_color = [0, 0, 1, 1]

    # handles the public selection buttons
    def public_selection(self, instance):
        buttons = [self.ids.cei_button, self.ids.emei_button, self.ids.emef_button,
                   self.ids.etec_button, self.ids.community_button, self.ids.employee_button]
        # toggle the selected button's color between blue and grey
        if instance.md_bg_color == [0, 0, 1, 1]:
            instance.md_bg_color = [0.35, 0.35, 0.35, 1]
        else:
            for button in buttons:
                button.md_bg_color = [0.35, 0.35, 0.35, 1]
            instance.md_bg_color = [0, 0, 1, 1]

    # save data method
    def save_data(self, instance=None, *args):
        # checks for the data where the file will be saved
        wb_path = 'assets/data.xlsx'
        # if the file isn't there, creates the file and sets up the sheet headers
        if not os.path.exists(wb_path):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Data"
            ws['A1'] = "Data"
            ws['B1'] = "Hora"
            ws['C1'] = "Faixa Etária"
            ws['D1'] = "Tipo de Público"
            wb.save(wb_path)
        else:
            wb = openpyxl.load_workbook(wb_path)
            ws = wb.active

        button_sets = [self.ids.public_age_row, self.ids.public_type_row]
        selected_options = []
        for button_set in button_sets:
            for button_id in button_set.children:
                if button_id.md_bg_color == [0, 0, 1, 1]:
                    selected_options.append(button_id.text)
                    print(selected_options)
        
            # checks if the TIME variable was set up manually
            if self.TIME == "Manhã":
                pass
            elif self.TIME == "Tarde":
                pass
            elif self.TIME == "Noite":
                pass
            # if the TIME variable was not set manually, gets the current time
            else:
                self.TIME = datetime.datetime.now().strftime("%H:%M:%S")

        # sets up the row order in the excel file
        row = [None] * 5
        row[0] = self.DATE
        row[1] = self.TIME
        for i in range(min(2, len(selected_options))):
            if i == 0:
                row[2] = selected_options[i]
            elif i == 1:
                row[3] = selected_options[i]

        ws.append(row)
        wb.save(wb_path)

        # sets up variables that stores the data saved for printing
        date_saved = "Informações salvas: Data: " + str(self.DATE)
        time_saved = ", Horário: " + str(self.TIME)
        if selected_options and len(selected_options) >= 2:
            age_saved = ", Faixa Etária: " + str(selected_options[0])
            public_saved = " e Público: " + str(selected_options[1])
            print(date_saved + time_saved + age_saved + public_saved)
        else:
            print("Selecione a faixa etária e o público.")

        # snackbar that shows the saved data count
        if self.snackbar is None:
            self.counter = 1
            text = f"Dados salvos x{self.counter}"
            self.snackbar = Snackbar(
                            text=text, 
                            bg_color=(0, 0.5, 0, 1), # green
                            font_size="16sp"
                        )
            self.snackbar.open()
            Clock.schedule_once(self.dismiss_snackbar, 3)
        else:
            self.counter += 1
            text = f"Dados salvos x{self.counter}"
            self.snackbar.text = text
            remaining_time = self.snackbar.duration - self.last_button_press_time + Clock.get_time()
            if remaining_time < 3:
                self.snackbar.duration += 3
            else:
                self.snackbar.duration = remaining_time + 3
            Clock.unschedule(self.dismiss_snackbar)
            Clock.schedule_once(self.dismiss_snackbar, self.snackbar.duration - remaining_time)

        self.last_button_press_time = Clock.get_time()

    # deals with the dismissal of the saved data's snackbar
    def dismiss_snackbar(self, dt):
        self.snackbar.dismiss()
        self.snackbar = None
        self.counter = 0

# app class
class MyApp(MDApp):
 
    def build(self):
        # sets the app window title
        self.title = 'Controle Diário de Circulação - Versão 0.2'
        #exibts the layout above in the user screen
        return MainScreen()      

# runs the program
if __name__ == '__main__':
    MyApp().run()
