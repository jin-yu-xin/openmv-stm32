//////////////////////////////////////////////////////////////////////////////////////
//              说明: 
//              ----------------------------------------------------------------
//              GND   电源地
//              VCC   接5V或3.3v电源
//              SCL   接PD6（SCL）
//              SDA   接PD7（SDA）            
//              ----------------------------------------------------------------
//All rights reserved
//////////////////////////////////////////////////////////////////////////////////

#include "delay.h"
#include "sys.h"
#include "oled.h"
#include "bmp.h"
#include "hsr04.h"
#include "stm32f10x.h"

//x:0~127
//y:0~63
extern unsigned char data_string[5][9];//接收字符串
extern float data[5];
extern float lengthTemp[5];

 int main(void)
  {	
		float length;
    unsigned char distance[9];
		delay_init();	    	 //延时函数初始化	  
		NVIC_Configuration(); 	 //设置NVIC中断分组2:2位抢占优先级，2位响应优先级 	LED_Init();			     //LED端口初始化
	
		uart1_init(19200);
    uart3_init(19200);
		OLED_Init();			//初始化OLED  
		OLED_Clear();
    Hcsr04Init();		
	
		//t=' ';
		
	while(1) 
	{		
		int i=0,j=0;
		OLED_Clear();
		
		Hcsr04GetLength();
		length=(lengthTemp[0]+lengthTemp[1]+lengthTemp[2]+lengthTemp[3]+lengthTemp[4])/5.0;
		//printf("距离为:%.3f\n",length);
		sprintf(distance,"%f",length);
    printf("%s\r\n",distance);
//   for(j=0;j<strlen(distance);j++)
//   {  		
//		  USART_SendData(USART3,distance[j]);
//   }
//		//get_message_from_openmv_and_send();
    get_message_from_openmv();
////		printf("data0:%s\r\n",data_string[0]);
////		printf("data1:%s\r\n",data_string[1]);
////		printf("data2:%s\r\n",data_string[2]);
////		printf("data3:%s\r\n",data_string[3]);
////		printf("data4:%s\r\n",data_string[4]);
		
		OLED_ShowString(0,0,"length: ",8);//被测物边长
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(65+7*i,0,data_string[0][i],12);
		}

		OLED_ShowString(0,1,"shape: ",7); //形状
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(55+7*i,1,data_string[1][i],12);
		}
		
		OLED_ShowString(0,2,"dist: ",6); //距离
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(57+7*i,2,distance[i],12);
		}
		
		OLED_ShowString(0,3,"focus: ",7); //中心点
		
    OLED_ShowString(0,4,"x : ",4); //中心点x坐标
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(30+7*i,4,data_string[3][i],12);
		}
		
	  OLED_ShowString(0,5,"y : ",4); //中心点y坐标
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(30+7*i,5,data_string[4][i],12);
		}
		delay_ms(1000);
	
		
	}	  
	
}
	