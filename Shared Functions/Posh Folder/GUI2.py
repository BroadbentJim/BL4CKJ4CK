import tkinter as tk   # python3
import datetime
import os
import numpy as np
from montecarlo import game as monte
from BasicStrategy import game as basic
from SimpleStrategy import game as simple

TITLE_FONT = ("Helvetica", 18, "bold")
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "BL4CKJ4CK")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.shared_data = {
            "strategy": tk.StringVar(),
            "results": {}
        }

        self.frames = {}
        for F in (StartPage, Main_Page, About_Page, Input_Page, GraphPage, Results):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    # def update_dictionary(self, button, arg):
    #     self.shared_data[button] = arg
    #
    # def get_page(self, page_class):
    #     return self.frames[page_class]


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text=("""BL4CKJ4CK Simulator"""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="About", command=lambda: controller.show_frame("About_Page"))
        button.pack()

        maintext = tk.Label(self, text=("""This program follows typical casino blackjack rules.
        This means no splitting on non-alike face cards,
        a soft 17 rule and inability to double after splitting.
        The house pays 3:2 on blackjack as per most casinos.
        The program tries to follow casino rules as strictly as
        possible in order to produce results that are comparable
        to the casino."""), font=NORM_FONT)
        maintext.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Continue",
                             command=lambda: controller.show_frame("Main_Page"))
        button1.pack()

        button2 = tk.Button(self, text="Quit",
                             command=quit)
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class Input_Page(tk.Frame):



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="This is the input page", font=TITLE_FONT)
        title.pack(side="top", fill="x", pady=10)
        options = ['Basic', 'Perfect', 'Simple', 'Monte Carlo']
        self.strategy = self.controller.shared_data["strategy"]
        self.strategy.set(str(options[0]))
        self.optionmenu = tk.OptionMenu(self, self.strategy, 'Basic', 'Perfect', 'Simple', 'Monte Carlo')
        self.optionmenu.pack()

        button = tk.Button(self, text="OK", command=self.Toggle)
        button.pack()

        self.hitto = tk.IntVar()
        self.basicbutton = tk.Entry(self, textvariable=self.hitto)
        self.basicbutton.config(state = tk.DISABLED)
        self.basicbutton.pack(pady=0)

        # if self.strategy.get() == "Basic":
        #     basicbutton.config(state=tk.NORMAL)


        simslabel = tk.Label(self, text="Number of times to simulate:")
        simslabel.pack()
        self.numberofsims = tk.IntVar()
        self.numberofsims.set(100)
        self.entrylist = tk.Entry(self, textvariable=self.numberofsims)
        self.entrylist.pack()


        startbutton = tk.Button(self, text="Start simulation", command=self.games)
        startbutton.pack()

    # def startsimulation(self):
    #     if self.strategy.get() == 'Basic':
    #         basic(self.numberofsims.get())
    #     elif self.strategy.get() == 'Simple':
    #         simple(self.numberofsims.get(), self.hitto.get())
    #     elif self.strategy.get() == 'Perfect':
    #         perfect(self.numberofsims.get())
    #     elif self.strategy.get() == 'Monte':
    #         monte(self.numberofsims.get())

    def games(self):
        strategy = self.strategy.get()
        numberofsims = self.numberofsims.get()
        wanted = self.hitto.get()
        if strategy == "Simple":
            results = simple(numberofsims, wanted)  # Dictionary
        elif strategy == "Basic":
            results = basic(numberofsims)
        elif strategy == "Perfect":
            pass
            #results = perfect(numberofsims)
        elif strategy == "Monte Carlo":
            results, HRM = monte(numberofsims)
            return results, HRM
        self.controller.show_frame("Results")
        print(results["winrate"])
        self.controller.shared_data["results"] = results



    def Toggle(self):
        #print("1>2")
        if self.strategy.get() == "Simple":
            print(self.strategy.get())
            self.basicbutton.config(state=tk.NORMAL)
            self.basicbutton.insert(0, "")
            self.basicbutton.pack()
        else:
            self.basicbutton.config(state=tk.DISABLED)
            self.basicbutton.pack()

class Main_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        button1 = tk.Button(self, text="Go to the input page",
                           command=lambda: controller.show_frame("Input_Page"))
        button1.pack()



class About_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        maintext = tk.Label(self, text="""This program serves to simulate casino blackjack played with one player and one dealer. This simulation allows for a variety of strategies to provide useful results. This includes:
	• Simple Strategy (The player simply hits until a given amount),
	• Basic Strategy (The player carefully follows a generic preprepared ruleset for every scenario),
	• Perfect Strategy(The player follows the Basic Strategy ruleset but with the accompaniment of perfect card counting and variable wagering to take advantage of this fact)
	• Machine Learning(The program plays randomly in each scenario at first but records its results and begins to adapt what it is the best play for each scenario).

It allows for a variety of simulation arguments and when the simulation is finished, the results are shown as raw data and as well as informative graphs.
This program can take advantage of multiple computers for the simulation if able and configured correctly.""")
        maintext.pack()

        button1 = tk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame("StartPage"))
        button1.pack()

class Results(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the results Page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        self.saving = tk.BooleanVar()
        tosaveornottosave = tk.Checkbutton(self, text="Save results to file", variable=self.saving, command=self.toggle)
        tosaveornottosave.pack()

        self.confirm = tk.Button(self, text="Are you sure?", command=self.saveresults, state=tk.DISABLED)
        self.confirm.pack()

        graphs = tk.Button(self, text="Go to the graphs page", command=lambda: controller.show_frame("GraphPage"))
        graphs.pack()

    def toggle(self):
        var = self.saving.get()
        if var == True:
            self.confirm.config(state=tk.NORMAL)
        else:
            self.confirm.config(state=tk.DISABLED)



    def saveresults(self):

        dictionary = self.controller.shared_data["results"]

        formatted_time = datetime.datetime.now().strftime("%Y-%m-%d; %H-%M-%S")
        os.mkdir(formatted_time)
        # strats_filepath = open(os.path.join(formatted_time, "strategy.txt"))
        np.save(os.path.join(formatted_time, "dictionary.npy"), dictionary)


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.strategy = self.controller.shared_data["strategy"]

        label = tk.Label(self, text="This is the graph page", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        GraphTypes = ['Normal Distrubition', 'Net gain over time']
        graph = tk.StringVar()
        graph.set(GraphTypes[0])

        dropdown = tk.OptionMenu(self, graph, *GraphTypes)
        dropdown.pack()

        if self.strategy == "Monte Carlo":

            self.HRMVar = tk.BooleanVar()
            self.HRMVar.set(False)
            HRMtoggle = tk.Checkbutton(self, text="Show the AI Strategy colourmap", variable=self.HRMVar)
            HRMtoggle.pack()

        startbtn = tk.Button(self, text="Plot the graphs", command=self.start)
        startbtn.pack()

    def start(self):
        pass



if __name__ == "__main__":
    app = SampleApp()
    app.geometry("1280x720")
    app.mainloop()
