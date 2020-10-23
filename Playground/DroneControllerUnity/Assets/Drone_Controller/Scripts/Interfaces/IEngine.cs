using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace DroneController
{

    public interface IEngine
    {
        void InitializeEngine();

        void UpdateEngine(Rigidbody rb);
    }
}
