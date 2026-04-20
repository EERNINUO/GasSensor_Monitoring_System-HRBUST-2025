################################################################################
# MRS Version: 2.3.0
# Automatically-generated file. Do not edit!
################################################################################
-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include middlewire/subdir.mk
-include User/subdir.mk
-include Startup/subdir.mk
-include Peripheral/src/subdir.mk
-include Driver/src/subdir.mk
-include Debug/subdir.mk
-include Core/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(ASM_UPPER_DEPS)),)
-include $(ASM_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
SECONDARY_FLASH += \
MCU_Program.hex \

SECONDARY_LIST += \
MCU_Program.lst \

SECONDARY_SIZE += \
MCU_Program.siz \


# All Target
all: 
	$(MAKE) --no-print-directory main-build 

main-build: MCU_Program.elf secondary-outputs

# Tool invocations
MCU_Program.elf: $(OBJS) $(USER_OBJS_ESCAPE)
	@	riscv-none-embed-gcc -march=rv32ecxw -mabi=ilp32e -msmall-data-limit=0 -msave-restore -fmax-errors=20 -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common -Wunused -Wuninitialized -g -T "c:/Users/18902/Desktop/传感器大作业/software/MCU/Ld/Link.ld" -nostartfiles -Xlinker --gc-sections -Wl,-Map,"MCU_Program.map" --specs=nano.specs --specs=nosys.specs -o "MCU_Program.elf" $(OBJS) $(LIBS) -lprintf
MCU_Program.hex: MCU_Program.elf
	@	riscv-none-embed-objcopy -O ihex "MCU_Program.elf" "MCU_Program.hex"
MCU_Program.lst: MCU_Program.elf
	@	riscv-none-embed-objdump --all-headers --demangle --disassemble -M xw "MCU_Program.elf" > "MCU_Program.lst"
MCU_Program.siz: MCU_Program.elf
	riscv-none-embed-size --format=berkeley "MCU_Program.elf"

# Other Targets
clean:
	-$(RM) $(DIR_OBJS) $(SECONDARY_FLASH)$(SECONDARY_LIST)$(SECONDARY_SIZE) MCU_Program.elf
	-$(RM) $(DIR_EXPANDS) $(CALLGRAPH_DOT)
	-$(RM) $(DIR_DEPS)
secondary-outputs: $(SECONDARY_FLASH) $(SECONDARY_LIST) $(SECONDARY_SIZE)

.PHONY: all clean dependents

-include ../makefile.targets