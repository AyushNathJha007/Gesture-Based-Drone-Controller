using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

namespace DroneController
{
    //[RequireComponent(typeof(ControllerBase))]
    public class Controller : ControllerBase
    {
        #region Variables
        [Header("Control Parameters")]
        [SerializeField] private float MinMaxPitch = 30f;
        [SerializeField] private float MinMaxRoll = 30f;
        [SerializeField] private float YawPow = 4f;
        [SerializeField] private float lerper = 2f;
        //public GameObject controller;
        private float yaw,finalPitch, finalYaw, finalRoll;

        private List<IEngine> engines = new List<IEngine>();
        #endregion
        // Start is called before the first frame update

        #region Main Methods
        void Start()
        {
            engines = GetComponentsInChildren<IEngine>().ToList<IEngine>();
        }

        #endregion

        #region Custom Functions
        protected override void SimulatePhysics()
        {
            SimulateControls();
            SimulateEngines();
        }

        protected virtual void SimulateControls()
        {
            float pitch = Input.GetAxis("Pitch") * MinMaxPitch;
            float roll = Input.GetAxis("Roll") * MinMaxRoll;
            yaw += Input.GetAxis("Horizontal") * YawPow;

            //float pitch = controller.GetComponent<ControlCommunicator>().pitch * MinMaxPitch;
            //float roll = controller.GetComponent<ControlCommunicator>().roll * MinMaxRoll;
            //yaw += controller.GetComponent<ControlCommunicator>().yaw * YawPow;

            finalPitch = Mathf.Lerp(finalPitch, pitch, Time.deltaTime * lerper);
            finalRoll = Mathf.Lerp(finalRoll, roll, Time.deltaTime * lerper);
            finalYaw = Mathf.Lerp(finalYaw, yaw, Time.deltaTime * lerper);
            Quaternion rotate = Quaternion.Euler(finalPitch, finalYaw, finalRoll);
            rb.MoveRotation(rotate);
        }

        protected virtual void SimulateEngines()
        {
            //rb.AddForce(Vector3.up * (rb.mass * Physics.gravity.magnitude));
            foreach(IEngine engine in engines)
            {
                engine.UpdateEngine(rb);
            }
        }
        #endregion
    }
}
