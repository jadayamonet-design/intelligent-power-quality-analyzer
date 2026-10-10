#include <stdint.h>
#include <stdio.h>

#define RCC_AHB1ENR  (*(volatile uint32_t *)0x40023830)
#define RCC_APB2ENR  (*(volatile uint32_t *)0x40023844)
#define GPIOA_MODER  (*(volatile uint32_t *)0x40020000)

#define ADC1_SMPR2 (*(volatile uint32_t *)0x40012010)
#define ADC1_SQR3 (*(volatile uint32_t *)0x40012034)
#define ADC1_CR2 (*(volatile uint32_t *)0x40012008)
#define ADC1_SR   (*(volatile uint32_t *)0x40012000)
#define ADC1_DR   (*(volatile uint32_t *)0x4001204C)

#define RCC_APB1ENR  (*(volatile uint32_t *)0x40023840)
#define GPIOA_AFRL   (*(volatile uint32_t *)0x40020020)

#define USART2_SR    (*(volatile uint32_t *)0x40004400)
#define USART2_DR    (*(volatile uint32_t *)0x40004404)
#define USART2_BRR   (*(volatile uint32_t *)0x40004408)
#define USART2_CR1   (*(volatile uint32_t *)0x4000440C)

void send_character(char c)
{
    while (!(USART2_SR & (1U << 7)))
    {
    }

    USART2_DR = c;
}

void send_number(uint32_t number)
{
    char digits[10];
    int count = 0;

    do
    {
        digits[count++] = '0' + (number % 10);
        number /= 10;
    }
    while (number > 0);

    while (count > 0)
    {
        send_character(digits[--count]);
    }
}
volatile uint32_t test_counter = 0;
volatile uint32_t adc_value = 0;

int main(void)
{
    /* Enable GPIOA clock */
    RCC_AHB1ENR |= (1U << 0);

	/* Enable USART2 clock */
	RCC_APB1ENR |= (1U << 17);

	/* Set PA2 to alternate function mode */
	GPIOA_MODER &= ~(3U << 4);
	GPIOA_MODER |=  (2U << 4);

	/* Select USART2 for PA2 */
	GPIOA_AFRL = (GPIOA_AFRL & ~(15U << 8)) | (7U << 8);

	/* Set baud rate to 9600 (assuming 16 MHz clock) */
	USART2_BRR = 0x683;

	/* Enable USART2 transmitter */
	USART2_CR1 |= (1U << 3);

	/* Enable USART2 */
	USART2_CR1 |= (1U << 13);

    /* Enable ADC1 clock */
    RCC_APB2ENR |= (1U << 8);

    /* Set PA0 to analog mode */
    GPIOA_MODER &= ~(3U << 0);
    GPIOA_MODER |=  (3U << 0);

    /* Set ADC channel 0 sample time */
    ADC1_SMPR2 &= ~(7U << 0);
    ADC1_SMPR2 |=  (7U << 0);
    /* First conversion = ADC channel 0 */
    ADC1_SQR3 = 0;
    /* Turn ADC1 on */
    ADC1_CR2 |= (1U << 0);

    while (1)
    {
        /* Start ADC conversion */
        ADC1_CR2 |= (1U << 30);

        /* Wait for conversion to finish */
        while (!(ADC1_SR & (1U << 1)))
        {
        }

        /* Read ADC result */
        adc_value = ADC1_DR;
        /* Send ADC reading to laptop */
        send_number(adc_value);
        send_character('\r');
        send_character('\n');

        /* Small delay between readings */
        for (volatile uint32_t i = 0; i < 800000; i++)
        {
        }
        test_counter++;
    }
}
