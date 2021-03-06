﻿using UnityEngine;
using System.Globalization;
using System.Collections.Generic;
using System.Collections.Concurrent;

public class ServerTest : ServerUser
{
    private static Queue<string> serverQueue = new Queue<string>();
    public static BlockingCollection<string> clientQueue = new BlockingCollection<string>(new ConcurrentQueue<string>(), 1);

    public void Start()
    {
        print("Ejecutando prueba en el servidor");
    }

    public void Update()
    {
        if (serverQueue.Count > 0)
        {
            string _msg = serverQueue.Dequeue();
            if (_msg.Equals("hola\n"))
                clientQueue.Add("hi");
            else if (_msg.Equals("adios\n"))
                clientQueue.Add("bye");
        }
    }

    public override void Receive_msg(string msg)
    {
        serverQueue.Enqueue(msg);
    }

    public override string Send_msg()
    {
        return clientQueue.Take();
    }
}
