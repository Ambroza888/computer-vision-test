import threading


class Toggle:
    patient_left = True
    patient_off_bed = True

    def toggle_switcher(self):
        self.patient_left = True

    def let_switch(self):
        timer = threading.Timer(5.0, self.toggle_switcher)
        timer.start()
