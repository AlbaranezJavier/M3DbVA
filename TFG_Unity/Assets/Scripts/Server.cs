using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;

internal class Server : MonoBehaviour
{
    /*
     * Clase encargada de gestionar las comunicaciones con otros entornos
     */
    private static int _port = 12345;
    public int port = 12345;

    private static ServerUser _serverUser;
    public ServerUser serverUser;

    private static bool debugging = true;
    private static bool isShutdown = false;
    private static Socket clientSocket;

    private void Start()
    {
        _port = port;
        _serverUser = serverUser;
        BuildServer();
        StartServer();
    }

    public static void BuildServer()
    {
        /*
         * Levanta el servidor en un puerto específico de esta máquina
         */
        IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddr = ipHost.AddressList[2];
        IPEndPoint localEndPoint = new IPEndPoint(ipAddr, _port);
        Socket listener = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            listener.Bind(localEndPoint);
            listener.Listen(50);
            Console.WriteLine("Waiting connection...");
            clientSocket = listener.Accept();
        }
        catch (Exception e)
        {
            Console.WriteLine(e.ToString());
        }
    }

    private static void ReceiveMsg(string data, byte[] bytes, int numByte, Socket clientSocket)
    {
        /*
         * Gestiona el mensaje recibido desde el cliente
         */
        data += Encoding.ASCII.GetString(bytes, 0, numByte);
        if (debugging) { print("Text received -> " + data); }
        if (data.Equals(""))
            Shutdown(clientSocket);
        else
        {
            _serverUser.Warning(data);
        }
    }

    private static void SendMsg(Socket clientSocket)
    {
        /*
         * Devuelve un mensaje de control al cliente
         */
        if (!isShutdown)
        {
            byte[] message = Encoding.ASCII.GetBytes("OK 200");
            clientSocket.Send(message);
        }
    }

    private static void Shutdown(Socket clientSocket)
    {
        /*
         * Controla que el cierre de comunicaciones con el cliente
         */
        isShutdown = true;
        clientSocket.Shutdown(SocketShutdown.Both);
        clientSocket.Close();
    }


    /*
     * Hilo encargado de gestionar las comunicaciones con el cliente de forma independiente
     */
    private void StartServer()
    {
        Thread myServerThread = new Thread(ServerThread);
        myServerThread.Start();
    }

    private void ServerThread()
    {
        while (!isShutdown)
        {
            byte[] bytes = new byte[1024];
            string data = null;

            int numByte = clientSocket.Receive(bytes);

            ReceiveMsg(data, bytes, numByte, clientSocket);

            SendMsg(clientSocket);
        }
    }
}

public abstract class ServerUser : MonoBehaviour
{
    public abstract void Warning(string msg);
}
