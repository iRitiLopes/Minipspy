# 2021-Arquitetura-Minips-Fase2-iRitiLopes

# MINIPSPY
A mini emulator of Mips

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
$ minipspy run ./examples/14.flutuantes
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


# [Relatorio EP2 em PDF](Relatorio-EP2.pdf)


### Nome: Richard da Cruz Lopes
### RA: 11122015
### Link vídeo: https://youtu.be/-5B0i5IyRKU


## Projeto Minips - EP2 - Arquitetura de Computadores - UFABC 2021

Esta Fase2 seguiu os mesmos princípios usados pela Fase1, portanto não foi necessária refatorações para adequar as novas features. Houve adição de dois novos módulos, o de COProcessador1 e o de Estatísticas que mostra ao final da execução alguns dados sobre a simulação. Continuou sendo bem desafiador.

Quando fui implementar a feature de Branch Delay Slot, não houveram grandes dificuldades, apenas identificar quais instruções eram as que causavam o BDL e fazer a implementação, creio que não seja das mais elegantes a maneira que foi implementada, mas como são instruções específicas, pude aproveitar bem a maneira em que foi implementado.

Uma dificuldade encontrada foi na implementação dos FP, especificamente a maneira de armazenar e carregar os valores aos registradores, inicialmente, talvez por desatenção, estava armazenando os bits de mais alta ordem nos registrador par da dupla de registradores por exemplo 63..32 no registrador f0 e 31..0 no registrador f1, e isto estava me causando alguns bugs, até que perguntei no canal do Discord e a dúvida foi sanada e a partir daí o bug foi corrigido e praticamente a implementação da fase 2 se encerrara, podendo então partir para a implementação do módulo de estatísticas.

Eu continuo achando que o ponto forte do meu projeto foi a modularização, e a maneira em que organizei as instruções e como elas funcionam, está extremamente fácil a adição de novas instruções, assim como uma correção de alguma, utilizei um design pattern chamado Factory. Creio que essa modularização irá me ajudar na Fase3 da mesma maneira que me ajudou nesta fase.

A implementação do minipspy, hoje está executando os 16 binários de teste com sucesso, tanto no modo run  quanto no modo decode, junto com mais um código compilado por mim chamado example que foi bastante utilizado durante a construção das instruções de FP.

