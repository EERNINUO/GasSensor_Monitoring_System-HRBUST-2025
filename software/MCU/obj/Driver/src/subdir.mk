################################################################################
# MRS Version: 2.3.0
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Driver/src/adc.c 

C_DEPS += \
./Driver/src/adc.d 

OBJS += \
./Driver/src/adc.o 

DIR_OBJS += \
./Driver/src/*.o \

DIR_DEPS += \
./Driver/src/*.d \

DIR_EXPANDS += \
./Driver/src/*.234r.expand \


# Each subdirectory must supply rules for building sources it contributes
Driver/src/%.o: ../Driver/src/%.c
	@	riscv-none-embed-gcc -march=rv32ecxw -mabi=ilp32e -msmall-data-limit=0 -msave-restore -fmax-errors=20 -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common -Wunused -Wuninitialized -g -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Debug" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Core" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/User" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Peripheral/inc" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/middlewire" -I"c:/Users/18902/Desktop/传感器大作业/software/MCU/Driver/inc" -std=gnu99 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"

