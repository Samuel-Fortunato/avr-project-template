cmake_minimum_required(VERSION 3.12)

project({{PROJECT_NAME}} C)

# --- AVR CONFIG ---
set(MCU "{{MCU}}")
set(CLOCK_SPEED "{{CLOCK_SPEED}}") # in Hz
set(PROGRAMMER "usbasp")
set(AVRDUDE_ARGS -p ${MCU} -c ${PROGRAMMER})

add_compile_options(-mmcu=${MCU})
add_compile_definitions(F_CPU=${CLOCK_SPEED}UL)
add_link_options(-mmcu=${MCU})

add_executable(${PROJECT_NAME}.elf main.c)

add_custom_command(
    TARGET ${PROJECT_NAME}.elf POST_BUILD
    COMMAND avr-objcopy -O ihex -R .eeprom ${PROJECT_NAME}.elf ${PROJECT_NAME}.hex
    COMMENT "Generating HEX file"
)

# --- FLASH TARGET ---
add_custom_target(flash
    COMMAND avrdude ${AVRDUDE_ARGS} -U flash:w:${PROJECT_NAME}.hex:i
    DEPENDS ${PROJECT_NAME}.elf
    COMMENT "Flashing ${PROJECT_NAME} to ${MCU}"
)
