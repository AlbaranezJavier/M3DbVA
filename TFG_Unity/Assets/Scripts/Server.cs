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
     * Class in charge of managing communications with other environments
     */
    private static int _port = 12345;
    public int port = 12345;
    public string ip_address = "192.168.1.1";
    private static string _ip_address = "192.168.1.1";
    private static ServerUser _serverUser;
    public ServerUser serverUser;

    private static bool debugging = true;
    private static bool isShutdown = false;
    private static Socket clientSocket;

    private void Start()
    {
        _port = port;
        _ip_address = ip_address;
        _serverUser = serverUser;
        BuildServer();
        StartServer();
    }

    public static void BuildServer()
    {
        /*
         * Pick up the server on a specific port on this machine
         */
        IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddr = IPAddress.Parse(_ip_address);
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
         * Manages the message received from the client
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
         * Returns a control message to the customer
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
         * Controls that the closing of communications with the client
         */
        isShutdown = true;
        clientSocket.Shutdown(SocketShutdown.Both);
        clientSocket.Close();
    }


    /*
     * Thread to manage communications with the client independently
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
