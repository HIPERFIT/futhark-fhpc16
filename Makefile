CFLAGS=-O3 -lm
TAIL_CFLAGS=${CFLAGS} -I ${TAIL_ROOT}/include
TAIL_PRELUDE=${TAIL_ROOT}/lib/prelude.apl
RUNS=30 # Note: hardcoded in APL programs.

COMPILERS=tail futhark-c futhark-opencl
BENCHMARKS=signal easter funintegral life2 blackscholes # sobol-pi

ifndef TAIL_ROOT
$(error TAIL_ROOT is not set)
endif

.PHONY: clean

all: $(BENCHMARKS:%=benchmark_%)

$(BENCHMARKS:%=benchmark_%): $(BENCHMARKS:%=runtimes/%-tail.avgtime) $(BENCHMARKS:%=runtimes/%-futhark-c.avgtime) $(BENCHMARKS:%=runtimes/%-futhark-opencl.avgtime)

runtimes/%-tail.avgtime: compiled/%-tail
	mkdir -p runtimes
	compiled/$*-tail | grep AVGTIMING | awk '{print $$2}' > $@

runtimes/%.avgtime: runtimes/%.runtimes
	awk '{sum += strtonum($$0) / 1000.0} END{print sum/NR}' < $< > $@

runtimes/%-futhark-c.runtimes: compiled/%-futhark-c
	compiled/$*-futhark-c -r ${RUNS} -t $@

runtimes/%-futhark-opencl.runtimes: compiled/%-futhark-opencl
	compiled/$*-futhark-opencl -r ${RUNS} -t $@

compiled/%-tail: benchmarks/%.apl
	mkdir -p compiled
	aplt -unsafe -c -O 2 -oc compiled/$*-tail.c  ${TAIL_PRELUDE} $<
	gcc -o $@ -O3 compiled/$*-tail.c ${TAIL_CFLAGS}

compiled/%-futhark-c: compiled/%.fut
	futhark-c $< -o $@

compiled/%-futhark-opencl: compiled/%.fut
	futhark-opencl $< -o $@

compiled/%.fut: compiled/%.tail
	tail2futhark $< > $@

compiled/%.tail: benchmarks/%.apl
	aplt  -p_types -p_tail -c -o $@ ${TAIL_PRELUDE} $<

clean:
	rm -rf runtimes
	rm -rf compiled
