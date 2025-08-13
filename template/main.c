#include <avr/io.h>
#include <util/delay.h>

#define LED_PIN PB0

int main(void) {
	// Set LED pin as output
	DDRB |= (1 << LED_PIN);

	while (1) {
		PORTB ^= (1 << LED_PIN);	// Toggle LED
		_delay_ms(500);				// Delay 500 ms
	}
}
