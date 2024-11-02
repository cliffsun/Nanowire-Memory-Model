## Nanowire Critical Current Model

This is a critical current model for multiple parallel superconducting nanowires bridging the gap between two superconducting electrodes. This model incorporates multiple vortex configurations, so the metastability nature of a nanowire memory device is predicted by this model. 

### Assumptions

This model assumes that each nanowires as a certain critical phase difference that it can support, and phase differences above that are assumed to turn the entire device normal. Phase slips are not included in this model, but can incoroporated in the future. 

### Requirements

To run the program, you must have the following installed: 
<ul>
    <li>g++: a C++ compiler</li>
    <li>Python</li>
    <li>Python Packages: numpy, pandas, & matplotlib</li>
</ul>

### How To Use

Clone the repository on your local machine. Then click on ic.bat and customize the values for geometry of the nanowires, its critical phases, and vortex states. After you're done, run ./ic.bat in the terminal when you've entered the Nanowire-Memory-Model directory. 

### How to set Vortex States

In the ic.bat file, the user has 2+ degrees of freedom. The first two would be the geometry of the wires (e.g. "0 0.5 1") and critical phases (e.g. "12 12 12"). If after "0 0.5 1" "12 12 12", the strings that follow are "0 1" "2 1", then those strings would be interpreted as the vortex states with the first number corresponding to the vortex trapped between wires "0 0.5", etc. If no string is present, then the program autocalculates the combinations of all possible vortex states within the range of -5 to 5 (this is hard coded). Note, the # of vortex states must be (# wires - 1). 

