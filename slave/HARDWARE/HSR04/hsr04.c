//���������
 
#include "hcsr04.h"
#include "delay.h"
#include "stm32f10x.h"

#define HCSR04_PORT     GPIOB
#define HCSR04_CLK      RCC_APB2Periph_GPIOB
#define HCSR04_TRIG     GPIO_Pin_5
#define HCSR04_ECHO     GPIO_Pin_6
 
#define TRIG_Send  PBout(5) 
#define ECHO_Reci  PBin(6)
 
u16 msHcCount = 0;//ms����
 
void Hcsr04Init()
{  
    TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;     //�������ڶ�ʱ�����õĽṹ��
    GPIO_InitTypeDef GPIO_InitStructure;
    RCC_APB2PeriphClockCmd(HCSR04_CLK, ENABLE);
     
        //IO��ʼ��
    GPIO_InitStructure.GPIO_Pin =HCSR04_TRIG;       //���͵�ƽ����
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;//�������
    GPIO_Init(HCSR04_PORT, &GPIO_InitStructure);
    GPIO_ResetBits(HCSR04_PORT,HCSR04_TRIG);
     
    GPIO_InitStructure.GPIO_Pin =   HCSR04_ECHO;     //���ص�ƽ����
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;//��������
    GPIO_Init(HCSR04_PORT, &GPIO_InitStructure);  
		GPIO_ResetBits(HCSR04_PORT,HCSR04_ECHO);	
	 
			//��ʱ����ʼ�� ʹ�û�����ʱ��TIM3
		RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE);  //ʹ�ܶ�ӦRCCʱ��
		//���ö�ʱ�������ṹ��
		TIM_DeInit(TIM3);
		TIM_TimeBaseStructure.TIM_Period = (1000-1); //��������һ�������¼�װ�����Զ���װ�ؼĴ������ڵ�ֵ         ������1000Ϊ1ms
		TIM_TimeBaseStructure.TIM_Prescaler =(72-1); //����������ΪTIMxʱ��Ƶ�ʳ�����Ԥ��Ƶֵ  1M�ļ���Ƶ�� 1US����
		TIM_TimeBaseStructure.TIM_ClockDivision=TIM_CKD_DIV1;//����Ƶ
		TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;  //TIM���ϼ���ģʽ
		TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure); //����TIM_TimeBaseInitStruct��ָ���Ĳ�����ʼ��TIMx��ʱ�������λ		 
		
		TIM_ClearFlag(TIM3, TIM_FLAG_Update);   //��������жϣ����һ���ж����������ж�
		TIM_ITConfig(TIM3,TIM_IT_Update,ENABLE);    //�򿪶�ʱ�������ж�
		hcsr04_NVIC();
    TIM_Cmd(TIM3,DISABLE);     
}
 
 
//tips��static����������������ڶ�������Դ�ļ��ڣ����Բ���Ҫ��ͷ�ļ�������
static void OpenTimerForHc()        //�򿪶�ʱ��
{
        TIM_SetCounter(TIM3,0);//�������
        msHcCount = 0;
        TIM_Cmd(TIM3, ENABLE);  //ʹ��TIMx����
}
 
static void CloseTimerForHc()        //�رն�ʱ��
{
        TIM_Cmd(TIM3, DISABLE);  //ʹ��TIMx����
}
 
 
 //NVIC����
void hcsr04_NVIC()
{
   NVIC_InitTypeDef NVIC_InitStructure;							//�ж����ȼ�NVIC����
	
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); 				//����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�
	
	NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;  				//TIM3�ж�
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;  		//��ռ���ȼ�0��
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;  			//�����ȼ�3��
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; 				//IRQͨ����ʹ��
	NVIC_Init(&NVIC_InitStructure);  	
}
 
 
void TIM3_IRQHandler(void)   										//TIM3�ж�
{
	if (TIM_GetITStatus(TIM3, TIM_IT_Update) != RESET)  			//���TIM3�����жϷ������
		{
			msHcCount++;
			TIM_ClearITPendingBit(TIM3, TIM_IT_Update  ); 				//���TIMx�����жϱ�־ 
		}
}
 
 
 
//��ȡ��ʱ��ʱ��
u32 GetEchoTimer(void)
{
        u32 t = 0;
        t = msHcCount*1000;//�õ�MS
        t += TIM_GetCounter(TIM3);//�õ�US
	      TIM3->CNT = 0;  //��TIM2�����Ĵ����ļ���ֵ����
				delay_ms(50);
        return t;
}
 
 float lengthTemp[5];
//һ�λ�ȡ������������� ���β��֮����Ҫ���һ��ʱ�䣬���ϻ����ź�
//Ϊ�����������Ӱ�죬ȡ������ݵ�ƽ��ֵ���м�Ȩ�˲���
void Hcsr04GetLength(void )
{
		u32 t = 0;
		int i = 0;
		float sum = 0;
		while(i!=5)
		{
		TRIG_Send = 1;      //���Ϳڸߵ�ƽ���
		delay_us(20);
		TRIG_Send = 0;
		while(ECHO_Reci == 0);      //�ȴ����տڸߵ�ƽ���
			OpenTimerForHc();        //�򿪶�ʱ��
			while(ECHO_Reci == 1);
			CloseTimerForHc();        //�رն�ʱ��
			t = GetEchoTimer();        //��ȡʱ��,�ֱ���Ϊ1US
			lengthTemp[i] = t/58.0;//cm
		//	printf("%f\r\n",lengthTemp[i]);
			i = i + 1;
	   }
}
 
