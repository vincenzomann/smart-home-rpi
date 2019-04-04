#include <wiringPi.h>
#include <pcf8591.h>
#include <stdio.h>

// ADC

#define Address 0x48         //pcf8591 address 
#define BASE 64
#define A0 BASE+0           //A0 input
#define A1 BASE+1           //A1 input
#define A2 BASE+2           //A2 input
#define A3 BASE+3           //A3 input

int main(void)
{
    unsigned char value;
	wiringPiSetup();
	pcf8591Setup(BASE,Address);        //configurationpcf8591
	
	while(1)
	{
               value=analogRead(A0);     // read A0 value          
               printf("A0:%d\n",value);  // print A0 value
               delay(100);	
	}
    return 0;
}