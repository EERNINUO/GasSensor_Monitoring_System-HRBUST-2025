/********************************** (C) COPYRIGHT *******************************
 * File Name          : adc.c
 * Author             : EERNINUO
 * Date               : 2026年1月
 * Description        : ADC采集模块 - 气体检测系统学年设计项目
 * 
 * 功能说明：
 * 1. 配置CH32V003内部ADC，采集TGS813传感器电压
 * 2. 10位分辨率，57个采样周期，提高抗干扰能力
 * 3. 单次转换模式，降低功耗
 * 
 * 技术参数：
 * - ADC时钟：PCLK2/8 = 6MHz
 * - 采样时间：57个ADC时钟周期 ≈ 9.5μs
 * - 输入通道：ADC通道7 (PD4)
 * - 数据对齐：右对齐
 * 
 * 许可证：GNU General Public License v3.0
 * 项目仓库：https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025
 *******************************************************************************/
#include "adc.h"

void adc_Init(){
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD, ENABLE);
    RCC_ADCCLKConfig(RCC_PCLK2_Div8);

    GPIO_InitTypeDef adc_GPIOInitStruct;
    adc_GPIOInitStruct.GPIO_Mode= GPIO_Mode_AIN;
    adc_GPIOInitStruct.GPIO_Pin= GPIO_Pin_4;
    adc_GPIOInitStruct.GPIO_Speed= GPIO_Speed_30MHz;
    GPIO_Init(GPIOD, &adc_GPIOInitStruct);

    ADC_RegularChannelConfig(ADC1,ADC_Channel_7, 1, ADC_SampleTime_57Cycles);

    ADC_InitTypeDef adc_InitStruct;
    adc_InitStruct.ADC_Mode= ADC_Mode_Independent;
    adc_InitStruct.ADC_ScanConvMode= DISABLE;
    adc_InitStruct.ADC_ContinuousConvMode= DISABLE;
    adc_InitStruct.ADC_ExternalTrigConv= ADC_ExternalTrigConv_None;
    adc_InitStruct.ADC_DataAlign= ADC_DataAlign_Right;
    adc_InitStruct.ADC_NbrOfChannel= 1;
    ADC_Init(ADC1, &adc_InitStruct);

    ADC_Cmd(ADC1, ENABLE);

    ADC_ResetCalibration(ADC1);
    while(ADC_GetResetCalibrationStatus(ADC1));
    ADC_StartCalibration(ADC1);
    while(ADC_GetCalibrationStatus(ADC1));
}

uint16_t get_adcValue(){
    ADC_SoftwareStartConvCmd(ADC1, ENABLE);
    while (ADC_GetFlagStatus(ADC1,ADC_FLAG_EOC) == RESET);
    return ADC_GetConversionValue(ADC1);
}

