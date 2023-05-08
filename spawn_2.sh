
tmux new-window "./Tools/simulation/sitl_multiple_run.sh 2 && ./Tools/simulation/jmavsim/jmavsim_run.sh -l " \; split-window -h  "./Tools/simulation/jmavsim/jmavsim_run.sh -p 4561 -l"
