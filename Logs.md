## 11_04_23
- Decido di utilizzare Ubuntu Jammy su WSL2 dato che risulta supportato e che le prestazioni sembrano essere molto buone
- Seguo [questa guida](https://github.com/Field-Robotics-Lab/dave/wiki/Install-on-Windows-using-WSL2) per l'installazione dei driver Nvidia per WSL ignorando le parti non necessarie. *{Forse i driver non sono necessari}*
- Installo Ubuntu Jammy su WSL2

## 12_04_23
- PX4 non è completamente supportato da Ubuntu Jammy (**attualmente**), passo a Ubuntu Focal
- Seguo [questa guida](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html) per installare PX4 facendo attenzione a non tralasciare il punto su GCC
- Seguo [questa guida](https://docs.px4.io/main/en/dev_setup/building_px4.html) per testare PX4 con jMAVSim:
	- Non mi sembra ci sia bisogno di clonare la repo dato che è già stata clonata al punto precedente
	- Durante l'esecuzione del comando `make` viene generato un errore dal JavaRuntimeEnvironment simile a quello riportato [qui](https://github.com/PX4/PX4-Autopilot/issues/21014)
		- Provo a seguire [questa guida](https://docs.px4.io/main/en/simulation/jmavsim.html#troubleshooting) per risolvere l'errore `java.lang.reflect.InvocationTargetException` senza successo
	- Seguo [questo commento](https://github.com/PX4/PX4-Autopilot/issues/21014#issuecomment-1408176068) e utilizzo Gazebo come simulatore
	- Installo qgroundcontrol tramite [questa guida](https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html):
		- Seguo [questo commento](https://github.com/mavlink/qgroundcontrol/issues/10306#issue-1251444649) per portare a termine l'installazione su WSL2
	- I punti successivi della guida (`commander takeoff` e `commander land`) funzionano correttamente su Gazebo
- Creo dei file eseguibili che contengono i comandi necessari per eseguire più velocemente i punti precedenti

## 13/04/23
- Provo a eseguire `make px4_sitl gazebo` ma dopo vari minuti non succede nulla (ieri funzionava)
	- Sembra che eseguire `make clean` e `make distclean` risolva il problema, il `make` richiede comunque una decida di minuti

## 14/04/23
- Testo qgc e funziona correttamente con px4 e gazebo, è sufficiente aprire il file .AppImage installato precedentemente e far partire la simulazione. ![[Pasted image 20230414183713.png]]
- Seguo [questa guida](https://docs.px4.io/main/en/modules/hello_sky.html) per capire come far interfacciare del codice con il drone
	- Sembra funzionare tutto correttamente (il codice è già presente nella cartella specificata). Essendo codice molto di basso livello (almeno apparentemente), non proseguo il tutorial per concentrarmi sul python.
- Prima di procedere credo sia opportuno installare e configurare il pacchetto `pipenv` per python che consente di gestire facilmente ambienti virtuali python. Ho creato un file per l'installazione rapida di pipenv. Dopo l'esecuzione del file è necessario uscire e rientrare.

## 15/04/22
- A quanto pare ciò che un tempo si chiamava Gazebo adesso è stato rinominato Gazebo-classic, il vecchio Ignition invece (la versione più moderna del simulatore), è stata rinominata Gazebo. Mi sembra molto facile fare confusione perché il termine Gazebo si può riferire a entrambe le versioni in base al periodo in cui è stato scritto il testo in questione. 
	- Dato che Gazebo-classic è obsoleto (non trovo la fonte) provo a capire come fare per utilizzare Gazebo (il vecchio Ignition) da ora in avanti
	- Seguo i primi punti di [questa guida](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu.html#simulation-and-nuttx-pixhawk-targets)  per installare px4 e gazebo (a regola il vecchio ignition) in una nuova cartella.
	- Il comando `make px4_sitl gz_x500` termina con errore `ninja: error: unknown target 'gz_x500'`, secondo [questi commenti](https://github.com/PX4/PX4-Autopilot/issues/21163) il problema può essere dovuto al fatto che la versione di gazebo installata non è quella corretta.
		- Non riesco a capire se la versione corretta è installata o no, probabilmente non è installata. Seguo [questa guida](https://gazebosim.org/docs/garden/install_ubuntu) per installare gazebo garden (dovrebbe essere l'ultima versione)
- Una volta installata la versione corretta noto che ci sono dei problemi di compatibilità con la versione di OpenGL, [questo commeto](https://answers.gazebosim.org/question/27597/ignition-crashes-directly-after-start/) suggerisce di cambiare il `rendering-engine`, cosa che sembra funzionare. Devo capire come far utilizzare a gazebo questa impostazione anche tramite px4 sitl
	- Dopo varie ricerche non trovo modo di cambiare il rendering-engine di default

## 16/04/23
- Continuo a cercare una soluzione per i problemi con openGL, gazebo parte solamente "standalone" con il comando `gz sim shapes.sdf --render-engine ogre`. Questo comando funziona perché il componente che richiede la versione più aggiornata di OpenGL è ogre2 (il renderer di default).
	- Non riesco a trovare un modo per settare un renderer diverso quando eseguo gazebo tramite px4.
	- Provo a seguire i suggerimenti di [questo thread](https://github.com/conda-forge/libignition-gazebo-feedstock/issues/27) senza successo
	- Provo ad aggiornare la versione di openGL senza successo
	- Provo ad eseguire px4 con gazebo settando `LIBGL_ALWAYS_SOFTWARE=1` come suggerito da [questo commento](https://github.com/gazebosim/gz-rendering/issues/662#issuecomment-1466984897) senza successo

## 17/04/23
- Non riuscendo a risolvere i problemi illustrati sopra decido di ricominciare con un'installazione pulita di ubuntu focal (Ubuntu 20.04.6 LTS) per escludere di aver causato problemi durante i vari tentativi.
	- Nota: ho avuto problemi durante la nuova installazione di ubuntu. Ho risolto eseguendo i comandi `wsl --list`, individuando la versione di ubuntu precedente (che non era stata rimossa completamente) e poi eseguendo `wsl --unregister *nomeversione_ubuntu*` 
- Seguo [questa guida](https://docs.px4.io/main/en/dev_setup/dev_env_windows_wsl.html) specifica per WSL che non avevo trovato nei tentativi precedenti:
	- L'installazione termina senza errori
	- La simulazione con jmavsim dà lo stesso errore del [[#12_04_23]].
	- La simulazione con gazebo classic funziona (`make px4_sitl gazebo`)
	- Seguo [questa guida](per installare gazebo-garden) e poi provo a eseguire `make px4_sitl gz_x500` senza successo (come ai tentativi precedenti)
	- Provo a installare i driver con lo script `install_cuda.sh` senza risolvere nulla
- Provo a installare ubuntu jammy anche se non è ancora completamente supportato da PX4 per vedere se riesco a risolvere i problemi precedenti:
	- La simulazione con jmavsim funziona correttamente
	- L'esecuzione del comando ` make px4_sitl gazebo` restituisce l'errore ```ninja: error: unknown target 'gz_x500' make: *** [Makefile:232: px4_sitl] Error 1```

## 18/04/23
- Faccio un ultimo tentativo per risolvere il problema di gazebo (non classic) su ubuntu 22.04 seguendo il **Troubleshooting** a [questo indirizzo](https://docs.px4.io/main/en/dev_setup/building_px4.html):
	- Eseguire `git submodule update --recursive` e `make distclean` risolve il problema di cui all'ultimo punto del [[#17/04/23]]
	- Il simulatore viene lanciato correttamente ma le performance non sono accettabili (a occhio un paio di fps)
	- Per risolvere il problema provo a reinstallare i driver cuda tramite [questa guida](https://ubuntu.com/tutorials/enabling-gpu-acceleration-on-ubuntu-on-wsl2-with-the-nvidia-cuda-platform#3-install-nvidia-cuda-on-ubuntu) (è possibile che lo script fallisse a causa della necessità dell'input dell'utente)
		- L'istallazione va a buon fine ma non cambia il risultato.
		- Gestione attività di windows non mostra nessun utilizzo della scheda video dedicata nvidia (GTX 1050 Ti)
		- Rimuovere il sole (oggetto "sun") dalla simulazione sembra migliorare notevolmente le prestazioni
- Installo qgc tramite l'installer
	- Tutto funziona correttamente
- Installo pipenv
- Seguo [questa guida](https://mavsdk.mavlink.io/main/en/python/quickstart.html) utilizzando pipenv invece che pip dopo aver creato l'ambiente virtuale con `pipenv shell` 
- Noto solo adesso che le anche con jmavsim le prestazioni sono pessime (3/4 fps) e provo a trovare una soluzione
	- 

## 24/04/23
- Devo formattare il pc, ne approfitto per seguire da zero una guida.
- Installo wsl dal microsoft store
- Eseguo il comando `wsl --install` da un terminale in modalità amministratore
	- Ricevo l'errore `0x80370114`
	- Non avevo abilitato le funzionalità "Sottosistema windows per linux" e "hyper-v" tra le funzionalità avanzate
	- Adesso ho ubuntu 22.04 LTS installato
- Seguo le istruzioni riportate [qui](https://docs.px4.io/main/en/dev_setup/dev_env_windows_wsl.html)
- Per l'installazione di qgc utilizzo il mio script
- aggiungo la riga `export PATH="/home/giacomo/.local/bin:$PATH"` al `.bashrc` a seguito di un warning avvenuto durante l'installazione
- La simulazione con jmavsim fuziona correttamente a circa 60fps
- La simulazione con gazebo dà errore

## 25/04/23
- Eseguire `make px4_sitl gz_x500` fa crashare gazebo all'apertura con il seguente errore `libEGL warning: failed to open /dev/dri/renderD128: Permission denied`, [questo commento](https://github.com/deepmind/dm_control/issues/214#issuecomment-996934472) mi fa pensare che sia necessario installare i driver nvidia.
	- Seguo [questa guida](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) (fermandomi al punto su CUDA escluso) ma il risultato non cambia dopo l'installazione dei driver (jmavisim continua a funzionare correttamente)
	- Do all'utente i permessi `xwr` alla cartella `/dev/dri`, l'errore cambia in `libEGL warning: NEEDS EXTENSION: falling back to kms_swrast`
	- Ripristino i permessi originali alla cartella `/dev/dri`
## 26/04/23
- Installo mavsdk seguendo [questa guida](https://mavsdk.mavlink.io/main/en/python/quickstart.html) 
	- Riesco a comunicare con il drone tramite la console di python
## 29/04/21
- Scarico gli esempi di mavsdkpython e creo una shell pipenv all'interno della cartella così da poter provare gli script isolati
	- (prima di procedere devo reinstallare le librerie necessarie all'iterno dell'ambiente virtuale analogamente a quanto fatto il [[#26/04/23]])
	- L'esempio `takeoff_and_land.py` funziona solo togliendo il parametro `system_address` alla funzione `run`
	- Riesco a eseguire gli script senza problemi (anche senza modificare il parametro `system_address`)
- Cerco un modo per programmare una logica sul drone, forse [questo link](https://mavsdk.mavlink.io/main/en/cpp/guide/connections.html) ha la risposta ma non è relativo a python
	- Non capisco se il codice python che scrivo viene eseguito sul drone oppure sulla gcs
	- [Possibile soluzione](http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/server_utility.html#module-mavsdk.server_utility)

## 01/05/23
- Cerco di far partire una simulazione con più droni seguendo [questa guida](https://docs.px4.io/main/en/simulation/multi_vehicle_jmavsim.html)
	- Il comando `./Tools/sitl_multiple_run.sh 2` non è presente, lo trovo al seguente percorso `PX4-Autopilot/Tools/simulation/sitl_multiple_run.sh`
	- I droni vengono simulati in finestre diverse di jmavis a differenza di quanto mi aspettavo
	- qgc non riesce a connettersi ai droni
	- Lo script `takeoff_and_land.py` non fa nulla
	- Il problema potrebbe essere dovuto al fatto che il comando `sitl_multiple_run.sh` contiene un path incorretto (trovato tramite il file `PX4-Autopilot/Tools/build/px4_sitl_default/instance_1/err.log` di cui riporto il conetenuto) ```./Tools/simulation/sitl_multiple_run.sh: line 31: /home/giacomo/PX4-Autopilot/Tools/simulation/../build/px4_sitl_default/bin/px4: No such file or directory```
		- Percorso `build/px4_sitl_default/bin/px4` è presente in `PX4-Autopilot/build/px4_sitl_default`, non all'interno della cartella `Tools` come specificato nel file di errore. Provo a modificare lo script per far sì che usi questo percorso cambiando la riga `src_path="$SCRIPT_DIR/.."` in `src_path="$SCRIPT_DIR/../../"` (questo errore mi sembra coerente con il fatto che la documentazione dichiara che lo script `sitl_multiple_run.sh` sia nella cartella "padre" di quella in cui non sia in realtà)

## 05/05/23
- Provo a utilizzare la [guida](https://docs.px4.io/main/en/test_and_ci/docker.html) per docker senza successo, probabilmente perché sono su ubuntu 22 e docker utilizza gazebo classic che non è più supportato come riferito [qui](https://github.com/PX4/PX4-SITL_gazebo-classic/issues/954)
- Seguo la stessa guida su ubuntu 20 appena installato
	- Devo eseguire lo script nella sezione "**Calling Docker Manually**" altrimenti non funziona
	- Sembra non sia necessario il comando `xhost +` su wsl2
	- Devo eseguire i soliti `make clean` e `make distclean`
	- Riesco ad eseguire la simulazione con gazebo classic
- Ritento gli stessi procedimenti su ubuntu 22 dato che prima non avevo eseguito lo script "manuale"
	- La simulazione funziona
- Continuo a lavorare su ubuntu 22
- il comando ` Tools/simulation/gazebo-classic/sitl_multiple_run.sh -m iris -n 2 -t px4_sitl_defaul` (prendendo spunto da [qui](https://docs.px4.io/main/en/sim_gazebo_classic/multi_vehicle_simulation_gazebo.html)fa partire correttamente una simulazione con 2 droni a cui però non mi riesco a connettere con lo script python di default, probabilmente devo gestire diversamente le porte

## 06/05/23
- Seguo [questi commenti](https://discuss.px4.io/t/connecting-qgroundcontrol-to-px4-sitl-running-inside-docker/17214/9) per capire come trovare la porta giusta su cui connettere qgc
	- Non trovo la soluzione ma posto un commento 
- Torno a sviluppare il codice python con jmavsim per il momento
	- Riesco a far decollare due droni contemporaneamente