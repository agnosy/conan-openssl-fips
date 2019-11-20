#include <iostream>
#include "openssl/crypto.h"

int main() {
    if(FIPS_mode_set(1)) {
        fputs("FIPS mode enabled\n", stderr);
    } else {
        fputs("FIPS mode not-enabled\n", stderr);
        return 1;
    }
    return 0;
}
