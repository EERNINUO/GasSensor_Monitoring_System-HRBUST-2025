################################################################################
# MRS Version: 2.3.0
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Hardware/adc.c 

C_DEPS += \
./Hardware/adc.d 

OBJS += \
./Hardware/adc.o 

DIR_OBJS += \
./Hardware/*.o \

DIR_DEPS += \
./Hardware/*.d \

DIR_EXPANDS += \
./Hardware/*.234r.expand \


# Each subdirectory must supply rules for building sources it contributes
Hardware/%.o: ../Hardware/%.c
	@	riscv-none-embed-gcc -march=rv32ecxw -mabi=ilp32e -msmall-data-limit=0 -msave-restore -fmax-errors=20 -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common -Wunused -Wuninitialized -g -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Debug" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Core" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/User" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Peripheral/inc" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Hardware" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/middlewire" -std=gnu99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"

