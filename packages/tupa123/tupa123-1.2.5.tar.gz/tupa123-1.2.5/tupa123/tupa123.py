import pandas as pd
import numpy as np 
import time
import matplotlib.pyplot as plt







#load data from an excel spreadsheet
def ExcelMatrix(namearq, namesheet, Lineini, Columini, columnquantity, linesquantity):
    print('Loading data...')
    df = pd.read_excel(namearq, sheet_name=namesheet, header=None)
    Matriz = df.iloc[Lineini-1:Lineini+linesquantity-1, Columini-1:Columini+columnquantity-1].values.astype(np.float64)
    print('Loading data = ok')
    return Matriz







#Make basic comparative statistics between two sets of data
def Statistics(Calculated, Targeted):
    
    numdata,numevar = Calculated.shape
    
    print('------------------------')
    print ('Statistics between predictor variables and target variables:')
    print('------------------------')
      
    for j in range(0,numevar):
        
        erroari = Calculated[:,j] - Targeted[:,j]
        erroper = (( Calculated[:,j] - Targeted[:,j] ) / Targeted[:,j])*100
        coefcorrelacao = np.corrcoef(Targeted[:,j], Calculated[:,j])[1][0]
        
        print ('Correlation coefficient, variable ' + str(j+1) +' = ' + str(coefcorrelacao))
        print('')
        print ('Mean difference, variable ' + str(j+1) +' = ' + str(np.mean(erroari)) + ' (' + str(np.mean(erroper)) + '%)')
        print('')
        print ('Standard deviation, variable ' + str(j+1) +' = ' + str(np.std(erroari)) + ' (' + str(np.std(erroper)) + '%)')
        print('')
        print ('Biggest absolute point difference, variable ' + str(j+1) +' = ' + str(np.max(abs(erroari))) + ' ('  + str(np.max(abs(erroper))) + '%)' )
        print('------------------------')







#Plot two variables ifferences in a sequential series
def PlotComparative(Calculated, Targeted):

    numdata,numevar = Calculated.shape
    eixoX = np.arange(0, numdata, dtype=int)

    for j in range(0,numevar):    
        eixoY1= Targeted[:,j]
        eixoY2= Calculated[:,j]
    
        plt.figure(figsize=(12, 5))
        plt.title('Comparison chart calculated variable vs targeted')
        plt.xlabel('Sequence of events')
        plt.ylabel('Target and predicted variable ' + str(j+1))
        plt.plot(eixoX, eixoY1, marker = '', color = 'darkblue', label='Targeted')  
        plt.plot(eixoX, eixoY2, marker = '', color = 'orangered', label='Calculated')
        plt.legend(loc = "upper left")
        plt.show()




#Plot the differences of two variables in a sequential series
def PlotComparative2(Calculated, Targeted):

    numdata,numevar = Calculated.shape
    eixoX = np.arange(0, numdata, dtype=int)

    for j in range(0,numevar):    
        eixoY1= Targeted[:,j]
        eixoY2= Calculated[:,j]
        eixoY3 = eixoY2 - eixoY1
    
        plt.figure(figsize=(12, 5))
        plt.title('Comparison chart calculated variable vs targeted')
        plt.xlabel('Sequence of events')
        plt.ylabel('Target and predicted variable ' + str(j+1))
        plt.plot(eixoX, eixoY3, marker = '', color = 'darkblue', label='Targeted')  
        plt.legend(loc = "upper left")
        plt.show()





#Plot correlation between calculated variables and objectives
def PlotCorrelation(Calculated, Targeted):

    numdata,numevar = Calculated.shape
    eixoX = np.arange(0, numdata, dtype=int)

    for j in range(0,numevar):    
        eixoY1= Targeted[:,j]
        eixoY2= Calculated[:,j]        
        coefcorrelacao = np.corrcoef(eixoY1,eixoY2)[1][0]
        plt.title('Correlation coefficient variable '+ str(j+1)+' = ' + str(coefcorrelacao))
        plt.scatter(eixoY1,eixoY2,color='blue',s=15,edgecolor='red') #grafico de correlação entre as variaveis procuradas e alvo---
        plt.xlabel('Targeted')
        plt.ylabel('Calculated')    
        plt.show()




#Plota histograma do erro %
def PlotHisto(Calculated, Targeted):

    numdata,numevar = Calculated.shape

    for j in range(0,numevar):    
        eixoY1= Targeted[:,j]
        eixoY2= Calculated[:,j]
        eixoY3 = 100*(eixoY2 - eixoY1)/eixoY1 #erro percentual 0-100%

        fig, ax = plt.subplots()
        
        desviopad = np.std(eixoY3) #devio padrão do erro
        erromedio = np.mean(eixoY3) #erro medio
        
        textstr = '\n'.join((r'$\mathrm{average}=%.2f$' % (erromedio, ),r'$\sigma=%.2f$' % (desviopad, )))

        ax.hist(eixoY3, bins=20, rwidth=0.9, color='blue', alpha=0.7, edgecolor='black')
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)

        plt.title('Percent error histogram', fontsize=15)
        plt.xlabel('Variable ' + str(j+1) + ', %', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)

        plt.show()





#Neural network 4 layers--------------------------------------------------------------------------------------------------------------------
class nnet4:

    #global variables-------------------------------------------------------------------------
    def __init__ (self, norma=2, coef=0, normout=1, nn1c=1, nn2c=5, nn3c=5, nn4c=1, rate=0.01, epochs=1000, fa2c=5, fa3c=5, fa4c=0):
        
        self.nn1c=nn1c
        self.nn2c=nn2c
        self.nn3c=nn3c
        self.nn4c=nn4c
        self.rate=rate
        self.epochs=epochs
        self.fa2c=fa2c
        self.fa3c=fa3c
        self.fa4c=fa4c
        self.norma=norma
        self.coef=coef
        self.normout=normout








    #data normalization by calculating maximums and minimums-----------------------------------------------
    def Normalize(self, data, maxiname, mininame, medianame, desvioname):          

        #=-1, standardization
        #=0, do anything
        #=1, between 0 and 1
        #=2, between -1 and 1 
        #=3, log(x+coef)
        #=4, log(x+coef)  between 0 and 1
        #=5, log(x+coef)  between -1 and 1
        #=6, log(x+coef)  and standardization

        if (self.norma>=3): 
            data = np.log(data + self.coef)
        normalized = data*1
        
        vetormax = np.max(data,0) 
        vetormin = np.min(data,0)
        vetormed = (vetormax+vetormin)/2
        media = np.mean(data,0)
        desvio = np.std(data,0)        
                                    
        if (self.norma==1) or (self.norma==4):  
            normalized = (data - vetormin) / (vetormax - vetormin)
            
        if (self.norma==2) or (self.norma==5):    
            normalized = (data - vetormed) / (vetormax - vetormed)

        if (self.norma==6) or (self.norma==-1):
            normalized = (data - media)/desvio

        np.savetxt(maxiname, vetormax)
        np.savetxt(mininame, vetormin)
        np.savetxt(medianame, media)
        np.savetxt(desvioname, desvio)
        return normalized








    #normalizing the data by entering maximums and minimums-----------------------------------------------
    def Normalize2(self, data, maxiname, mininame, medianame, desvioname):         

        vetormax = np.loadtxt(maxiname) 
        vetormin = np.loadtxt(mininame) 
        vetormed = (vetormax+vetormin)/2
        media = np.loadtxt(medianame)
        desvio = np.loadtxt(desvioname)  

        if (self.norma>=3): 
            data = np.log(data + self.coef)
        normalized = data*1
                                                
        if (self.norma==1) or (self.norma==4):  
            normalized = (data - vetormin) / (vetormax - vetormin)
            
        if (self.norma==2) or (self.norma==5):    
            normalized = (data - vetormed) / (vetormax - vetormed)                                 

        if (self.norma==6) or (self.norma==-1):
            normalized = (data - media)/desvio
            
        return normalized







    #data denormalization-------------------------------------------------------------------
    def DesNormalize(self, normalized, maxiname, mininame, medianame, desvioname):         

        vetormax = np.loadtxt(maxiname) 
        vetormin = np.loadtxt(mininame) 
        vetormed = (vetormax+vetormin)/2
        media = np.loadtxt(medianame)
        desvio = np.loadtxt(desvioname) 
        
        desnorma = normalized*1
                            
        if (self.norma==1) or (self.norma==4):  
            desnorma = normalized * (vetormax - vetormin) + vetormin
            
        if (self.norma==2) or (self.norma==5):  
            desnorma = normalized * (vetormax - vetormed) + vetormed

        if (self.norma==6) or (self.norma==-1):          
            desnorma = normalized*desvio + media

        if (self.norma>=3): 
            desnorma = np.exp(desnorma) - self.coef
                               
        return desnorma








    #Definition of activation functions---------------------------------------------------------
    def Activation(self, typee, x):

        if (typee==0): #linear (-inf,inf)
            y = x
            return y
    
        if (typee==1): #Sigmoide (0,1)
            y = 1/(1+np.exp(-x))
            return y

        if (typee==2): #softpluss (0,inf)
            y = np.log(1+np.exp(x)) #log é na base natural
            return y

        if (typee==3): #gaussinana (0,1)
            y = np.exp(-1*(x**2)) 
            return y

        if (typee==4): #ReLU (0,inf)
            y=np.where(x < 0, 0, x)       
            return y

        if (typee==5): #tanh (-1,1)
            y = (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
            return y

        if (typee==6): #LReLU (-inf,inf)
            y=np.where(x < 0, x*0.5, x)
            return y
        
        if (typee==7): #arctan (-inf, inf)
            y = np.arctan(x)
            return y

        if (typee==8): #exp (-inf, inf)
            y = np.exp(x)
            return y
    
        if (typee==9): #seno (-inf, inf)
            y = np.sin(x)
            return y

        if (typee==10): #swish (0, inf)
            y = x/(1+np.exp(-x))
            return y

        if (typee==11): #selu (-1, inf)
            y=np.where(x >= 0, x, np.exp(x)-1)
            return y
      
        if (typee==12): #logsigmoide (0,1)
            y = np.log( 1/(1+np.exp(-x)) )
            return y

        if (typee==13): #x^2 (inf,inf)
            y = x*x
            return y

        if (typee==14): #x^3 (inf,inf)
            y = x*x*x
            return y

        if (typee==15): # Simetric Rectified Linear (inf,inf)
            y2 = np.where(x > 1, x*0.25, x)
            y = np.where(y2 < -1, y2*0.25, y2)
            return y




    def DeActivation(self, typee,x):

        if (typee==0): #linear (-inf,inf)
            y = 1
            return y    
    
        if (typee==1): #Sigmoide (0,1)
            w = 1/(1+np.exp(-x))
            y = w*(1-w)
            return y

        if (typee==2): #softpluss (0,inf)
            y = 1/(1 + np.exp(-x))
            return y
    
        if (typee==3): #gaussinana (0,1)
            y = -2*x*np.exp(-1*(x**2)) 
            return y

        if (typee==4): #ReLU (0,inf)
            y=np.where(x < 0, 0, 1)       
            return y    

        if (typee==5): #tanh (-1,1)
            w = (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
            y = 1 - w**2
            return y
    
        if (typee==6): #LReLU (-inf,inf)
            y=np.where(x < 0, 0.5, 1)        
            return y
    
        if (typee==7): #arctan (-inf, inf)
            y = 1/(1+x**2)
            return y

        if (typee==8): #exp (-inf, inf)
            y = np.exp(x)
            return y

        if (typee==9): #seno (-inf, inf)
            y = np.cos(x)
            return y  

        if (typee==10): #swish (0, inf)
            y = (x/(1+np.exp(-x))) + (1/(1+np.exp(-x)))*(1 - (x/(1+np.exp(-x))) )         
            return y

        if (typee==11): #selu (-1, inf)
            y = np.where(x >= 0, 1, np.exp(x))        
            return y        

        if (typee==12): #logsigmoide (0,1)
            y = np.exp(-x)/(1+np.exp(-x))
            return y

        if (typee==13): #x^2 (inf,inf)
            y = 2*x
            return y

        if (typee==14): #x^3 (inf,inf)
            y = 3*x*x
            return y

        if (typee==15): # Simetric Rectified Linear (inf,inf)
            y2 = np.where(x > 1, 0.25, 1)
            y = np.where(y2 < -1, 0.25, 1)
            return y







    #machine learning,  single batch with ADAM accelerator-----------------------------------------------------
    def Fit_ADAM(self, matX, matY):

        tinicio = time.time()
        
        #Criação ou leitura da matriz dos pesos--------

        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))
        P34 = np.zeros((self.nn3c,self.nn4c))

        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))
        B4= np.zeros((self.nn4c))

        #pesos memorizados
        P12m = np.zeros((self.nn1c,self.nn2c))
        P23m = np.zeros((self.nn2c,self.nn3c))
        P34m = np.zeros((self.nn3c,self.nn4c))

        #bias memorizados
        B2m = np.zeros((self.nn2c))
        B3m = np.zeros((self.nn3c))
        B4m = np.zeros((self.nn4c))

        #variaçao pesos
        VP12 = np.zeros((self.nn1c,self.nn2c))
        VP23 = np.zeros((self.nn2c,self.nn3c))
        VP34 = np.zeros((self.nn3c,self.nn4c))

        #variaçao bias
        VB2= np.zeros((self.nn2c))
        VB3= np.zeros((self.nn3c))
        VB4= np.zeros((self.nn4c))

        #velocidade pesos
        veloP12 = np.zeros((self.nn1c,self.nn2c))
        veloP23 = np.zeros((self.nn2c,self.nn3c))
        veloP34 = np.zeros((self.nn3c,self.nn4c))

        #velocidade bias
        veloB2= np.zeros((self.nn2c))
        veloB3= np.zeros((self.nn3c))
        veloB4= np.zeros((self.nn4c))

        #massa pesos
        massaP12 = np.zeros((self.nn1c,self.nn2c))
        massaP23 = np.zeros((self.nn2c,self.nn3c))
        massaP34 = np.zeros((self.nn3c,self.nn4c))

        #massa bias
        massaB2= np.zeros((self.nn2c))
        massaB3= np.zeros((self.nn3c))
        massaB4= np.zeros((self.nn4c))

        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))
        c4= np.zeros((self.nn4c))

        #derivadas
        d1= np.zeros((self.nn1c))
        d2= np.zeros((self.nn2c))
        d3= np.zeros((self.nn3c))
        d4= np.zeros((self.nn4c))

        #erros
        e1= np.zeros((self.nn1c))
        e2= np.zeros((self.nn2c))
        e3= np.zeros((self.nn3c))
        e4= np.zeros((self.nn4c))

        #resultados
        R = np.zeros((self.nn4c))

        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------
    
            if self.nn1c ==1: #uma linha de data ele sempre le como vetor de colunas, e a transposta disso precisa de um esquema especial
                P12 = np.array([np.loadtxt("P12.txt")])        
            else:
                P12 = np.loadtxt("P12.txt")  
            P23 = np.loadtxt("P23.txt")
            if self.nn4c ==1: #uma linha de data ele sempre le como vetor de colunas, e a transposta disso precisa de um esquema especial
                P34aux = np.array([np.loadtxt("P34.txt")])
                P34 = P34aux.T
            else:
                P34 = np.loadtxt("P34.txt")
            B2 = np.loadtxt("B2.txt")
            B3 = np.loadtxt("B3.txt")
            B4 = np.loadtxt("B4.txt")

        except: #Inicializa randomicamente-------------------------------

            B2 = -0.1 + 2*0.1*(np.random.rand(self.nn2c))
            B3 = -0.1 + 2*0.1*(np.random.rand(self.nn3c))
            B4 = -0.1 + 2*0.1*(np.random.rand(self.nn4c))    
            P12 = -0.1 + 2*0.1*(np.random.rand(self.nn1c,self.nn2c))
            P23 = -0.1 + 2*0.1*(np.random.rand(self.nn2c,self.nn3c))
            P34 = -0.1 + 2*0.1*(np.random.rand(self.nn3c,self.nn4c))


        #Normaliza os parametros-------------------------
        matX = self.Normalize(matX,"vmax_in.txt","vmin_in.txt","media_in.txt","desvio_in.txt")
        if (self.normout==1):
            matY = self.Normalize(matY,"vmax_out.txt","vmin_out.txt","media_out.txt","desvio_out.txt")


        #Processo de aprendizado------------------------------------------------------------

        VetorErro = np.zeros((self.epochs))
        MenorErro = 999999999

        NumdataEstudo = len(matX)

        monit=0
        for ite in range(0,self.epochs): #Processo iterativo global, epocas, cada epoca passa por todos os dados de aprendizagem-----------------
            Tempo = ite+1
    
            if ite > (self.epochs*monit/100): #só um monitor de progresso
                print(str(monit) + '%')
                monit=monit+10


            #Calculo do erro----------------------------

            EMQ = 0
            for caso in range (0, NumdataEstudo): #Verificação do aprendizado---

                #Camada 1, data de entrada
                c1 = matX[caso,:self.nn1c]
                R = matY[caso,:]  
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2        
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                c3 = self.Activation(self.fa3c,c3)
        
                c4 = np.dot(c3,P34)- B4
                c4 = self.Activation(self.fa4c,c4)         

                #calculo efetivo do erro ------------
                m_aux = (R - c4)**2
                EMQ = EMQ + np.sum(m_aux)/(NumdataEstudo*self.nn4c)
                   
            VetorErro[ite] = EMQ 

 
            #memorização dos melhores pesos-----------
            if (EMQ < MenorErro):
                itememo = ite
                MenorErro = EMQ
                P12m = P12*1
                P23m = P23*1
                P34m = P34*1
                B2m = B2*1
                B3m = B3*1
                B4m = B4*1

        
            for caso in range (0, NumdataEstudo): #varredura em todos os casos de estudo--------

                #Camada 1, data de entrada
                c1 = matX[caso,:self.nn1c]
                R = matY[caso,:]                        
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2
                d2 = self.DeActivation(self.fa2c,c2)
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                d3 = self.DeActivation(self.fa3c,c3)
                c3 = self.Activation(self.fa3c,c3)
        
                c4 = np.dot(c3,P34)- B4
                d4 = self.DeActivation(self.fa4c,c4)
                c4 = self.Activation(self.fa4c,c4)          

                #Calcula o erro da ultima camada 
                e4 = d4 * ( R - c4 )
                 
                #Propagação do erro para traz, backprop     
                e3 = np.dot(e4, np.transpose(P34))
                e3 = d3 * e3
            
                e2 = np.dot(e3, np.transpose(P23))
                e2 = d2 * e2

                #Calculo da variação acumulativa bruta dos pesos                
                VP12 += np.dot(c1.reshape(-1, 1), e2.reshape(1, -1))                
                VP23 += np.dot(c2.reshape(-1, 1), e3.reshape(1, -1))
                VP34 += np.dot(c3.reshape(-1, 1), e4.reshape(1, -1))
                
                VB2 += - e2         
                VB3 += - e3      
                VB4 += - e4           

        
            #Atualização efetiva dos pesos----------------------------------

            Gd12 = VP12 / NumdataEstudo
            Gd23 = VP23 / NumdataEstudo
            Gd34 = VP34 / NumdataEstudo

            massaP12 = 0.9*massaP12 + (1-0.9)*Gd12
            massaP23 = 0.9*massaP23 + (1-0.9)*Gd23
            massaP34 = 0.9*massaP34 + (1-0.9)*Gd34

            veloP12 = 0.999*veloP12 + (1-0.999)*(Gd12**2)
            veloP23 = 0.999*veloP23 + (1-0.999)*(Gd23**2)
            veloP34 = 0.999*veloP34 + (1-0.999)*(Gd34**2)

            aux1= 1-(0.9**Tempo)
            aux2 = 1 - (0.999**Tempo)
    
            P12 = P12 + self.rate*( (massaP12/aux1) / np.sqrt(veloP12/aux2) )
            P23 = P23 + self.rate*( (massaP23/aux1) / np.sqrt(veloP23/aux2) )
            P34 = P34 + self.rate*( (massaP34/aux1) / np.sqrt(veloP34/aux2) )
       
            Gd2 = VB2 / NumdataEstudo
            Gd3 = VB3 / NumdataEstudo
            Gd4 = VB4 / NumdataEstudo

            massaB2 = 0.9*massaB2 + (1-0.9)*Gd2
            massaB3 = 0.9*massaB3 + (1-0.9)*Gd3
            massaB4 = 0.9*massaB4 + (1-0.9)*Gd4

            veloB2 = 0.999*veloB2 + (1-0.999)*(Gd2**2)
            veloB3 = 0.999*veloB3 + (1-0.999)*(Gd3**2)
            veloB4 = 0.999*veloB4 + (1-0.999)*(Gd4**2) 
    
            B2 = B2 + self.rate*( (massaB2/aux1) / np.sqrt(veloB2/aux2) )
            B3 = B3 + self.rate*( (massaB3/aux1) / np.sqrt(veloB3/aux2) )
            B4 = B4 + self.rate*( (massaB4/aux1) / np.sqrt(veloB4/aux2) )
 
            VP12 = np.zeros((self.nn1c,self.nn2c))
            VP23 = np.zeros((self.nn2c,self.nn3c))
            VP34 = np.zeros((self.nn3c,self.nn4c))
            VB2= np.zeros((self.nn2c))
            VB3= np.zeros((self.nn3c))
            VB4= np.zeros((self.nn4c))


        print('100%')

        P12 = P12m*1
        P23 = P23m*1
        P34 = P34m*1
        B2 = B2m*1
        B3 = B3m*1
        B4 = B4m*1


        #Salva os pesos e bias em arquivos txt----------------------------------------------------------
        np.savetxt("P12.txt", P12)
        np.savetxt("P23.txt", P23)
        np.savetxt("P34.txt", P34)
        np.savetxt("B2.txt", B2)
        np.savetxt("B3.txt", B3)
        np.savetxt("B4.txt", B4)
        np.savetxt("Convergencia.txt", VetorErro)

        tfim = time.time()
        print('runtime(s) = ' , tfim-tinicio)








    #machine learning stochastic case by case------------------------------------------------------
    def Fit_STOC(self, matX, matY):

        tinicio = time.time()
        
        #Criação ou leitura da matriz dos pesos--------

        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))
        P34 = np.zeros((self.nn3c,self.nn4c))

        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))
        B4= np.zeros((self.nn4c))

        #pesos memorizados
        P12m = np.zeros((self.nn1c,self.nn2c))
        P23m = np.zeros((self.nn2c,self.nn3c))
        P34m = np.zeros((self.nn3c,self.nn4c))

        #bias memorizados
        B2m = np.zeros((self.nn2c))
        B3m = np.zeros((self.nn3c))
        B4m = np.zeros((self.nn4c))

        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))
        c4= np.zeros((self.nn4c))

        #derivadas
        d1= np.zeros((self.nn1c))
        d2= np.zeros((self.nn2c))
        d3= np.zeros((self.nn3c))
        d4= np.zeros((self.nn4c))

        #erros
        e1= np.zeros((self.nn1c))
        e2= np.zeros((self.nn2c))
        e3= np.zeros((self.nn3c))
        e4= np.zeros((self.nn4c))

        #resultados
        R = np.zeros((self.nn4c))

        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------
    
            if self.nn1c ==1: #uma linha de data ele sempre le como vetor de colunas, e a transposta disso precisa de um esquema especial
                P12 = np.array([np.loadtxt("P12.txt")])        
            else:
                P12 = np.loadtxt("P12.txt")  
            P23 = np.loadtxt("P23.txt")
            if self.nn4c ==1: #uma linha de data ele sempre le como vetor de colunas, e a transposta disso precisa de um esquema especial
                P34aux = np.array([np.loadtxt("P34.txt")])
                P34 = P34aux.T
            else:
                P34 = np.loadtxt("P34.txt")
            B2 = np.loadtxt("B2.txt")
            B3 = np.loadtxt("B3.txt")
            B4 = np.loadtxt("B4.txt")

        except: #Inicializa randomicamente-------------------------------

            B2 = -0.1 + 2*0.1*(np.random.rand(self.nn2c))
            B3 = -0.1 + 2*0.1*(np.random.rand(self.nn3c))
            B4 = -0.1 + 2*0.1*(np.random.rand(self.nn4c))    
            P12 = -0.1 + 2*0.1*(np.random.rand(self.nn1c,self.nn2c))
            P23 = -0.1 + 2*0.1*(np.random.rand(self.nn2c,self.nn3c))
            P34 = -0.1 + 2*0.1*(np.random.rand(self.nn3c,self.nn4c))


        #Normaliza os parametros-------------------------
        matX = self.Normalize(matX,"vmax_in.txt","vmin_in.txt","media_in.txt","desvio_in.txt")
        if (self.normout==1):
            matY = self.Normalize(matY,"vmax_out.txt","vmin_out.txt","media_out.txt","desvio_out.txt") 


        #Processo de aprendizado------------------------------------------------------------

        VetorErro = np.zeros((self.epochs))
        MenorErro = 999999999

        NumdataEstudo = len(matX)

        monit=0
        for ite in range(0,self.epochs): #iteração global, cada epoca varred todos os casos de estudo-------------------------
            Tempo = ite+1
    
            if ite > (self.epochs*monit/100): #só um monitor de progresso
                print(str(monit) + '%')
                monit=monit+10


            #Calculo do erro---------------------------

            EMQ = 0
            for caso in range (0, NumdataEstudo): #Verificação do aprendizado-------

                #Camada 1, data de entrada
                c1 = matX[caso,:self.nn1c]
                R = matY[caso,:]  
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2        
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                c3 = self.Activation(self.fa3c,c3)
        
                c4 = np.dot(c3,P34)- B4
                c4 = self.Activation(self.fa4c,c4)         

                #calculo efetivo do erro -------
                m_aux = (R - c4)**2
                EMQ = EMQ + np.sum(m_aux)/(NumdataEstudo*self.nn4c)
                   
            VetorErro[ite] = EMQ 

 
            #memorização dos melhores pesos------------
            if (EMQ < MenorErro):
                itememo = ite
                MenorErro = EMQ
                P12m = P12*1
                P23m = P23*1
                P34m = P34*1
                B2m = B2*1
                B3m = B3*1
                B4m = B4*1


            for caso in range (0, NumdataEstudo): #varredura em todos os casos, mas no estocastico, atualiza os pesos caso a caso---

                #Camada 1, data de entrada
                c1 = matX[caso,:self.nn1c]
                R = matY[caso,:]                        
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2
                d2 = self.DeActivation(self.fa2c,c2)
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                d3 = self.DeActivation(self.fa3c,c3)
                c3 = self.Activation(self.fa3c,c3)
        
                c4 = np.dot(c3,P34)- B4
                d4 = self.DeActivation(self.fa4c,c4)
                c4 = self.Activation(self.fa4c,c4)          

                #Calcula o erro da ultima camada 
                e4 = d4 * ( R - c4 )
                 
                #Propagação do erro para traz, backprop     
                e3 = np.dot(e4, np.transpose(P34))
                e3 = d3 * e3
            
                e2 = np.dot(e3, np.transpose(P23))
                e2 = d2 * e2

                #Atualização dos pesos
                P12 += self.rate*(np.dot(c1.reshape(-1, 1), e2.reshape(1, -1)))
                P23 += self.rate*(np.dot(c2.reshape(-1, 1), e3.reshape(1, -1)))
                P34 += self.rate*(np.dot(c3.reshape(-1, 1), e4.reshape(1, -1)))                
                B2 += - self.rate * e2
                B3 += - self.rate * e3
                B4 += - self.rate * e4
        

        print('100%')

        P12 = P12m*1
        P23 = P23m*1
        P34 = P34m*1
        B2 = B2m*1
        B3 = B3m*1
        B4 = B4m*1


        #Salva os pesos e bias em arquivos txt----------------------------------------------------------
        np.savetxt("P12.txt", P12)
        np.savetxt("P23.txt", P23)
        np.savetxt("P34.txt", P34)
        np.savetxt("B2.txt", B2)
        np.savetxt("B3.txt", B3)
        np.savetxt("B4.txt", B4)
        np.savetxt("Convergencia.txt", VetorErro)

        tfim = time.time()
        print('runtime(s) = ' , tfim-tinicio)










    #make prediction----------------------------------------------------------
    def Predict(self, matX):
        
        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))
        P34 = np.zeros((self.nn3c,self.nn4c))
        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))
        B4= np.zeros((self.nn4c))
        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))
        c4= np.zeros((self.nn4c))


        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------
    
            if self.nn1c ==1: #uma linha de data ele sempre le como vetor de colunas, e a transposta disso precisa de um esquema especial
                P12 = np.array([np.loadtxt("P12.txt")])        
            else:
                P12 = np.loadtxt("P12.txt")  
            P23 = np.loadtxt("P23.txt")
            if self.nn4c ==1: #uma linha de data ele sempre le como vetor de colunas, e a transposta disso precisa de um esquema especial
                P34aux = np.array([np.loadtxt("P34.txt")])
                P34 = P34aux.T
            else:
                P34 = np.loadtxt("P34.txt")
            B2 = np.loadtxt("B2.txt")
            B3 = np.loadtxt("B3.txt")
            B4 = np.loadtxt("B4.txt")

        except: #se nao tem pesos salvos encerra o programa-------------------------------

           input('No saved weight files')
           exit()

        #Normaliza a entrada de data----------------------
        matX = self.Normalize2(matX,"vmax_in.txt","vmin_in.txt","media_in.txt","desvio_in.txt") 

        
        #Predição----------------------------
        numdata = len(matX)
        Calculated = np.zeros((numdata, self.nn4c)) #inicializa a matriz dos resultados Calculated
        
        for caso in range (0, numdata):

            #Camada 1, data de entrada
            c1 = matX[caso,:self.nn1c]                     
                
            #propagacao sinal
            c2 = np.dot(c1,P12)- B2     
            c2 = self.Activation(self.fa2c,c2)

            c3 = np.dot(c2,P23)- B3
            c3 = self.Activation(self.fa3c,c3)
        
            c4 = np.dot(c3,P34)- B4
            c4 = self.Activation(self.fa4c,c4)         

            # saida----------------------------
            Calculated[caso][:] = c4[:]

        if (self.normout==1):            
            Calculated = self.DesNormalize(Calculated, "vmax_out.txt", "vmin_out.txt","media_out.txt","desvio_out.txt") 

        return Calculated










    #Plota a convergencia ----------------------------------------------------------
    def Plotconv(self):

        #grafico da convergencia
        Conve = np.loadtxt("Convergencia.txt")
        tamanho = len(Conve)
        MenorErro = np.min(Conve)

        eixoX = np.zeros((tamanho)) 
        eixoY = np.zeros((tamanho))

        eixoX = np.arange(0, tamanho, dtype=int)
        eixoY = Conve*1  
    
        plt.figure(figsize=(12, 5))
        plt.title('Mean squared error = ' + str(MenorErro))
        plt.xlabel('Study data')
        plt.ylabel('Error, mse')
        plt.plot(eixoX, eixoY, marker = '', color = 'darkblue')  
        plt.show()





        
