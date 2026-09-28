import os
import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.storage.jsonstore import JsonStore

DATA_FILE = 'asistencia.json'
CSV_FILE = 'asistencia.csv'

class AsistenciaApp(App):
    def build(self):
        self.store = JsonStore(DATA_FILE)
        self.empleados = self.store.get('empleados')['lista'] if self.store.exists('empleados') else []
        self.registros = self.store.get('registros')['data'] if self.store.exists('registros') else []
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        root.add_widget(Label(text='SISTEMA DE ASISTENCIA', font_size=24, bold=True, size_hint_y=0.1))
        
        # Selector empleado
        sel_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        sel_layout.add_widget(Label(text='Empleado:', size_hint_x=0.3))
        self.spinner = Spinner(text='Seleccionar...', values=self.empleados, size_hint_x=0.7)
        sel_layout.add_widget(self.spinner)
        root.add_widget(sel_layout)
        
        # Botones entrada/salida
        btn_layout = BoxLayout(spacing=10, size_hint_y=0.2)
        self.btn_entrada = Button(text='ENTRADA', background_color=(0.2, 0.7, 0.2, 1), font_size=20)
        self.btn_salida = Button(text='SALIDA', background_color=(0.8, 0.3, 0.3, 1), font_size=20)
        self.btn_entrada.bind(on_press=lambda x: self.registrar('ENTRADA'))
        self.btn_salida.bind(on_press=lambda x: self.registrar('SALIDA'))
        btn_layout.add_widget(self.btn_entrada)
        btn_layout.add_widget(self.btn_salida)
        root.add_widget(btn_layout)
        
        # Gestión empleados
        emp_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        self.nuevo_emp = TextInput(hint_text='Nuevo empleado', multiline=False)
        btn_add = Button(text='Agregar', size_hint_x=0.3)
        btn_add.bind(on_press=self.agregar_empleado)
        emp_layout.add_widget(self.nuevo_emp)
        emp_layout.add_widget(btn_add)
        root.add_widget(emp_layout)
        
        # Lista registros
        root.add_widget(Label(text='REGISTROS DE HOY:', font_size=16, bold=True, size_hint_y=0.05))
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        root.add_widget(self.scroll)
        
        # Botones exportar/limpiar
        foot_layout = BoxLayout(spacing=10, size_hint_y=0.1)
        btn_exp = Button(text='Exportar CSV', background_color=(0.3, 0.5, 0.9, 1))
        btn_exp.bind(on_press=self.exportar_csv)
        btn_clr = Button(text='Limpiar hoy', background_color=(0.9, 0.5, 0.3, 1))
        btn_clr.bind(on_press=self.limpiar_hoy)
        foot_layout.add_widget(btn_exp)
        foot_layout.add_widget(btn_clr)
        root.add_widget(foot_layout)
        
        self.actualizar_lista()
        return root

    def agregar_empleado(self, instance):
        nombre = self.nuevo_emp.text.strip()
        if nombre and nombre not in self.empleados:
            self.empleados.append(nombre)
            self.store.put('empleados', lista=self.empleados)
            self.spinner.values = self.empleados
            self.nuevo_emp.text = ''
            self.mostrar_popup('Éxito', f'Empleado "{nombre}" agregado')

    def registrar(self, tipo):
        emp = self.spinner.text
        if emp == 'Seleccionar...':
            self.mostrar_popup('Error', 'Seleccione un empleado')
            return
        ahora = datetime.now()
        fecha = ahora.strftime('%Y-%m-%d')
        hora = ahora.strftime('%H:%M:%S')
        self.registros.append({'empleado': emp, 'fecha': fecha, 'hora': hora, 'tipo': tipo})
        self.store.put('registros', data=self.registros)
        self.actualizar_lista()
        self.mostrar_popup('Registrado', f'{emp} - {tipo} a las {hora}')

    def actualizar_lista(self):
        self.grid.clear_widgets()
        hoy = datetime.now().strftime('%Y-%m-%d')
        for r in reversed(self.registros):
            if r['fecha'] == hoy:
                color = (0.2, 0.8, 0.2, 1) if r['tipo'] == 'ENTRADA' else (0.9, 0.3, 0.3, 1)
                btn = Button(
                    text=f"{r['empleado']} | {r['hora']} | {r['tipo']}",
                    size_hint_y=None, height=40,
                    background_color=color
                )
                self.grid.add_widget(btn)

    def exportar_csv(self, instance):
        try:
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['empleado', 'fecha', 'hora', 'tipo'])
                writer.writeheader()
                writer.writerows(self.registros)
            self.mostrar_popup('Exportado', f'Guardado en {CSV_FILE}')
        except Exception as e:
            self.mostrar_popup('Error', str(e))

    def limpiar_hoy(self, instance):
        hoy = datetime.now().strftime('%Y-%m-%d')
        self.registros = [r for r in self.registros if r['fecha'] != hoy]
        self.store.put('registros', data=self.registros)
        self.actualizar_lista()
        self.mostrar_popup('Limpio', 'Registros de hoy eliminados')

    def mostrar_popup(self, titulo, mensaje):
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.4)).open()

if __name__ == '__main__':
    AsistenciaApp().run()