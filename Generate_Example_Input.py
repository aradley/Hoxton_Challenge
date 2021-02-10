### Dependencies ###
import argparse
import numpy as np
### Dependencies ###

### Create Example Input ###

def Create_Example_Input(Rack_Dimensions,Initial_Num_Tubes,Num_Operations,Operation_1_Probability,Operation_2_Probability,File_Name="Example_Input"):
    if np.sum(Operation_1_Probability+Operation_2_Probability) != 1:
        raise ValueError("Operation probabilities must sum to 1.")
    if Initial_Num_Tubes > Rack_Dimensions**2:
        raise ValueError("Number of initial tubes must be smaller than the rack.")
    # Set up output array
    Output = np.empty(((Num_Operations + 2),3),dtype="object")
    # Provide Rack Dimensions
    Output[0,0] = Rack_Dimensions
    # Provide initial tube positions
    Inds = np.random.choice(Rack_Dimensions**2, Initial_Num_Tubes, replace=False)
    Inds = np.unravel_index(Inds, (Rack_Dimensions,Rack_Dimensions))
    Inds = np.stack((Inds[0],Inds[1]))
    Output[1,0] = list(zip(Inds[0],Inds[1]))
    ## Provide Operations
    # Set operation types, where (1) is the removal operation and (2) is the movement operation.
    Operation_Probabilites = np.array([Operation_1_Probability,Operation_2_Probability])
    Operations = np.random.choice(("(1)","(2)"), p=Operation_Probabilites, size= Num_Operations)
    # Assign Operations (1)
    Inds = np.where(Operations == "(1)")[0]
    Operation_Inds = np.random.choice(Rack_Dimensions**2, Inds.shape[0])
    Operation_Inds = np.unravel_index(Operation_Inds, (Rack_Dimensions,Rack_Dimensions))
    Operation_Inds = np.stack((Operation_Inds[0],Operation_Inds[1]))
    Output[(Inds+2),0] = list(zip(Operation_Inds[0],Operation_Inds[1]))
    # Note operation type
    Output[(Inds+2),2] = "(1)"
    # Assign Operations (2)
    # Set start point
    Inds = np.where(Operations == "(2)")[0]
    Operation_Inds = np.random.choice(Rack_Dimensions**2, Inds.shape[0])
    Operation_Inds = np.unravel_index(Operation_Inds, (Rack_Dimensions,Rack_Dimensions))
    Operation_Inds = np.stack((Operation_Inds[0],Operation_Inds[1]))
    Output[(Inds+2),0] = list(zip(Operation_Inds[0],Operation_Inds[1]))
    # Repeat for destination
    Operation_Inds = np.random.choice(Rack_Dimensions**2, Inds.shape[0])
    Operation_Inds = np.unravel_index(Operation_Inds, (Rack_Dimensions,Rack_Dimensions))
    Operation_Inds = np.stack((Operation_Inds[0],Operation_Inds[1]))
    Output[(Inds+2),1] = list(zip(Operation_Inds[0],Operation_Inds[1]))
    # Note operation type 
    Output[(Inds+2),2] = "(2)"
    # Save Output
    np.savetxt(File_Name+'.txt',Output,delimiter='\t',fmt="%s")


parser = argparse.ArgumentParser(description='usage:  Generate_Example_Input.py --Rack_Dimensions Number --Initial_Num_Tubes Number --Num_Operations Number --Operation_1_Probability Number --Operation_2_Probability Number')
parser.add_argument('--Rack_Dimensions', help='Dimension of the rack.',required=True,type=int)
parser.add_argument('--Initial_Num_Tubes', help='Starting number of tubes.',required=True,type=int)
parser.add_argument('--Num_Operations', help='Number of input operations',required=True,type=int)
parser.add_argument('--Operation_1_Probability', help='Operation (1) probability',required=True,type=float)
parser.add_argument('--Operation_2_Probability', help='Operation (2) probability',required=True,type=float)
args = parser.parse_args()

Rack_Dimensions=args.Rack_Dimensions
Initial_Num_Tubes=args.Initial_Num_Tubes
Num_Operations=args.Num_Operations
Operation_1_Probability=args.Operation_1_Probability
Operation_2_Probability=args.Operation_2_Probability

Create_Example_Input(Rack_Dimensions,Initial_Num_Tubes,Num_Operations,Operation_1_Probability,Operation_2_Probability,File_Name="Example_Input")

# # Example inputs
# Rack_Dimensions = 1000
# Initial_Num_Tubes = 100
# Num_Operations = 100000
# Operation_1_Probability = 0.5
# Operation_2_Probability = 0.5

# Run with following:
#python Generate_Example_Input.py --Rack_Dimensions 1000 --Initial_Num_Tubes 100 --Num_Operations 100000 --Operation_1_Probability 0.2 --Operation_2_Probability 0.8
