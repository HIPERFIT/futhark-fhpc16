#ifndef COMMON_H
#define COMMON_H
/* Common option parsing and timing code. */

#include <sys/time.h>
#include <getopt.h>
#include <stdlib.h>
#include <errno.h>
#include <error.h>

static struct timeval t_start, t_end;

static FILE *runtime_file = NULL;
static int runs = 0;

void parse_args(int argc, char **argv) {
  char c;

  while ((c = getopt(argc, argv, "r:t:")) != -1)
    switch (c) {
    case 'r':
      runs = atoi(optarg);
      break;
    case 't':
      runtime_file = fopen(optarg, "w");
      if (runtime_file == NULL) {
        error(1, errno, "when opening %s", optarg);
      }
      break;
    default:
      error(1, 0, "unknown option %c", c);
    }
}

static void start_run() {
  gettimeofday(&t_start, NULL);
}

static void end_run() {
  gettimeofday(&t_end, NULL);
  fprintf(runtime_file,
          "%ld\n",
          (t_end.tv_sec*1000000+t_end.tv_usec) - (t_start.tv_sec*1000000+t_start.tv_usec));
}

#endif
