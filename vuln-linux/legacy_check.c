#include <stdio.h>
#include <string.h>

// Legacy compatibility utility used by older authentication scripts
int main(int argc, char *argv[]) {

    // Handle help flag
    if (argc > 1 &&
        (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0)) {

        printf(
            "Legacy system compatibility tool.\n\n"
            "Required for backward compatibility with legacy authentication scripts.\n\n"
            "Reads system authentication data from /etc/shadow.\n"
        );
        return 0;
    }

    // Open system shadow file (requires elevated privileges)
    FILE *f = fopen("/etc/shadow", "r");
    if (!f) {
        perror("Cannot open shadow");
        return 1;
    }

    // Stream file contents to stdout
    char line[512];
    while (fgets(line, sizeof(line), f)) {
        printf("%s", line);
    }

    fclose(f);
    return 0;
}
