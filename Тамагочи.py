import tkinter as tk
from tkinter import ttk
import time


class Tamagochi:


    def __init__(self, name):
        self.name = name
        self.hunger_behav = 50
        self.thirst_behav = 50
        self.energy_behav = 50
        self.happiness_behav = 50
        self.life = True



    def feed(self):
        if not self.life:
            print("Питомец мёртв")
            return
        self.hunger_behav = min(100, self.hunger_behav + 15)



    def give_water(self):
        if not self.life:
            print("Питомец мёртв")
            return
        self.thirst_behav = min(100, self.thirst_behav + 15)



    def play(self):
        if not self.life:
            print("Питомец мёртв")
            return
        self.happiness_behav = min(100, self.happiness_behav + 20)
        self.hunger_behav = max(0, self.hunger_behav - 10)
        self.energy_behav = max(0, self.energy_behav - 15)



    def sleep(self):
        if not self.life:
            print("Питомец мёртв")
            return
        self.energy_behav = min(100, self.energy_behav + 30)
        self.hunger_behav = max(0, self.hunger_behav - 15)
        self.thirst_behav = max(0, self.thirst_behav - 15)
        print("Сон окончен")



    def update_behav(self):
        if not self.life:
            print("Питомец мёртв")
            return
        self.hunger_behav = max(0, self.hunger_behav - 5)
        self.thirst_behav = max(0, self.thirst_behav - 5)
        self.energy_behav = max(0, self.energy_behav - 5)
        self.happiness_behav = max(0, self.happiness_behav - 5)


class TamagochiVIS:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamagotchi VIS")
        self.root.geometry("300x500")
        self.pet = Tamagochi("Pet")
        self.emoj = tk.Label(root, text="UwU", font=("Comic Sans MS", 48))
        self.emoj.pack(pady=8)
        self.status_lbl = tk.Label(root, text="Статус: OK", font=("Comic Sans MS", 14, "bold"))
        self.status_lbl.pack()
        self.Bars()
        #EasterEgg_№1;)
        self.Buttons()
        self.Reset()
        self.root.after(1000, self.game_tick)

    def Bars(self):
        self.bars = {}
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        self._create_bar(frame, "Сытость", "hunger_behav")
        self._create_bar(frame, "Жажда", "thirst_behav")
        self._create_bar(frame, "Энергия", "energy_behav")
        self._create_bar(frame, "Счастье", "happiness_behav")

    def Buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.feed_btn = tk.Button(btn_frame, text="Покормить", width=12,
                                  command=lambda: self.start(self.pet.feed))
        self.feed_btn.grid(row=0, column=0, padx=6, pady=6)
        self.water_btn = tk.Button(btn_frame, text="Напоить", width=12,
                                   command=lambda: self.start(self.pet.give_water))
        self.water_btn.grid(row=0, column=1, padx=6, pady=6)
        self.play_btn = tk.Button(btn_frame, text="Поиграть", width=12,
                                  command=lambda: self.start(self.pet.play))
        self.play_btn.grid(row=1, column=1, padx=6, pady=6)
        self.sleep_btn = tk.Button(btn_frame, text="Спать", width=12,
                                   command=lambda: self.start(self.pet.sleep))
        self.sleep_btn.grid(row=1, column=0, padx=6, pady=6)



    def Reset(self):
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=8)
        #EasterEgg_№2;)
        tk.Button(ctrl_frame, text="Сброс", command=self.reset_pet).pack(side="left", padx=6)



    def _create_bar(self, parent, label_text, attr_name):
        tk.Label(parent, text=label_text, anchor="w").pack(fill="x", padx=12)
        bar = ttk.Progressbar(parent, orient="horizontal", length=320, 
                             mode="determinate", maximum=100)
        bar.pack(padx=12, pady=(0, 8))
        self.bars[attr_name] = bar



    def start(self, func):
        if not self.pet.life:
            print("Питомец мёртв")
            return
        func()
        self.refresh()



    def refresh(self):
        try:
            self.bars['hunger_behav']['value'] = self.pet.hunger_behav
            self.bars['thirst_behav']['value'] = self.pet.thirst_behav
            self.bars['energy_behav']['value'] = self.pet.energy_behav
            self.bars['happiness_behav']['value'] = self.pet.happiness_behav
        except Exception as e:
            print("Error updating bars:", e)
        try:
            avg = (self.pet.hunger_behav + self.pet.thirst_behav + 
                   self.pet.energy_behav + self.pet.happiness_behav) / 4
        except Exception:
            avg = 0
        if avg > 80:
            status_text = "Отлично!"
            emoj = ":)"
        elif avg > 60:
            status_text = "Нормально"
            emoj = ":)"
        elif avg > 40:
            status_text = "Плохо"
            emoj = ":("
        else:
            status_text = "Критично!"
            emoj = ":("
        try:
            self.status_lbl.config(text=f"Статус: {status_text}")
        except Exception:
            pass
        try:
            self.emoj.config(text=emoj)
        except Exception:
            pass



    def reset_pet(self):
        self.pet.hunger_behav = 50
        self.pet.thirst_behav = 50
        self.pet.energy_behav = 50
        self.pet.happiness_behav = 50
        self.pet.life = True
        self.refresh()



    def game_tick(self):
        self.pet.update_behav()
        self.refresh()
        self.root.after(1000, self.game_tick)



if __name__ == "__main__":
    root = tk.Tk()
    #EasterEgg_№3;)
    app = TamagochiVIS(root)
    root.mainloop()
