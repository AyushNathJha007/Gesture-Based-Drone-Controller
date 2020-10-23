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
