#include <serd/serd.h> // Only one header file is required to be included

int main() {
    auto dummy = serd_reader_new(SERD_NTRIPLES, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr);
    serd_reader_free(dummy);
    return 0;
}