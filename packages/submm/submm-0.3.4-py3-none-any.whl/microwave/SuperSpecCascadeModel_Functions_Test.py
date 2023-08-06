# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:26:51 2015

TEST CHANGES TO FUNCTIONS CODE

Functions for the cascaded SuperSpec filter bank circuit Model. These include 
implementations of the broadband detector and spectral channel as 2 and
3-port networks. A complete list of functions is as follows:

ABCD2S - converts ABCD-matrix to S-matrix
S2ANCD - converts S-matrix to ABCD-matrix
TransmissionLine - creates a 2 or 3-port transmission line network
SpectralChannel3PortNetwork - creates a 2 or 3-port spectral channel network
FilterBank - creates a full filter bank of arbitrary size
ChannelFrequencies - calculates channel frequencies given a band and Sigma
IsolatedChannel - analytically calculates S-paramters for an isolated channel
 
@author: AlienGeorge
"""
import numpy as np
import skrf as rf
from matplotlib import pyplot as plt
import time
from multiprocessing import Pool

c = 3.0e8 # speed of light in vacuum

'''
Function to convert ABCD-matrix to S-matrix.

Arguments: A, B, C, D, Z0.
Returns: 2x2xf array S-matrix.
 
Notes: Transposition to fxnxn format is done externally.
'''
def ABCD2S(A,B,C,D, Z0):
    S11 = (1.0*A+B/Z0-C*Z0-D)/(A+B/Z0+C*Z0+D)
    S12 = 2.0*(A*D-B*C)/(A+B/Z0+C*Z0+D)
    S21 = 2.0/(A+B/Z0+C*Z0+D)
    S22 = (-1.0*A+B/Z0-C*Z0+D)/(A+B/Z0+C*Z0+D)
    return np.array([[S11, S12],[S21, S22]])
    
'''
Function to convert S-matrix to ABCD-matrix.

Arguments: S11, S12, S21, S22, Z0.
Returns 2x2xf array ABCD-matrix.

Notes: Transposition for fxnxn format is done externally.
'''
def S2ABCD(S11, S12, S21, S22, Z0):
    A = ((1.0+S11)*(1.0-S22)+S12*S21)/(2.0*S21)
    B = Z0*((1.0+S11)*(1.0+S22)-S12*S21)/(2.0*S21)
    C = 1.0/Z0*((1.0-S11)*(1.0-S22)-S12*S21)/(2.0*S21)
    D = ((1.0-S11)*(1.0+S22)+S12*S21)/(2.0*S21)
    return np.array([[A,B],[C,D]])

'''
Function to convert 2-port S-matrix with arbitrary port impedances Z01 and Z02
to Z-matrix.

Arguments: S (fx2x2 S-matrix), Z01 (fx1 Z0 vector), Z02 (fx1 Z0 vector)
Returns Z (fx2x2 Z-matrix)
'''
def S2Z(S, Z01, Z02):
    S11=S[:,0,0]; S12=S[:,0,1]; S21=S[:,1,0]; S22=S[:,1,1]
    Z11=((np.conj(Z01)+S11*Z01)*(1.0-S22)+S12*S21*Z01)/((1.0-S11)*(1.0-S22)-S12*S21)
    Z12=2.0*S12*np.sqrt(np.real(Z01)*np.real(Z02))/((1.0-S11)*(1.0-S22)-S12*S21)
    Z21=2.0*S21*np.sqrt(np.real(Z01)*np.real(Z02))/((1.0-S11)*(1.0-S22)-S12*S21)
    Z22=((1.0-S11)*(np.conj(Z02)+S22*Z02)+S12*S21*Z02)/((1.0-S11)*(1.0-S22)-S12*S21)
    Z=np.array([[Z11, Z12], [Z21, Z22]]).transpose(2, 0, 1)
    return Z
    
'''
Function to convert 2-port Z-matrix to S-matrix with arbitrary port impedances
Z01 and Z02.

Arguments: Z (fx2x2 S-matrix), Z01 (fx1 Z0 vector), Z02 (fx1 Z0 vector)
Returns S (fx2x2 S-matrix)
'''
def Z2S(Z, Z01, Z02):
    Z11=Z[:,0,0]; Z12=Z[:,0,1]; Z21=Z[:,1,0]; Z22=Z[:,1,1]
    S11=((Z11-np.conj(Z01))*(Z22+Z02)-Z12*Z21)/((Z11+Z01)*(Z22+Z02)-Z12*Z21)
    S12=2.0*Z12*np.sqrt(np.real(Z01)*np.real(Z02))/((Z11+Z01)*(Z22+Z02)-Z12*Z21)
    S21=2.0*Z21*np.sqrt(np.real(Z01)*np.real(Z02))/((Z11+Z01)*(Z22+Z02)-Z12*Z21)
    S22=((Z11+np.conj(Z01))*(Z22-np.conj(Z02))-Z12*Z21)/((Z11+Z01)*(Z22+Z02)-Z12*Z21)
    S=np.array([[S11, S12],[S21, S22]]).transpose(2, 0, 1)
    return S

'''
OLD Function to create a network object representing a transmission line.

Arguments: frequency band, physical length, char. impedance, ind. of refrac.,
attenuation constant, # of ports. 
Returns: transmission line network object
'''
def TransmissionLine(Band, l, Z0, n=1.0, alpha=0.0, nPorts=2):
    v = c/n # wave speed in transmission line    
    beta = 2.0*np.pi*Band.f/v # real propagation constant
    gamma = alpha + 1j*beta # complex propagation constant (with annuation)
    
    # construct ABCD matrix of the lossy line
    A = np.cosh(gamma*l)
    B = Z0*np.sinh(gamma*l)
    C = 1/Z0*np.sinh(gamma*l)
    D = np.cosh(gamma*l)
    
    S_2port = ABCD2S(A, B, C, D, Z0) # convert lossy line ABCD to S-parameters
    S11=S_2port[0,0]; S12=S_2port[0,1]; S21=S_2port[1,0]; S22=S_2port[1, 1];    
    
    if nPorts==2:
        S_2port = np.array([[S11, S12],[S21, S22]]).transpose(2, 0, 1)
        return rf.Network(frequency=Band, s=S_2port, z0=Z0)
    elif nPorts==3:
        S13 = np.sqrt(1-np.conj(S11)*S11-np.conj(S12)*S12)    
        S31 = S13
        theta23 = np.pi/2-beta*l    
        S23 = np.abs(S13)*np.exp(1j*theta23)
        S32 = S23
        S33 = np.zeros(np.size(Band.f))
        S_3port = np.array([[S11, S12, S13],[S21, S22, S23],[S31, S32, S33]]).transpose(2, 0, 1)
        return rf.Network(frequency = Band, s = S_3port, z0 = Z0)

'''
Function to create a network object representing a lossy transmission line.

Arguments: frequency band, physical length, char. impedance, propagation speed,
relative permittivity of dielectric, loss tangent of dielectric, # of ports. 
Returns: transmission line network object
Note: we assume that loss is dominated by dielectric loss
'''
def TransmissionLineLossy(Band, l, Z0, v, epsr=11.7, lossTan=0.0, nPorts=2):   
    beta = 2.0*np.pi*Band.f/v # real propagation constant
    #alpha = np.pi*np.sqrt(epsr)*Band.f/v*lossTan # attenuation constant in Np/m
    alpha = np.pi*Band.f/v*lossTan # attenuation constant in Np/m so that the units are on chip normalized for epsilonr
    gamma = alpha + 1j*beta # complex propagation constant (with attenuation)
    
    # construct ABCD matrix of the lossy line
    A = np.cosh(gamma*l)
    B = Z0*np.sinh(gamma*l)
    C = 1/Z0*np.sinh(gamma*l)
    D = np.cosh(gamma*l)
    
    S_2port = ABCD2S(A, B, C, D, Z0) # convert lossy line ABCD to S-parameters
    S11=S_2port[0,0]; S12=S_2port[0,1]; S21=S_2port[1,0]; S22=S_2port[1, 1];    
    
    if nPorts==2:
        S_2port = np.array([[S11, S12],[S21, S22]]).transpose(2, 0, 1)
        return rf.Network(frequency=Band, s=S_2port, z0=Z0)
    elif nPorts==3:
        S13 = np.sqrt(1-np.conj(S11)*S11-np.conj(S12)*S12)    
        S31 = S13
        theta23 = np.pi/2-beta*l    
        S23 = np.abs(S13)*np.exp(1j*theta23)
        S32 = S23
        S33 = np.zeros(np.size(Band.f))
        S_3port = np.array([[S11, S12, S13],[S21, S22, S23],[S31, S32, S33]]).transpose(2, 0, 1)
        return rf.Network(frequency = Band, s = S_3port, z0 = Z0)

'''
OLD Function to create a network object representing a spectral channel as
a 3-port network.

Arguments: freq. band, char. impedance, resonant freq., coupling Q, internal Q,
approach ("1" for matched ports, "2" for unmatched ports).
Returns: spectral channel network object
'''
def SpectralChannel3PortNetwork(Band, Z0, fres, Qc, Qi, approach=1):
    x = (Band.f-fres)/fres
    ZL = Z0/2*Qc/Qi+1j*Z0*Qc*x   # shunt impedance of the entire resonator
    # ZR = ZL-Z0  # resonator impedance minus impedance of matched port
    
    # 3-port network with all ports referenced to 50 Ohm; terminate port 2 with ZL
    if approach==1:
        S_3port = np.ones((np.size(x), 3, 3))
        
        # create 3-port S-matrix for the 50 Ohm matched network
        S_3port[:,0, 0]=-1.0/3; S_3port[:,0, 1]=2.0/3; S_3port[:,0, 2]=2.0/3
        S_3port[:,1, 0]=2.0/3; S_3port[:,1, 1]=-1.0/3; S_3port[:,1, 2]=2.0/3
        S_3port[:,2, 0]=2.0/3; S_3port[:,2, 1]=2.0/3; S_3port[:,2, 2]=-1.0/3
        
        # create a network object for the 50 Ohm matched network        
        MatchedNtwk = rf.Network(frequency = Band, s = S_3port, z0 = Z0)
        
        # create 1-port S-matrix for the resonator load
        S11_L=(ZL-Z0)/(ZL+Z0)
        Resonator = rf.Network(frequency = Band, s = S11_L, z0 = Z0)
        Ntwk = rf.connect(MatchedNtwk, 2, Resonator, 0)
        return Ntwk
    
    # 3-port network with all ports referenced to 50 Ohm; renormalize so port 2
    # is referenced to ZL
    elif approach==2:
        S_3port = np.ones((np.size(x), 3, 3))
        
        # create 3-port S-matrix for the 50 Ohm matched network
        S_3port[:,0, 0]=-1.0/3; S_3port[:,0, 1]=2.0/3; S_3port[:,0, 2]=2.0/3
        S_3port[:,1, 0]=2.0/3; S_3port[:,1, 1]=-1.0/3; S_3port[:,1, 2]=2.0/3
        S_3port[:,2, 0]=2.0/3; S_3port[:,2, 1]=2.0/3; S_3port[:,2, 2]=-1.0/3
        
        # create a network object for the 50 Ohm matched network        
        Ntwk = rf.Network(frequency = Band, s = S_3port, z0 = Z0)
        
        # create port reference impedance matrix
        Zmatrix = np.empty([len(Band.f),3], dtype=complex)
        Zmatrix[:,2]=Z0; Zmatrix[:,0]=Z0; Zmatrix[:,1]=ZL
        
        Ntwk.renormalize(Zmatrix, powerwave=True)
        return Ntwk
#    elif approach==2:
#        # create 3-port S-matrix for the network referenced at ZL for port 3        
#        S11=-Z0/(2*ZL+Z0); S22=S11; S12=2*ZL/(2*ZL+Z0); S21=S12
#        S31=np.sqrt(Z0/np.real(ZL))*2*np.real(ZL)/(2*ZL+Z0); S32=S31
#        S13=np.sqrt(np.real(ZL)/Z0)*2*(Z0+4*np.imag(ZL))/(2*ZL+Z0); S23=S13
#        S33=(Z0-ZL)/(Z0+2*np.conj(ZL))
#        S_3port = np.array([[S11, S12, S13],[S21, S22, S23],[S31, S32, S33]]).transpose(2,0,1)
#        
#        # create port reference impedance matrix
#        Zmatrix = np.empty([len(x),3], dtype=complex)
#        Zmatrix[:,2]=Z0; Zmatrix[:,0]=Z0; Zmatrix[:,1]=Z0
#        
#        return rf.Network(frequency = Band, s = S_3port, z0=Zmatrix)
    
    elif approach==3:
        # create 2-port S-matrix for the network
        S11=-Z0/(2*ZL+Z0); S22=S11; S12=2*ZL/(2*ZL+Z0); S21=S12
        S_2port=np.array([[S11, S12],[S21, S22]]).transpose(2, 0, 1)
        
        return rf.Network(frequency = Band, s = S_2port, z0=Z0)

'''
Function to create a network object representing a spectral channel as either a
2-port or 3-port network. Incorporates lossy dielectric as Qloss.

Arguments: freq. band, char. impedance, resonant freq., coupling Q, internal Q,
loss Q, approach ("1" for 3-port representation all referenced to Z0 and
terminated in ZL, "2" for 3-port representation with port 2 referenced to ZL, 
"3" for 2-port representation).
Returns: spectral channel network object
'''
def SpectralChannelLossy(Band, Z0, fres, Qc, Qdet, Qloss, approach=1,normalize = True):
    x = (Band.f-fres)/fres
    ZL = Z0/2*Qc*(1/Qdet+1/Qloss)+1j*Z0*Qc*x   # shunt impedance of the entire resonator
    # ZR = ZL-Z0  # resonator impedance minus impedance of matched port
    
    # 3-port network with all ports referenced to 50 Ohm; terminate port 2 with ZL
    if approach==1:
        S_3port = np.ones((np.size(x), 3, 3))
        
        # create 3-port S-matrix for the 50 Ohm matched network
        S_3port[:,0, 0]=-1.0/3; S_3port[:,0, 1]=2.0/3; S_3port[:,0, 2]=2.0/3
        S_3port[:,1, 0]=2.0/3; S_3port[:,1, 1]=-1.0/3; S_3port[:,1, 2]=2.0/3
        S_3port[:,2, 0]=2.0/3; S_3port[:,2, 1]=2.0/3; S_3port[:,2, 2]=-1.0/3
        
        # create a network object for the 50 Ohm matched network        
        MatchedNtwk = rf.Network(frequency = Band, s = S_3port, z0 = Z0)
        
        # create 1-port S-matrix for the resonator load
        S11_L=(ZL-Z0)/(ZL+Z0)
        Resonator = rf.Network(frequency = Band, s = S11_L, z0 = Z0)
        Ntwk = rf.connect(MatchedNtwk, 2, Resonator, 0)
        return Ntwk
    
    # 3-port network with all ports referenced to 50 Ohm; renormalize so port 2
    # is referenced to ZL
    elif approach==2:
        S_3port = np.ones((np.size(x), 3, 3))
        
        # create 3-port S-matrix for the 50 Ohm matched network
        # had to add in small values to allow matrix to be imported jordan 5/29/2020
        S_3port[:,0, 0]=-1.0/3+0.0000001; S_3port[:,0, 1]=2.0/3; S_3port[:,0, 2]=2.0/3
        S_3port[:,1, 0]=2.0/3; S_3port[:,1, 1]=-1.0/3+0.0000001; S_3port[:,1, 2]=2.0/3
        S_3port[:,2, 0]=2.0/3; S_3port[:,2, 1]=2.0/3; S_3port[:,2, 2]=-1.0/3+0.0000001
        #print(S_3port)
        # create a network object for the 50 Ohm matched network        
        Ntwk = rf.Network(frequency = Band, s = S_3port, z0 = Z0)
        #print(Ntwk)
        #print(Ntwk.z0)
        #print(Ntwk.z0.shape)
        #print(Ntwk.s)
        #print(Ntwk.s.shape)
        # create port reference impedance matrix
        if normalize:
            Zmatrix = np.empty([len(Band.f),3], dtype=complex)
            Zmatrix[:,2]=Z0
            Zmatrix[:,0]=Z0
            Zmatrix[:,1]=ZL
            #print("ZL is",ZL)
            #print("Z0 is",Z0)
            #print(Zmatrix)
            #print(Zmatrix.shape)
            Ntwk.renormalize(Zmatrix,s_def='power')#, powerwave=True)
        return Ntwk
    
    elif approach==3:
        # create 2-port S-matrix for the network
        S11=-Z0/(2*ZL+Z0); S22=S11; S12=2*ZL/(2*ZL+Z0); S21=S12
        S_2port=np.array([[S11, S12],[S21, S22]]).transpose(2, 0, 1)
        
        return rf.Network(frequency = Band, s = S_2port, z0=Z0)
    
'''
OLD Function to create a network object for a filter bank with an arbitrary # of 
channels, reorder the ports to the standard filter bank convention, and 
optionally plot the thru power and power absorbed by each channel. User input 
determines whether or not to plot, plot title, start/stop frequency, whether or
not to save, and file name.

Arguments: freq. band, design data for all channels, char. impedance, ind. of 
refrac., physical separation between channels. 
Returns: filter bank network object with correctly ordered ports

Notes: Physical separation refers to the wavelength corresponding to the resonant
frequency of left channel in each pair of channels.
'''
def FilterBank(Band, Data, Z0=50.0, n=1.0, physSep = 0.25, approach=3, doPlot=False):
    v = c/n
    # initialize current network to the first spectral channel
    CurrentNtwk = SpectralChannel3PortNetwork(Band, Z0, Data[0,0], Data[1,0], Data[2,0], approach)
        
    # loop to create filter bank with arbitrary # of channels and create network
    for i in range(np.shape(Data)[1]):
        if i < np.shape(Data)[1]-1:
            # resonant frequencies and quality factors for current and next SCs
            fres_current = Data[0,i]    
            fres_nxt = Data[0,i+1]; Qc_nxt = Data[1,i+1]; Qi_nxt = Data[2,i+1]
            
            # create Network object for next SC
            NextSC = SpectralChannel3PortNetwork(Band, Z0, fres_nxt, Qc_nxt, Qi_nxt, approach)
            
            # create interconnecting transmission line
            lambda_current = v/fres_current
            # lambda_nxt = v/fres_nxt
            lineLength = physSep*lambda_current
            # lineLength = physSep*(lambda_current+lambda_nxt)/2.0
            TLine = TransmissionLine(Band, lineLength, Z0, n)
            
            # connect current network to the transmission line
            N = CurrentNtwk.nports
            InterNtwk = rf.connect(CurrentNtwk, N-1, TLine, 0)
            
            # connect current network to the next SC
            N = InterNtwk.nports
            CurrentNtwk = rf.connect(InterNtwk, N-1, NextSC, 0)
    
    # for 3-port approach, reorder port numbers so S10 is thru & channels are in order from 2 to N-1
#    if approach==2:
#        N = CurrentNtwk.nports    
#        OldS = CurrentNtwk.s
#        NewS = np.empty([len(Band), N, N], dtype=complex)
#        NewS[:,0,0]=OldS[:,0,0]; NewS[:,0,N-1]=OldS[:,0,N-1]
#        NewS[:,N-1,0]=OldS[:,N-1,0]; NewS[:,N-1,N-1]=OldS[:,N-1,N-1];
#        
#        # ugly numerology code
#        for l in range(N):
#            for k in range(N):
#                if l==0 or l==N-1:
#                    if k in range(1,N-2):
#                        NewS[:,k+1,l]=OldS[:,k,l]
#                    elif k==N-2:
#                        NewS[:,1,l]=OldS[:,k,l]
#                elif l==N-2:
#                    if k in range(1,N-2):
#                        NewS[:,k+1,1]=OldS[:,k,l]
#                    elif k==0:
#                        NewS[:,k,1]=OldS[:,k,l]
#                    elif k==N-2:
#                        NewS[:,1,1]=OldS[:,k,l]
#                elif l in range(1,N-2):
#                    if k in range(1,N-2):
#                        NewS[:,k+1,l+1]=OldS[:,k,l]
#                    elif k==0:
#                        NewS[:,k,l+1]=OldS[:,k,l]
#                    elif k==N-2:
#                        NewS[:,1,l+1]=OldS[:,k,l]
#                    elif k==N-1:
#                        NewS[:,k,l+1]=OldS[:,k,l]
#                        
#        # create a new network with the correct port order to represent the filter bank
#        CurrentNtwk = rf.Network(frequency = Band, s = NewS, z0 = CurrentNtwk.z0)     
    
    # code to do plotting if doPlot is True      
    if doPlot:
        # full filter bank S-Matrix with correct port ordering
        nPorts = CurrentNtwk.number_of_ports
        
        # readout and plot reflected, thru, and each individual channel
#        PowerS = np.empty([len(Band), nPorts], dtype=complex)
#        PowerS[:,0] = CurrentNtwk.s[:,0,0]; PowerS[:,1] = CurrentNtwk.s[:,nPorts-2,0]
        
        # plots for arbitrary number of channels
        plt.figure(1); plt.clf()
        plt.rc('legend', fontsize = 12)
#        plt.plot(Band.f/1.0e9, np.conj(PowerS[:,1])*PowerS[:,1], linewidth = '2', 
#                 label = 'Thru')
        plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,1,0])*CurrentNtwk.s[:,1,0], linewidth = '2', 
                 label = 'Thru')
        plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,0,0])*CurrentNtwk.s[:,0,0], linewidth = '2', 
                 label = 'Reflected')
        
        # plot absorbed powers if using 3-port approach for spectral channels
        if approach == 2:
            # if there are 5 or less channels, each channel is different color
            if np.shape(Data)[1] <= 5:        
                for i in range(2, nPorts-1):
                    # PowerS[:,i]=CurrentNtwk.s[:,i-1,0]
                    plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,i,0])*CurrentNtwk.s[:,i,0], '--', linewidth = '2', 
                             label = 'Ch ' + str(i-1))
                # PowerS[:,nPorts-1] = CurrentNtwk.s[:,nPorts-1,0]
                plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,nPorts-1,0])*CurrentNtwk.s[:,nPorts-1,0], '--', linewidth = '2', 
                         label = 'Ch ' + str(nPorts-2))
                         
            # otherwise plot all channels in black with no legend entries
            else:
                for i in range(2, nPorts-1):
                    # PowerS[:,i]=CurrentNtwk.s[:,i-1,0]
                    plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,i,0])*CurrentNtwk.s[:,i,0], 'k:', linewidth = '3')
    
                #PowerS[:,nPorts-1] = CurrentNtwk.s[:,nPorts-1,0]
                plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,nPorts-1,0])*CurrentNtwk.s[:,nPorts-1,0], 'k:', linewidth = '3')
        
        # prompt user to enter plot title and start/stop frequencies
        plotTitle = raw_input('What would you like to title your plot? ')
        start = raw_input('Start frequency (GHz): ')
        stop = raw_input('Stop frequency (GHz): ')
        
        plt.title(plotTitle)
        plt.legend(loc='best')
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Power')
        plt.xlim(float(start), float(stop))
        plt.ylim(0, 1)
        plt.ion()
        plt.show()
        
        # prompt user about whether or not to save plot
        while True:
            isSave = raw_input('Would you like to save the plot? Y or N ')
            if isSave in ('y', 'n', 'Y', 'N'):
                break
            else:
                print("""You must enter 'Y' or 'N'! """)
        
        # if yes, prompt for file name and save as .png file
        if isSave in ('y', 'Y'):
            plotFileName = raw_input('What name would you like to save your plot as? ')
            plt.savefig('PythonPlots/' + plotFileName + '.png') 
    return CurrentNtwk

'''
Function to create an unterminated network object for a filter bank with an 
arbitrary # of channels taking into account possible dielectric loss and 
optionally plot the reflected power, thru power, and power absorbed by each 
channel. User input determines whether or not to plot, plot title, start/stop 
frequency, whether or not to save, and file name.

Arguments: freq. band, design data for all channels, char. impedance, 
propagation speed on feedline, physical separation between channels (in 
wavelengths), transmission line attenuation, spectral channel approach, to plot
or not to plot. 
Returns: filter bank network object

Notes: Physical separation refers to the wavelength corresponding to the resonant
frequency of left channel in each pair of channels.
'''
def FilterBankLossy(Band, Data, Z0=50.0, v=c, physSep=0.25, epsr=11.7, lossTan=0.0, approach=3,processors = 1, doPlot=False):
    
    # initialize current network to the first spectral channel
    net_dict = {}
    CurrentNtwk = SpectralChannelLossy(Band, Z0, Data[0,0], Data[1,0], Data[2,0], Data[3,0], approach)
    net_dict['net0'] = CurrentNtwk
    then = time.time()    
    # loop to create filter bank with arbitrary # of channels and create network
    for i in range(np.shape(Data)[1]):
        if i < np.shape(Data)[1]-1:
            # resonant frequencies and quality factors for current and next SCs
            fres_current = Data[0,i]    
            fres_nxt = Data[0,i+1]; Qc_nxt = Data[1,i+1]; Qdet_nxt = Data[2,i+1]; Qloss_nxt = Data[3,i+1]
            
            # create Network object for next SC
            #NextSC = SpectralChannelLossy(Band, Z0, fres_nxt, Qc_nxt, Qdet_nxt, Qloss_nxt, approach)
            NextSC = connect_spectral_and_Tline(Band, Z0, fres_nxt, Qc_nxt, Qdet_nxt, Qloss_nxt, approach,v,physSep,epsr)
            net_dict['net'+str(i+1)] = NextSC
            # connect current network to the transmission line
            #N = CurrentNtwk.nports
            #CurrentNtwk = rf.connect(CurrentNtwk, N-1, NextSC, 0)
    print(time.time() -then)
    #print(len(net_dict.keys()))
    then = time.time()                    
    fast_net = connect_net_dict_multi(net_dict,processors = processors)
    #CurrentNtwk = fast_net[0] #uncomment for parrallel processsing
    #print(fast_net.keys())
    CurrentNtwk = fast_net['net0']
    #print(CurrentNtwk.nports)
    #print(CurrentNtwk.f)
    print(time.time() -then)
    then = time.time()    
    # renormalize the ports out here becuase it is faster that doing for each spectral channel individually
    Zmatrix = np.empty([len(Band.f),CurrentNtwk.nports], dtype=complex)
    Zmatrix[:,CurrentNtwk.nports-1]=Z0
    Zmatrix[:,0]=Z0
    for i in range(1,CurrentNtwk.nports-1):
        x = (Band.f-Data[0,i-1])/Data[0,i-1]
        ZL = Z0/2*Data[1,i-1]*(1/Data[2,i-1]+1/Data[3,i-1])+1j*Z0*Data[1,i-1]*x
        Zmatrix[:,i]=ZL
    print(Zmatrix.shape)
    CurrentNtwk.renormalize(Zmatrix,s_def='power')#, powerwave=True)
    print(time.time() -then)
            
    # code to do plotting if doPlot is True      
    if doPlot:
        # full filter bank S-Matrix with correct port ordering
        nPorts = CurrentNtwk.number_of_ports
        
        # plots for arbitrary number of channels
        plt.figure(1); plt.clf()
        plt.rc('legend', fontsize = 12)

        plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,nPorts-1,0])*CurrentNtwk.s[:,nPorts-1,0], linewidth = '2', 
                 label = 'Thru')
        plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,0,0])*CurrentNtwk.s[:,0,0], linewidth = '2', 
                 label = 'Reflected')
        
        # plot absorbed powers if using 3-port approach for spectral channels
        if approach == 2:
            # if there are 5 or less channels, each channel is different color
            if np.shape(Data)[1] <= 5:        
                for i in range(1, nPorts-1):
                    # PowerS[:,i]=CurrentNtwk.s[:,i-1,0]
                    plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,i,0])*CurrentNtwk.s[:,i,0], '--', linewidth = '2', 
                             label = 'Ch ' + str(i-1))
                # PowerS[:,nPorts-1] = CurrentNtwk.s[:,nPorts-1,0]
                plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,nPorts-1,0])*CurrentNtwk.s[:,nPorts-1,0], '--', linewidth = '2', 
                         label = 'Ch ' + str(nPorts-2))
                         
            # otherwise plot all channels in black with no legend entries
            else:
                for i in range(1, nPorts-1):
                    # PowerS[:,i]=CurrentNtwk.s[:,i-1,0]
                    plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,i,0])*CurrentNtwk.s[:,i,0], 'k:', linewidth = '3')
    
                #PowerS[:,nPorts-1] = CurrentNtwk.s[:,nPorts-1,0]
                plt.plot(Band.f/1.0e9, np.conj(CurrentNtwk.s[:,nPorts-1,0])*CurrentNtwk.s[:,nPorts-1,0], 'k:', linewidth = '3')
        
        # prompt user to enter plot title and start/stop frequencies
        plotTitle = raw_input('What would you like to title your plot? ')
        start = raw_input('Start frequency (GHz): ')
        stop = raw_input('Stop frequency (GHz): ')
        
        plt.title(plotTitle)
        plt.legend(loc='best')
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Power')
        plt.xlim(float(start), float(stop))
        plt.ylim(0, 1)
        plt.ion()
        plt.show()
        
        # prompt user about whether or not to save plot
        while True:
            isSave = raw_input('Would you like to save the plot? Y or N ')
            if isSave in ('y', 'n', 'Y', 'N'):
                break
            else:
                print("""You must enter 'Y' or 'N'! """)
        
        # if yes, prompt for file name and save as .png file
        if isSave in ('y', 'Y'):
            plotFileName = raw_input('What name would you like to save your plot as? ')
            plt.savefig('PythonPlots/' + plotFileName + '.png') 
    return CurrentNtwk

'''
Function to create a network object for a filter bank terminated in an arbitrary
load. Also connects length of transmission line between the final channel and
termination.

Arguments: same as for FilterBank + length of line preceding filter bank, length of line after filter bank, impedance of
termination

Returns: terminated filter bank network object
'''
def TerminatedFilterBank(Band, Data, lBack, ZT, Z0=50.0, n=1.0, physSep=0.25, approachFB=3, approachT=1):
    UnterminatedFB = FilterBank(Band, Data, Z0, n, physSep, approachFB)
    
    # transmission line between final channel and termination
    TLine = TransmissionLine(Band, lBack, Z0, n)

    # convert Z-matrix to S-matrix with port 2 referenced to termination impedance
    # resulting in a 2-port Ntwk; used for computing response of BB detector after
    # the spectral channels; only works if SC is represented by 2-port network
    if approachT==1:
        # 2-port network with FB connected to end transmission line
        InterNtwk = rf.connect(UnterminatedFB, 1, TLine, 0)
        Z01=Z0*np.ones(Band.npoints) # InterNtwk port 1 ref. impedance
        Z02=ZT*np.ones(Band.npoints) # InterNtwk port 2 ref. impedance
        Z0Matrix=np.vstack((Z01, Z02)).transpose(1,0)
        TermS=Z2S(InterNtwk.z, Z01, Z02)
        Ntwk=rf.Network(frequency=Band, s=TermS, z0=Z0Matrix)
        
    # create 1-port network for termination and connect to unterminated FB resulting
    # in a 1-port Ntwk
    elif approachT==2:
        # create 1-port S-matrix for the termination
        S11_T=(ZT*np.ones(Band.npoints)-Z0)/(ZT*np.ones(Band.npoints)+Z0)
        Term=rf.Network(frequency=Band, s=S11_T, z0=Z0)
        
        # 3-port representation of spectral channels
        if approachFB==2:
            InterNtwk = rf.connect(UnterminatedFB, UnterminatedFB.nports-1, TLine, 0)
            # terminate filter bank
            Ntwk = rf.connect(InterNtwk, InterNtwk.nports-1, Term, 0)
            
        # 2-port representation of spectral channels
        elif approachFB==3:
            InterNtwk = rf.connect(UnterminatedFB, 1, TLine, 0)
            # terminate filter bank
            Ntwk = rf.connect(InterNtwk, 1, Term, 0)
    
    return Ntwk

'''
Function to create a network object for a filter bank terminated in an arbitrary
load taking in account possible dielectric loss. Also connects length of 
transmission line between the final channel and termination.

Arguments: same as for FilterBankLossy + 
length of line after filter bank, impedance of termination

Returns: terminated filter bank network object
'''
def TerminatedFilterBankLossy(Band, Data, lBack, ZT, Z0=50.0, v=c, physSep=0.25, epsr=11.7, lossTan=0.0, approachFB=3, approachT=1):
    UnterminatedFB = FilterBankLossy(Band, Data, Z0, v, physSep, epsr, lossTan, approachFB)

    # transmission line between final channel and termination
    TLine = TransmissionLineLossy(Band, lBack, Z0, v, epsr, lossTan)

    # convert Z-matrix to S-matrix with port 2 referenced to termination impedance
    # resulting in a 2-port Ntwk; used for computing response of BB detector after
    # the spectral channels; only works if SC is represented by 2-port network
    if approachT==1:
        # 2-port network with FB connected to end transmission line
        InterNtwk = rf.connect(UnterminatedFB, 1, TLine, 0)
        Z01=Z0*np.ones(Band.npoints) # InterNtwk port 1 ref. impedance
        Z02=ZT*np.ones(Band.npoints) # InterNtwk port 2 ref. impedance
        Z0Matrix=np.vstack((Z01, Z02)).transpose(1,0)
        TermS=Z2S(InterNtwk.z, Z01, Z02)
        Ntwk=rf.Network(frequency=Band, s=TermS, z0=Z0Matrix)
        
    # create 1-port network for termination and connect to unterminated FB resulting
    # in a 1-port Ntwk
    elif approachT==2:
        # create 1-port S-matrix for the termination
        S11_T=(ZT*np.ones(Band.npoints)-Z0)/(ZT*np.ones(Band.npoints)+Z0)
        Term=rf.Network(frequency=Band, s=S11_T, z0=Z0)
        
        # 3-port representation of spectral channels
        if approachFB==2:
            InterNtwk = rf.connect(UnterminatedFB, UnterminatedFB.nports-1, TLine, 0)
            # terminate filter bank
            Ntwk = rf.connect(InterNtwk, InterNtwk.nports-1, Term, 0)
            
        # 2-port representation of spectral channels
        elif approachFB==3:
            InterNtwk = rf.connect(UnterminatedFB, 1, TLine, 0)
            # terminate filter bank
            Ntwk = rf.connect(InterNtwk, 1, Term, 0)
    
    return Ntwk

'''
Function to create a network object for a filter bank terminated in an arbitrary
load taking in account possible dielectric loss. Also connects length of 
transmission line between the final channel and termination. Used to
calculate response of BB1, a broadband absorber placed before the spectral channels.

Arguments: same as for FilterBankLossy + 
length of line after filter bank, impedance of termination

Returns: terminated filter bank network object
'''
def TerminatedFBLossyEnd(Band, Data, lBack, ZT, Z0=50.0, v=c, physSep=0.25, epsr=11.7, lossTan=0.0, approachFB=3, approachT=1):
    UnterminatedFB = FilterBankLossy(Band, Data, Z0, v, physSep, epsr, lossTan, approachFB)

    # transmission line between final channel and termination
    TLine = TransmissionLineLossy(Band, lBack, Z0, v, epsr, lossTan)

    # convert Z-matrix to S-matrix with port 2 referenced to termination impedance
    # resulting in a 2-port Ntwk; used for computing response of BB detector after
    # the spectral channels; only works if SC is represented by 2-port network
    if approachT==1:
        # 2-port network with FB connected to end transmission line
        InterNtwk = rf.connect(UnterminatedFB, 1, TLine, 0)
        Z01=Z0*np.ones(Band.npoints) # InterNtwk port 1 ref. impedance
        Z02=ZT*np.ones(Band.npoints) # InterNtwk port 2 ref. impedance
        Z0Matrix=np.vstack((Z01, Z02)).transpose(1,0)
        TermS=Z2S(InterNtwk.z, Z01, Z02)
        Ntwk=rf.Network(frequency=Band, s=TermS, z0=Z0Matrix)
        
    # create 1-port network for termination and connect to unterminated FB resulting
    # in a 1-port Ntwk
    elif approachT==2:
        # create 1-port S-matrix for the termination
        S11_T=(ZT*np.ones(Band.npoints)-Z0)/(ZT*np.ones(Band.npoints)+Z0)
        Term=rf.Network(frequency=Band, s=S11_T, z0=Z0)
        
        # 3-port representation of spectral channels
        if approachFB==2:
            InterNtwk = rf.connect(UnterminatedFB, UnterminatedFB.nports-1, TLine, 0)
            # terminate filter bank
            Ntwk = rf.connect(InterNtwk, InterNtwk.nports-1, Term, 0)
            
        # 2-port representation of spectral channels
        elif approachFB==3:
            InterNtwk = rf.connect(UnterminatedFB, 1, TLine, 0)
            # terminate filter bank
            Ntwk = rf.connect(InterNtwk, 1, Term, 0)
            
    # same as approachT = 1, but using renormalize function instead of converting
    # between S and Z parameters
    elif approachT==3:
        Ntwk = rf.connect(UnterminatedFB, UnterminatedFB.nports-1, TLine, 0)
            
        NewPortZ = np.empty([Band.npoints, Ntwk.nports], dtype=complex)
        NewPortZ[:,Ntwk.nports-1]=ZT
        for i in range(0, Ntwk.nports-1):
            NewPortZ[:,i] = Ntwk.z0[:,i]
        Ntwk.renormalize(NewPortZ)
    return Ntwk

'''
Function to create a network object for a filter bank preceeded by an antenna
with arbitrary impedance taking into account possible dielectric loss. Also connects 
length of transmission line between the antenna and first channel. Used to
calculate response of BB2, a broadband absorber placed after the spectral channels.

Arguments: same as for FilterBankLossy + length of line preceding filter bank, 
impedance of antenna

Returns: terminated filter bank network object
'''
def TerminatedFBLossyBegin(Band, Data, lFront, ZA, Z0=50.0, v=c, physSep=0.25, epsr=11.7, lossTan=0.0, approachFB=3, approachT=1):
    UnterminatedFB = FilterBankLossy(Band, Data, Z0, v, physSep, epsr, lossTan, approachFB)

    # transmission line between antenna and first channel
    TLine = TransmissionLineLossy(Band, lFront, Z0, v, epsr, lossTan)

    # convert Z-matrix to S-matrix with port 2 referenced to termination impedance
    # resulting in a 2-port Ntwk; used for computing response of BB detector after
    # the spectral channels; only works if SC is represented by 2-port network
    if approachT==1:
        # 2-port network with FB connected to end transmission line
        InterNtwk = rf.connect(TLine, 1, UnterminatedFB, 0)
        Z01=ZA*np.ones(Band.npoints) # InterNtwk port 1 ref. impedance
        Z02=Z0*np.ones(Band.npoints) # InterNtwk port 2 ref. impedance
        Z0Matrix=np.vstack((Z01, Z02)).transpose(1,0)
        TermS=Z2S(InterNtwk.z, Z01, Z02)
        Ntwk=rf.Network(frequency=Band, s=TermS, z0=Z0Matrix)
        
    # same as approachT = 1, but using renormalize instead of converting between
    # S and Z parameters. If using 3-port SC representation, the through S-parameter
    # is S[nports-1,0]
    elif approachT==2:
        # for 2-port and 3-port representations of spectral channels
        Ntwk = rf.connect(TLine, 1, UnterminatedFB, 0)
        NewPortZ = np.empty([Band.npoints, Ntwk.nports], dtype=complex)
        NewPortZ[:,0]=ZA
        for i in range(1, Ntwk.nports):
            NewPortZ[:,i] = Ntwk.z0[:,i]
        Ntwk.renormalize(NewPortZ)
    return Ntwk

'''
Function to create a network object for a filter bank preceeded by an antenna
with arbitrary impedance AND terminated in an arbitrary load taking into account 
possible dielectric loss. Lengths of transmission line connect antenna to first
channel and final channel to termination. Used to calculate response of each 
spectral channel under realistic input and output port termination conditions.

Arguments: same as for FilterBankLossy + length of line preceding filter bank, 
impedance of antenna, length of line following filter bank, impedance of
termination

Returns: terminated filter bank network object
'''
def TerminatedFBLossyBoth(Band, Data, lFront, lBack, ZA, ZT, Z0=50.0, v=c, physSep=0.25, epsr=11.7, lossTan=0.0, approachFB=3, approachT=1,processors = 1):
    
    UnterminatedFB = FilterBankLossy(Band, Data, Z0, v, physSep, epsr, lossTan, approachFB, processors)
    

    # transmission line between antenna and first channel
    TLineBegin = TransmissionLineLossy(Band, lFront, Z0, v, epsr, lossTan)
    # transmission line between final channel and termination
    TLineEnd = TransmissionLineLossy(Band, lBack, Z0, v, epsr, lossTan)
    
    # convert Z-matrix to S-matrix with port 2 referenced to termination impedance
    # resulting in a 2-port Ntwk; only works if SC is represented by 2-port network
    if approachT==1:
        # 2-port network with FB connected to end transmission line
        InterNtwk1 = rf.connect(TLineBegin, 1, UnterminatedFB, 0)
        InterNtwk2 = rf.connect(InterNtwk1, 1, TLineEnd, 0)
        Z01=ZA*np.ones(Band.npoints) # InterNtwk port 1 ref. impedance
        Z02=ZT*np.ones(Band.npoints) # InterNtwk port 2 ref. impedance
        Z0Matrix=np.vstack((Z01, Z02)).transpose(1,0)
        TermS=Z2S(InterNtwk2.z, Z01, Z02)
        Ntwk=rf.Network(frequency=Band, s=TermS, z0=Z0Matrix)
        
    # same as approachT = 1, but using renormalize instead of converting between
    # S and Z parameters. If using 3-port SC representation, the through S-parameter
    # is S[nports-1,0]
    elif approachT==2:
        # for 2-port and 3-port representations of spectral channels
        InterNtwk = rf.connect(TLineBegin, 1, UnterminatedFB, 0)
        Ntwk = rf.connect(InterNtwk, InterNtwk.nports-1, TLineEnd, 0)
        
        NewPortZ = np.empty([Band.npoints, Ntwk.nports], dtype=complex)
        NewPortZ[:,0]=ZA
        NewPortZ[:,Ntwk.nports-1]=ZT
        for i in range(1, Ntwk.nports-1):
            NewPortZ[:,i] = Ntwk.z0[:,i]
        Ntwk.renormalize(NewPortZ)
    
    return Ntwk

'''
Function to calculate response of BB1, a broadband absorber placed inline with 
the transmission line in front of a terminated filter bank.

Arguments: coupling constant of BB1, frequency band, transmission line length, 
coupling length, center position, characteristic impedance of transmission line, 
antenna impedance, propagation speed on transmission line, dielectric constant, 
loss tangent of dielectric layer, reflection coefficient at input of terminated 
filter bank (assuming matched impedance), approach (1 normalizes response to V 
at antenna, 2 normalizes response to V after antenna)

Returns: an array of BB1 response at each frequency point in the band
'''
def BroadbandChannelBefore(epsilon1, Band, lLine, lCoupling, zc, Z0, ZA, v, epsr, lossTan, GammaFB, approach=1):
    beta = 2.0*np.pi*Band.f/v # real propogation constant
    alpha = np.pi*np.sqrt(epsr)*Band.f/v*lossTan # attenuation constant in Np/m
    gamma = alpha + 1j*beta # complex propagation constant (with attenuation)
    
    # input impedance immediately after antenna looking toward termination
    Zin = Z0*(1.0+GammaFB*np.exp(-2.0*gamma*lLine))/(1.0-GammaFB*np.exp(-2.0*gamma*lLine))
    # incident voltage at end of transmission line
    V0plus = Zin/((ZA+Zin)*(np.exp(gamma*lLine)+GammaFB*np.exp(-gamma*lLine)))
    
    # power coupled to BB1 normalized to power immediately after antenna
    BB1 = epsilon1*(np.sinc(1j*alpha*lCoupling)*np.exp(-2*alpha*zc)\
                                   + 2.0*np.abs(GammaFB)*np.cos(2.0*beta*zc+np.angle(GammaFB))\
                                   *np.sinc(beta*lCoupling) + np.conj(GammaFB)*GammaFB\
                                   *np.sinc(1j*alpha*lCoupling)*np.exp(2.0*alpha*zc))
    
    # unity is Voc at antenna
    if approach==1:
        return np.conj(V0plus)*V0plus*BB1
    # unity is at end of transmission line, immediately before the first channel
    elif approach==2:
        return BB1
    
'''
Function to calculate response of BB2, a broadband absorber placed inline with 
the transmission line behind of a terminated filter bank.

Arguments: coupling constant of BB2, frequency band, coupling length, center 
position, propagation speed on transmission line, dielectric constant, 
loss tangent of dielectric layer, transmission coefficient (S21) at termination
of filter bank (filter bank object used must contain end transmission line with
load port referenced to termination impedance)

Returns: an array of BB2 response at each frequency point in the band
'''
def BroadbandChannelAfter(epsilon2, Band, lCoupling, zc, v, epsr, lossTan, TFB):
    alpha = np.pi*np.sqrt(epsr)*Band.f/v*lossTan # attenuation constant in Np/m
    
    # calculate response of BB2
    BB2 = epsilon2*np.conj(TFB)*TFB*np.sinc(1j*alpha*lCoupling)*np.exp(-2.0*alpha*zc)
    return BB2

'''
Function to calculate the response of individual channels of arbitrary filter
bank using the "adjacent subtraction method."
'''
def ChannelResponse(Band, Data, lback, ZT, Z0=50.0, n=1.0, physSep = 0.25, approachFB=3, approachT=1):
    v = c/n # wavespeed    
    # create nChannels x f array to store the response of all channels
    Response = np.empty([np.shape(Data)[1], Band.npoints], dtype=complex)
    
    # array to store aggregate response of channels up to current-1
    PreviousResponse = np.zeros(Band.npoints, dtype = complex)
    for i in range(np.shape(Data)[1]):
        # data for FB up to and including channel i and line after channel i
        DataBefore = Data[:, 0:i+1]
         
        if i<np.shape(Data)[1]-1:
            # create transmission line after channel i
            lineLength = physSep*v/DataBefore[0, i]
            TLine = TransmissionLine(Band, lineLength, Z0, n)
            # FB up to and including channel i and line after channel i
            FBBefore = rf.connect(FilterBank(Band, DataBefore, Z0, n, physSep, approachFB), 1, TLine, 0)            
            
            # create FB of the remaining channels
            DataAfter = Data[:, i+1:np.shape(Data)[1]]
            FBAfter = TerminatedFilterBank(Band, DataAfter, lback, ZT, Z0, n, physSep, approachFB)
            
            # input impedance looking toward load at port 1 of FBAfter
            ZinAfter = Z0*(1.0+FBAfter.s[:,0,0])/(1.0-FBAfter.s[:,0,0])
        else:
            # transmission line after final channel before termination
            TLine = TransmissionLine(Band, lback, Z0, n)
            FBBefore = rf.connect(FilterBank(Band, DataBefore, Z0, n, physSep, approachFB), 1, TLine, 0)
            ZinAfter = ZT*np.ones(Band.npoints)
        
        # port reference impedances for FBBefore
        Z01 = Z0*np.ones(Band.npoints)
        Z02 = ZinAfter
        
        # convert to S-parameters with port 2 referenced to ZinAfter
        S11 = Z2S(FBBefore.z, Z01, Z02)[:,0,0]
        S21 = Z2S(FBBefore.z, Z01, Z02)[:,1,0]
        
        # aggregate response of channels up to and including channel i
        CurrentResponse = 1.0-np.conj(S11)*S11-np.conj(S21)*S21
        
        # calculate channel i response and store in Response
        CurChannelResponse = CurrentResponse-PreviousResponse
        Response[i,:]=CurChannelResponse
        
        PreviousResponse = CurrentResponse
    
    return Response
    
'''
Function to calculate the channel center frequencies of a band.

Arguments: lowest frequency, highest frequency, spectral resolution, 
oversampling ratio
Returns: # of channels, array of channel frequencies
'''
def ChannelFrequencies(fl, fu, R, Sigma):
    Nc = np.int(np.floor(Sigma*R*np.log(fu/fl)))  # number of channels, rounded down
    # print(Nc)
    x = np.exp(-(np.log(fu)-np.log(fl))/(Nc-1)) # frequency scaling of channels
    Channels = np.ones(Nc) # array to hold all the spectral channel frequencies
    Channels[0] = fu # initialize the first channel    
    for i in range(1, Nc):
        Channels[i]=x*Channels[i-1]
    return Nc, Channels
    
'''
Function to calculate S11 and S21 of an isolated channel.

Arguments: freq. band, coupling Q, internal Q
Returns: S11, S21 as a tuple.
'''
def IsolatedChannel(Band, fres, Qc, Qi):
    Qr = 1.0/(1.0/Qi+1.0/Qc)
    x = (Band.f-fres)/fres
    S21 = 1.0-(Qr/Qc)/(1.0+2.0j*Qr*x)
    S11 = S21-1.0
    return np.array([S11, S21])

#makeing spectral line and Tline one function since they are never apart
def connect_spectral_and_Tline(Band, Z0, fres_nxt, Qc_nxt, Qdet_nxt, Qloss_nxt, approach,v,physSep,epsr):
    NextSC = SpectralChannelLossy(Band, Z0, fres_nxt, Qc_nxt, Qdet_nxt, Qloss_nxt, approach,normalize = False)      
    # create interconnecting transmission line
    lambda_current = v/fres_nxt
    # lambda_nxt = v/fres_nxt
    lineLength = physSep*lambda_current
    # lineLength = physSep*(lambda_current+lambda_nxt)/2.0
    TLine = TransmissionLineLossy(Band, lineLength, Z0, v, epsr, 1/Qloss_nxt) 
    # connect Tline to spectral channel
    Ntwk = rf.connect(TLine, 1, NextSC, 0)
    return Ntwk


#define functions for multiprocessing
net_dict_global = {}
def connect_two(net1,net2):
    #print(net_dict_global)
    N = net_dict_global['net0'].nports
    net = rf.connect(net_dict_global['net'+str(net1)],N-1,net_dict_global['net'+str(net2)],0)
    return net
def multi_run_wrapper(args):
    return connect_two(*args)    
        
# function for connecting up the filter bank using multiple processors
# conncts them up in a pyrmid type fashion
# i.e. connects the nearest neighbers in the filter bank the repeats until there is just
# one network left unfortunaly the most time intensive network connctions are still just
# handeled with one processor.
# visually it looks like this
# N    N    N    N    N    N    N    N    N    N    N    N    N    N    N    N    N    N  
# |____|    |____|    |____|    |____|    |____|    |____|    |____|    |____|    |____|  could use 9 processors
#    N         N         N         N         N         N         N         N         N    
#    |_________|         |_________|         |_________|         |_________|         |    use 4 processsors
#         N                   N                   N                   N              N
#         |___________________|                   |___________________|              |    use 2 processors
#                   N                                       N                        N
#                   |_______________________________________|                        |    use 1 processor
#                                       N                                            N
#                                       |____________________________________________|    use 1 processor
#                                                                 N

'''
def connect_net_dict_multi(net_dict,processors):
    print(processors)
    global net_dict_global #probably bad coding edicate but it works
    net_dict_global = net_dict 
    len_networks = 10 #intilize while condition to get into the loop
    while len_networks>1: #while there is more that one network to be stiched together

        tot_networks = len(net_dict_global.keys())
        #print("tot_netorks", tot_networks)
        #make the list of indicies to connect
        connect_list = []
        if np.mod(tot_networks,2) == 0: #if even connect them all
            for i in range(0,tot_networks,2):
                connect_list.append((i,i+1))
        else: #if odd leave a straggler
            for i in range(0,tot_networks-1,2):
                connect_list.append((i,i+1))
        print(connect_list)
        pool = Pool(processes=processors) #intialize multiprocesssing pool
        result = pool.map(multi_run_wrapper, connect_list) #do the multiprocessing connecting
        pool.close() #close open files
        # put the results into a dictionary
        new_dict = {}
        len_result = len(result)
        #print("len_result", len_result)
        for i in range(0,len_result):
            new_dict['net'+str(i)] = result[i]
        if np.mod(tot_networks,2) == 1:
            new_dict['net'+str(i+1)] = net_dict_global['net'+str(tot_networks -1)]
        net_dict_global = new_dict
        len_networks = len(new_dict.keys())
        #print("assem",len(new_dict.keys()))
    return result
'''

def connect_net_dict_multi(net_dict,processors):
    #print(processors)
    global net_dict_global #probably bad coding edicate but it works
    net_dict_global = net_dict 
    len_networks = 10 #intilize while condition to get into the loop
    while len_networks>1: #while there is more that one network to be stiched together

        tot_networks = len(net_dict_global.keys())
        #print("tot_netorks", tot_networks)
        #make the list of indicies to connect
        connect_list = []
        if np.mod(tot_networks,2) == 0: #if even connect them all
            for i in range(0,tot_networks,2):
                connect_list.append((i,i+1))
        else: #if odd leave a straggler
            for i in range(0,tot_networks-1,2):
                connect_list.append((i,i+1))
        #print(connect_list)
        #print(len(connect_list))
        #pool = Pool(processes=processors) #intialize multiprocesssing pool #currently not using multiple processors but still connecting in pyramid fashion
        new_dict = {}
        N = net_dict_global['net0'].nports
        for i in range(0,len(connect_list)):
            #print("fast")
            result =  rf.connect(net_dict_global['net'+str(connect_list[i][0])],N-1,net_dict_global['net'+str(connect_list[i][1])],0)
            new_dict['net'+str(i)] = result
        if np.mod(tot_networks,2) == 1:
            new_dict['net'+str(i+1)] = net_dict_global['net'+str(tot_networks -1)]
        #result = pool.map(multi_run_wrapper, connect_list) #do the multiprocessing connecting
        #pool.close() #close open files
        # put the results into a dictionary
        len_result = len(result)
        #print("len_result", len_result)
        net_dict_global = new_dict
        len_networks = len(new_dict.keys())
        #print("assem",len(new_dict.keys()))
    return net_dict_global

