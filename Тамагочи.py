import tkinter as tk
import threading
import time
from tkinter import messagebox


TICK_MS = 5000


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
        time.sleep(2)
        self.hunger_behav = min(100, self.hunger_behav + 15)
        self.thirst_behav = max(0, self.thirst_behav - 5)



    def give_water(self):
        if not self.life:
            print("Питомец мёртв")
            return
        time.sleep(2)
        self.thirst_behav = min(100, self.thirst_behav + 15)



    def play(self):
        if not self.life:
            print("Питомец мёртв")
            return
        time.sleep(2)
        self.happiness_behav = min(100, self.happiness_behav + 20)
        self.hunger_behav = max(0, self.hunger_behav - 10)
        self.energy_behav = max(0, self.energy_behav - 15)
        self.thirst_behav = max(0, self.thirst_behav - 5)



    def sleep(self):
        if not self.life:
            print("Питомец мёртв")
            return
        time.sleep(2)
        self.energy_behav = min(100, self.energy_behav + 30)
        self.hunger_behav = max(0, self.hunger_behav - 15)
        self.thirst_behav = max(0, self.thirst_behav - 15)
        self.happiness_behav = max(0, self.happiness_behav - 5)



    def update_behav(self):
        if not self.life:
            print("Питомец мёртв")
            return
        self.hunger_behav = max(0, self.hunger_behav - 5)
        self.thirst_behav = max(0, self.thirst_behav - 5)
        self.energy_behav = max(0, self.energy_behav - 5)
        self.happiness_behav = max(0, self.happiness_behav - 5)
        if (self.hunger_behav <= 0 or self.thirst_behav <= 0 or 
            self.energy_behav <= 0 or self.happiness_behav <= 0):
            self.life = False



    def pet_status(self):
        if not self.life:
            print("Питомец мёртв")
            return
        stat = (self.hunger_behav + self.thirst_behav + self.energy_behav + self.happiness_behav) / 4
        if stat > 80:
            return "Отлично!"
        if stat > 60:
            return "Нормально"
        if stat > 40:
            return "Плохо"
        if stat > 20:
            return "Критично!"
        return "Очень плохо"



class TamagochiVIS:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamagotchi VIS")
        self.root.geometry("380x480")
        self.pet = Tamagochi("Pet")
        self.action_lock = threading.Lock()
        self.action_thread = None
        self.running = True
        #EasterEgg_№1;)
        self.emoj = tk.Label(root, text="(UwU)", font=("Comic Sans MS", 48))
        self.emoj.pack(pady=8)
        self.status_lbl = tk.Label(root, text="Статус: OK", font=("Comic Sans MS", 14, "bold"))
        self.status_lbl.pack()
        self.create_bars()
        self.create_buttons()
        self.create_controls()
        self.root.after(TICK_MS, self.game_tick)
        self.refresh()



    def create_bars(self):
        self.bars = {}
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        self._create_bar(frame, "Сытость", "hunger_behav")
        self._create_bar(frame, "Жажда", "thirst_behav")
        self._create_bar(frame, "Энергия", "energy_behav")
        self._create_bar(frame, "Счастье", "happiness_behav")



    def _create_bar(self, parent, label_text, attr_name):
        tk.Label(parent, text=label_text, anchor="w").pack(fill="x", padx=12)
        bar = tk.Progressbar(parent, orient="horizontal", length=320, mode="determinate", maximum=100)
        bar.pack(padx=12, pady=(0, 8))
        self.bars[attr_name] = bar



    def create_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.feed_btn = tk.Button(btn_frame, text="Покормить", width=12,
                                  command=lambda: self.start_action(self.pet.feed))
        self.feed_btn.grid(row=0, column=0, padx=6, pady=6)
        self.water_btn = tk.Button(btn_frame, text="Напоить", width=12,
                                   command=lambda: self.start_action(self.pet.give_water))
        self.water_btn.grid(row=0, column=1, padx=6, pady=6)
        #EasterEgg_№2;)
        self.play_btn = tk.Button(btn_frame, text="Поиграть", width=12,
                                  command=lambda: self.start_action(self.pet.play))
        self.play_btn.grid(row=1, column=0, padx=6, pady=6)
        self.sleep_btn = tk.Button(btn_frame, text="Спать", width=12,
                                   command=lambda: self.start_action(self.pet.sleep))
        self.sleep_btn.grid(row=1, column=1, padx=6, pady=6)



    def create_controls(self):
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=8)
        tk.Button(ctrl_frame, text="Сброс", command=self.reset_pet).pack(side="left", padx=6)



    def start_action(self, func):
        if not self.pet.life:
            messagebox.showinfo("Info", "Питомец мёртв")
            return
        if self.action_thread and self.action_thread.is_alive():
            return
        self.action_thread = threading.Thread(target=self._execute_action, args=(func,), daemon=True)
        self.action_thread.start()



    def _execute_action(self, func):
        with self.action_lock:
            func()
            self.root.after(0, self.refresh)



    def refresh(self):
        self.bars['hunger_behav']['value'] = self.pet.hunger_behav
        self.bars['thirst_behav']['value'] = self.pet.thirst_behav
        self.bars['energy_behav']['value'] = self.pet.energy_behav
        self.bars['happiness_behav']['value'] = self.pet.happiness_behav



        if not self.pet.life:
            status_text = "СМЕРТЬ"
            emoj = "💀"
        else:
            avg = (self.pet.hunger_behav + self.pet.thirst_behav + 
                  self.pet.energy_behav + self.pet.happiness_behav) / 4
            if avg > 80:
                status_text = "Отлично!"
                emoj = "(UwU)"
            elif avg > 60:
                status_text = "Нормально"
                emoj = "(UwU)"
            elif avg > 40:
                status_text = "Плохо"
                emoj = "(>_<)"
            elif avg > 20:
                status_text = "Критично!"
                emoj = "(x_x)"
            else:
                status_text = "Очень плохо"
                emoj = "(x_x)"
        self.status_lbl.config(text=f"Статус: {status_text}")
        self.emoj.config(text=emoj)
        #EasterEgg_№3;)
        state = "normal" if self.pet.life else "disabled"
        self.feed_btn.config(state=state)
        self.water_btn.config(state=state)
        self.play_btn.config(state=state)
        self.sleep_btn.config(state=state)



    def game_tick(self):
        if self.pet.life:
            self.pet.update_behav()
            self.refresh()
        if self.running:
            self.root.after(TICK_MS, self.game_tick)



    def reset_pet(self):
        self.pet.hunger_behav = 50
        self.pet.thirst_behav = 50
        self.pet.energy_behav = 50
        self.pet.happiness_behav = 50
        self.pet.life = True
        self.refresh()



if __name__ == "__main__":
    root = tk.Tk()
    app = TamagochiVIS(root)
    root.mainloop()