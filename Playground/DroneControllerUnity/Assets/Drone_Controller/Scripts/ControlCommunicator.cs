using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ControlCommunicator : MonoBehaviour
{
    private RequestScript _helloRequester;
    public float pitch = 0;
    public float yaw = 0;
    public float roll = 0;

    private void Start()
    {
        _helloRequester = new RequestScript();
        _helloRequester.Start();
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }

    private void Update()
    {
        if (_helloRequester.message == null)
            return;

        if (_helloRequester.message[0] == 'U')
            pitch = 1;
        else if (_helloRequester.message[0] == 'D')
            pitch = -1;
        else
            pitch = 0;

        if (_helloRequester.message[1] == 'L')
            yaw = -1;
        else if (_helloRequester.message[1] == 'R')
            yaw = 1;
        else
            yaw = 0;

        /*if (_helloRequester.message[2] == 'L')
            roll = 1;
        else if (_helloRequester.message[2] == 'R')
            roll = -1;
        else
            roll = 0;*/

        if (Input.GetKeyDown(KeyCode.E))
            _helloRequester.forceExit = true;
    }
}
