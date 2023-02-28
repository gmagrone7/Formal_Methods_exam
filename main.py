# GIOVANNI MAGRONE COMPUTER SCIENCE YEAR 2022/2023
import pm4py
import os
## Import the Petri Net visualizer object
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
# Import of Token-based replay
from pm4py.algo.conformance.tokenreplay import algorithm as token_based_replay
# Import library for Petri Net building
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
# Import woflan
from pm4py.algo.analysis.woflan import algorithm as woflan
# Import simulation library
from pm4py.algo.simulation.playout.petri_net import algorithm as simulator

def get_place_by_name(net, place_name):
    """
    Get a place by its name "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    net
        Petri net
    place_name
        Place name

    Returns
    ------------
    place
        Place object
    """
    for p in net.places:
        if p.name == place_name:
            return p
    return None

def Random_merge(net,name):
    """
    It merges the net with the new places that you create, it's based on two iterations
    the first that goes from the new place to a other places randomly and the second that goes
    from the transition for the new places to other places randomly so we connect the new place
    "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    net
    name(name of the new transition)

    Returns
    ------------
    net
    """
    new_place = PetriNet.Place(name)
    net.places.add(new_place)
    t_name = name
    t_new = PetriNet.Transition(t_name, t_name)
    net.transitions.add(t_new)
    i3 = 0
    for p in net.places:
        for t in net.transitions:
            if i3<1:
                petri_utils.add_arc_from_to(new_place, t, net)
                petri_utils.add_arc_from_to(t, p, net)
                i3 = i3+1
            else:
                break
    #and now we just let it point from the transition to other places randomly
    i3 = 0
    for p in net.places:
        for t in net.transitions:
            if i3 < 1:
                petri_utils.add_arc_from_to(p, t_new, net)
                petri_utils.add_arc_from_to(t_new, p, net)
                i3 = i3 + 1
            else:
                break
    petri_utils.add_arc_from_to(p, t_new, net)
    petri_utils.add_arc_from_to(t_new, p, net)
    return net

def Create_new_component(net):
    """
    It creates new random components for the Petri net, it takes a place or a transition as input and it links it randomly
    with the others places and transitions of the Petri Net.
      "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    net
        Petri net (To be update)
    Returns
    ------------
    net
        Petri net (Updated)
    """
    i3 = 0
    print("If you want to add places type 1, if you want to do nothing type 3: ")
    i3 = int(input())
    if i3 == 1:
        print("Insert a name for a new place in Petri Net")
        p_name = input()
        net = Random_merge(net,p_name)
        i3 = 0
        return net
    else:
        return net

def check_boundness(net,im,fm):
    """
        It checks if is it bounded the function
          "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"
        IMPORTANT:To work the net should be a woflan PN

        Parameters
        ------------
        net
        im(initial_marking)
        fm(final_marking)

        Returns
        ------------
        null
    """
    is_sound = woflan.apply(net, im, fm, parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
                                                     woflan.Parameters.PRINT_DIAGNOSTICS: False,
                                                     woflan.Parameters.RETURN_DIAGNOSTICS: False})
    print("So this Petri Net is sound?")
    print(is_sound)

def pn_playout(net, im):
    """
    It performs a fast simulation of the log
      "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    net
    im(initial_marking)
        Petri net (To be update)
    Returns
    ------------
    simulated log
        if empty, simulation went wrong, if is not is executed correctly
    """

    simulated_log = simulator.apply(net, im, variant=simulator.Variants.BASIC_PLAYOUT,
                                    parameters={simulator.Variants.BASIC_PLAYOUT.value.Parameters.NO_TRACES: 60})

    print("simulation log")
    print(simulated_log)
    return simulated_log

def Find_new_transitions(net_1,net_2,Type):
    """
    It searches for new transition bewteen a newer and an older log
      "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    net_1
    net_2
        Petri net (To be update)
    Returns
    ------------
        Boolean 1 find new transition, 0 else
    """
    t_find = 0
    for t2 in net_2.transitions:
        t_find = 0
        for t1 in net_1.transitions:
            if t2.name == t1.name:
                t_find = 1

        if "hid" in t2.name:
            t_find = 1
        counter = 0
        if t_find == 0:
            print("A new transition has been founded")
            print(t2.name)
            if Type == 1:
                for place in net_2.places:
                    if t2.name in place.name:
                        for arc in place.in_arcs:
                            counter = counter + 1
                print("Transition is linked with other " + str(counter) + " activities")
                print("Do you want to add it? Type 1 yes, or type 2 for no: ...")
                check = int(input())
                if check == 1:
                    return 1
                else:
                    return 0
            else:
                print("A new transition has been founded")
                print(t2.name)
                print("Do you want to add it? Type 1 yes, or type 2 for no: ...")
                check = int(input())
                if check == 1:
                    return 1
                else:
                    return 0

def check_petri_net(Type,Path):
    """
    It takes the original PN and compare it with the modified new one and check if there are difference,
    if they are different, it will update the PN saved with the new one, otherwise it will do nothing
    "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------

    Type(used to see which kind of mining we are analyzing)
    Path(the path of the new modified log)

    Returns
    ------------
    none
    """
    Path_new = Path
    print(Path_new)
    Path_original = "C:/Users/176996/Desktop/progetto/petri.pnml"
    net_1, initial_marking, final_marking = pm4py.read_pnml(os.path.join("tests", "input_data", Path_original))
    event_log = pm4py.read_xes(Path_new)
    if Type == 1:
        net_2, im, fm = heuristics_miner.apply(event_log)
    else:
        net_2, im, fm = pm4py.discover_petri_net_inductive(event_log)
    check = Find_new_transitions(net_1, net_2,Type)
    if check == 1:
        pm4py.write_pnml(net_2, im, fm, Path_original)
        pm4py.view_petri_net(net_2, initial_marking, final_marking)
        print("Petri Net Updated")
    else:
        print("The nets are equivalent, no new transitions")



def Heuristic_mining(file_path):
    """
    It does the Heuristic mining on the selected log, it returns the process map and allows to perform several other
    action on the mined log
    "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    file_path

    Returns
    ------------
    none
    """
    event_log = pm4py.read_xes(file_path)
    print(event_log)
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    # Here we print the number of the activities started and in witch node they finished.
    print("Start activities: {}\nEnd activities: {}".format(start_activities, end_activities))
    # heuristics miner
    heu_net = heuristics_miner.apply_heu(event_log)
    # Visualise Process model
    gviz = hn_visualizer.apply(heu_net)
    hn_visualizer.view(gviz)
    # heuristics miner algorithm returning model, initial marking and
    # final marking
    Path_original = "C:/Users/176996/Desktop/progetto/petri.pnml"
    net, im, fm = heuristics_miner.apply(event_log)
    pm4py.write_pnml(net, im, fm, Path_original)
    # Petri net visualization
    gviz = pn_visualizer.apply(net, im, fm)
    ## print(net) print the petri net results
    pn_visualizer.view(gviz)
    # Here we analize the if the model obtained fit with the log
    print("do you want to check if the model fit with the log?")
    print("Print 1 to check, 0 to procede")
    i2 = 0
    i2 = int(input())
    if i2 == 1:
        parameters_tbr = {token_based_replay.Variants.TOKEN_REPLAY.value.Parameters.DISABLE_VARIANTS: True,
                          token_based_replay.Variants.TOKEN_REPLAY.value.Parameters.ENABLE_PLTR_FITNESS: True}
        replayed_traces, place_fitness, trans_fitness, unwanted_activities = token_based_replay.apply(event_log, net,im,
                                                                                                      fm,
                                                                                                      parameters=parameters_tbr)
        print("Model fit")
        print(replayed_traces)
        print("Place fitness")
        print(place_fitness)
        print("Transactions fitness")
        print(trans_fitness)
        print("Unwanted activities")
        print(unwanted_activities)

    # Part of inserting new component
    print("Do you want to try to insert a new components and see how it works Petri Net? Then type 1, otherwise type 0")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        # Here i set the new docuemnts in xes file, changing the log inserting new values basing on user inputs of place, transition and arrows
        net = Create_new_component(net)
        pm4py.view_petri_net(net, im, fm)

    # Part of checking petri net comparing to a newest event_Log
    print("Do you want to check the Petri Net generated with a newest log? Then type 1, otherwise type 0")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        if file_path == "C:/Users/176996/Desktop/progetto/edited_hh110_weekends.xes":
            check_petri_net(1, "C:/Users/176996/Desktop/progetto/edited_hh110_weekends_umm.xes")
        elif file_path == "C:/Users/176996/Desktop/progetto/activitylog_uci_detailed_labour.xes":
            check_petri_net(1,"C:/Users/176996/Desktop/progetto/activitylog_uci_detailed_labour_umm.xes")
        else:
            print("This log does not have a much more updated log actually")
    # Part of checking Boundness
    print("Do you want to check the Petri Net generated is bounded? Type 1 to check, type 0 otherwise")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        check_boundness(net, im, fm)

    # Part of Simulation Playout
    print("Do you want to a Playout of Petri Net? Type 1 to check, type 0 otherwise")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        result = pn_playout(net, im)
        if result != "":
            print("Simulation correctly executed")
        else:
            print("Simulation went wrong")

    #Just used to remind the main control commands
    print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")

def Inductive_mining(file_path):
    """
    It does the Inductive mining on the selected log, it returns the process tree and allows to perform several other
    action on the mined log
    "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    file_path

    Returns
    ------------
    none
    """
    event_log = pm4py.read_xes(file_path)
    # Discovering the process tree using the inductive miner
    Path_original = "C:/Users/176996/Desktop/progetto/petri.pnml"
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    pm4py.write_pnml(net, initial_marking, final_marking, Path_original)
    tree = pm4py.discover_process_tree_inductive(event_log)
    # Petri net visualization
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.view(gviz)
    # Discovery process tree
    pm4py.view_process_tree(tree)
    #Here we analize the if the model obtained fit with the log
    print("do you want to check if the model fit with the log?")
    print("Print 1 to check, 0 to procede")
    i2 = 0
    i2 = int(input())
    if i2 == 1:
        parameters_tbr = {token_based_replay.Variants.TOKEN_REPLAY.value.Parameters.DISABLE_VARIANTS: True,
                          token_based_replay.Variants.TOKEN_REPLAY.value.Parameters.ENABLE_PLTR_FITNESS: True}
        replayed_traces, place_fitness, trans_fitness, unwanted_activities = token_based_replay.apply(event_log, net,initial_marking,
                                                                                                      final_marking,
                                                                                                      parameters=parameters_tbr)
        print("Model fit")
        print(replayed_traces)
        print("Place fitness")
        print(place_fitness)
        print("Transactions fitness")
        print(trans_fitness)
        print("Unwanted activities")
        print(unwanted_activities)

    # Part of inserting new component
    print("Do you want to try to insert a new components and see how it works Petri Net? Then type 1, otherwise type 0")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        # Here i set the new docuemnts in xes file, changing the log inserting new values basing on user inputs of place, transition and arrows
        net = Create_new_component(net)
        pm4py.view_petri_net(net, initial_marking, final_marking)

    # Part of checking petri net comparing to a newest event_Log
    print("Do you want to check the Petri Net generated with a newest log? Then type 1, otherwise type 0")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        if file_path == "C:/Users/176996/Desktop/progetto/edited_hh110_weekends.xes":
            check_petri_net(2, "C:/Users/176996/Desktop/progetto/edited_hh110_weekends_umm.xes")
        elif file_path == "C:/Users/176996/Desktop/progetto/activitylog_uci_detailed_labour.xes":
            check_petri_net(2,"C:/Users/176996/Desktop/progetto/activitylog_uci_detailed_labour_umm.xes")
        else:
            print("This log does not have a much more updated log actually")

    # Part of Simulation Playout
    print("Do you want to a Playout of Petri Net? Type 1 to check, type 0 otherwise")
    i3 = 0
    i3 = int(input())
    if i3 == 1:
        result = pn_playout(net, initial_marking)
        if result != "":
            print("Simulation correctly executed")
        else:
            print("Simulation went wrong")

    #Just used to remind the main control commands
    print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")

def Process_Map(file_path):
    """
    It do the process map of the selected log, that shows you which activity are connected and how many times they reach one another
    "FUNCTION CREATED BY AUTHOR OF THIS PROGRAMS"

    Parameters
    ------------
    file_path

    Returns
    ------------
    none
    """
    event_log = pm4py.read_xes(file_path)
    #Obtaining the ProcessMap with DFG (Direct Following Graph)
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
    pm4py.view_dfg(dfg, start_activities, end_activities)

def Input_Log():
    """
    Simple function that allow to us to select the path of the selected log from the given ones
    Parameters
    ------------
    none

    Returns
    ------------
    path(string)
    """
    print("Select path: 1 for detailed labour, 2 for detailed weeks, 3 for edited hh102 labour, 4 for edited hh102 weekends, 5 for edited hh104 labour, 6 for edited hh104 weekends, 7 for edited hh110 labour, 8 for edited hh110 weekends ")
    i3= int(input())
    Path=""
    if i3 == 1:
        Path= "C:/Users/176996/Desktop/progetto/activitylog_uci_detailed_labour.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 2:
        Path= "C:/Users/176996/Desktop/progetto/activitylog_uci_detailed_weekends.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 3:
        Path="C:/Users/176996/Desktop/progetto/edited_hh102_labour.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 4:
        Path="C:/Users/176996/Desktop/progetto/edited_hh102_weekends.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 5:
        Path="C:/Users/176996/Desktop/progetto/edited_hh104_labour.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 6:
        Path="C:/Users/176996/Desktop/progetto/edited_hh104_weekends.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 7:
        Path="C:/Users/176996/Desktop/progetto/edited_hh110_labour.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    elif i3 == 8:
        Path = "C:/Users/176996/Desktop/progetto/edited_hh110_weekends.xes"
        # Just used to remind the main control commands
        print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    else:
        Path=""
        # Control for error
        print("Hey, it seems something went wrong, restart the program")

    return Path

if __name__ == "__main__":
    os.environ["PATH"] += os.pathsep + 'C:/Programmi/Graphviz/bin/'
    i = 0
    Path = Input_Log()
    print("Type 1 for Heuristic miner, type 2 for Inductive miner, type 3 for Process Map , type 4 to change log,type 5 to close")
    print(Path)
    while i == 0:
        i=int(input())
        if i == 1:
            Heuristic_mining(Path)
            i = 0
        if i == 2:
            Inductive_mining(Path)
            i = 0
        if i == 3:
            Process_Map(Path)
            i = 0
        if i == 4:
            Path = Input_Log()
            i = 0
        if i == 5:
            break