#!/usr/bin/python3

import cgi, cgitb

import os
import io
import base64
import numpy as np
import matplotlib.pyplot as plt

from nut2 import PyNUTClient
#==========================================================
#  Print header
#
#
#
#==========================================================

nInfo_Flag = 0
nWarn_Flag = 0
nAlert_Flag = 0
Info_Text_List = []
Expected_Runtime = 2400

#====================================================
# Graphic design constants
#====================================================
B_Col = '#f8f8f8'
AB_Col = '#555'
T_Col = '#333'
ST_Col = '#666'
Tick_Col = '#111'
Bar_Back = '#e8e8e8'
tfs = 11
cfs = 12
T_XP = 0.4
T_YP = 0.95
Title_B_Alpha = 0.9
Axis_B_Alpha = 0.2
Wedge_Data = { "Inner_Width" : 0.18, "Outer_Width" : 0.1, "Inner_Radius" : 0.9, "Outer_Radius" : 1.1 }
Subtext = { "x" : 0.5, "y" : 0.15, "t" : "---", "s" : 11, "c" : ST_Col }
tick_w = 0.55
tick_r = 1.2

#====================================================
# Chart data
#====================================================
Charts = {
    "Vin" : { # In V
    "Plot_Data"  : { "T_FSize" : tfs, "T_XP" : T_XP, "T_YP" : T_YP, "T_Col" : T_Col, "B_Col" : B_Col, "B_Alpha" : Title_B_Alpha, "Title" : "Input Voltage" },
    "Axis_Data"  : { "B_Col" : AB_Col, "B_Alpha" : Axis_B_Alpha, "T_FSize" : cfs, "T_XP" : 0.5, "T_YP" : 0.45, "T_Col" : T_Col, "Title" : "240V" },
    "Wedge_Data" : Wedge_Data,
    "Scale_Data" : { "Sizes" : [ 0.4, 0.2, 0.15, 0.0 ], "Explode" : [ 0, 0, 0, 0 ], "Labels" : [ '', '', '', '' ], "Colors" : [ 'yellow', 'green', 'yellow', Bar_Back] },   
    "Bar_Data"   : { "Sizes" : [ 0.5, 0.0, 0.0, 0.25 ], "Explode" : [ 0, 0, 0, 0 ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },
    "Subtext"    : Subtext,
    "Tick_Data"  : { "Width" :tick_w, "Radius" : tick_r, "Marks" : [ 228, 3, 69 ], "Cols" : [ B_Col, Tick_Col, B_Col] },
    "Plot_Arc"   : 0.75
    },     
    "Vout" : {
    "Plot_Data"  : { "T_FSize" : tfs, "T_XP" : T_XP, "T_YP" : T_YP, "T_Col" : T_Col, "B_Col" : B_Col, "B_Alpha" : Title_B_Alpha, "Title" : "Output Voltage" },
    "Axis_Data"  : { "B_Col" : AB_Col, "B_Alpha" : Axis_B_Alpha, "T_FSize" : cfs, "T_XP" : 0.5, "T_YP" : 0.45, "T_Col" : T_Col, "Title" : "250V" },
    "Wedge_Data" : Wedge_Data,
    "Scale_Data" : { "Sizes" : [ 0.4, 0.2, 0.15, 0.0 ], "Explode" : [ 0, 0, 0, 0 ], "Labels" : [ '', '', '', '' ], "Colors" : [ 'red', 'green', 'red', Bar_Back] },   
    "Bar_Data"   : { "Sizes" : [ 0.55, 0.0, 0.0, 0.20 ], "Explode" : [ 0, 0, 0, 0 ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },
    "Tick_Data"  : { "Width" :tick_w, "Radius" : tick_r, "Marks" : [ 228, 3, 69 ], "Cols" : [ B_Col, Tick_Col, B_Col] },
    "Subtext"    : Subtext,
    "Plot_Arc"   : 0.75
    },
    "OutLoad" : {
    "Plot_Data"  : { "T_FSize" : tfs, "T_XP" : T_XP, "T_YP" : T_YP, "T_Col" : T_Col, "B_Col" : B_Col, "B_Alpha" : Title_B_Alpha, "Title" : "Output Load" },
    "Axis_Data"  : { "B_Col" : AB_Col, "B_Alpha" : Axis_B_Alpha, "T_FSize" : cfs, "T_XP" : 0.5, "T_YP" : 0.45, "T_Col" : T_Col, "Title" : "125W" },
    "Wedge_Data" : Wedge_Data,
    "Scale_Data" : { "Sizes" : [ 0.45, 0.15, 0.15, 0.0 ], "Explode" : [ 0, 0, 0, 0 ], "Labels" : [ '', '', '', '' ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },   
    "Bar_Data"   : { "Sizes" : [ 0.45, 0.10, 0.0, 0.2 ], "Explode" : [ 0, 0, 0, 0 ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },
    "Tick_Data"  : { "Width" :tick_w, "Radius" : tick_r, "Marks" : [ 228, 3, 69 ], "Cols" : [ B_Col, B_Col, B_Col] },
    "Subtext"    : Subtext,
    "Plot_Arc"   : 0.75
    },     
    "BatCh" : { # Bat charge
    "Plot_Data"  : { "T_FSize" : tfs, "T_XP" : T_XP, "T_YP" : T_YP, "T_Col" : T_Col, "B_Col" : B_Col, "B_Alpha" : Title_B_Alpha, "Title" : "Battery Charge" },
    "Axis_Data"  : { "B_Col" : AB_Col, "B_Alpha" : Axis_B_Alpha, "T_FSize" : cfs, "T_XP" : 0.5, "T_YP" : 0.45, "T_Col" : T_Col, "Title" : "---%" },
    "Wedge_Data" : Wedge_Data,
    "Scale_Data" : { "Sizes" : [ 0.1, 0.2, 0.45, 0.0 ], "Explode" : [ 0, 0, 0, 0 ], "Labels" : [ '', '', '', '' ], "Colors" : [ 'red', 'yellow', 'green', Bar_Back] },   
    "Bar_Data"   : { "Sizes" : [ 0.0, 0.0, 0.0, 1.0 ], "Explode" : [ 0, 0, 0, 0 ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },
    "Tick_Data"  : { "Width" :tick_w, "Radius" : tick_r, "Marks" : [ 228, 3, 69 ], "Cols" : [ B_Col, B_Col, B_Col] },
    "Subtext"    : Subtext,
    "Plot_Arc"   : 0.75
    },   
    "Bvolt" : {  
    "Plot_Data"  : { "T_FSize" : tfs, "T_XP" : T_XP, "T_YP" : T_YP, "T_Col" : T_Col, "B_Col" : B_Col, "B_Alpha" : Title_B_Alpha, "Title" : "Battery Voltage" },
    "Axis_Data"  : { "B_Col" : AB_Col, "B_Alpha" : Axis_B_Alpha, "T_FSize" : cfs, "T_XP" : 0.5, "T_YP" : 0.45, "T_Col" : T_Col, "Title" : "--V" },
    "Wedge_Data" : Wedge_Data,
    "Scale_Data" : { "Sizes" : [ 0.3, 0.2, 0.25, 0.0 ], "Explode" : [ 0, 0, 0, 0 ], "Labels" : [ '', '', '', '' ], "Colors" : [ 'red', 'yellow', 'green', Bar_Back] },   
    "Bar_Data"   : { "Sizes" : [ 0.0, 0.0, 0.0, 1.0 ], "Explode" : [ 0, 0, 0, 0 ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },
    "Tick_Data"  : { "Width" :tick_w, "Radius" : tick_r, "Marks" : [ 0.99, 0.01, 0.15 ], "Cols" : [ B_Col, Tick_Col, B_Col] },
    "Subtext"    : Subtext,
    "Plot_Arc"   : 0.75
    },   
    "Runtime" : { # Run time
    "Plot_Data"  : { "T_FSize" : tfs, "T_XP" : T_XP, "T_YP" : T_YP, "T_Col" : T_Col, "B_Col" : B_Col, "B_Alpha" : Title_B_Alpha, "Title" : "Run Time" },
    "Axis_Data"  : { "B_Col" : AB_Col, "B_Alpha" : Axis_B_Alpha, "T_FSize" : cfs, "T_XP" : 0.5, "T_YP" : 0.45, "T_Col" : T_Col, "Title" : "--m" },
    "Wedge_Data" : Wedge_Data,
    "Scale_Data" : { "Sizes" : [ 0.2, 0.2, 0.35, 0.0 ], "Explode" : [ 0, 0, 0, 0 ], "Labels" : [ '', '', '', '' ], "Colors" : [ 'red', 'yellow', 'green', Bar_Back] },   
    "Bar_Data"   : { "Sizes" : [ 0.0, 0.0, 0.0, 1.0 ], "Explode" : [ 0, 0, 0, 0 ], "Colors" : [ 'green', 'yellow', 'red', Bar_Back] },
    "Tick_Data"  : { "Width" :tick_w, "Radius" : tick_r, "Marks" : [ 0.99, 0.01, 0.15 ], "Cols" : [ B_Col, Tick_Col, B_Col] },
    "Subtext"    : Subtext,
    "Plot_Arc"   : 0.75
    }
    }

#====================================================
# Base64 encoder function
#====================================================
def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue())

#====================================================
# Normalise the sectors of the pie chart
#====================================================
def Normalise( arr, range ):
    s = np.sum(arr)
    normal_array = (arr/s)*range
    return normal_array

#====================================================
# Pie chart plotter
#====================================================
def Make_Pie( Chart_Data ): #fig, ax, 
    fig, ax = plt.subplots(
        figsize     = (1.5, 1.5), 
        subplot_kw  = dict(aspect="equal")
        )

    fig.patch.set_facecolor( Chart_Data["Plot_Data"]["B_Col"] )
    fig.patch.set_alpha( Chart_Data["Plot_Data"]["B_Alpha"] )
    ax.patch.set_facecolor( Chart_Data["Axis_Data"]["B_Col"] )
    ax.patch.set_alpha( Chart_Data["Axis_Data"]["B_Alpha"] )

    Plot_Arc = Chart_Data["Plot_Arc"]
    Start_Angle = ((360 * (1-Plot_Arc))/2) + 180

#====================================================
# Make tick marks
#====================================================
    wedgeprops = {
        'width'     :  Chart_Data["Tick_Data"]["Width"],
        'linewidth' : 0, 'edgecolor' : 'black', 'clip_on' : True }

    ax.pie(
        Normalise( Chart_Data["Tick_Data"]["Marks"], Plot_Arc),
        #explode         = Chart_Data["Bar_Data"]["Explode"], 
    #    labels          = Bar_Data["Labels"], 
        radius = Chart_Data["Tick_Data"]["Radius"],
        #frame           = True,
        frame           = False,
        colors = Chart_Data["Tick_Data"]["Cols"],
        shadow          = False, 
        counterclock    = False,
        wedgeprops      = wedgeprops,
        normalize = False,
    #        textprops       = dict(color=Chart_Text_Colour,fontsize=Chart_Font_Size),
        startangle      = Start_Angle
        )

#################################################
# Make outer scale
#################################################
    wedgeprops = {
        'width'     : Chart_Data["Wedge_Data"]["Outer_Width"],
        'linewidth' : 0, 'edgecolor' : 'black', 'clip_on'   : True }

    ax.pie(
        Normalise( Chart_Data["Scale_Data"]["Sizes"], Plot_Arc),    
        explode         = Chart_Data["Scale_Data"]["Explode"], 
        labels          = Chart_Data["Scale_Data"]["Labels"], 
        radius = Chart_Data["Wedge_Data"]["Outer_Radius"],
        #frame           = True,
        frame           = False,
        colors = Chart_Data["Scale_Data"]["Colors"],
        shadow          = False, 
        counterclock    = False,
        wedgeprops      = wedgeprops,
        normalize = False,
    #        textprops       = dict(color=Chart_Text_Colour,fontsize=Chart_Font_Size),
        startangle      = Start_Angle
        )

#################################################
# Make measurement bar
#################################################
    wedgeprops = {
        'width'     :  Chart_Data["Wedge_Data"]["Inner_Width"],
        'linewidth' : 0, 'edgecolor' : 'black', 'clip_on'   : True }

    ax.pie(
        Normalise( Chart_Data["Bar_Data"]["Sizes"], Plot_Arc),  
        explode         = Chart_Data["Bar_Data"]["Explode"], 
    #    labels          = Bar_Data["Labels"], 
        radius = Chart_Data["Wedge_Data"]["Inner_Radius"],
        #frame           = True,
        frame           = False,
        colors = Chart_Data["Bar_Data"]["Colors"],
        shadow          = False, 
        counterclock    = False,
        wedgeprops      = wedgeprops,
        normalize = False,
    #        textprops       = dict(color=Chart_Text_Colour,fontsize=Chart_Font_Size),
        startangle      = Start_Angle
        )

    fig.suptitle(
       Chart_Data["Plot_Data"]["Title"], 
       fontsize            = Chart_Data["Plot_Data"]["T_FSize"], 
       color               = Chart_Data["Plot_Data"]["T_Col"], 
    #    verticalalignment   = 'top', 
    #    horizontalalignment = 'center', 
       x = Chart_Data["Plot_Data"]["T_XP"], 
       y = Chart_Data["Plot_Data"]["T_YP"]  
       )

    ax.set_title(
        Chart_Data["Axis_Data"]["Title"], 
        fontsize            = Chart_Data["Axis_Data"]["T_FSize"], 
        #loc                 = 'right', 
        fontweight 	        = 'bold',  #[ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']
        color               = Chart_Data["Axis_Data"]["T_Col"],
        verticalalignment   ='center', 
        horizontalalignment ='center', 
        x                   = Chart_Data["Axis_Data"]["T_XP"],
        y                   = Chart_Data["Axis_Data"]["T_YP"]
        )

    fig.text(
        x                   = Chart_Data["Subtext"]["x"],
        y                   = Chart_Data["Subtext"]["y"],
        s                   = Chart_Data["Subtext"]["t"],
        fontsize            = Chart_Data["Subtext"]["s"],
        color               = Chart_Data["Subtext"]["c"],
        horizontalalignment = 'center'
    ) 

    encoded = fig_to_base64(fig)
    Chart_HTML = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
    #plt.show()
    plt.close(fig)

    return Chart_HTML

#====================================================
# Print the V in graphic
#====================================================
def Vin_Block(ups_vars):
    print("<div id='src-vin'>")
    Chart_Data = Charts["Vin"]

    Chart_Data["Subtext"]["t"] = "Nom: " + str(ups_vars["input.voltage.nominal"]) +"V"

    vmax = 300
    itl = float(ups_vars["input.transfer.low"])
    ith = float(ups_vars["input.transfer.high"])
    s1 = (itl/vmax) * 0.75
    s2 = ((ith/vmax) * 0.75) - s1
    s3 = 0.75 - (s1 + s2) 
    Chart_Data["Scale_Data"]["Sizes"] = [s1, s2, s3, 0.0]

    vnom = float(ups_vars["input.voltage.nominal"])
    s1 = vnom - 1
    s2 = 2
    s3 = vmax - (s1 + s2)
    Chart_Data["Tick_Data"]["Marks"] = [s1, s2, s3]

    vin = float(ups_vars["input.voltage"])
    d1 = (vin/vmax)* 0.75
    d2 = 0.75 - d1
    Chart_Data["Bar_Data"]["Sizes"] = [d1, 0.0, 0.0, d2]

    Chart_Data["Axis_Data"]["Title"] = str(int(vin)) + "V"

    Chart_HTML = Make_Pie( Chart_Data = Chart_Data )
    print(Chart_HTML)

    print("</div>")
    return

#====================================================
# Print the V out graphic
#====================================================
def Vout_Block(ups_vars):
    print("<div id='src-vout'>")
    Chart_Data = Charts["Vout"]

    Chart_Data["Subtext"]["t"] = "Nom: " + str(ups_vars["input.voltage.nominal"]) +"V"
    vmax = 300
    vo_nom = float(ups_vars["input.voltage.nominal"])
    vo_min = vo_nom * 0.8
    vo_max = vo_nom * 1.2
    s1 = (vo_min/vmax) * 0.75
    s2 = ((vo_max/vmax) * 0.75) - s1
    s3 = 0.75 - (s1 + s2) 
    Chart_Data["Scale_Data"]["Sizes"] = [s1, s2, s3, 0.0]

    vnom = float(ups_vars["input.voltage.nominal"])
    s1 = vnom - 1
    s2 = 2
    s3 = vmax - (s1 + s2)
    Chart_Data["Tick_Data"]["Marks"] = [s1, s2, s3]

    vout = float(ups_vars["output.voltage"])
    d1 = (vout/vmax)* 0.75
    d2 = 0.75 - d1
    Chart_Data["Bar_Data"]["Sizes"] = [d1, 0.0, 0.0, d2]

    Chart_Data["Axis_Data"]["Title"] = str(int(vout)) + "V"

    Chart_HTML = Make_Pie( Chart_Data = Chart_Data )
    print(Chart_HTML)

    print("</div>")
    return

#====================================================
# Print the load graphic
#====================================================
def Outload_Block(ups_vars):
    print("<div id='src-outload'>")
    Chart_Data = Charts["OutLoad"]

    Chart_Data["Subtext"]["t"] = "Now: " + ups_vars["ups.load"] + "%"

    Current_Percent_Load = float(ups_vars["ups.load"])
    Max_Power = float(ups_vars["ups.realpower.nominal"])
    Current_Load = Current_Percent_Load * Max_Power / 100.0
    Chart_Data["Axis_Data"]["Title"] = str(int(Current_Load)) + "W"

    p1 = Max_Power * 0.6
    p2 = Max_Power * 0.85
    s1 = (p1/Max_Power) * 0.75
    s2 = ((p2/Max_Power) * 0.75) - s1
    s3 = 0.75 - (s1 + s2) 
    Chart_Data["Scale_Data"]["Sizes"] = [s1, s2, s3, 0.0]

    d1 = (Current_Load/Max_Power)* 0.75
    d2 = 0.75 - d1
    Chart_Data["Bar_Data"]["Sizes"] = [d1, 0.0, 0.0, d2]

    Chart_HTML = Make_Pie( Chart_Data = Chart_Data )
    print(Chart_HTML)

    print("</div>")
    return

#====================================================
# Print the bat charge graphic
#====================================================
def Bchar_Block(ups_vars):
    print("<div id='src-bchar'>")
    Chart_Data = Charts["BatCh"]

    Chart_Data["Subtext"]["t"] = "Now: " + ups_vars["battery.charge"] + "%"

    Chart_Data["Axis_Data"]["Title"] = ups_vars["battery.charge"] + "%"

    s1 = float(ups_vars["battery.charge.low"])
    s2 = float(ups_vars["battery.charge.warning"])
    s3 = 100 - (s1 + s2)
    Chart_Data["Scale_Data"]["Sizes"] = [s1, s2, s3, 0.0]

    d1 = float(ups_vars["battery.charge"])
    d2 = 100.0 - d1
    Chart_Data["Bar_Data"]["Sizes"] = [d1, 0.0, 0.0, d2]

    Chart_HTML = Make_Pie( Chart_Data = Chart_Data )
    print(Chart_HTML)

    print("</div>")
    return

#====================================================
# Print the bat voltage graphic
#====================================================
def Bvolt_Block(ups_vars):
    print("<div id='src-bvolt'>")
    Chart_Data = Charts["Bvolt"]

    Chart_Data["Subtext"]["t"] = "Nom: " + ups_vars["battery.voltage.nominal"] + "V"

    Nom_Vbat = float(ups_vars["battery.voltage.nominal"])
    # Max_Power = float(ups_vars["ups.realpower.nominal"])
    # Current_Load = Current_Percent_Load * Max_Power / 100.0
    Chart_Data["Axis_Data"]["Title"] = ups_vars["battery.voltage"] + "V"

    Bat_Overvolt = 1.20
    Max_Vbat = Bat_Overvolt * Nom_Vbat
    s1 = Nom_Vbat * 0.6
    s2 = (Nom_Vbat * 0.8) - s1
    s3 = Max_Vbat - (s1 + s2)
    Chart_Data["Scale_Data"]["Sizes"] = [s1, s2, s3, 0.0]

    s1 = Nom_Vbat - 0.3
    s2 = 0.3
    s3 = Max_Vbat - (s1 + s2)
    Chart_Data["Tick_Data"]["Marks"] = [s1, s2, s3]

    d1 = float(ups_vars["battery.voltage"])
    d2 = Max_Vbat - d1
    Chart_Data["Bar_Data"]["Sizes"] = [d1, 0.0, 0.0, d2]

    Chart_HTML = Make_Pie( Chart_Data = Chart_Data )
    print(Chart_HTML)

    print("</div>")
    return

#====================================================
# Print the bat runtime graphic
#====================================================
def Runtime_Block(ups_vars):
    print("<div id='src-runtime'>")
    Chart_Data = Charts["Runtime"]

    # Current_Percent_Load = float(ups_vars["ups.load"])
    # Max_Power = float(ups_vars["ups.realpower.nominal"])
    # Current_Load = Current_Percent_Load * Max_Power / 100.0
    # Chart_Data["Axis_Data"]["Title"] = str(int(Current_Load)) + "W"

    # p1 = Max_Power * 0.6
    # p2 = Max_Power * 0.85

    et_max = Expected_Runtime * 1.2
    et_wedge = 0.01 * et_max
    s1 = Expected_Runtime - et_wedge
    s2 = et_wedge
    s3 = et_max - (s1 + s2)
    Chart_Data["Tick_Data"]["Marks"] = [s1, s2, s3]

    s1 = float(ups_vars["battery.runtime.low"])
    s2 = (Expected_Runtime * 0.35) - s1
    s3 = et_max - (s1 + s2) 
    Chart_Data["Scale_Data"]["Sizes"] = [s1, s2, s3, 0.0]

    Current_rt = float(ups_vars["battery.runtime"])
    d1 = Current_rt
    d2 = et_max - d1
    Chart_Data["Bar_Data"]["Sizes"] = [d1, 0.0, 0.0, d2]

    rts = float(ups_vars["battery.runtime"])
    tm = str(int(rts/60)) + "m " + str(int(rts%60)) + "s"
    Chart_Data["Subtext"]["t"] = "Now: " + tm

    Chart_Data["Axis_Data"]["Title"] = str(int((rts/Expected_Runtime)*100)) + "%"


    Chart_HTML = Make_Pie( Chart_Data = Chart_Data )
    print(Chart_HTML)

    print("</div>")
    return

#====================================================
# Print the text dump diagnostics block
#====================================================
def Diag_Block(ups_vars):
    print("<div id='src-diag'>")
    for v in ups_vars:
        print(" <b>{}</b> : {}<br>".format( v, ups_vars[v]))
    print("</div>")
    return

#====================================================
# Print the flags block
#====================================================
def Flag_Block(ups_vars):
    global nInfo_Flag
    global nWarn_Flag
    global nAlert_Flag
    
    print("<div id='src-badge-info'>")
    print('<i class="bi-info-circle position-relative header-icons">')
    if nInfo_Flag > 0:
        print('<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-success header-icon-pill">')
        print( nInfo_Flag )
    print("</span></i>")    
    print("</div>")

    print("<div id='src-badge-warn'>")
    print('<i class="bi-exclamation-triangle position-relative header-icons">')
    if nWarn_Flag > 0:
        print('<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning header-icon-pill" style="color: black;">')
        print( nWarn_Flag )
    print("</span></i>")    
    print("</div>")

    print("<div id='src-badge-alert'>")
    print('<i class="bi-bell position-relative header-icons">')
    if nAlert_Flag > 0:
        print('<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger header-icon-pill">')
        print( nAlert_Flag )
    print("</span></i>")    
    print("</div>")

    return

#====================================================
# Print the info text block
#====================================================
def Infotext_Block(ups_vars):
    global Info_Text_List

    print("<div id='src-infotext'>")
    for t in Info_Text_List:
        print("{}<br>".format(t))
    print("</div>")
    return

#====================================================
# Print the headline block
#====================================================
def Headline_Block(ups_vars):
    global nInfo_Flag
    global nWarn_Flag
    global nAlert_Flag
    global Info_Text_List

    print("<div id='src-headline'>")
    if ups_vars["ups.status"].find("OL") != -1:
        print('<i class="fa-solid fa-plug-circle-bolt h1 text-success pe-1"></i>')
        nInfo_Flag = nInfo_Flag + 1
        Info_Text_List.append("<span class='text-success'>Power supply good</span>")
    elif ups_vars["ups.status"].find("OB") != -1:
        print('<i class="fa-solid fa-plug-circle-xmark h1 text-danger pe-1"></i>')
        nAlert_Flag = nAlert_Flag + 1
        Info_Text_List.append("<span class='text-danger'>Power supply failed</span>")
    else:
        print('<i class="fa-solid fa-plug-circle-exclamation h1 text-warning pe-1"></i>')
        nWarn_Flag = nWarn_Flag + 1
        Info_Text_List.append("<span class='text-warning'>Power supply state unknown</span>")

    if float(ups_vars["battery.charge"]) < float(ups_vars["battery.charge.low"]):
        print('<i class="fa-solid fa-battery-empty h1 text-success pe-1"></i>')
        nAlert_Flag = nAlert_Flag + 1
        Info_Text_List.append("<span class='text-danger'>Battery level critical</span>")
    elif float(ups_vars["battery.charge"]) < float(ups_vars["battery.charge.warning"]):
        print('<i class="fa-solid fa-battery-quarter h1 text-warning pe-1"></i>')
        nAlert_Flag = nAlert_Flag + 1
        Info_Text_List.append("<span class='text-danger'>Battery significantly discharged</span>")
    elif float(ups_vars["battery.charge"]) < 50:
        print('<i class="fa-solid fa-battery-half h1 text-warning pe-1"></i>')
        nWarn_Flag = nWarn_Flag + 1
        Info_Text_List.append("<span class='text-warning'>Battery partly discharged</span>")
    elif float(ups_vars["battery.charge"]) < 80:
        print('<i class="fa-solid fa-battery-three-quarters h1 text-success pe-1"></i>')
        nWarn_Flag = nWarn_Flag + 1
        Info_Text_List.append("<span class='text-warning'>Battery partly discharged</span>")
    else:
        print('<i class="fa-solid fa-battery-full h1 text-success pe-1"></i>')

    if ups_vars["ups.beeper.status"].lower() == 'enabled':
        # print('<span class="fa-stack h5">')
        # print('<i class="fa-solid fa-bell fa-stack-1x" ></i>')      
        # print('</span>')
        print('<i class="fa-solid fa-volume-high h1 text-success pe-1"></i>')
    else:
        # print('<span class="fa-stack h5">')
        # print('<i class="fa-solid fa-bell fa-stack-1x" ></i><i class="fa-solid fa-ban fa-stack-2x" style="color:Tomato"></i>')      
        # print('</span>')
        print('<i class="fa-solid fa-volume-xmark h1 text-warning pe-1"></i>')
        nWarn_Flag = nWarn_Flag + 1
        Info_Text_List.append("<span class='text-warning'>Alarm is muted</span>")

    print("</div>")
    return

#====================================================
# Print the topbar status block
#====================================================
def Topbar_Status_Block(ups_vars):
    print("<div id='src-topbar-status'>")
    if ups_vars["ups.status"].find("OL") != -1:
        # print('<i class="fa-solid fa-plug-circle-bolt text-success"></i>')
        print('<i class="bi bi-plugin text-success"></i>')
    else:
        # print('<i class="fa-solid fa-plug-circle-xmark text-danger"></i>')
        print('<i class="bi bi-plugin text-danger"></i>')
    print("</div>")
    return

#====================================================
# Main function
#====================================================
def main():
    print("Content-Type: text/html\n")

    username = 'monuser'
    password = 'secret'
    server_address = ''
    server_port = 3493
    interval = 30

    if os.path.exists('/config/config.txt'):
        with open('/config/config.txt') as f:
            for line in f:
                fields = line.strip().split()
                if fields[0] == 'name':
                    if len(fields) > 1:
                        username = fields[1]
                elif fields[0] == 'pass':
                    if len(fields) > 1:
                        password = fields[1]
                elif fields[0] == 'addr':
                    if len(fields) > 1:
                        server_address = fields[1]
                elif fields[0] == 'port':
                    if len(fields) > 1:
                        server_port = int(fields[1])
                elif fields[0] == 'time':
                    if len(fields) > 1:
                        interval = int(fields[1])

    client = PyNUTClient( host=server_address, port=server_port, login=username, password=password )
    ups_vars = client.list_vars("ups")

    Diag_Block(ups_vars)
    Vin_Block(ups_vars)
    Vout_Block(ups_vars)
    Outload_Block(ups_vars)
    Bchar_Block(ups_vars)
    Bvolt_Block(ups_vars)
    Runtime_Block(ups_vars)
    Headline_Block(ups_vars)
    Topbar_Status_Block(ups_vars)
    Infotext_Block(ups_vars)
    Flag_Block(ups_vars)

    return

if __name__ == "__main__":
    main()
