using UnityEngine;
using System.Globalization;
using System.Collections.Generic;

public class Factory_floor : ServerUser
{ 
    /*
    * Modificación de la clase Factory, donde se pinta un suelo y los objetos a nivel de este,
    * con el requisito de representar una planicie y que el horizonte del suelo se encuentre
    * centrado a mitad de altura de la imagen.
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

    // Parámetros del mensaje
    private float px, py, depth, pw, ph, rot;

    // Parámetros de posición, rotación, tamaño y color
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
     * Inicializa las variables fijas necesarias para procesar cada mensaje. 
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
     * Para cada fotograma y si hay un mensaje desde el cliente, se procesa y se pintan los objetos que contuviera.
     */
    private void ProcessMSGV10()
    {
        // Si hay nuevos mensajes del cliente los procesa
        if (frames2Draw.Count > 0)
        {
            ClearScene();
            string frame = frames2Draw.Dequeue();
            // Si el mensaje recibido es 'empty' no pinta nada (Yolo no habrá detectado nada)
            if (!frame.Equals("empty"))
            {
                int i = 0;
                string[] newobjects = frame.Split(',');
                string[] obj_params;
                int len = newobjects.Length - 1;
                // Para cada objeto en el mensaje
                while (i < len)
                {
                    obj_params = newobjects[i].Split(' ');
                    // Extrae la información del cliente
                    pw = float.Parse(obj_params[3], ci);
                    ph = float.Parse(obj_params[4], ci);
                    px = float.Parse(obj_params[1], ci);
                    py = float.Parse(obj_params[2], ci);
                    depth = float.Parse(obj_params[5], ci);
                    rot = float.Parse(obj_params[6], ci);

                    // Distancia
                    dist = parameters.minDistance + ((maxGrayScale - depth) * parameters.maxDistance) / maxGrayScale;
                    // Escala
                    x = pw / fdH * dist;
                    y = ph / fdV * dist;
                    z = classes.ContainsKey(obj_params[0]) ? classes[obj_params[0]].GetZ(x) : classes["default"].GetZ(x);
                    scale = new Vector3(x, y, z);
                    // Distancia
                    dist += scale.z / 2; // Profundidad del objeto estimado
                    // Posición del objeto
                    z = Mathf.Cos(Mathf.Atan(px / fdH)) * dist;
                    x = px / fdH * z;
                    y = scale.y / 2;
                    pos = new Vector3(x + camera.transform.position.x, y, z + camera.transform.position.z);
                    // Rotacion
                    y = Mathf.Atan(px / fdH) * Mathf.Rad2Deg;
                    rotation = new Vector3(0, y + rot, 0);

                    // Pinta el objeto en el entorno 3D
                    GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
                    cube.transform.position = pos;
                    cube.transform.localScale = scale;
                    cube.transform.localEulerAngles = rotation;
                    // Da un color al objeto según su clase
                    m_Renderer = cube.GetComponent<Renderer>();
                    m_Renderer.material.color = classes.ContainsKey(obj_params[0]) ? classes[obj_params[0]].color : classes["default"].color;

                    // Se agrega el objeto a la lista para poder limpiarlo
                    objectsList.Add(cube);
                    i++;
                }
            }
        }
    }


    /*
     * Limpia los objetos de la escena almacenados en la lista "objectsList".
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
