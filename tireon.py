from math import *
from time import time
try:
	from tkinter import filedialog
	from tkinter import *
except:
	import tkFileDialog as filedialog
	from Tkinter import *

coeff_base = ['Fz','Camber', 'aos']

coeff_fy = ['a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a111','a112','a12','a13']

coeff_fx = ['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','b10']

coeff_mz = ['c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17']

coeff_fxy = ['gy1','gy2','gx1','gx2'] 

coeff_min = {
# Base parameters
'Fz':0.5,
'Camber':-8.0,
'aos':2.0,
# Lateral force
'a0':1,
'a1':-100,
'a2':1,
'a3':1,
'a4':1,
'a5':-0.1,
'a6':-10,
'a7':-10,
'a8':-0.5,
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
'c2':-30,
'c3':-10,
'c4':-100,
'c5':-10,
'c6':-10,
'c7':-10,
'c8':-10,
'c9':-30,
'c10':-10,
'c11':-10,
'c12':-10,
'c13':-10,
'c14':-10,
'c15':-10,
'c16':-10,
'c17':-10,
# Combined
'gy1':0,
'gy2':0,
'gx1':0,
'gx2':0,
}

coeff_max = {
# Base parameters
'Fz':8.5,
'Camber':8.0,
'aos':30.0,
# Lateral force
'a0':3,
'a1':100,
'a2':2500,
'a3':5000,
'a4':100,
'a5':0.1,
'a6':10,
'a7':10,
'a8':0.5,
'a9':10,
'a10':10,
'a111':10,
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
# Combined
'gy1':50,
'gy2':50,
'gx1':50,
'gx2':50,
}

coeff_default = {
# Base parameters
'Fz':3.0,
'Camber':0.0,
'aos':8.0,
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
# Combined
'gy1':11.14388,
'gy2':10.14162,
'gx1':24.8565,
'gx2':22.43545,
}

coeff_info = {
# Base parameters
'Fz':'Current tire load [N]',
'Camber':'Current camber [deg]',
'aos':'Current angle of slip [deg]',
# Lateral force
'a0':'Shape factor',
'a1':'Peak variation with square load',
'a2':'Peak variation with load',
'a3':'Slope factor',
'a4':'Slope variation with load',
'a5':'Slope variation with camber',
'a6':'Curvature variation with load',
'a7':'Curvature factor',
'a8':'Horizontal shift variation with camber',
'a9':'Horizontal shift variation with load',
'a10':'Horizontal shift',
'a111':'Vertical shift variation with camber and square load',
'a112':'Vertical shift variation with camber and load',
'a12':'Vertical shift variation with load',
'a13':'Vertical shift',
# Longitudinal force
'b0':'Shape factor',
'b1':'Peak variation with square load',
'b2':'Peak variation with load',
'b3':'Slope variation with square load',
'b4':'Slope variation with load',
'b5':'Slope variation exp load factor',
'b6':'Curvature variation with square load',
'b7':'Curvature variation with load',
'b8':'Curvature factor',
'b9':'Horizontal shift variation with load',
'b10':'Horizontal shift',
# Aligning moment
'c0':'Shape factor',
'c1':'Peak variation with square load',
'c2':'Peak variation with load',
'c3':'Slope variation with square load',
'c4':'Slope variation with load',
'c5':'Slope variation exp load factor',
'c6':'Slope variation camber factor',
'c7':'Curvature variation with camber and square load',
'c8':'Curvature variation with camber and load',
'c9':'Curvature variation with camber',
'c10':'Curvature variation camber factor',
'c11':'Horizontal shift variation with camber',
'c12':'Horizontal shift variation with load',
'c13':'Horizontal shift',
'c14':'Vertical shift variation with camber and cubic load',
'c15':'Vertical shift variation with camber and load',
'c16':'Vertical shift variation with load',
'c17':'Vertical shift',
# Combined
'gy1':'Slope factor for combined Fy reduction',
'gy2':'Slope variation of Fy reduction with slip angle',
'gx1':'Slope factor of Fx reduction for combined slip',
'gx2':'Slope variation of Fx reduction with slip',
}


# |x| <= 1, error 2.5E-6
def Atan1(x):
    s = x * x
    p = -1.2490720064867844e-02
    p = +5.5063351366968050e-02 + p * s
    p = -1.1921576270475498e-01 + p * s
    p = +1.9498657165383548e-01 + p * s
    p = -3.3294527685374087e-01 + p * s
    p = 1 + p * s
    p = p * x
    return p

# error 2.5E-6
def Atan(x):
    if x * x < 1:
        return Atan1(x)
    return copysign(pi * 0.5, x) - Atan1(1 / x)

# |x| <= pi/2
# max error: 1E-6
def SinPi2(x):
    s = x * x
    p = -1.8447486103462252e-04
    p = +8.3109378830028557e-03 + p * s
    p = -1.6665578084732124e-01 + p * s
    p = 1 + p * s
    p = p * x
    return p

# |x| <= pi
# max error: 1E-6
def SinPi(x):
    if abs(x) > pi * 0.5:
        x = copysign(pi, x) - x
    return SinPi2(x)

def CosAtan(x):
    return 1 / sqrt(x * x + 1)

def Sin2Atan(x, y):
    return 2 * x * y / (x * x + y * y)


def Pacejka(P, S):
    B, C, D, E, Sh, Sv = P
    BS = B * (S + Sh)
    return D * SinPi(C * Atan(BS - E * (BS - Atan(BS)))) + Sv


# Longitudinal force
def PacejkaFx(p, Fz):
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

    Sv = 0.0

    # vertical shift 1993
    #Sv = p['b11'] * Fz + p['b12']

    return B, C, D, E, Sh, Sv


# Lateral force
def PacejkaFy(p, gamma, Fz):
    # shape factor
    C = p['a0']

    # peak factor
    D = (p['a1'] * Fz + p['a2']) * Fz

    # peak factor 1993
    # D = D * (1 - p['a14'] * gamma * gamma)

    # slope at origin
    BCD = p['a3'] * Sin2Atan(Fz, p['a4']) * (1 - p['a5'] * fabs(gamma))

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

    return B, C, D, E, Sh, Sv


# Aligning moment
def PacejkaMz(p, gamma, Fz):
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

    return B, C, D, E, Sh, Sv


# Longitudinal force combining factor, alpha in rad
def PacejkaGx(p, sigma, alpha):
    a = p['gx2'] * sigma
    b = p['gx1'] * alpha
    c = a * a + 1
    return sqrt(c / (c + b * b))


# Lateral force combining factor, alpha in rad
def PacejkaGy(p, sigma, alpha):
    a = p['gy2'] * alpha
    b = p['gy1'] * sigma
    c = a * a + 1
    return sqrt(c / (c + b * b))


def PacejkaFx0(p, sigma, Fz, dFz):
    Fz0 = p['FZ0']

    # vertical shift
    Sv = Fz * (p['PVX1'] + p['PVX2'] * dFz)

    # horizontal shift
    Sh = p['PHX1'] + p['PHX2'] * dFz

    # composite slip
    S = sigma + Sh

    # slope at origin
    K = Fz * (p['PKX1'] + p['PKX2'] * dFz) * exp(-p['PKX3'] * dFz)

    # curvature factor
    E = (p['PEX1'] + p['PEX2'] * dFz + p['PEX3'] * dFz * dFz) * (1 - p['PEX4'] * copysign(1, S))

    # peak factor
    D = Fz * (p['PDX1'] + p['PDX2'] * dFz)

    # shape factor
    C = p['PCX1']

    # stiffness factor
    B =  K / (C * D)

    BS = B * S

    # force
    return D * sin(C * atan(BS - E * (BS - atan(BS)))) + Sv


def PacejkaFy0(p, alpha, gamma, Fz, dFz):
    Fz0 = p['FZ0']

    # vertical shift
    Sv = Fz * (p['PVY1'] + p['PVY2'] * dFz + (p['PVY3'] + p['PVY4'] * dFz) * gamma)

    # horizontal shift
    Sh = p['PHY1'] + p['PHY2'] * dFz + p['PHY3'] * gamma

    # composite slip angle
    A = alpha + Sh;

    # slope at origin
    K = p['PKY1'] * Fz0 * Sin2Atan(Fz, p['PKY2'] * Fz0) * (1 - p['PKY3'] * abs(gamma))

    # curvature factor
    E = (p['PEY1'] + p['PEY2'] * dFz) * (1 - (p['PEY3'] + p['PEY4'] * gamma) * copysign(1, A))

    # peak factor
    D = Fz * (p['PDY1'] + p['PDY2'] * dFz) * (1 - p['PDY3'] * gamma * gamma)

    # shape factor
    C = p['PCY1']

    # stiffness factor
    B = K / (C * D)

    BA = B * A

    # force
    Fy = D * sin(C * atan(BA - E * (BA - atan(BA)))) + Sv

    Dy = D
    BCy = B * C
    Shf = Sh + Sv / K

    return Fy, Dy, BCy, Shf


def PacejkaMz0(p, alpha, gamma, Fz, dFz, Fy, BCy, Shf):
    Fz0 = p['FZ0']
    R0 = 0.3
    yz = gamma
    cosa = cos(alpha)

    Sht = p['QHZ1'] + p['QHZ2'] * dFz + (p['QHZ3'] + p['QHZ4'] * dFz) * yz

    At = alpha + Sht

    Bt = (p['QBZ1'] + p['QBZ2'] * dFz + p['QBZ3'] * dFz * dFz) * (1 + p['QBZ4'] * yz + p['QBZ5'] * abs(yz))

    BAt = Bt * At

    Ct = p['QCZ1']

    Dt = Fz * (p['QDZ1'] + p['QDZ2'] * dFz) * (1 + p['QDZ3'] * yz + p['QDZ4'] * yz * yz) * (R0 / Fz0)

    Et = (p['QEZ1'] + p['QEZ2'] * dFz + p['QEZ3'] * dFz * dFz) * (1 + (p['QEZ4'] + p['QEZ5'] * yz) * atan(Ct * BAt))

    Mzt = -Fy * Dt * cos(Ct * atan(BAt - Et * (BAt - atan(BAt)))) * cosa

    Ar = alpha + Shf

    Br = p['QBZ10'] * BCy

    Dr = Fz * (p['QDZ6'] + p['QDZ7'] * dFz + (p['QDZ8'] + p['QDZ9'] * dFz) * yz) * R0

    Mzr = Dr * CosAtan(Br * Ar) * cosa

    return Mzt + Mzr


def PacejkaGx0(p, sigma, alpha):
    # CosAtan(x)) = 1 / sqrt(1 + x * x)
    B = p['RBX1'] * CosAtan(p['RBX2'] * sigma)
    C = p['RCX1']
    Sh = p['RHX1']
    S = alpha + Sh
    G0 = cos(C * atan(B * Sh))
    G = cos(C * atan(B * S)) / G0
    return G


def PacejkaGy0(p, sigma, alpha):
    B = p['RBY1'] * CosAtan(p['RBY2'] * (alpha - p['RBY3']))
    C = p['RCY1']
    Sh = p['RHY1']
    S = sigma + Sh
    G0 = cos(C * atan(B * Sh))
    G = cos(C * atan(B * S)) / G0
    return G


def PacejkaSvy0(p, sigma, alpha, gamma, dFz, Dy):
    Dv = Dy * (p['RVY1'] + p['RVY2'] * dFz + p['RVY3'] * gamma) * CosAtan(p['RVY4'] * alpha)
    Sv = Dv * sin(p['RVY5'] * atan(p['RVY6'] * sigma))
    return Sv


def PacejkadFz0(p, Fz):
    Fz0 = p['FZ0']
    dFz = (Fz - Fz0) / Fz0;
    return dFz


def Pacejka0(p, sigma, alpha, gamma, Fz):
    dFz = PacejkadFz0(p, Fz)
    Fx = PacejkaFx0(p, sigma, Fz, dFz)
    Fy, Dy, BCy, Shf = PacejkaFy0(p, alpha, gamma, Fz, dFz)
    Mz = PacejkaMz0(p, alpha, gamma, Fz, dFz, Fy, BCy, Shf)
    return Fx, Fy, Mz


def PacejkaCombine0(p, sigma, alpha, gamma, Fx0, Fy0, Dy, dFz):
    Gx = PacejkaGx0(p, sigma, alpha)
    Gy = PacejkaGy0(p, sigma, alpha)
    Svy = PacejkaSvy0(p, sigma, alpha, gamma, Dy, dFz)
    Fx = Gx * Fx0
    Fy = Gy * Fy0 + Svy
    return Fx, Fy


class ToolTip( Toplevel ):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """ 
    def __init__( self, wdgt, msg=None, msgFunc=None, delay=1, follow=True ):
        """
        Initialize the ToolTip
        
        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        self.parent = self.wdgt.master                                          # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__( self, self.parent, bg='black', padx=1, pady=1 )      # Initalise the Toplevel
        self.withdraw()                                                         # Hide initially
        self.overrideredirect( True )                                           # The ToolTip Toplevel should have no frame or title bar
        
        self.msgVar = StringVar()                                               # The msgVar will contain the text displayed by the ToolTip        
        if msg == None:                                                         
            self.msgVar.set( 'No message provided' )
        else:
            self.msgVar.set( msg )
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        Message( self, textvariable=self.msgVar, bg='#FFFFDD',
                 aspect=1000 ).grid()                                           # The test of the ToolTip is displayed in a Message widget
        self.wdgt.bind( '<Enter>', self.spawn, '+' )                            # Add bindings to the widget.  This will NOT override bindings that the widget already has
        self.wdgt.bind( '<Leave>', self.hide, '+' )
        self.wdgt.bind( '<Motion>', self.move, '+' )
        
    def spawn( self, event=None ):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget
        
        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        self.after( int( self.delay * 1000 ), self.show )                       # The after function takes a time argument in miliseconds
        
    def show( self ):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
            
    def move( self, event ):
        """
        Processes motion within the widget.
        
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        if self.follow == False:                                                # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
            self.withdraw()
            self.visible = 1
        self.geometry( '+%i+%i' % ( event.x_root+10, event.y_root+10 ) )        # Offset the ToolTip 10x10 pixes southwest of the pointer
        try:
            self.msgVar.set( self.msgFunc() )                                   # Try to call the message function.  Will not change the message if the message function is None or the message function fails
        except:
            pass
        self.after( int( self.delay * 1000 ), self.show )
            
    def hide( self, event=None ):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


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
    def __init__(self, parent, id, v, vmin, vmax, call):
        Frame.__init__(self, parent)
        self.call = call
        self.id = id
        self.vmin = vmin
        self.vmax = vmax
        self.dv = DoubleVar()
        self.sv = StringVar()
        self.sv.trace('w', lambda name, idx, mode, var=self.sv: self.validate(var))
        self.tl = Label(self, text=id)
        self.tl.pack(side=LEFT, anchor=S)
        self.s = Scale(self, from_=vmin, to=vmax, resolution=(vmax-vmin)/10000.0,
            length=160, orient="horizontal", showvalue=0,
            variable=self.dv, command=self.command)
        self.s.pack(side=RIGHT, anchor=S)
        vl = Entry(self, width=8, textvariable=self.sv)
        vl.pack(side=RIGHT, anchor=S)
        self.set(v)

    def set(self, val):
        self.dv.set(val)
        self.sv.set(str(val))
        self.call(self.id, val)

    def validate(self, val):
        vn = val.get()
        #print("validate", self.id, vn)
        try:
            vn = float(vn)
            if (vn >= self.vmin and vn <= self.vmax):
                self.dv.set(vn)
                self.call(self.id, vn)
        except:
            return

    def command(self, val):
        #print("command", self.id, val)
        self.sv.set(val)
        self.call(self.id, float(val))
        

def addSlider(parent, txt, val, vmin, vmax, vinfo, call):
    s = Slider(parent, txt, val, vmin, vmax, call)
    s.pack(anchor=N, fill=X)
    ToolTip(s.tl, msg=vinfo, delay=0.3)
    return s


class App:
    def __init__(self, root):
        self.need_redraw = False
        self.canvas_size = 512
        self.samples = 256
        self.slip_max = 1.0
        self.slip_angle_max = 30.0
        self.coeff = coeff_default.copy()
        self.coeffn = {}
        self.file_opt = {
            'defaultextension':'.tire',
            'filetypes':[('tire files', '.tire'), ('all files', '.*')],
            'initialdir':'.',
            'initialfile':'touring.tire',
            'parent':root,
            'title':'Select tire config file',
        }
        self.file_optn = {
            'defaultextension':'.tiren',
            'filetypes':[('tire files', '.tiren'), ('all files', '.*')],
            'initialdir':'.',
            'initialfile':'touring.tiren',
            'parent':root,
            'title':'Select tire config file',
        }

        root.title('VDrift Tire Editor ON')

        frame = VerticalScrolledFrame(root)
        frame.pack(fill=BOTH, expand=TRUE)
        
        sframe = Frame(frame.interior, width=256)
        sframe.pack(side=LEFT, fill=Y)
        cframe = Frame(frame.interior, width=512)
        cframe.pack(side=TOP, anchor=NW)

        self.canvas = Canvas(cframe, width=self.canvas_size, height=self.canvas_size)
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
            s = addSlider(sframe, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        # tire coeff slider tabs
        bar = TabBar(sframe, "Fx")
        tabx = Tab(sframe, "Fx", 'red')
        taby = Tab(sframe, "Fy", 'blue')
        tabz = Tab(sframe, "Mz", 'brown')
        tabc = Tab(sframe, 'Fxy', 'black')

        for n in coeff_fx:
            s = addSlider(tabx, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        for n in coeff_fy:
            s = addSlider(taby, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        for n in coeff_mz:
            s = addSlider(tabz, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        for n in coeff_fxy:
            s = addSlider(tabc, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s
 
        bar.add(tabx)
        bar.add(taby)
        bar.add(tabz)
        bar.add(tabc)
        bar.show()

    def loadref(self):
        f = filedialog.askopenfile(mode='r', **self.file_optn)
        if not f:
            return
        for line in f:
            line = line.split('#')[0]
            if line.startswith('F') or line.startswith('P') or line.startswith('Q') or line.startswith('R'):
                name, value = line.split('=')
                name, value = name.strip(), value.strip()
                #print(name, value)
                self.coeffn[name] = float(value)
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
            if line.startswith('a') or line.startswith('b') or line.startswith('c') or line.startswith('g'):
                name, value = line.split('=')
                if name in self.coeff:
                    name, value = name.strip(), value.strip()
                    self.sliders[name].set(float(value))

    def writeCoeff(self, f):
        f.write('restitution = 0.1\n')
        f.write('tread = 0.25\n')
        f.write('rolling-resistance = 1.3e-2, 6.5e-6\n')
        f.write('# Lateral force\n')
        for n in coeff_fy:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Longitudinal force\n')
        for n in coeff_fx:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Aligning moment\n')
        for n in coeff_mz:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Combined\n')
        for n in coeff_fxy:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))

    def sampleData(self, coeff):
        scale = 0.5 * self.canvas_size
        scalea = scale / self.slip_angle_max
        scales = scale / self.slip_max
        scalef = 0.5 * scale
        slip_angle_scale = 2.0 * self.slip_angle_max / self.samples
        slip_scale = 2.0 * self.slip_max / self.samples
        camber = self.coeff['Camber']
        sa = self.coeff['aos'] / 180.0 * pi
        fz = self.coeff['Fz']
        rfz = 1 / fz
        px = PacejkaFx(coeff, fz)
        py = PacejkaFy(coeff, camber, fz)
        pz = PacejkaMz(coeff, camber, fz)
        fyp = Pacejka(py, sa / pi * 180.0)
        fyn = Pacejka(py, -sa / pi * 180.0)
        afx, afy, amz, acp, acn = [], [], [], [], []
        for i in range(-self.samples // 2, self.samples // 2, 1):
            s = i * slip_scale
            a = i * slip_angle_scale
            fx = Pacejka(px, s * 100)
            fy = Pacejka(py, a)
            mz = Pacejka(pz, a)
            gx = PacejkaGx(coeff, s, sa)
            gy = PacejkaGy(coeff, s, sa)
            mux = gx * 0.001 * fx * rfz
            muyp = gy * 0.001 * fyp * rfz
            muyn = gy * 0.001 * fyn * rfz
            afx.append((scale + s * scales, (2 - 0.001 * fx * rfz) * scalef))
            afy.append((scale + a * scalea, (2 - 0.001 * fy * rfz) * scalef))
            amz.append((scale + a * scalea, (2 - 0.01 * mz * rfz) * scalef))
            acp.append(((2 - mux) * scalef, (2 - muyp) * scalef))
            acn.append(((2 - mux) * scalef, (2 - muyn) * scalef))
        return afx, afy, amz, acp, acn

    def sampleDataRef(self, coeff):
        slip_angle_max = self.slip_angle_max / 180.0 * pi
        scale = 0.5 * self.canvas_size
        scalea = scale / slip_angle_max
        scales = scale / self.slip_max
        scalef = 0.5 * scale
        slip_angle_scale = 2.0 * slip_angle_max / self.samples
        slip_scale = 2.0 * self.slip_max / self.samples
        camber = -self.coeff['Camber'] / 180.0 * pi
        sa = self.coeff['aos'] / 180.0 * pi
        fz = self.coeff['Fz'] * 1000
        dfz = PacejkadFz0(coeff, fz)
        fyp, dyp, bcyp, shfp = PacejkaFy0(coeff, sa, camber, fz, dfz)
        fyn, dyn, bcyn, shfn = PacejkaFy0(coeff, -sa, camber, fz, dfz)
        afx, afy, amz, acp, acn = [], [], [], [], []
        for i in range(-self.samples // 2, self.samples // 2, 1):
            s = i * slip_scale
            a = i * slip_angle_scale
            fx = PacejkaFx0(coeff, s, fz, dfz)
            fy, dy, bcy, shf = PacejkaFy0(coeff, a, camber, fz, dfz)
            mz = PacejkaMz0(coeff, a, camber, fz, dfz, fy, bcy, shf)
            gx = PacejkaGx0(coeff, s, sa)
            gy = PacejkaGy0(coeff, s, sa)
            svyp = PacejkaSvy0(coeff, s, sa, camber, dyp, dfz)
            svyn = PacejkaSvy0(coeff, s, sa, camber, dyn, dfz)
            mux = gx * fx / fz
            muyp = (gy * fyp + svyp) / fz
            muyn = (gy * fyn + svyn) / fz
            afx.append((scale + s * scales, (2 - fx / fz) * scalef))
            afy.append((scale + a * scalea, (2 + fy / fz) * scalef))
            amz.append((scale + a * scalea, (2 + 10 * mz / fz) * scalef))
            acp.append(((2 - mux) * scalef, (2 - muyp) * scalef))
            acn.append(((2 - mux) * scalef, (2 - muyn) * scalef))
        return afx, afy, amz, acp, acn

    def updateCanvas(self):
        # clear canvas
        s = self.canvas_size
        self.canvas.delete(ALL)
        self.canvas.create_line(s/4, 2, s/4, s, width=1, fill="grey")
        self.canvas.create_line(s/2, 2, s/2, s, width=1, fill="black")
        self.canvas.create_line(3*s/4, 2, 3*s/4, s, width=1, fill="grey")
        self.canvas.create_line(2, s/4, s, s/4, width=1, fill="grey")
        self.canvas.create_line(2, s/2, s, s/2, width=1, fill="black")
        self.canvas.create_line(2, 3*s/4, s, 3*s/4, width=1, fill="grey")
        # draw ref curves
        if self.coeffn:
            fx, fy, mz, cp, cn = self.sampleDataRef(self.coeffn)
            self.canvas.create_line(fx, width=1, fill="light pink")
            self.canvas.create_line(fy, width=1, fill="light blue")
            self.canvas.create_line(mz, width=1, fill="sandy brown")
            self.canvas.create_line(cp, width=1, fill="dark grey")
            self.canvas.create_line(cn, width=1, fill="dark grey")
        # draw curves
        fx, fy, mz, cp, cn = self.sampleData(self.coeff)
        self.canvas.create_line(fx, width=1, fill="red")
        self.canvas.create_line(fy, width=1, fill="blue")
        self.canvas.create_line(mz, width=1, fill="brown")
        self.canvas.create_line(cp, width=1, fill="black")
        self.canvas.create_line(cn, width=1, fill="black")
        self.need_redraw = False

    def update(self, id, val):
        #print("update", id, val)
        self.coeff[id] = val
        if not self.need_redraw:
            #print("redraw")
            self.need_redraw = True
            self.canvas.after_idle(self.updateCanvas)

    def resize(event):
        #todo: event.width, event.height
        canvas.bind("<Configure>", resize)


tk = Tk()
app = App(tk)
tk.mainloop()
