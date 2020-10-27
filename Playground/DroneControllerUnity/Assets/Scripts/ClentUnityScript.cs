using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ClentUnityScript : MonoBehaviour
{
    private RequestScript _helloRequester;

    private void Start()
    {
        _helloRequester = new RequestScript();
        _helloRequester.Start();
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }
}
