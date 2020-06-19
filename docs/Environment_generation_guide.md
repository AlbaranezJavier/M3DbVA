# Guide for the generation of environments
This guide lists the steps required to make use of the tool developed in this project.

1. The following modules must be installed in the virtual Python environment (version 3.7): Tensorflow 2.1, opencv-python, absl-py, matplotlib, scikit-learn and numpy.
2. Open the project called TFG_Python and configure the interpreter with the previous virtual environment.
3. Download the weights of the pretrained neural network of [Yolo](https://pjreddie.com/darknet/yolo/), called YOLOv3-320 (YOLOv3-tiny is optional), in Repository/TFG_Python/data, renaming the file to yolov3-320.
4. In the directory Repository/TFG_Python/ is executed the file "convert.py", in charge of translating the weights to the format that the program needs and save them in the folder called "checkpoints".
5. Then, you must install the 2019.2.17f1 version with Unity Hub or from the [file](https://unity3d.com/get-unity/download/archive) to be able to open the Unity project that is in Repository/TFG_Unity.
6. You can choose between two versions ("server and server_floor", both in the "Scenes" folder of "Assets"), "server_floor" being a modification of "server" that generates a floor on which the models are located.
7. Check the IPv4 address of the equipment (execute in the system console the command "ipconfig" in Widnows or "ifconfig" in Linux/Max) and copy it to the "Ip_address" section of the server.
8. When you press the play button of Unity, the server is lifted and waits for the connection of the Python environment, where executing "detect_video.py" starts the process of model generation. The results are seen in Unity's environment, while Python's generates another window where you can see the images that are being processed at that moment.

## Documentation
In the Python environment there are 4 different versions for processing videos: "detect_video.py" applies all the exposed algorithms, "detect_video_wo_gl.py", "detect_video_wo_gl.py", "detect_video_wo_gl_r.py" and "detect_video_wo_r.py". The last 3 versions are modifications of the first one, where "gl" means that it does not adjust the frame rate and "r" that does not estimate the orientation of the models. While the version of "detect.py" only applies Yolo to an image, saving the result in the specified place and name.

In the Unity environment we can find the following adjustable parameters for the files "Factory, Factory_floor and Server":

- "Min Distance and Max Distance" determine the range of distance in which the objects of the simulation can be found.
- "Field Of View Vertical / Horizontal" and the resolution, are the parameters of the camera involved in the recording.
- Port is the port where the server will listen to the client's requests.

The Python environment has the following parameters:

- "weights" determines the directory where the weights of the neural network are located.
- "output" is the storage directory.
- "tiny" is a variable of boolean type. If its value is true, the "yolov3-tiny" version will be used in the execution.
- "classes" directory where there is a file with the classes to be detected by Yolo.
- "size" size to which the input images are resized.
- "image" specifies the place where the image or images to be processed are located, depending on the version of the program executed.
- "fps_record" is the frames per second at which the video was made.
- "x_resolution e y_resolution" is the resolution of the images to be processed.

[Back to the main page](../README.md)