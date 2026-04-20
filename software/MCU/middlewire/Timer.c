/********************************** (C) COPYRIGHT *******************************
 * File Name          : Timer.c
 * Author             : EERNINUO
 * Date               : 2026年1月
 * Description        : 定时器控制模块 - 气体检测系统学年设计项目
 * 
 * 功能说明：
 * 1. TIM2定时器控制数据采集频率
 * 2. 支持动态调整采样率（响应上位机指令）
 * 3. 串口中断处理上位机控制命令
 * 
 * 注意：沁恒RISC-V MCU需要使用WCH-Interrupt-fast中断属性
 * 
 * 许可证：GNU General Public License v3.0
 * 项目仓库：https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025
 *******************************************************************************/

#include "Timer.h"

void USART1_IRQHandler(void) __attribute__((interrupt("WCH-Interrupt-fast")));

// ... 后续代码
#include "Timer.h"

void USART1_IRQHandler(void) __attribute__((interrupt("WCH-Interrupt-fast")));

void Timer_Init(){
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);

    TIM_TimeBaseInitTypeDef timbase_InitStruct;
    timbase_InitStruct.TIM_ClockDivision= TIM_CKD_DIV1;
    timbase_InitStruct.TIM_CounterMode= TIM_CounterMode_Up;
    timbase_InitStruct.TIM_RepetitionCounter= 50;
    timbase_InitStruct.TIM_Period= 1000 - 1;
    timbase_InitStruct.TIM_Prescaler= 48000 - 1;
    TIM_TimeBaseInit(TIM2, &timbase_InitStruct);
    
    TIM_ClearITPendingBit( TIM2, TIM_IT_Update );

    NVIC_InitTypeDef nvic_InitStruct;
    nvic_InitStruct.NVIC_IRQChannel= TIM2_IRQn;
    nvic_InitStruct.NVIC_IRQChannelPreemptionPriority= 1;
    nvic_InitStruct.NVIC_IRQChannelSubPriority= 1;
    nvic_InitStruct.NVIC_IRQChannelCmd= ENABLE;
    NVIC_Init(&nvic_InitStruct);

    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE);
    TIM_Cmd(TIM2, ENABLE);
}

/*********************************************************************
 * @fn      USART1_IRQHandler
 *
 * @brief   This function handles TIM2 exception, Recevice TIM Period 
 *
 * @return  none
 */
void USART1_IRQHandler(void){
    if(USART_GetITStatus(USART1, USART_IT_RXNE)){
        // TIM_Cmd(TIM2, DISABLE);
        uint8_t ReceiveData = USART_ReceiveData(USART1);
        TIM_SetAutoreload(TIM2, ReceiveData - 1);
        TIM_SetCounter(TIM2, 0);
        // TIM_Cmd(TIM2, ENABLE);
    }
    USART_ClearITPendingBit(USART1, USART_IT_RXNE);
}
