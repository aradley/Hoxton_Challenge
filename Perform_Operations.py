### Dependencies ###
import argparse
import numpy as np
import sys
import ast
import copy
### Dependencies ###

### Move bars via operations functions ###

def Perform_Operations(Input_File = "Example_Input.txt", Output_File = "Output_Result.txt"):
    # Load Inpute File
    Input = np.loadtxt(Input_File,delimiter='\t',dtype='str')
    # Load dimensions (at present we don't actually use this)
    Dimension = int(Input[0,0])
    # Setup initial tube positions
    Positions = Input[1,0]
    Positions = ast.literal_eval(Positions)
    Positions = np.asarray([str(i) for i in Positions])
    # Setup Output
    Output = [np.array(["Initial Position","End Position"])]
    # Save initial positions
    Initial_Positions = copy.copy(Positions)
    # Setup operations
    Operations = np.delete(Input,np.array([0,1]),axis=0)
    # Perform a search for relevent operations regarding the current tube positions.
    # We are going to use this to skip over operations that don't interact with any tubes
    # therby avoiding loops. This should be more useful the larger the input number of
    # operations becomes.
    Relevent_Operations = np.empty(Positions.shape[0],dtype="object")
    for i in np.arange(Relevent_Operations.shape[0]):
        Relevent_Operations[i] = np.argwhere(Operations[:,0] == Positions[i])
    Closest_Operations = np.zeros(Positions.shape[0]).astype("i")
    # Now we will cycle through the operations, updating the Relevent_Operations object
    # when required.
    # This while loop will continue until all operations are gone. Hence ending with the while loop indicates
    # that there are still bars left in the rack.
    while Initial_Positions.shape[0] > 0: 
        # Identify the closest meaningful operation.
        for i in np.arange(Relevent_Operations.shape[0]):
            if Relevent_Operations[i].shape[0] > 0:
                Closest_Operations[i] = Relevent_Operations[i][0]
            else:
                # This states that currently there are no operations that could be applied to bar i.
                Closest_Operations[i] = Operations.shape[0] + 1
        Closest_Operation = np.min(Closest_Operations)
        # If all bars have no possible operations to be applied to them, then nothing will change and the
        # system is in its final state. Hence end the script and save the output.
        if np.sum(Closest_Operations) == ((Operations.shape[0] + 1) * Relevent_Operations.shape[0]):
            # Log the initial and final positions of the bars left in the rack.
            for i in np.arange(Initial_Positions.shape[0]):
                Output.append(np.array([Initial_Positions[i],Positions[i]]))
            # Save Output
            np.savetxt(Output_File,Output,delimiter='\t',fmt="%s")
            print("No remaining operations will change the tube arrangments.")
            # End
            return
        # If operations can be performed, take the colosest one to the current position and carry it out.
        Closest_Operation_Tube = int(np.where(Closest_Operations == Closest_Operation)[0])
        Operation = Operations[Closest_Operation,:]
        if Operation[2] == "(1)": # Perform Operation (1)
            Positions,Relevent_Operations, Closest_Operations, Output, Initial_Positions = Operation_1(Operation,Positions,Relevent_Operations,Closest_Operations,Output,Initial_Positions)
        if Operation[2] == "(2)": # Perform Operation (2)
            if np.isin(Operation[1],Positions) == 1: # If destination is already occupied.
                # Remove the first point from this vector of nearest operations as it is invalid, and try again.
                Relevent_Operations[Closest_Operation_Tube] = np.delete(Relevent_Operations[Closest_Operation_Tube],0)
            else: # Perform operation (2)
                Positions, Relevent_Operations, Operations = Operation_2(Operation,Positions,Relevent_Operations,Operations,Closest_Operation_Tube,Closest_Operation)
    print("All operations were completed.")
    # Save Output
    np.savetxt(Output_File,Output,delimiter='\t',fmt="%s")


def Operation_1(Operation,Positions,Relevent_Operations,Closest_Operations,Output,Initial_Positions): 
    # Operation (1) removes a tube from the rack. 
    # Identify tube to be removed.
    Remove_Tube = int(np.argwhere(Positions == Operation[0])[0])
    # Remove it from system.
    Positions =  np.delete(Positions,Remove_Tube)
    Relevent_Operations = np.delete(Relevent_Operations,Remove_Tube)
    Closest_Operations = np.delete(Closest_Operations,Remove_Tube)
    # Log the removal of the bar and it's initial position.
    Output.append(np.array([Initial_Positions[Remove_Tube],"Removed"]))
    Initial_Positions = np.delete(Initial_Positions,Remove_Tube)
    return Positions,Relevent_Operations,Closest_Operations,Output,Initial_Positions


def Operation_2(Operation,Positions,Relevent_Operations,Operations,Closest_Operation_Tube,Closest_Operation):
    # Operation (2) moves a tube from one position to another.  
    if np.isin(Operation[1],Positions) == 0:
        # Update the tubes position.
        Positions[Closest_Operation_Tube] = Operation[1]
        # Update Relevent_Operations based on tubes new position.
        Relevent_Operations[Closest_Operation_Tube] = np.argwhere(Operations[:,0]==Operation[1])
        # Truncate Operations so to reduce furture search time.
        Operations = np.delete(Operations,np.arange(Closest_Operation+1),axis=0)
            # Adjust Relevent_Operations to account for shift in distance when Operations was truncated.
        for i in np.arange(len(Relevent_Operations)):
            Relevent_Operations[i] = Relevent_Operations[i] - (Closest_Operation+1)
            Negative = np.where(Relevent_Operations[i] < 0)[0]
            if Negative.shape[0] > 0:
                Relevent_Operations[i] = np.delete(Relevent_Operations[i],Negative)
        return Positions,Relevent_Operations,Operations


###

parser = argparse.ArgumentParser(description='usage:  Perform_Operations.py --Input_File path --Output_File string')
parser.add_argument('--Input_File', help='Correctly formatted input file of operations',required=True,type=str)
parser.add_argument('--Output_File', help='File name of outputed results. Default is "Output_Result.txt"',default='Output_File.txt',type=str)

args = parser.parse_args()

Input_File=args.Input_File
Output_File=args.Output_File

Perform_Operations(Input_File, Output_File)

# Run with following:
#python Perform_Operations.py --Input_File "Example_Input.txt" --Output_File "Output_Result.txt"
