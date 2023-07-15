# tesi_droni

Materiale prodotto durante il progetto di tesi di laurea triennale dal titolo:

__***Creazione di uno scenario pilota per il volo  di droni in pattuglia basato su simulatori industriali open source***__

## mavsdk_swarm

Questa cartella contiene il codice principale da prendere come riferimento per lavori futuri.

## Codice

Questa cartella contiene vari script di testing secondari, sconsiglio di utilizzare il codice qui presente dato che non è stato revisionato ma ho deciso di lasciarlo pensando che potrebbe comunque essere di aiuto.

## File `install_`

Questi file contengono i comandi presi dalle varie guide (i cui link sono riportati nel file stesso).
Possono far comodo per eseguire tutti i comandi velocemente ma potrebbero dar luogo a errori o 
nascondere eventuali warning.

## Logs.md

Questo file contiene tutti i tentativi fatti durante l'installazione dell'ambiente di sviluppo. Essendo organizzato cronologicamente potrebbe non essere immediato trovare la soluzione al proprio problema (ammesso che lo abbia incontrato anche io)

## spawn2.sh

Questo script, che deve essere copiato nella root di PX4, permette di lanciare 2 simulazioni parallele con JMAVSim. È necessario essere all'interno di un terminale tmux affinché lo script funzioni.
Lo script può essere modificato per aumentare il numero di simulazioni lanciate ricordandosi di incrementare ogni il parametro `-p`.
