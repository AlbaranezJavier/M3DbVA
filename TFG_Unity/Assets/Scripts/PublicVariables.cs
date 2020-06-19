using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * Parameters required to process the message received by the customer
 */

public class PublicVariables
{
    [System.Serializable]
    public class Parameters
    {
        public float minDistance = 0.01f;
        public float maxDistance = 20f;
        public float fieldOfViewVertical = 54f;
        public float fieldOfViewHorizontal = 85f;
        public float[] resolution = {1280f, 720f};
    }
}
