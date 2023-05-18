import time
# Vi skal i main / __init__ få positionen af motorene og

# Vi starter med at skabe kontakt til Arduino og Matlab

# Vi importerer vores trajectory Planning fra excel + nogle t-værdier:D

# Vent på at inputtet i consollen er "Go" eller "start" eller lign.

# Definerer TGlobal og TVar Tsample = konstant, Tslut = Mål tiden koden tager

# Opstil if-statement som ser om det er tid til at køre koden?
# Hvis det er tid, er if true.
# Man ser så på om TVar er lig tfinish, som er tiden det tager fra startpunkt til desiredPos.
# Man kører så Controlleren med input q, qdot qdotdot og t(i)-værdierne fra trajectory planning.
# Få position og hastighed fra motorene

# Output er en current, som sendes til arduino
# Man slutter med at lægge 1 til t(i) - antallet af loops man har gennemført.
TVar = time.time()#Relative to current trajectory
TGlobal = time.time() #Always increasing when
tNow = time.time()
TStop = time.time()
TSample = 0.5
ti = 0 #Number of itterations through the loop

if(tNow < TGlobal):
    tNow = tNow + TSample

else:
    TGlobal = time.time()

def main():
    print(time.time())

if __name__ == "__main__":
    main()