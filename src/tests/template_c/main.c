#include <neorv32.h>

#define BAUD_RATE 19200

int main() {
    // neorv32_rte_setup();
    neorv32_uart0_setup(BAUD_RATE, 0);
    neorv32_uart0_puts("AAA\n");
  return 0;
}
