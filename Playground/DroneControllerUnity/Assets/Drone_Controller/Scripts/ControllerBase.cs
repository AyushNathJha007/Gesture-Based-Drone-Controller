using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace DroneController
{

    [RequireComponent(typeof(Rigidbody))]

    public class ControllerBase : MonoBehaviour
    {
        #region Variables
        [Header("RigidBody Parameters")]
        [SerializeField]private float weight = 1.0f;
        protected Rigidbody rb;
        #endregion
        // Start is called before the first frame update

        #region Main Functions

        void Awake()
        {
            rb = this.gameObject.GetComponent<Rigidbody>();
            if(rb)
            {
                rb.mass = weight;
            }
        }

        // Update is called once per frame
        void FixedUpdate()
        {
            if (!rb)
                return;

            SimulatePhysics();
        }
        #endregion

        #region Custom Functions

        protected virtual void SimulatePhysics() { }

        #endregion
    }
}
