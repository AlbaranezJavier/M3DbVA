using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * Class that defines the properties of the objects that can be represented in the 3D environment.
 */
public class Classes
{
    public Color color;
    private float widthx, longz, hypo;

    public Classes(Color color, float widthx, float longz)
    {
        this.color = color;
        this.widthx = widthx;
        this.longz = longz;
        this.hypo = Mathf.Sqrt(Mathf.Pow(widthx, 2) + Mathf.Pow(longz, 2));
    }

    public float GetZ(float xz)
    {
        /*
         * Returns the estimated depth, depending on whether it is made wider or longer.
         */
        if (xz - widthx <= (longz-widthx)/2)
            return widthx;
        return longz;
    }
}
