import threading
import tkinter


class ShowResultGUI(threading.Thread):
    def run(self):
        self.window = tkinter.Tk()  # create window
        self.window.title('ntub installtion art')
        # set lable info
        self.lable = tkinter.Label(self.window,
                                   text='Hello~',
                                   width=30,
                                   height=15,
                                   font=('Helvetica', 80))
        self.lable.pack()  # put lable in window
        # set close function
        self.window.protocol('WM_DELETE_WINDOW', self.close)
        # start window
        self.window.mainloop()

    def change_text(self, text):
        self.lable['text'] = text  # set lable text
        self.background_color = False

    def close(self):
        self.window.quit()
