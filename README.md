# 2021-Arquitetura-Minips-Fase3-iRitiLopes

# MINIPSPY
A mini emulator of Mips

## Cache modes and regression checks

All six memory modes are supported:

| Mode | Configuration |
| --- | --- |
| 1 | RAM only |
| 2 | Unified 1 KiB L1, 32-byte lines |
| 3 | Split L1, 512 bytes each, 32-byte lines |
| 4 | Split fully associative L1, 16 ways per bank, LRU replacement |
| 5 | Split four-way L1, 512 bytes each, 32-byte lines |
| 6 | Split four-way L1, 64-byte lines, plus eight-way 2 KiB L2 |

Caches use write-back and write allocation. Invalid ways are filled before
replacement; only dirty victims are written back. Mode 6 uses a non-inclusive
L2: an L1 eviction writes to L2, and an L2 eviction writes to RAM. Call
`emulator.memory.flush()` before inspecting final RAM from Python. An unmapped
word remains empty on both cache hits and misses, so program decoding terminates
consistently. Instruction addresses select L1I; other addresses select L1D.
The supplied self-modifying programs also use L1I for writes to text.

```bash
python3 main.py run 6 examples/11.surpresinha
python3 main.py run 6 examples/11.surpresinha --stat
python3 -m pytest tests/ -q
python3 tools/check_examples.py
```

Execution statistics are hidden by default. Add `--stat` to show them in `run`,
`trace`, or `debug` mode; the flag can appear before or after the positional
arguments. For the root Makefile, use `make run SOURCE=examples/my_test.c STAT=1`.
Python callers can use `Minips(mem_mode=6, show_statistics=True)`.

The comparison command runs the 17 smaller supplied programs in modes 1–6 with
fixed input, compares their output to mode 1, and fails on errors or timeouts.
Matrix multiplication and Mandelbrot take longer; include them explicitly:

```bash
python3 tools/check_examples.py --all --timeout 900
```

Access counters count requests to each level, including stores and writebacks;
RAM transfers of an entire cache line count as one access. Simulated cycle
estimates include L1, L2, and RAM latency.

## Compile your own C or C++ test programs

From the repository root, use the root Makefile (Docker required):

```bash
make build SOURCE=examples/cache_probe.c
make build SOURCE=examples/cache_probe_cpp.cpp
make run SOURCE=examples/cache_probe.c MODE=6
make check SOURCE=examples/cache_probe_cpp.cpp
```

`make` builds the C sample by default. The compiler image is built automatically
if missing. Set `DOCKER=0` to use an installed cross-compiler instead, and run
`make help` for the available commands. Use relative source/output paths under
the repository when building with Docker.

Install a little-endian MIPS cross-toolchain on Debian/Ubuntu:

```bash
sudo apt-get install make gcc-mipsel-linux-gnu g++-mipsel-linux-gnu binutils-mipsel-linux-gnu
make -f tools/Makefile.mips SOURCE=examples/cache_probe.c
make -f tools/Makefile.mips SOURCE=examples/cache_probe_cpp.cpp
```

Alternatively, use the included Docker toolchain from the repository root:

```bash
docker build -t minipspy-toolchain -f tools/Dockerfile.mips .
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD:/work" minipspy-toolchain \
  make -f tools/Makefile.mips SOURCE=examples/cache_probe.c
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD:/work" minipspy-toolchain \
  make -f tools/Makefile.mips SOURCE=examples/cache_probe_cpp.cpp
```

Run the resulting section files by their shared prefix:

```bash
python3 main.py run 6 build/mips/cache_probe
python3 main.py run 6 build/mips/cache_probe_cpp
python3 tools/check_examples.py build/mips/cache_probe build/mips/cache_probe_cpp
```

The C sample prints `523776`; the C++ sample prints `32640`. Copy either sample,
include `minips.h`, implement `main`, and set `SOURCE` to your file. Use `p_int`,
`p_str`, `p_char`, `p_float`, and `p_double` for output. Returning from `main`
exits the emulator automatically. `BUILD_DIR` overrides the output directory;
`CROSS` overrides the toolchain prefix. `.c`, `.cpp`, `.cc`, and `.cxx` are accepted.

This is a freestanding environment without libc or the C++ standard library.
Use plain arithmetic, arrays, functions, and C++ classes/templates; avoid
`printf`, iostreams, heap allocation, exceptions, RTTI, and global objects that
need constructors. The emulator implements a subset of MIPS I, so compiler
output for more complex programs may require additional instruction support.
The build uses [GCC's MIPS I/o32 options](https://gcc.gnu.org/onlinedocs/gcc-15.1.0/gcc/MIPS-Options.html),
places startup code first, and links `.text`, `.rodata`, and `.data` at the
emulator's fixed addresses. Uninitialized globals are included as zero-filled
data in the raw binary sections. Build outputs live under ignored `build/`.

The older `examples/Makefile` and binaries are retained; the new build uses
`tools/Makefile.mips` and `tools/linker.ld`.

### Interactive MD5 example

`examples/md5.cpp` implements streaming MD5 from
[RFC 1321](https://www.rfc-editor.org/rfc/rfc1321). Compile and run it yourself:

```bash
make build SOURCE=examples/md5.cpp
python3 main.py run 6 build/mips/md5
```

Type your input and press Enter. The program prints a lowercase 32-character
MD5 hash. Add `--stat` when running to also print execution statistics.
It hashes the UTF-8 bytes of
the input, preserving spaces and excluding the terminating newline. Empty input
and input spanning multiple 64-byte blocks are supported. For `abc`, expect
`900150983cd24fb0d6963f7d28e17f72`; empty input gives
`d41d8cd98f00b204e9800998ecf8427e`. The emulator supports syscall 12 for reading
characters from a line, including Enter; EOF returns -1.

This project use pyenv and pipenv as Python dependency as Project Manager
to install pipenv just
https://pypi.org/project/pipenv/

```bash
pip3 install pipenv
```

Install Development dependencies (Dependencies for developments e.g. linter, formatter, test framework)

```bash
pipenv install --dev
```

## How to install

```bash
pip install -e .
```

## Execute

```bash
$ minipspy run ./examples/14.flutuantes --stat
3.1415927410125732
2.7182817459106445
3.141592653589793
2.718281828459045
Digite um float: 3
Você digitou: 3.0
Digite um double: 3
Você digitou: 3.0
------------------------------------------
Instruction count:
R: 22 I: 51 J: 0 FR: 8 FI: 4 
Total: 85
Simulation time: 1.848447322845459 sec
Average IPS: 45.98454007829278
------------------------------------------
```

```bash
$ minipspy decode examples/09.contador
J 4194344
nop
ADDI $v0, $zero, 1
LUI $at, 64
ORI $t0, $at, 8
LW $t1, 0($t0)
ADDI $t1, $t1, 1
SW $t1, 0($t0)
JR $ra
nop
JAL 4194312
nop
ADDU $a0, $zero, $v0
ADDIU $v0, $zero, 1
SYSCALL
SLTI $t0, $a0, 9
BEQ $zero, $t0, 3
nop
J 4194344
nop
ADDI $v0, $zero, 10
SYSCALL
```


# [Relatorio EP3 em PDF](Relatorio-EP3.pdf)


### Nome: Richard da Cruz Lopes
### RA: 11122015
### Link vídeo: https://youtu.be/XVwSI-Y3SlI


## Projeto Minips - EP3 - Arquitetura de Computadores - UFABC 2021

The report below describes the original 2021 implementation, before the cache fixes above.

Bem, o que as fases 1 e 2 foram esta fase 3 não foi. A facilidade de implementação das instruções ainda foi tranquila e a parte mais difícil com certeza deste projeto começou, a implementação das Caches. Talvez essa dificuldade tenha sido na maneira modelada inicialmente do comportamento da memória no emulador. Até que me deparei com questões de performance, principalmente pela maneira em que resolvia a decodificação e a maneira em que as palavras eram armazenadas, como strings, os métodos de transformação dessas strings estavam sendo bastante custosas ao desempenho, foi verificado que ao executar o código de exemplo 18.naive_dgemm estava demorando muito além do que deveria, cerca de 10 minutos (péssimo) então resolvi paralisar o desenvolvimento da Cache para resolver os problemas de performance.

Para resolver o problema de performance foi necessário refatorar grande parte do projeto, remover todo e qualquer tipo de tratamento de strings para número, após algum tempo refatorando com auxílio de uma ferramenta chamada cProfile, foi-se identificando em quais pontos acabavam sendo críticos à performance. Após a refatoração a performance melhorou significamente caindo para próximo dos 4 minutos para executar o 18.naive_dgemm, ainda não perfeito porém uma grande melhoria.

Após resolver a refatoração de strings matches para o uso de bitmasks e números, foi possível prosseguir, feita a implementação do modo trace e do modo debug. Estes modos por fim acabaram sendo resolvidos utilizando a própria ferramenta de logging da linguagem, alternando o log level dependendo do modo de execução, e por fim chegamos a Cache.

Ao deparar com o problema das Caches, havia uma dificuldade inicial devido a maneira com que a memória havia sido implementada, após um bom tempo analisando como poderia ser implementada, por fim iniciei. O código implementado não é dos melhores que este projeto vivenciou, mas passou a funcionar para os exemplos básicos até que deparado com o SURPRESINHA, motivo até do qual perguntei no canal do Discord qual o bug que o Surpresinha pretendia evidenciar, após isso foi corrigido o problemas e pude continuar. Com isso me vi com pouco tempo para finalizar a implementação dos outros modos de configuração das Caches, portanto o modo que funciona é o 2 (unificado, randômico), a maneira em que foi implementado facilita a modificação dessa cache unificada em seu tamanho, tamanho de linha e mapeamento de n vias(para casos de exemplos mais simples funciona). Gostaria muito de ter conseguido implementar totalmente as Caches, mas me vi com pouco tempo para conseguir a partir do momento em que pude iniciar o desenvolvimento das mesmas.

Por fim, foi muito divertido esse projeto, pretendo futuramente finalizá-lo mesmo após a entrega. Tive que fazer uso de diversos conhecimentos adquiridos ao longo da graduação até aqui. Vejo que essa dificuldade que existiu na implementação das Caches poderia ter sido minimizado se desde o início tivesse continuado implementando os casos de teste (teria ajudado a manter o código conciso e limpo ao longo das novas implementações), fica de aprendizado aos próximos projetos de escopo semelhante (a nível de detalhamento e tamanho). Muito obrigado.
