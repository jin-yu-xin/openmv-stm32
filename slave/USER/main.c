//////////////////////////////////////////////////////////////////////////////////////
//              ˵��: 
//              ----------------------------------------------------------------
//              GND   ��Դ��
//              VCC   ��5V��3.3v��Դ
//              SCL   ��PD6��SCL��
//              SDA   ��PD7��SDA��            
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
extern unsigned char data_string[5][9];//�����ַ���
extern float data[5];
extern float lengthTemp[5];

 int main(void)
  {	
		float length;
    unsigned char distance[9];
		delay_init();	    	 //��ʱ������ʼ��	  
		NVIC_Configuration(); 	 //����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ� 	LED_Init();			     //LED�˿ڳ�ʼ��
	
		uart1_init(19200);
    uart3_init(19200);
		OLED_Init();			//��ʼ��OLED  
		OLED_Clear();
    Hcsr04Init();		
	
		//t=' ';
		
	while(1) 
	{		
		int i=0,j=0;
		OLED_Clear();
		
		Hcsr04GetLength();
		length=(lengthTemp[0]+lengthTemp[1]+lengthTemp[2]+lengthTemp[3]+lengthTemp[4])/5.0;
		//printf("����Ϊ:%.3f\n",length);
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
		
		OLED_ShowString(0,0,"length: ",8);//������߳�
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(65+7*i,0,data_string[0][i],12);
		}

		OLED_ShowString(0,1,"shape: ",7); //��״
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(55+7*i,1,data_string[1][i],12);
		}
		
		OLED_ShowString(0,2,"dist: ",6); //����
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(57+7*i,2,distance[i],12);
		}
		
		OLED_ShowString(0,3,"focus: ",7); //���ĵ�
		
    OLED_ShowString(0,4,"x : ",4); //���ĵ�x����
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(30+7*i,4,data_string[3][i],12);
		}
		
	  OLED_ShowString(0,5,"y : ",4); //���ĵ�y����
		for(i=0;i<8;i++)
		{
		   OLED_ShowChar(30+7*i,5,data_string[4][i],12);
		}
		delay_ms(1000);
	
		
	}	  
	
}
	