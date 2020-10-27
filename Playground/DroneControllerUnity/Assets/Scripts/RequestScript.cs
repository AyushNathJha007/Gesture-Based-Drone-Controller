using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

public class RequestScript : RunAbleThread
{
    public string message = null;
    public bool forceExit = false;
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");

            while(Running)
            {
                Debug.Log("Sending Hello");
                client.SendFrame("Hello");
                // ReceiveFrameString() blocks the thread until you receive the string, but TryReceiveFrameString()
                // do not block the thread, you can try commenting one and see what the other does, try to reason why
                // unity freezes when you use ReceiveFrameString() and play and stop the scene without running the server
                //                string message = client.ReceiveFrameString();
                //                Debug.Log("Received: " + message);
                message = null;
                bool gotMessage = false;
                while (Running)
                {
                    gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                    if (gotMessage) break;
                }

                if (gotMessage) Debug.Log("Received " + message);
                if (forceExit)
                {
                    client.SendFrame("Stop");
                    break;
                }

            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}
