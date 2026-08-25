#ifndef __common_h__
#define __common_h__

#include <sys/time.h>

/*
 * Spin(n)
 *
 * Wait approximately n seconds.
 *
 * Use this helper function
 * so that the program prints once per second.
 */
void Spin(int howlong)
{
    struct timeval t;
    double t1 = 0.0;
    double t2 = 0.0;

    gettimeofday(&t, NULL);
    t1 = t.tv_sec + (t.tv_usec / 1000000.0);

    while (t2 - t1 < howlong) {
        gettimeofday(&t, NULL);
        t2 = t.tv_sec + (t.tv_usec / 1000000.0);
    }
}

#endif