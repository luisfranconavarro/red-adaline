import matplotlib.pyplot as plt   
import numpy as np
from matplotlib.widgets import Button
from matplotlib.widgets import Cursor
from matplotlib.backend_bases import MouseButton
from matplotlib.lines import Line2D


def onclick(event):
    if event.xdata != None and event.y > 37:
        xy = []
        colorP = ""
        print("posicion y:",event.y)
        
        xy.append(1)
        xy.append(event.xdata)
        xy.append(event.ydata)
        entradas.append(xy)
        
        if event.button is MouseButton.LEFT:
            print('click izquierdo')
            colorP = "r"
            salEsperada.append(1)
            entradasRojas.append(xy)
            
        if event.button is MouseButton.RIGHT:
            print('click derecho')
            colorP = "g"
            salEsperada.append(0)
            entradasVerdes.append(xy)
            
        ax.plot(xy[1], xy[2], "o", color = colorP)
        plt.draw()
        print("puntos: ",len(entradas))


def nuevosPesos(datos, pesos, error, y):
        #w[i] = w[i] + eta*x[i]*e
        eta = 0.4
        pesosNuevos = []
        for i in range(len(pesos)):
            pesosNuevos.append(pesos[i] + eta * error * datos[i] * y * (1 - y))
        #print("pesos nuevos: ",pesosNuevos)
        return pesosNuevos
    
def entrenar(self):  
    
    pesos = []
    umbral = -1.5
    pesos.append(umbral)
    pesos.append(0.3)
    pesos.append(0.3)
    
    tolerancia = 0.1
    promedio = 1
    
    fig.canvas.mpl_disconnect(cid)
    
    fig1, ax = plt.subplots()#
    
    while promedio > tolerancia:
        
        pos = 0    
        sumErrores = 0
        totErrores = 0
        #totalErrores = 0   
        #errores = []

        while pos < len(entradas):
            
            salida = np.dot(entradas[pos],pesos)
            salida = 1 / (1 + np.e**-salida)
            
            if salida != salEsperada[pos]:                
                error = salEsperada[pos] - salida
                pesos = nuevosPesos(entradas[pos], pesos, error, salida)
                sumErrores += error * error
                totErrores += 1
                #errores.append(error)
            pos += 1
            
        m = (-1 * pesos[1]) / pesos[2]#
        b = (pesos[0] * -1) / pesos[2]#
                
        rectaX = [-1.5, 1.5]#
        rectaY = [m * rectaX[0] + b, m * rectaX[1] + b]#
                
        auxR1 = []#
        auxR2 = []#
        auxV1 = []#
        auxV2 = []#
                
        for i in range(len(entradasRojas)):#
            for j in range(len(entradasRojas[i])):#
                if j == 1:#
                    auxR1.append(entradasRojas[i][j])#
                if j == 2:#
                    auxR2.append(entradasRojas[i][j])#
                            
        for i in range(len(entradasVerdes)):#
            for j in range(len(entradasVerdes[i])):#
                if j == 1:#
                    auxV1.append(entradasVerdes[i][j])#
                if j == 2:#
                    auxV2.append(entradasVerdes[i][j])#
                            
        ax.set(xlim = (-.5, 1.5), ylim = (-.5, 1.5))
        plt.ylabel("y")
        plt.xlabel("x")
        plt.title("Entrenamiento", fontsize = 20, color = "blue")
        plt.plot(auxR1, auxR2, "ro", auxV1, auxV2, "go", rectaX, rectaY, "b-")
        plt.draw()
        plt.pause(.1)
        plt.clf()    
        
        """for i in range(len(errores)):
            f errores[i] < 0:
                totalErrores += errores[i] * -1
            else:
                totalErrores += errores[i] 
            totalErrores += errores[i] * errores[i]
        promedio = totalErrores / len(errores)"""
        promedio = sumErrores / totErrores
        print(promedio)
            
            
    m = (-1 * pesos[1]) / pesos[2]
    b = (pesos[0] * -1) / pesos[2]
    
    rectaX = [-1.5, 1.5]
    rectaY = [m * rectaX[0] + b, m * rectaX[1] + b]
   
    
    #lineas para crear nueva figura con el resultado del perceptron
    
    auxR1 = []
    auxR2 = []
    auxV1 = []
    auxV2 = []
    
    for i in range(len(entradasRojas)):
        for j in range(len(entradasRojas[i])):
            if j == 1:
                auxR1.append(entradasRojas[i][j])
            if j == 2:
                auxR2.append(entradasRojas[i][j])
                
    for i in range(len(entradasVerdes)):
        for j in range(len(entradasVerdes[i])):
            if j == 1:
                auxV1.append(entradasVerdes[i][j])
            if j == 2:
                auxV2.append(entradasVerdes[i][j])

         
    #fig1, ax = plt.subplots()
    ax.set(xlim = (-.5, 1.5), ylim = (-.5, 1.5))
    plt.ylabel("y")
    plt.xlabel("x")
    plt.title("Resultado del perceptron", fontsize = 20, color = "blue")
    plt.plot(auxR1, auxR2, "ro", auxV1, auxV2, "go", rectaX, rectaY, "b-")
    plt.show()
    plt.pause(.1)
    
entradas = []  
entradasRojas = []
entradasVerdes = [] 
salEsperada = [] 

legend_elements = [Line2D([0], [0],  marker='o', color='w', label='click der',
                          markerfacecolor='r', markersize=10),
                   Line2D([0], [0], marker='o', color='w', label='click izq',
                          markerfacecolor='g', markersize=10)]

fig, ax = plt.subplots()
ax.set(xlim = (-.5, 1.5), ylim = (-.5, 1.5))
ax.legend(handles=legend_elements, loc='upper left')
plt.ylabel("y")
plt.xlabel("x")
plt.title("Perceptron", fontsize = 20, color = "blue")
i = plt.axes([0.80, 0.01, 0.1, 0.075])


iniciar = Button(i, 'Iniciar', color = "cyan")
iniciar.on_clicked(entrenar)

    
cursor = Cursor(ax, useblit=True, color='black', linewidth=1)
cid = fig.canvas.mpl_connect('button_press_event', onclick)

