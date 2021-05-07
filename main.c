#include <stdint.h>
#include <msp430.h>
#include <string.h>

void printf(char *, ...);

// The I/O backend library
int io_putchar(int c) {
    while (!(UCA0IFG&UCTXIFG));                // USCI_A0 TX buffer ready?
    UCA0TXBUF = c;
    return 0;
}

int io_puts_no_newline(const char *str) {
  uint8_t len_str = strlen(str);
  volatile uint8_t i;
  for(i=0;i<len_str;i++) {
    while (!(UCA0IFG&UCTXIFG));                // USCI_A0 TX buffer ready?
    UCA0TXBUF = str[i];
  }
  return 0;
}

void init_clocks(){
    // Startup clock system with max DCO setting ~8MHz
    CSCTL0_H = CSKEY_H;                     // Unlock CS registers
    CSCTL1 = DCOFSEL_3 | DCORSEL;           // Set DCO to 8MHz
    CSCTL2 = SELA__VLOCLK | SELS__DCOCLK | SELM__DCOCLK;
    CSCTL3 = DIVA__1 | DIVS__1 | DIVM__1;   // Set all dividers
    CSCTL0_H = 0;                           // Lock CS registers
}

void init_uart() {
    // Pins, 2.1/UCA0RXD (to MCU), 2.0/UCA0TXD (from MCU)
    P2REN = 0;
    P2SEL1 |= (BIT1 | BIT0);
    P2SEL0 &= ~(BIT1 | BIT0);

    // Configure USCI_A0 for UART mode
    UCA0CTLW0 = UCSWRST;                    // Put eUSCI in reset
    UCA0CTLW0 |= UCSSEL_2;             // CLK = SMCLK
    // Baud Rate calculation
    // 8000000/(16*9600) = 52.083
    // Fractional portion = 0.083
    // User's Guide Table 21-4: UCBRSx = 0x04
    // UCBRFx = int ( (52.083-52)*16) = 1
    UCA0BRW = 52;                           // 8000000/16/9600
    //UCA0BR1 = 0x00;
    UCA0MCTLW |= UCOS16 | UCBRF_1 | 0x4900;
    UCA0CTLW0 &= ~UCSWRST;                  // Initialize eUSCI
}



int main(void)
{

	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	PM5CTL0 &= ~LOCKLPM5; // Disable the GPIO power-on default high-impedance mode

	init_clocks();
	init_uart();

    // Init button pin
    //setting up button at P1.5: left
    P1DIR &= ~BIT5; //set mode to input mode
    P1REN |= BIT5; //resistor enabled for P1.5
    //pin is floating whenever button isn't pressed, so use pullup resistor

    //whenever button is pressed, will be low so
    P1OUT |= BIT5; //make resistor pullup, since button is connected to GND when pushed, P1.5 low

    //setting up button at P1.4: right
    P1DIR &= ~BIT4; //set mode to input mode
    P1REN |= BIT4; //resistor enabled for P1.5
    //pin is floating whenever button isn't pressed, so use pullup resistor

    //whenever button is pressed, will be low so
    P1OUT |= BIT4; //make resistor pullup, since button is connected to GND when pushed, P1.5 low

       //setting up button at P3.3: up
    P1DIR &= ~BIT3; //set mode to input mode
    P1REN |= BIT3; //resistor enabled for P1.5
    //pin is floating whenever button isn't pressed, so use pullup resistor

    //whenever button is pressed, will be low so
    P1OUT |= BIT3; //make resistor pullup, since button is connected to GND when pushed, P1.5 low

        //setting up button at P3.3: down
     P3DIR &= ~BIT3; //set mode to input mode
     P3REN |= BIT3; //resistor enabled for P1.5
     //pin is floating whenever button isn't pressed, so use pullup resistor

     //whenever button is pressed, will be low so
     P3OUT |= BIT3; //make resistor pullup, since button is connected to GND when pushed, P1.5 low

    uint8_t i=0;
    uint8_t x=0;


	while(1) {
        if (!(P1IN & BIT5)) { //the pin is low, so the button is pressed

            printf("left-%i\n\r", i++);
         __delay_cycles(100000);
        }

        if (!(P1IN & BIT4)) {
            printf("right-%i\n\r", i++);
         __delay_cycles(100000);
        }

        if (!(P1IN & BIT3)) {
            printf("up-%i\n\r", i++);
         __delay_cycles(100000);
        }

        if (!(P3IN & BIT3)) {
            printf("down-%i\n\r", i++);
         __delay_cycles(100000);
        }


	}
}
