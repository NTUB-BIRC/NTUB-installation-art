import threading
import tkinter


class ShowResultGUI(threading.Thread):
    def run(self):
        self.window = tkinter.Tk()
        self.window.title('NTUB vote')
        self.lable = tkinter.Label(self.window,
                                   text='Hello~',
                                   width=30,
                                   height=15,
                                   font=('Helvetica', 80))
        self.lable.pack()
        self.window.protocol('WM_DELETE_WINDOW', self.close)
        self.window.mainloop()

    def change_text(self, text):
        self.lable['text'] = text
        background_color = False

    def close(self):
        self.window.quit()
