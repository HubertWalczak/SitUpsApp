#Projekt brzuszki
#Założeniem projektu jest wykorzystanie umiejętności pozyskanych na
#zajęciach z przetwarzania sygnałów
#w celu stworzenia prostego programu, który analizowałby poprawność
#wykonanych brzuszków poprzez przetwarzanie sygnałów
#pochodzących z czujnika inercyjnego, dokładniej z magnetometru.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, rfft
import scipy.signal as sig

def project(signal, alfa, sensitivity, time, interval):
    data = np.genfromtxt(signal, delimiter = ";", skip_header = 1)
    x = data[:,0]
    y = data[:,2]

    for i in range(len(y)):
        y[i] = -y[i] #Odwrócenie wartości, ponieważ badany kąt jest na minusie

    y_dcOut = y - y.mean() #usunięcie stałej składowej

    y_dcOut -= y_dcOut[0]

    #Zastosowanie filtru średniej ruchomej
    b = np.ones(51)/51
    y_dcOut_clear = sig.filtfilt(b, 1, y_dcOut)

    #Wyznaczenie ekstremów funckji
    y_extremum = []
    x_extremum = []
    listOfCrunches_alfa = []
    listOfCrunches_time = []
    for i in sig.argrelextrema(y_dcOut_clear, np.greater)[0]:
        y_extremum.append(y_dcOut_clear[i])
        x_extremum.append(x[i])
        if y_dcOut_clear[i] >= 20: #Wszystko powyżej 20 stopni to brzuszek
            listOfCrunches_alfa.append(y_dcOut_clear[i])
            listOfCrunches_time.append(x[i])

    #Analiza brzuszków:
    #Analiza poprawności kąta
    listOfCorrect_alfa = []
    for i in listOfCrunches_alfa:
        if i >= alfa - sensitivity and i <= alfa + sensitivity:
            listOfCorrect_alfa.append(True)
        else:
            listOfCorrect_alfa.append(False)

    numOfTrue_alfa = 0
    for i in listOfCorrect_alfa:
        if i == True:
            numOfTrue_alfa += 1

    #Analiza systematyczności
    listOfPeriod = []
    for i in range(1, len(listOfCrunches_time)):
        listOfPeriod.append(listOfCrunches_time[i] - listOfCrunches_time[i-1])

    listOfCorrect_time = [True]
    for i in listOfPeriod:
        if i >= time - interval and i <= time + interval:
            listOfCorrect_time.append(True)
        else:
            listOfCorrect_time.append(False)

    numOfTrue_time = 0
    for i in listOfCorrect_time:
        if i == True:
            numOfTrue_time += 1

    #Interfejs użytkownika
    print("Przetwarzanie sygnału natywnego...")
    plt.figure(0)
    plt.subplot(2, 2, 1)
    plt.plot(x, y) #Wykreślenie sygnału pierwotnego
    plt.xlabel("Czas [s]")
    plt.ylabel("Kąt [°]")
    plt.subplot(2, 2, 2)
    plt.plot(x, y, label = "Sygnał pierwotny")
    plt.plot(x, y_dcOut, label = "Sygnał po usunięciu stałej składowej")
    plt.legend()
    plt.xlabel("Czas [s]")
    plt.ylabel("Kąt [°]")
    plt.subplot(2, 2, 3)
    plt.plot(x, y_dcOut_clear)
    plt.xlabel("Czas [s]")
    plt.ylabel("Kąt [°]")
    plt.subplot(2, 2, 4)
    plt.plot(x, y_dcOut_clear, label = "Sygnał po filtracji")
    plt.plot(x_extremum, y_extremum, "bo", label = "Ekstrema lokalne")
    plt.legend()
    plt.xlabel("Czas [s]")
    plt.ylabel("Kąt [°]")
    print("Usunięcie stałej składowej sygnału...")
    print("Zastosowanie filtru średniej ruchomej...")
    print("Wyznaczenie ekstremów lokalnych sygnału...")
    print("Analiza poprawności wykonanego ćwiczenia...")
    print("Liczba brzuszków:", len(listOfCrunches_alfa))
    print("*******************************")
    print("Analiza poprawności kąta")
    print("Liczba poprawnych brzuszków:", numOfTrue_alfa)
    print("*******************************")
    print("Analiza systematyczności")
    print("Liczba poprawnych brzuszków:", numOfTrue_time)
    print("*******************************")
    if numOfTrue_alfa < numOfTrue_time:
        print("Liczba poprawnych brzuszków ogółem:", numOfTrue_alfa)
        print("Procent poprawnie wykonanych brzuszków:", round(numOfTrue_alfa/len(listOfCrunches_alfa)*100), "%")
    else:
        print("Liczba poprawnych brzuszków ogółem:", numOfTrue_time)
        print("Procent poprawnie wykonanych brzuszków:", round(numOfTrue_time/len(listOfCrunches_alfa)*100), "%")
    print("***********************************")
    plt.show()
    

project("orientacja_zle.csv", 40, 5, 2.0, 0.5)
project("orientacja_poprawna.csv", 40, 5, 2.0, 0.5)


    
    

