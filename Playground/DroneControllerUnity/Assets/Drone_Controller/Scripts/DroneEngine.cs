using System.Collections;
using System.Collections.Generic;
using UnityEngine;


namespace DroneController
{
    public class DroneEngine : MonoBehaviour,IEngine
    {


        #region Variables
        [Header("Engine Parameters")]
        [SerializeField] private float EngineMaxPower = 4f;
        #endregion

        #region Interface Functions

        public void InitializeEngine()
        {
            throw new System.NotImplementedException();
        }

        public void UpdateEngine(Rigidbody rb)
        {
            //throw new System.NotImplementedException();
            //Debug.Log("Running " + gameObject.name);

            Vector3 EngineForce = Vector3.zero;
            EngineForce = transform.up * ((rb.mass * Physics.gravity.magnitude) + (Input.GetAxis("Vertical") * EngineMaxPower)) / 2f;
            rb.AddForce(EngineForce, ForceMode.Force);
        }

        #endregion
    }
}
