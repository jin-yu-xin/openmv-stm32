#ifndef __HCSRO4_H
#define __HCSR04_H	
#include "sys.h" 

void Hcsr04Init();
static void OpenTimerForHc();
static void CloseTimerForHc();
void hcsr04_NVIC();
u32 GetEchoTimer(void);
void Hcsr04GetLength(void);

#endif  