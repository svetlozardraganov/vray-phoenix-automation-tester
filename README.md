# V-Ray/Phoenix GUI automation build tester
Automation GUI tester software for end to end test of V-Ray and Phoenix products of Chaos. The main focus is to ensure the basic functionality of V-Ray/Phoenix works as expected. The software also captures the tests on video, that could be quite handy in case of additional troubleshooting.

Here is short list of the automated process:

__V-Ray for 3ds Max automation procedure__:
1. Install V-Ray
2. Launch 3ds Max
3. Create a sample scene in 3ds Max
4. Render the scene within 3ds Max with:
    * V-Ray CPU Production
    * V-Ray CPU IPR
    * V-Ray GPU CUDA Production
    * V-Ray CPU CUDA IPR
9. Export .vrscene for V-Ray Standalone Rendering
10. Render exported .vrscene in V-Ray Standalone with:
    * V-Ray CPU Production
    * V-Ray CPU IPR
    * V-Ray GPU CUDA IPR

__Phoenix for 3ds Max automation procedure__:
1. Install Phoenix
2. Launch 3ds Max
3. Create sample Phoenix fire scene in 3ds Max
4. Run Phoenix fire simulation
5. Render the scene in 3ds Max
6. Create sample Phoenix liquid scene in 3ds Max
7. Run Phoenix liquid simulation
8. Render the scene in 3ds Max

# Challenges

# Technology
* SikuliX - most of the code is written SikuliX IDE.
* Python - some part of the code are implemented in Python due to SikuliX limitation.

# What I learned

# Demos/Examples
https://youtu.be/3r-NcAcDccQ

https://youtu.be/d8TIRa9wW4Y
