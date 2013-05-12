#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define QR_DIST 1500.0
 
/*  
    
    This function sets the 2x4 matrix corresponding to the
    coefficients of x and y respetively, with respect to 
    the 3-degree Bezier curve for the input points.

*/

void bezier (double x[4], double y[4], double coeff[2][4])
{
    coeff[0][0] = x[0];
    coeff[0][1] = 3 * (x[1] - x[0]);
    coeff[0][2] = 3 * (x[0] + x[2] - (2 * x[1]));
    coeff[0][3] = (3 * x[1] - x[0] - 3 * x[2] + x[3]);

    coeff[1][0] = y[0];
    coeff[1][1] = 3 * (y[1] - y[0]);
    coeff[1][2] = 3 * (y[0] + y[2] - (2 * y[1]));
    coeff[1][3] = (3 * y[1] - y[0] - 3 * y[2] + y[3]);

    return;
}
 
int main()
{
    double x[4], y[4];
    double coeff[2][4];
    double del_theta, del_d;

    printf("\nEnter delta-theta and delta-d: ");
    scanf("%lf %lf", &del_theta, &del_d);
    del_theta = M_PI / 180.0 * del_theta;

    x[0] = del_d;
    y[0] = 0.0;

    x[1] = (del_d > 0) ? (del_d + (QR_DIST / 2) * tan(del_theta)) :
                         (del_d - (QR_DIST / 2) * tan(del_theta));
    y[1] = QR_DIST / 2;

    x[2] = 0.0;
    y[2] = QR_DIST / 2;

    x[3] = 0.0;
    y[3] = QR_DIST;

    bezier(x, y, coeff);

    printf("%f %f %f %f\n", coeff[0][0], coeff[0][1], coeff[0][2], coeff[0][3]);
    printf("%f %f %f %f\n", coeff[1][0], coeff[1][1], coeff[1][2], coeff[1][3]);
}