from tkinter import *
from random import randint, shuffle
from math import sqrt
from time import time


class Trials:
    def __init__(self):
        self.trial_data = dict()
        self.current_trial = 0
        self.sizes = [10, 20, 40]
        self.distances = [100, 300]
        self.trials = self.generateTrials()
        self.mouse_lastx = 0
        self.mouse_lasty = 0

    def generateTrials(self):
        trials = list()
        for i in range(0, 1):
            block = list()
            for side in [-1, 1]:
                for size in self.sizes:
                    for distance in self.distances:
                        block.append((side * distance, size))
            shuffle(block)  # randomize the order of trials
            trials = trials + block
        return trials

    def new_trial(self):
        self.trial_data[self.current_trial] = dict()
        self.trial_data[self.current_trial]["errors"] = 0
        self.trial_data[self.current_trial]["distance"] = 0
        self.trial_data[self.current_trial]["start_time"] = time()
        self.trial_data[self.current_trial]["end_time"] = 0

        self.current_trial += 1

        return self.trials[self.current_trial - 1]

    def misclick(self):
        if self.current_trial > 0:
            self.trial_data[self.current_trial - 1]["errors"] = (self.trial_data[self.current_trial - 1]["errors"]) + 1

    def setEndTime(self, end_time):
        if self.current_trial > 0:
            self.trial_data[self.current_trial - 1]["end_time"] = end_time

    def updateMouseLast(self, mouse_x, mouse_y):
        self.mouse_lastx = mouse_x
        self.mouse_lasty = mouse_y

    def trackMouseDistance(self, mouse_x, mouse_y):
        dist = self.distance([self.mouse_lastx, self.mouse_lasty], [mouse_x, mouse_y])
        self.trial_data[self.current_trial - 1]["distance"] = self.trial_data[self.current_trial - 1]["distance"] + dist
        self.updateMouseLast(mouse_x, mouse_y)

    @staticmethod
    def distance(p0, p1):
        return sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)


class MainCanvas:
    border_enter_color = "red"
    border_leave_color = "white"

    def __init__(self, root, canvas, color, width, height):
        self.app_root = root
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, width, height, fill=MainCanvas.border_leave_color, tags="background")
        self.canvas.bind('<Motion>', self.mouseMotion)
        self.width = width
        self.height = height

        self.text_id = self.canvas.create_text(width / 2 + 10, 20, anchor='se')
        self.canvas.itemconfig(self.text_id, text='', fill="blue")

        self.canvas.tag_bind("background", '<ButtonPress-1>', self.onBackgroundClick)
        self.canvas.tag_bind("circle", '<ButtonPress-1>', self.onCircleClick)

        self.canvas_item_to_object = dict()  # maps canvas object ids to the object they're linked to
        self.trial_tracker = Trials()  # create tracker to manage input data

        self.center_box = canvas.create_rectangle(width / 2 - 10, height / 2 - 10, width / 2 + 10, height / 2 + 10,
                                                  fill="orange", tags="center_box")
        self.canvas.tag_bind("center_box", '<ButtonPress-1>', self.centerBoxClick)

        self.task_was_reset = False  # flag to force people to click the center button to reset the task

    def centerBoxClick(self, event):
        # user clicked center box to get new task
        mouse_x, mouse_y = event.x, event.y
        if not self.task_was_reset:
            self.trial_tracker.setEndTime(time())

            if self.trial_tracker.current_trial < len(self.trial_tracker.trials):
                self.task_was_reset = True
                self.trial_tracker.updateMouseLast(mouse_x, mouse_y)
                self.createTrialCircle()  # make new trial circle
            else:
                print("trial data", self.trial_tracker.trial_data)
                self.app_root.changePage(ThanksPage)  # experiment ended; switch to the thank you page

    def mouseMotion(self, event):
        mouse_x, mouse_y = event.x, event.y
        if self.task_was_reset:
            self.trial_tracker.trackMouseDistance(mouse_x, mouse_y)

    def onBackgroundClick(self, event):
        # user missed the button
        x, y = event.x, event.y
        self.trial_tracker.misclick()

    def onCircleClick(self, event):
        x, y = event.x, event.y
        # print('you clicked at {}, {}'.format(x, y))

        # get the item that was clicked and remove it
        if self.canvas.find_withtag(CURRENT):
            # print(self.canvas_item_to_object[self.canvas.find_withtag(CURRENT)[0]]) # get the actual circle linked to the canvas
            self.removeCircle(self.canvas.find_withtag(CURRENT)[0])
            self.task_was_reset = False
            self.updateProgressBar()

    def updateProgressBar(self):
        self.canvas.itemconfig(self.text_id,
                               text=str(self.trial_tracker.current_trial) + '/ ' + str(len(self.trial_tracker.trials)),
                               fill="blue")

    def createTrialCircle(self):
        # grab the trial data, then make a new circle
        trial = self.trial_tracker.new_trial()  # get the first trial
        circle_radius = trial[1]
        circle_x = trial[0] + (self.width / 2)
        circle_y = self.height / 2
        self.createCircle(circle_x, circle_y, circle_radius, "green")

    def createCircle(self, x, y, radius, color):
        canvas_circle = self.canvas.create_oval(0, 0, radius * 2, radius * 2, fill=color, tags="circle")
        circle = Circle(self, self.canvas, canvas_circle)
        self.canvas.move(canvas_circle, x - radius, y - radius)  # starts at 0,0 so move it to new position
        self.canvas_item_to_object[canvas_circle] = circle

    def removeCircle(self, canvas_object):
        self.canvas.delete(canvas_object)
        self.canvas_item_to_object.pop(canvas_object)


class Circle:
    def __init__(self, parent, canvas, circle_id):
        self.parent = parent
        self.canvas = canvas
        self.circle_id = circle_id


class App(Tk):
    # manages pages and data across the app
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.configureApp()
        self.changePage(ConsentPage)

    def configureApp(self):
        self.attributes("-fullscreen", False)  # starts in windowed
        self.resizable(width=False, height=False)  # cannot resize window
        self.maxsize(1000, 800)
        self.title("Clicking Experiment")

    def changePage(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()


class ConsentPage(Frame):
    def __init__(self, master=None):
        f = Frame.__init__(self, master)

        text = Label(self, text="This is a test consent form\n"
                                "some legal things here\n "
                                "we're not liable for death or maimings")
        text.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        consent_button = Button(self, text="I consent to this experiment",
                                command=lambda: master.changePage(InstructionPage))

        consent_button.grid(row=1, column=0)
        self.rowconfigure(1, minsize=100, weight=6)


class InstructionPage(Frame):
    def __init__(self, master=None):
        f = Frame.__init__(self, master)

        text = Label(self, text="Instructions\n\n\n"
                                "Click the orange square in the center to begin a task\n "
                                "Then click the circle that pops up as quickly as possible\n"
                                "Repeat as many times as directed"
                     )
        text.config(font=("Courier", 20))
        text.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        begin_button = Button(self, text="Begin trials",
                              command=lambda: master.changePage(ApplicationPage))

        begin_button.grid(row=1, column=0)
        self.rowconfigure(1, minsize=100, weight=6)


class ApplicationPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.elements = dict()  # create a dictionary that houses all the objects, so you can reference them in other methods

        # configure all the rows and columns to have default weights
        for r in range(1):  # height in rows
            self.rowconfigure(r, weight=1)
        for c in range(1):  # width in columns
            self.columnconfigure(c, weight=1)

        ########### main canvas for graph rendering
        # make a frame to house the main canvas. The frame adheres to the grid scheme but the canvas is packed
        self.elements["main_canvas_background"] = Frame(self, bg="grey")
        self.elements["main_canvas_background"].grid(row=0, column=0, rowspan=1, columnspan=1, sticky=N + W + S + E)
        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=100, weight=6)

        # main canvas
        self.elements["main_canvas"] = Canvas(self.elements["main_canvas_background"], width=1000, height=700, bd=0,
                                              highlightthickness=0)
        self.elements["main_canvas"].pack()

        # add a background renderer and a ball to the canvas
        border = MainCanvas(master, self.elements["main_canvas"], "white", 1000, 700)


class ThanksPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        text = Label(master, text="Thank you for participating in this study")
        text.config(font=("Courier", 20))
        text.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        consent_button = Button(self, text="close", command=quit)

        consent_button.grid(row=1, column=0)
        self.rowconfigure(1, minsize=100, weight=6)


if __name__ == "__main__":
    app = App()
    app.mainloop()
