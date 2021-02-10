# Hoxton Challenge
This repository contains my solution to a coding challenge.

### The challenge is described by the following:

Consider a square rack of size N. Each position can either be empty or be
occupied by a tube. The position of a tube is defined by an x-coordinate and
a y-coordinate. Once the initial state of the rack is set up, any number of operations
can occur. There are two types of operations:

Remove a tube:
Specified by a position. If the position is occupied, that tube is
removed and the position can be occupied by another tube. If there is no tube,
nothing happens.

Move a tube to another position:
Specified by an initial position and a final position. Two tubes
cannot occupy the same position at the end of a move operation.

Given the initial state of a rack and a series of operations, output the
final state of the rack (the position of all tubes and whether they have
been removed or not). The input should be a file and the output stored in
another file.

### Description of my solution
I decided to try and avoid looping over every operation given in the input file, so to try and reduce runtime. To achieve this the script does an initial search for operations that have the starting positions of current tube positions and notes where these occur. I then jump from each applicable argument to the next, skipping over operations that will make no difference to the arrangement. 
As a consequence, each time a bar does successful move, the relevent operations for that tube must be updated. This adds a slight overhead to the script as it has to search all the operations again for that tubes new position. Hence, I have created code that is likely slower for dense systems where the number of bars approaches the number of spaces in the rack. However, it should be far quicker for sparse situations where there are many operations in the input file that have no affect on the arrangement of the tubes. Honestly, I mainly did it this way because this is the first problem in a while I've had to tackle that was nothing like my research and just stepping through the operations seemed unimaginative. 

Also a quick note on the input file. Operations have been tagged as operation (1) or (2). This is to allow the easy integration of new operations. The benfits of this would be for example an operation (3) that switched the postitions of two tubes. Similar to (2), this would have a start and end position and so you would no longer be able to rely just on the fact that there were two provided co-ordinates.

### Usage
##### Retreive the ripository
`git clone https://github.com/aradley/Hoxton_Challenge`

##### Create Example Input_File
I provide script, Generate_Example_Input.py, to generate example input operations in the correct format.

To run, be in the directory and execute the following on the command line:

`python Generate_Example_Input.py --Rack_Dimensions 1000 --Initial_Num_Tubes 100 --Num_Operations 100000 --Operation_1_Probability 0.2 --Operation_2_Probability 0.8`

You may change each of the variables by changing the numbers as desired. Operation_1_Probability and Operation_2_Probability dictate the likelyhood of the operations being generated being a remove tube operations (1) or move tube operation (2). These must sum to equal 1. 

The output file is a .txt file with 3 columns and Number_Operations + 2 rows. The first row designates the Rack_Dimensions and the second row the starting positions of the tubes. The third column designates whether the operation for a particular row is operation (1) or operation (2).

##### Perform Operations
With any given correctly formatted Input_File, you can then run the following code to output the final positions of the tubes.

`python Perform_Operations.py --Input_File "Example_Input.txt" --Output_File "Output_Result.txt"`

Change "Example_Input.txt" to the path of your input file if necessary. Change "Output_Result.txt" to any file name you would like, as long as it ends with .txt 

The output is a .txt file with two columns. The first column states the initial position of the tube, and the second column states the final position.

#### Dependencies
`numpy`







