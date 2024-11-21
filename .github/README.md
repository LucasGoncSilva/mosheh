<h1 align="center">
  <img src="./logo.svg" height="300" width="300" alt="Logo Mosheh" />
  <br>
  Mosheh
</h1>

![GitHub License](https://img.shields.io/github/license/LucasGoncSilva/mosheh?labelColor=101010)

<!-- ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LucasGoncSilva/mosheh/XXXXXX.yml?style=flat&labelColor=%23101010) -->

Mosheh é um script para geração de documentações de projetos, de Python para Python.

Basicamente, Mosheh lista todos os arquivos para onde vocẽ apontar, armazena cada declaração de definição notória em cada arquivo varrido através da manipulação da AST com o módulo `ast` e, posteriormente, gera a documentação - com uso de MkDocs - respeitando os dados obtidos e a hierarquia dos diretórios e arquivos.

Os elementos documentados para cada arquivo estão listados abaixo:

- Importações [ast.Import | ast.ImportFrom]

  - Tipo [Nativo | Terceiros | Local]
  - Path (e.g. 'django.http')

- Constantes [ast.Assign | ast.AnnAssign]

  - Nome (token name)
  - Anotação de Tipo (datatype)
  - Valor (um literal, uma operação ou uma chamada)

- Classes [ast.ClassDef]

  - Descrição (docstring)
  - Nome (nome da classe)
  - Pais (heranças)
  - Métodos Definidos (quantidade e nomes)
  - Examplo de Uso

- Funções [ast.FunctionDef | ast.AsyncFunctionDef]

  - Descrição (docstring)
  - Nome (nome da função)
  - Tipo [Func | Método | Gerador | Corrotina]
  - Parâmetros (nome, tipo e valor padrão)
  - Tipo de Retorno (datatype)
  - Exceções (disparo de erros)
  - Examplo de Uso

- Asserções: [ast.Assert]
  - Teste (asserção)
  - Mensagem (opcional, caso falhe)

## Stack

![Python logo](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=FFD43B)

## Arquitetura

A definir

## Comandos e Parâmetros

### Comandos

A definir

### Parâmetros

|    Chamada     |     Tipo      | Exemplo                         | Ação                                   |
| :------------: | :-----------: | :------------------------------ | :------------------------------------- |
| `-h`, `--help` |     `str`     | `-h`, `--help`                  | Apresenta estes parâmetros de chamada  |
|    `-root`     |     `str`     | `-root example/`                | Raíz, diretório base para o mapeamento |
|    `--lang`    | `pt-BR \| en` | `--lang pt-BR \| en`            | Idioma de saída da documentação        |
| `--repo-name`  |     `str`     | `--repo-name toicin`            | Nome do repositório/projeto            |
|  `--repo-url`  |     `str`     | `--repo-url https://random.com` | Nome do repositório                    |
|    `--exit`    |     `str`     | `--exit doc/`                   | Caminho de saída da documentação       |

## Licença

This project is under [MIT License](https://choosealicense.com/licenses/mit/). A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
