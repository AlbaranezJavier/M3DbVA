using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * Clase que define las propiedades del los objetos representables en el entorno 3D.
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
         * Devuelve la profundidad estimada, dependiendo de si se hacerca más al ancho o al largo.
         */
        if (xz - widthx <= (longz-widthx)/2)
            return widthx;
        return longz;
    }
}
