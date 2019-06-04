# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:53:22 2019

@author: meire
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

"Designs ------------------------------------------------------------------"
#ClassI = weight [kg], input value
ClassI = 360.0

#LF = load factor [-], input value
LF = 2.1

#Config = [#Tri(SR),#Tri(CR),#Quad(CR),#Hex(CR)] number of engines
config = [3,6,8,12]

#loads[Tri(SR),Tri(CR),Quad(CR),Hex(CR)]
loads = [0,0,0,0]
for i in range(len(loads)):
    loads[i] = ((ClassI * LF)/config[i])*9.81
 
#Factor of merit for different configs, [Tri(SR),Tri(CR),Quad(CR),Hex(CR)]     
FM = [0.8,0.7,0.7,0.7]

D = np.arange(1,2,0.01)    
"Calculations -------------------------------------------------------------"
def type(T): #T = 0,1,2,3 based on loads
    
    rho = 1.225
    A = np.zeros(len(D)) 
    V = np.zeros(len(D))
    Pideal = np.zeros(len(D))
    Pactual = np.zeros(len(D))
    Ptotal = np.zeros(len(D))
    
    for i in range(len(D)):
        A[i] = 0.25 * np.pi * (D[i])**2
    
    for i in range(len(D)):
        V[i] = np.sqrt(loads[T]/(2*A[i]*rho))
        
    for i in range(len(D)):
        Pideal[i] = V[i]*loads[T]
    
    for i in range(len(D)):
        Pactual[i] = Pideal[i]*(1/FM[T])
    
    for i in range(len(D)):
        Ptotal[i] = Pactual[i]*config[T]
    
    return Ptotal
 
def FlightTime(T):
    LF = 1.05
    
    #Normalize the values
    Pref = type(3)[-1]
    BatCap = Pref * 3600

    #continue
    Ptotal = type(T)
    tflight = np.zeros(len(Ptotal))
    
    for i in range(len(Ptotal)): 
        tflight[i] = (BatCap / Ptotal[i])/3600
        
    return tflight
        
def MotorW(T):
    pd = 4100 #Assumed power density [W/kg]
     
    MotorW = np.zeros(len(D))
    
    for i in range(len(D)):
        MotorW[i] = (type(T)[i])/pd
    
    return MotorW

#----------------------------------------- Iterate ---------------------------------------------
#Number iterations
k = 5

#Propulsion fractional weight (Assumed)
pf = 0.5
totalfrac = (0.2/2.1)

#Assumed power density motor
pd = 4100

#Chosen diameter (rounded to nearest cm)
Dass = 1.6

#payload weight
pl = 120

#assumed structure weight
struc = 80

#Find D index
for i in range(len(D)):
    if Dass == D[i]:
        j = i
        break 

Weight = np.zeros(k+1)
Weight[0] = ClassI

#main iterative loop
def iter(T):
    log = []
    for i in range(k):
        loads[T] = (( Weight[i] * LF)/config[T])*9.81
        p = type(T)[99]
        esc = (((1.2 - 0.9)/25000)*p)*config[T]
        w = p/pd
        neww = struc + 50 + pl + esc + (1/pf)*w
        Weight[i+1] = neww
        entry = [config[T],loads[T],p,esc,w,neww]
        log.append(entry)
    return list(Weight)





triSR = iter(0)
triCR = iter(1)
quadCR = iter(2)
hexaCR = iter(3)

x = np.arange(0,k+1,1)

fig, ax = plt.subplots()
ax.plot(x, triSR, label='Tri (SR)')
ax.plot(x, triCR, label='Tri (CR)')
ax.plot(x, quadCR, label='Quad (CR)')
ax.plot(x, hexaCR, label='Hexa (CR)')

ax.set(xlabel='x', ylabel='y',
       title='test')
ax.grid()

legend = ax.legend(loc='upper right', shadow=True, fontsize='large')


#fig.savefig("PropellerSize.png")
plt.show()
        
        
       






















