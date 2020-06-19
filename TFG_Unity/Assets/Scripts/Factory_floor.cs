using UnityEngine;
using System.Globalization;
using System.Collections.Generic;

public class Factory_floor : ServerUser
{
    /*
    * Modification of the Factory class, where a floor is painted and the objects at that height,
    * with the requirement to represent a plain and that the horizon of the floor is centered halfway up the image.
    */
    public PublicVariables.Parameters parameters;
    public Camera camera;
   
    private readonly Dictionary<string, Classes> classes = new Dictionary<string, Classes>()
        {
            { "person", new Classes(Color.blue, 0.5f, 0.5f)},
            { "car", new Classes(Color.red, 4.5f, 2f)},
            { "default", new Classes(Color.white, 0.5f, 0.5f)}
        };
    private Queue<string> frames2Draw = new Queue<string>();
    private List<GameObject> objectsList = new List<GameObject>();
    private CultureInfo ci = CultureInfo.InvariantCulture;
    private float fdH, fdV;
    private float maxGrayScale = 255f;

    // Message parameters
    private float px, py, depth, pw, ph, rot;

    // Position, rotation, size and color parameters
    private float x, y, z, dist;
    private Vector3 pos, scale, rotation;
    private Renderer m_Renderer;

    internal void Start()
    {
        InitVariables();
    }

    internal void Update()
    {
        ProcessMSGV10();
    }

    /*
     * It initializes the fixed variables required to process each message.
     */
    private void InitVariables()
    {
        float aspect = parameters.resolution[1] / parameters.resolution[0];
        fdH = parameters.resolution[0] * 0.5f / Mathf.Tan(Mathf.Deg2Rad * parameters.fieldOfViewHorizontal * 0.5f);
        fdV = parameters.resolution[1] * 0.5f / Mathf.Tan(Mathf.Deg2Rad * parameters.fieldOfViewVertical * 0.5f);
        print("Focal Depth Horizontal: " + fdH);
        print("Focal Depth Vertical: " + fdV);
        camera.fieldOfView = parameters.fieldOfViewVertical;
    }

    /*
     * For each frame and if there is a message from the client, the objects it contains are processed and painted.
     */
    private void ProcessMSGV10()
    {
        // If there are new messages from the customer it process them
        if (frames2Draw.Count > 0)
        {
            ClearScene();
            string frame = frames2Draw.Dequeue();
            // If the message received is empty, Yolo will not have detected anything
            if (!frame.Equals("empty"))
            {
                int i = 0;
                string[] newobjects = frame.Split(',');
                string[] obj_params;
                int len = newobjects.Length - 1;
                // For each object in the message
                while (i < len)
                {
                    obj_params = newobjects[i].Split(' ');
                    // Extract customer information
                    pw = float.Parse(obj_params[3], ci);
                    ph = float.Parse(obj_params[4], ci);
                    px = float.Parse(obj_params[1], ci);
                    py = float.Parse(obj_params[2], ci);
                    depth = float.Parse(obj_params[5], ci);
                    rot = float.Parse(obj_params[6], ci);

                    // Distance
                    dist = parameters.minDistance + ((maxGrayScale - depth) * parameters.maxDistance) / maxGrayScale;
                    // Escale
                    x = pw / fdH * dist;
                    y = ph / fdV * dist;
                    z = classes.ContainsKey(obj_params[0]) ? classes[obj_params[0]].GetZ(x) : classes["default"].GetZ(x);
                    scale = new Vector3(x, y, z);
                    // Distance
                    dist += scale.z / 2; // Estimated object depth
                    // Object position
                    z = Mathf.Cos(Mathf.Atan(px / fdH)) * dist;
                    x = px / fdH * z;
                    y = scale.y / 2;
                    pos = new Vector3(x + camera.transform.position.x, y, z + camera.transform.position.z);
                    // Rotation
                    y = Mathf.Atan(px / fdH) * Mathf.Rad2Deg;
                    rotation = new Vector3(0, y + rot, 0);

                    // Paint the object in the 3D environment
                    GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
                    cube.transform.position = pos;
                    cube.transform.localScale = scale;
                    cube.transform.localEulerAngles = rotation;
                    // It gives a color to the object according to its class
                    m_Renderer = cube.GetComponent<Renderer>();
                    m_Renderer.material.color = classes.ContainsKey(obj_params[0]) ? classes[obj_params[0]].color : classes["default"].color;

                    // The object is added to the list so that it can be cleaned
                    objectsList.Add(cube);
                    i++;
                }
            }
        }
    }


    /*
     * Cleans the objects of the scene stored in the list "objectsList".
     */
    private void ClearScene()
    {
        foreach(GameObject obj in objectsList)
        {
            DestroyImmediate(obj);
        }
        objectsList.Clear();
    }

    public override void Warning(string msg)
    {
        frames2Draw.Enqueue(msg);
    }
}
