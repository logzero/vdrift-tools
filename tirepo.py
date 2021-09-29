from math import *
from time import time
try:
    from tkinter import filedialog
    from tkinter import *
except:
    import tkFileDialog as filedialog
    from Tkinter import *

coeff_base = [
'fz',
'camber',
'slip angle',
'vcx',
]

coeff = [
'radius',
'width',
'ar',
'pt',
'ktx',
'kty',
'kcb',
'ccb',
'cfy',
#'cfz',
#'fz0',
'dz0',
'p0',
'mus',
'muc',
'vs'
]

coeff_min = {
'fz':500,
'camber':-9.0,
'slip angle':2.0,
'vcx':5.0,
'radius':0.1,
'width':0.1,
'ar':0.25,
'pt':0.5,
'ktx':500,
'kty':500,
'kcb':1000,
'ccb':0.0,
'cfy':0.5,
#'cfz':-0.5,
#'fz0':500,
'dz0':0.001,
'p0':1.0,
'mus':0.5,
'muc':0.1,
'vs':1.0
}

coeff_max = {
'fz':8500,
'camber':9.0,
'slip angle':30.0,
'vcx':60.0,
'radius':1.0,
'width':0.5,
'ar':1.0,
'pt':3.5,
'ktx':1200,
'kty':1200,
'kcb':5000,
'ccb':1.0,
'cfy':1.0,
#'cfz':0.0,
#'fz0':5500,
'dz0':0.021,
'p0':3.0,
'mus':4.0,
'muc':2.0,
'vs':9.0
}

coeff_default = {
'fz':3000,
'camber':0.0,
'slip angle':8.0,
'vcx':15.0,
'radius':0.28,
'width':0.2,
'ar':0.45,
'pt':2.0,
'ktx':700,
'kty':700,
'kcb':1500,
'ccb':0.5,
'cfy':1.0,
#'cfz':-0.2,
#'fz0':4000,
'dz0':0.01,
'p0':2.0,
'mus':1.5,
'muc':0.8,
'vs':4.0
}

coeff_info = {
'fz':'Current tire load [N]',
'camber':'Current camber [deg]',
'slip angle':'Current angle of slip [deg]',
'vcx':'Longitudinal wheel center velocity [m/s]',
'radius':'Tire radius [m]',
'width':'Tire width [m]',
'ar':'Tire aspect ratio',
'pt':'Tire inflation pressure [bar]',
'ktx':'Longitudinal tread stiffness [GPa/m]',
'kty':'Lateral tread stiffness [GPa/m]',
'kcb':'Carcass bending stiffness [N/mm]',
'ccb':'Carcass bending due to camber coefficient',
'cfy':'Lateral force correction factor',
#'cfz':'Friction coefficient scaling with tire load',
#'fz0':'Tire load at which friction coeff scaling is 1 [N]',
'dz0':'Displacement at which full width contact is achieved [m]',
'p0':'Contact pressure at which friction coeff scaling is 1 [bar]',
'mus':'Static friction coefficient',
'muc':'Sliding friction coefficient',
'vs':'Stribeck friction velocity [m/s]'
}

#log = open("log.txt", 'w')

def ComputePatch(coeff, fz, camber):
    r = coeff['radius']
    w = coeff['width']
    ar = coeff['ar']
    pt = coeff['pt']
    ccb = coeff['ccb']
    #cfz = coeff['cfz']
    #fz0 = coeff['fz0']
    dz0 = coeff['dz0']
    p0 = coeff['p0']

    # vertical stiffness
    cf = 0.28 * sqrt((1.03 - 0.4 * ar) * w * r * 2)
    kz = 9.81 * (1E5 * pt * cf + 3450) # ~200000 N/m
    
    # vertical deflection
    dz = fz / kz
    
    # patch width
    if dz < dz0:
        sz = 1 - dz / dz0
        w = w * sqrt(1 - sz * sz)
    
    # patch half length
    #a = sqrt(r**2 - (r - dz)**2)
    a = 0.30 * (dz + 2.25 * sqrt(r * dz))
    wa = w * a * 1E5

    # contact pressure
    # p(u) = p * (1 - u^2) * (1 + u / 4) with u = x / a
    # fz = w * a * p * 4 / 3
    p = 0.75 * fz / wa

    # friction coeff
    mu = (p / p0)**(-1/3.0)

    # tread bending due to camber 
    ym = ccb * dz * sin(camber)

    return mu * p, w * a * 1E5, a, ym

def ComputeSlipPoint(qx, qy, qb, qp):
    c4 = 1/16.0 * qp * qp
    c3, c2, c1, c0 = 6 * c4, 9 * c4 - qb * qb, 2 * qy * qb, -(qx * qx + qy * qy)
    d3, d2, d1, d0 = 4 * c4, 3 * c3, 2 * c2, c1
    def f(x): return x * (x * (x * (x * c4 + c3) + c2) + c1) + c0
    def d(x): return x * (x * (x * d3 + d2) + d1) + d0
    if qx * qx + (qy - qb)**2 > 0: 
        f2 = f(2)
        f1 = f(1)
        if f1 > 0:
            uc = 1 - f1 / d(1)
            for i in range(3):
                uc = uc - f(uc) / d(uc)
            return uc - 1
        if f2 * f1 < 0:
            uc = 2 - f2 / d(2)
            for i in range(3):
                uc = uc - f(uc) / d(uc)
            return uc - 1
        return 1
    return -1

def ComputeFx(coeff, patch, slip):
    vcx = coeff['vcx']
    ktx = coeff['ktx']
    mus = coeff['mus']
    muc = coeff['muc']
    vs = coeff['vs']

    vrx = vcx * slip
    vr = abs(vrx)

    mup, wa, a, ym = patch
    muv = muc + (mus - muc) * exp(-sqrt(vr / vs))
    mup = mup * muv

    sx = -slip / (1 - slip)
    nx = -1.0 if slip > 0 else 1.0
    qx = ktx * a * sx;

    # |qx| * (1 - u) = mup / 4 * (1 - u^2) * (4 + u)
    t = sqrt(4.0 * abs(qx) / mup + 2.25)
    uc = t - 2.5
    if uc > 1.0: uc = 1.0
    ud = uc + 1
    ue = uc - 1
    uf = 3 * uc + 5

    ts = 0.5 * wa * (ue * ue)
    tc = mup * wa * (ud * ud)
    fc = tc * (7/9.0 - 1/144.0 * (uf * uf))
    fcx = fc * nx
    fsx = ts * qx
    fx = fsx + fcx

    return -fx

def ComputeFy(coeff, patch, slip_angle):
    vcx = coeff['vcx']
    kty = coeff['kty']
    kcb = coeff['kcb'] * 1000
    cfy = coeff['cfy']
    mus = coeff['mus']
    muc = coeff['muc']
    vs = coeff['vs']

    tsa = tan(slip_angle)
    vr = vcx * abs(tsa)

    mup, wa, a, ym = patch
    muv = muc + (mus - muc) * exp(-sqrt(vr / vs))
    mup = mup * muv

    sy = -tsa
    ny = -1.0 if tsa > 0 else 1.0
    qy = kty * a * sy;

    rkb = 1 / kcb
    rp4 = 4.0 / mup
    rq4 = 4.0 * rp4 * abs(qy)
    fy, fyo = 0.0, 0.0
    for i in range(4):
        fy = 0.5 *(fy + fyo)
        fyo = fy
        
        yb = fy * rkb + ym
        qb = kty * yb

        # qy - qb * (1 + u) = mup / 4 * (1 + u) * (4 + u)
        t0 = rp4 * abs(qb)
        t1 = t0 + 3
        t2 = sqrt(t1 * t1 + rq4)
        uc = 0.5 * (t2 - t0 - 5)
        if uc > 1.0: uc = 1.0
        ud = uc + 1
        ue = uc - 1
        uf = 3 * uc + 5

        ts = 0.5 * wa * (ue * ue)
        tb = 1/3.0 * wa * ((uc * uc - 3) * uc + 2)
        tc = mup * wa * (ud * ud)
        fc = tc * (7/9.0 - 1/144.0 * (uf * uf))
        fcy = fc * ny
        fsy = ts * qy - tb * qb
        fy = fsy + fcy

    msz = 1/6.0 * ts * a * (qy * (4 * uc + 2) - (3 * qb) * (ud * ud))
    mcz = -1/60.0 * tc * a * ny * (((3 * uc + 9) * uc - 26) * uc + 13)
    mz = msz + mcz
    
    return fy * cfy, mz


def friction(coeff, patch, slip, slip_angle):
    vcx = coeff['vcx']
    ktx = coeff['ktx']
    kty = coeff['kty']
    kcb = coeff['kcb'] * 1000
    cfy = coeff['cfy']
    mus = coeff['mus']
    muc = coeff['muc']
    vs = coeff['vs']

    mup, wa, a, ym = patch

    # vcx > 0
    vcy = vcx * tan(slip_angle)
    vc = vcx / cos(slip_angle)
    rw = vcx * (1 - slip)

    vrx = vcx - rw
    vry = vcy
    vr = sqrt(vrx * vrx + vry * vry)

    sx = -vrx / rw
    sy = -vry / rw
    
    nx, ny = 0.0, 0.0
    if vr > 0:
        nx = -vrx / vr
        ny = -vry / vr

    # friction coeff
    muv = muc + (mus - muc) * exp(-sqrt(vr / vs))
    mup = mup * muv

    # carcass bending: ycb = yb + ym
    #                  yb = fy / kcb * (1 - u^2)
    #                  ym = ccb * dz * sin(camber) * (1 - u^2)
    # displacement: dx(x) = sx * (a - x)
    #               dy(x) = sy * (a - x) - ycb
    # shear stress: qx(x) = ktx * dx(x)
    #               qy(x) = kty * dy(x)
    # shear limit:  |q(x)| = mu * p(x)
    qx = ktx * sx * a
    qy = kty * sy * a

    fy, fyo = 0.0, 0.0
    for i in range(4):
        fy = 0.5 * (fy + fyo)
        fyo = fy
        
        yb = fy / kcb
        ycb = yb + ym
        qcb = kty * ycb

        # (qy - qcb * (1 + u))^2 + qx^2 = (mu * p)^2 * (1 + u)^2 * (1 + u / 4)^2
        uc = ComputeSlipPoint(qx, qy, qcb, mup)
        
        # fs = integrate w * q(x) from xc to a
        # fc = integrate w * mu * p(x) from -a to xc
        ts = wa * 0.5 * (1 - uc)**2
        tb = wa / 3.0 * kty * ((uc * uc - 3) * uc + 2)
        tc = mup * wa * (1 + uc)**2
        fc = tc * (7 / 9.0 - (5 + 3 * uc)**2 / 12.0**2)
        fcy = fc * ny
        fy = (ts * qy - tb * ym + fcy) / (1 + tb / kcb)

    fy = cfy * fy

    fcx = fc * nx
    fsx = ts * qx
    fx = fsx + fcx

    # msz = integrate w * (x * qy(x) - ycb(x) * qx(x)) from xc to a
    msz = (ts * a * (qy * (2 + 4 * uc) - 3 * qcb * (1 + uc)**2)
           - fsx * ycb * (1 - uc) * (5 + 3 * uc)) / 6.0
    
    # mcz = integrate w * mu * p(x) * (x * ny - ycb(x) * nx) from -a to xc
    mcz = -tc / 60.0 * (
        (((3 * uc + 9) * uc - 26) * uc + 13) * a * ny +
        (((5 * uc + 9) * uc - 57) * uc + 59) * (1 + uc) * 0.5 * ycb * nx)
    
    mz = msz + mcz

    return -fx, fy, mz  


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


def Pacejka0(P, S):
    B, C, D, E, Sh, Sv = P
    BS = B * (S + Sh)
    return D * SinPi(C * Atan(BS - E * (BS - Atan(BS)))) + Sv


# Longitudinal force
def PacejkaFx0(p, Fz):
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
def PacejkaFy0(p, gamma, Fz):
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
def PacejkaMz0(p, gamma, Fz):
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
def PacejkaGx0(p, sigma, alpha):
    a = p['gx2'] * sigma
    b = p['gx1'] * alpha
    c = a * a + 1
    return sqrt(c / (c + b * b))


# Lateral force combining factor, alpha in rad
def PacejkaGy0(p, sigma, alpha):
    a = p['gy2'] * alpha
    b = p['gy1'] * sigma
    c = a * a + 1
    return sqrt(c / (c + b * b))


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
        self.coeff0 = {}
        self.file_opt = {
            'defaultextension':'.tirep',
            'filetypes':[('tire files', '.tirep'), ('all files', '.*')],
            'initialdir':'.',
            'initialfile':'touring.tirep',
            'parent':root,
            'title':'Select tire config file',
        }
        self.file_opt_ref = {
            'defaultextension':'.tire',
            'filetypes':[('tire files', '.tire'), ('all files', '.*')],
            'initialdir':'.',
            'initialfile':'touring.tire',
            'parent':root,
            'title':'Select tire config file',
        }

        root.title('VDrift Tire Editor PO')

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
  
        # coeff sliders
        self.sliders = {}
        for n in coeff_base:
            s = addSlider(sframe, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s
        for n in coeff:
            s = addSlider(sframe, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

    def loadref(self):
        f = filedialog.askopenfile(mode='r', **self.file_opt_ref)
        if not f: return
        for line in f:
            line = line.split('#')[0]
            if line.startswith('a') or line.startswith('b') or line.startswith('c') or line.startswith('g'):
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

    def readCoeff(self, f):
        for line in f:
            if not line.startswith('#'):
                name, value = line.split('=')
                name, value = name.strip(), value.strip()
                self.sliders[name].set(float(value))
        self.updateCanvas()

    def writeCoeff(self, f):
        for n in coeff:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))

    def sampleData0(self, coeff):
        scale = 0.5 * self.canvas_size
        scalea = scale / self.slip_angle_max
        scales = scale / self.slip_max
        scalef = 0.5 * scale
        slip_angle_scale = 2.0 * self.slip_angle_max / self.samples
        slip_scale = 2.0 * self.slip_max / self.samples
        camber = self.coeff['camber']
        sa = self.coeff['slip angle'] / 180.0 * pi
        fz = self.coeff['fz'] * 0.001
        rfz = 1 / fz
        px = PacejkaFx0(coeff, fz)
        py = PacejkaFy0(coeff, camber, fz)
        pz = PacejkaMz0(coeff, camber, fz)
        fyp = Pacejka0(py, sa / pi * 180.0)
        fyn = Pacejka0(py, -sa / pi * 180.0)
        afx, afy, amz, acp, acn = [], [], [], [], []
        for i in range(-self.samples // 2, self.samples // 2, 1):
            s = i * slip_scale
            a = i * slip_angle_scale
            fx = Pacejka0(px, s * 100)
            fy = Pacejka0(py, a)
            mz = Pacejka0(pz, a)
            gx = PacejkaGx0(coeff, s, sa)
            gy = PacejkaGy0(coeff, s, sa)
            mux = gx * 0.001 * fx * rfz
            muyp = gy * 0.001 * fyp * rfz
            muyn = gy * 0.001 * fyn * rfz
            afx.append((scale + s * scales, (2 - 0.001 * fx * rfz) * scalef))
            afy.append((scale + a * scalea, (2 - 0.001 * fy * rfz) * scalef))
            amz.append((scale + a * scalea, (2 - 0.01 * mz * rfz) * scalef))
            acp.append(((2 - mux) * scalef, (2 - muyp) * scalef))
            acn.append(((2 - mux) * scalef, (2 - muyn) * scalef))
        return afx, afy, amz, acp, acn

    def sampleData(self, coeff):
        slip_angle_max = self.slip_angle_max / 180.0 * pi
        scale = 0.5 * self.canvas_size
        scalea = scale / slip_angle_max
        scales = scale / self.slip_max
        scalef = 0.5 * scale
        slip_angle_scale = 2.0 * slip_angle_max / self.samples
        slip_scale = 2.0 * self.slip_max / self.samples
        camber = -coeff['camber'] / 180.0 * pi
        sa = self.coeff['slip angle'] / 180.0 * pi
        fz = self.coeff['fz']
        # force, torque curves
        afx, afy, amz = [], [], []
        patch = ComputePatch(coeff, fz, camber)
        for i in range(-self.samples // 2, self.samples // 2, 1):
            s = i * slip_scale
            a = i * slip_angle_scale
            fx = ComputeFx(coeff, patch, s)
            fy, mz = ComputeFy(coeff, patch, a)
            afx.append((scale + s * scales, (2 - fx / fz) * scalef))
            afy.append((scale + a * scalea, (2 + fy / fz) * scalef))
            amz.append((scale + a * scalea, (2 + 10 * mz / fz) * scalef))
        # combined force curve
        atcp, atcn = [], []
        for i in range(-self.samples // 2, self.samples // 2, 1):
            s = i * slip_scale
            fxp, fyp, _ = friction(coeff, patch, s, sa)
            fxn, fyn, _ = friction(coeff, patch, s, -sa)
            atcp.append(((2 - fxp / fz) * scalef, (2 - fyp / fz) * scalef))
            atcn.append(((2 - fxn / fz) * scalef, (2 - fyn / fz) * scalef))
        return afx, afy, amz, atcp, atcn
        
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
        if self.coeff0:
            fx, fy, mz, tcp, tcn = self.sampleData0(self.coeff0)
            self.canvas.create_line(fx, width=1, fill="light pink")
            self.canvas.create_line(fy, width=1, fill="light blue")
            self.canvas.create_line(mz, width=1, fill="sandy brown")
            self.canvas.create_line(tcp, width=1, fill="dark grey")
            self.canvas.create_line(tcn, width=1, fill="dark grey")
        # draw curves
        fx, fy, mz, tcp, tcn = self.sampleData(self.coeff)
        self.canvas.create_line(fx, width=1, fill="red")
        self.canvas.create_line(fy, width=1, fill="blue")
        self.canvas.create_line(mz, width=1, fill="brown")
        self.canvas.create_line(tcp, width=1, fill="black")
        self.canvas.create_line(tcn, width=1, fill="black")
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
