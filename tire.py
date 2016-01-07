from tkinter import filedialog
from tkinter import *
from math import *

coeff_base = ['Fz','Camber']

coeff_fy = ['a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a111','a112','a12','a13']

coeff_fx = ['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','b10']

coeff_mz = ['c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17']

coeff_min = {
# Base parameters
'Fz':0.5,
'Camber':-8.0,
# Lateral force
'a0':1,
'a1':-100,
'a2':1,
'a3':1,
'a4':-100,
'a5':-10,
'a6':-10,
'a7':-10,
'a8':-10,
'a9':-10,
'a10':-10,
'a111':-10,
'a112':-10,
'a12':-100,
'a13':-10,
# Longitudinal force
'b0':1,
'b1':-300,
'b2':1,
'b3':-100,
'b4':-1000,
'b5':-10,
'b6':-10,
'b7':-10,
'b8':-10,
'b9':-10,
'b10':-10,
# Aligning moment
'c0':1,
'c1':-10,
'c2':-10,
'c3':-10,
'c4':-100,
'c5':-10,
'c6':-10,
'c7':-10,
'c8':-10,
'c9':-10,
'c10':-10,
'c11':-10,
'c12':-10,
'c13':-10,
'c14':-10,
'c15':-10,
'c16':-10,
'c17':-10,
}

coeff_max = {
# Base parameters
'Fz':5.5,
'Camber':8.0,
# Lateral force
'a0':3,
'a1':100,
'a2':2500,
'a3':5000,
'a4':100,
'a5':10,
'a6':10,
'a7':10,
'a8':10,
'a9':10,
'a10':10,
'a111':100,
'a112':10,
'a12':100,
'a13':10,
# Longitudinal force
'b0':3,
'b1':300,
'b2':2500,
'b3':100,
'b4':1000,
'b5':10,
'b6':10,
'b7':10,
'b8':10,
'b9':10,
'b10':10,
# Aligning moment
'c0':7,
'c1':10,
'c2':10,
'c3':10,
'c4':100,
'c5':10.0,
'c6':10.0,
'c7':10,
'c8':10,
'c9':10,
'c10':10,
'c11':10,
'c12':10,
'c13':10,
'c14':10,
'c15':10,
'c16':10,
'c17':10,
}

coeff_default = {
# Base parameters
'Fz':3.0,
'Camber':0.0,
# Lateral force
'a0':1.4,
'a1':-0,
'a2':1688,
'a3':2400,
'a4':6.026,
'a5':0,
'a6':-0.359,
'a7':1.0,
'a8':0,
'a9':-0.00611,
'a10':-0.0322,
'a111':0,
'a112':0,
'a12':0,
'a13':0,
# Longitudinal force
'b0':1.65,
'b1':0,
'b2':1690,
'b3':0,
'b4':229,
'b5':0,
'b6':0,
'b7':0,
'b8':-10,
'b9':0,
'b10':0,
# Aligning moment
'c0':2.3,
'c1':-3.8,
'c2':-3.14,
'c3':-1.16,
'c4':-7.2,
'c5':0.0,
'c6':0.0,
'c7':0.044,
'c8':-0.58,
'c9':0.18,
'c10':0.0,
'c11':0.0,
'c12':0.0,
'c13':0.0,
'c14':0.14,
'c15':-1.029,
'c16':0.0,
'c17':0.0,
}


# Longitudinal force 
def PacejkaFx(p, sigma, Fz):
    # shape factor
    C = p['b0']

    # peak factor
    D = (p['b1'] * Fz + p['b2']) * Fz

    # slope at origin
    BCD = (p['b3'] * Fz + p['b4']) * Fz * exp(-p['b5'] * Fz)

    # stiffness factor
    B =  BCD / (C * D)

    # curvature factor
    E = p['b6'] * Fz * Fz + p['b7'] * Fz + p['b8']

    # curvature factor 1993
    #E = E * (1 - p['b13'] * sgn(S))

    # horizontal shift
    Sh = p['b9'] * Fz + p['b10']

    # vertical shift 1993
    #Sv = p['b11'] * Fz + p['b12']

    # composite
    S = 100 * sigma + Sh

    # longitudinal force
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S))))


# Lateral force
def PacejkaFy(p, alpha, gamma, Fz):
    # shape factor
    C = p['a0']

    # peak factor
    D = (p['a1'] * Fz + p['a2']) * Fz

    # peak factor 1993
    # D = D * (1 - p['a14'] * gamma * gamma)

    # slope at origin
    BCD = p['a3'] * sin(2.0 * atan(Fz / p['a4'])) * (1.0 - p['a5'] * fabs(gamma))

    # stiffness factor
    B = BCD / (C * D)

    # curvature factor
    E = p['a6'] * Fz + p['a7']

    # curvature factor 1993
    # E = E * (1 - (p['a15'] * gamma + p['a16']) * sgn(alpha + Sh))

    # horizontal shift
    Sh = p['a8'] * gamma + p['a9'] * Fz + p['a10']

    # horizontal shift 1993
    # Sh = p['a8'] * Fz + p['a9'] + p['a10'] * gamma

    # vertical shift
    Sv = ((p['a111'] * Fz + p['a112']) * gamma + p['a12']) * Fz + p['a13']

    # vertical shift 1993
    # Sv = p['a111'] * Fz + p['a112'] + (p['a12'] * Fz * Fz + p['a13'] * Fz) * gamma

    # composite
    S = alpha + Sh

    # lateral force
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S)))) + Sv


# Aligning moment
def PacejkaMz(p, sigma, alpha, gamma, Fz):
    # shape factor
    C = p['c0']

    # peak factor
    D = (p['c1'] * Fz + p['c2']) * Fz

    # peak factor 1993
    # D = D * (1 - p['c18'] * gamma * gamma)

    # slope at origin
    BCD = (p['c3'] * Fz + p['c4']) * Fz * (1.0 - p['c6'] * fabs(gamma)) * exp (-p['c5'] * Fz)

    # stiffness factor
    B =  BCD / (C * D)

    # curvature factor
    E = (p['c7'] * Fz * Fz + p['c8'] * Fz + p['c9']) * (1.0 - p['c10'] * fabs(gamma))

    # curvature factor 1993
    # E = (p['c7'] * Fz * Fz + p['c8'] * Fz + p['c9']) * (1.0 - (p['c19'] * gamma + p['c20']) * sgn(S)) / (1.0 - p['c10'] * fabs(gamma))

    # horizontal shift
    Sh = p['c11'] * gamma + p['c12'] * Fz + p['c13']

    # horizontal shift 1993
    # Sh = p['c11'] * Fz + p['c12'] + p['c13'] * gamma

    # vertical shift
    Sv = (p['c14'] * Fz * Fz + p['c15'] * Fz) * gamma + p['c16'] * Fz + p['c17']

    # vertical shift 1993
    # Sv = p['c14'] * Fz + p['c15'] + (p['c16'] * Fz * Fz + p['c17'] * Fz) * gamma

    # composite
    S = alpha + Sh

    # self-aligning torque
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S)))) + Sv


def Pacejka(p, sigma, alpha, gamma, Fz):
    Fx = PacejkaFx(p, sigma, Fz)
    Fy = PacejkaFy(p, alpha, gamma, Fz)
    Mz = PacejkaMz(p, sigma, alpha, gamma, Fz)
    return Fx, Fy, Mz


# a vertical scrollable frame
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


# a base tab class
class Tab(Frame):
    def __init__(self, master, name, color):
        Frame.__init__(self, master)
        self.tab_name = name
        self.color = color

# the actual tab bar
class TabBar(Frame):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name
    
    def show(self):
        self.pack(side=TOP, anchor=N, fill=X)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])         # switch to the first tab
    
    def add(self, tab):
        tab.pack_forget()                                               # hide the tab on init
        self.tabs[tab.tab_name] = tab                                   # add it to the list of tabs
        b = Button(self, text=tab.tab_name, fg=tab.color, relief=RAISED,
            command=(lambda name=tab.tab_name: self.switch_tab(name)))  # set the command to switch tabs
        b.pack(side=LEFT, fill=X, expand=YES)                           # pack the buttont to the left
        self.buttons[tab.tab_name] = b                                  # add it to the list of buttons
    
    def delete(self, tabname):
        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])
        else:
            del self.tabs[tabname]
        self.buttons[tabname].pack_forget()
        del self.buttons[tabname] 
    
    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=RAISED)
            self.tabs[self.current_tab].pack_forget()           # hide the current tab
        self.tabs[name].pack(side=TOP, fill=X)                  # add the new tab to the display
        self.current_tab = name                                 # set the current tab to itself
        self.buttons[name].config(relief=FLAT)                  # set it to the selected style


# custom slider class
class Slider(Frame):
    def __init__(self, parent, text, v, vmin, vmax, call):
        Frame.__init__(self, parent)
        self.call = call
        self.v = StringVar()
        tl = Label(self, text=text)
        tl.pack(side=LEFT, anchor=S)
        self.s = Scale(self, from_=vmin, to=vmax, resolution=(vmax-vmin)/10000.0,
                           length=160, orient="horizontal", showvalue=0, command=self.command)
        self.s.pack(side=RIGHT, anchor=S)
        vl = Label(self, textvariable=self.v)
        vl.pack(side=RIGHT, anchor=S)
        self.set(v)
 
    def command(self, event):
        self.v.set(str(event))
        self.call(event)

    def get(self):
        return self.s.get()

    def set(self, v):
        self.v.set(str(v))
        self.s.set(v)
        

def addSlider(parent, txt, val, vmin, vmax, call):
    s = Slider(parent, txt, val, vmin, vmax, call)
    s.pack(anchor=N, fill=X)
    return s


class App:
    def __init__(self, root):
        self.need_redraw = False
        self.samples = 512
        self.slip_angle_scale = 30.0 / self.samples
        self.slip_scale = 1.0 / self.samples
        self.coeff = coeff_default.copy()
        self.coeff0 = {}
        self.file_opt = {
            'defaultextension':'.tire',
            'filetypes':[('tire files', '.tire'), ('all files', '.*')],
            'initialdir':'C:\\',
            'initialfile':'touring.tire',
            'parent':root,
            'title':'Select tire config file',
        }

        root.title('VDrift Tire Editor')

        frame = VerticalScrolledFrame(root)
        frame.pack(fill=BOTH, expand=TRUE)
        
        sframe = Frame(frame.interior, width=256)
        sframe.pack(side=LEFT, fill=Y)
        cframe = Frame(frame.interior, width=512)
        cframe.pack(side=TOP, anchor=NW)

        self.canvas = Canvas(cframe, width=512, height=512)
        self.canvas.pack(fill=BOTH, expand=YES)

        # load/save buttons
        bframe = Frame(sframe, width=256)
        Button(bframe, text='Load Ref', command=self.loadref).pack(side=LEFT, fill=X, expand=YES)
        Button(bframe, text='Load', command=self.load).pack(side=LEFT, fill=X, expand=YES)
        Button(bframe, text='Save', command=self.save).pack(side=LEFT, fill=X, expand=YES)
        bframe.pack(anchor=N, fill=X)
        
        # base coeff sliders
        self.sliders = {}
        for n in coeff_base:
            s = addSlider(sframe, n, self.coeff[n], coeff_min[n], coeff_max[n], self.update)
            self.sliders[n] = s

        # tire coeff slider tabs
        bar = TabBar(sframe, "Fx")
        tabx = Tab(sframe, "Fx", 'red')
        taby = Tab(sframe, "Fy", 'blue')
        tabz = Tab(sframe, "Mz", 'brown')

        for n in coeff_fx:
            s = addSlider(tabx, n, self.coeff[n], coeff_min[n], coeff_max[n], self.update)
            self.sliders[n] = s

        for n in coeff_fy:
            s = addSlider(taby, n, self.coeff[n], coeff_min[n], coeff_max[n], self.update)
            self.sliders[n] = s

        for n in coeff_mz:
            s = addSlider(tabz, n, self.coeff[n], coeff_min[n], coeff_max[n], self.update)
            self.sliders[n] = s

        bar.add(tabx)
        bar.add(taby)
        bar.add(tabz)
        bar.show()

        self.update('')

    def loadref(self):
        f = filedialog.askopenfile(mode='r', **self.file_opt)
        if not f: return
        for line in f:
            line = line.split('#')[0]
            if line.startswith('a') or line.startswith('b') or line.startswith('c'):
                name, value = line.split('=')
                name, value = name.strip(), value.strip()
                self.coeff0[name] = float(value)
        self.updateCanvas()

    def load(self):
        f = filedialog.askopenfile(mode='r', **self.file_opt)
        if f:
            self.readCoeff(f)

    def save(self):
        f = filedialog.asksaveasfile(mode='w', **self.file_opt)
        if f:
            self.writeCoeff(f)
        else:
            print(f)

    def readCoeff(self, f):
        for line in f:
            line = line.split('#')[0]
            if line.startswith('a') or line.startswith('b') or line.startswith('c'):
                name, value = line.split('=')
                if name in self.coeff:
                    name, value = name.strip(), value.strip()
                    self.coeff[name] = float(value)
                    self.sliders[name].set(float(value))

    def writeCoeff(self, f):
        f.write('restitution = 0.1\n')
        f.write('tread = 0.25\n')
        f.write('rolling-resistance = 1.3e-2, 6.5e-6\n')
        f.write('# Lateral force\n')
        for n in coeff_fx:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Longitudinal force\n')
        for n in coeff_fy:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Aligning moment\n')
        for n in coeff_mz:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))

    def sampleData(self, coeff):
        camber = self.coeff['Camber']
        fz = self.coeff['Fz']
        samples = self.samples
        samples2 = self.samples / 2
        afx, afy, amz = [], [], []
        for i in range(0, samples, 1):
            s = self.slip_scale * (i - samples2)
            a = self.slip_angle_scale * (i - samples2)
            fx, fy, mz = Pacejka(coeff, s, a, camber, fz)
            afx.append((i, samples2 * (1 - 0.0005 * fx / fz)))
            afy.append((i, samples2 * (1 - 0.0005 * fy / fz)))
            amz.append((i, samples2 * (1 - 0.0100 * mz / fz)))
        return afx, afy, amz

    def updateCanvas(self):
        # clear canvas
        s = self.samples
        self.canvas.delete(ALL)
        self.canvas.create_line(s/4, 2, s/4, s, width=1, fill="grey")
        self.canvas.create_line(s/2, 2, s/2, s, width=1, fill="black")
        self.canvas.create_line(3*s/4, 2, 3*s/4, s, width=1, fill="grey")
        self.canvas.create_line(2, s/4, s, s/4, width=1, fill="grey")
        self.canvas.create_line(2, s/2, s, s/2, width=1, fill="black")
        self.canvas.create_line(2, 3*s/4, s, 3*s/4, width=1, fill="grey")
        # draw ref curves
        if self.coeff0:
            fx, fy, mz = self.sampleData(self.coeff0)
            self.canvas.create_line(fx, width=1, fill="light pink")
            self.canvas.create_line(fy, width=1, fill="light blue")
            self.canvas.create_line(mz, width=1, fill="sandy brown") 
        # draw curves
        fx, fy, mz = self.sampleData(self.coeff)
        self.canvas.create_line(fx, width=1, fill="red")
        self.canvas.create_line(fy, width=1, fill="blue")
        self.canvas.create_line(mz, width=1, fill="brown")
        self.need_redraw = False

    def update(self, event):
        need_redraw = False
        for n, s in self.sliders.items():
            need_redraw = need_redraw | (self.coeff[n] != s.get())
            self.coeff[n] = s.get()
        if not self.need_redraw and need_redraw:
            self.need_redraw = need_redraw
            self.canvas.after_idle(self.updateCanvas)

    def resize(event):
        #todo: event.width, event.height
        canvas.bind("<Configure>", resize)


tk = Tk()
app = App(tk)
tk.mainloop()
