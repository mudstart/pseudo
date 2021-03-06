[![Build Status](https://travis-ci.org/alehander42/pseudo.svg?branch=master)](https://travis-ci.org/alehander42/pseudo)
[![codecov.io](https://codecov.io/github/alehander42/pseudo/coverage.svg?branch=master)](https://codecov.io/github/alehander42/pseudo?branch=master)
[![MIT License](http://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# pseudo

[![Join the chat at https://gitter.im/alehander42/pseudo](https://badges.gitter.im/alehander42/pseudo.svg)](https://gitter.im/alehander42/pseudo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Pseudo takes an algorithm / a simple program and generates idiomatic code for it in Python, JavaScript, C#, Go and Ruby.

Pseudo achieves that with translation on two layers: it uses the target language syntax and it can express standard library methods/api of language X using language Y's native standard library

Pseudo consumes "Pseudo AST" which corresponds to a very clear, statically typed and somehow limited subset of a language:

  * basic types and collections and standard library methods for them
  
  * integer, float, string, boolean
  * lists
  * dicts
  * sets
  * tuples/structs(fixed length heterogeneous lists)
  * fixed size arrays
  * regular expressions

  * functions with normal parameters (no default/keyword/vararg parameters)
  * classes 
    * single inheritance
    * polymorphism
    * no dynamic instance variables
    * basically a constructor + a collection of instance methods, no fancy metaprogramming etc supported

  * exception-based error handling with support for custom exceptions
  (target languages support return-based error handling too)
  
  * I/O: print/input, file read/write, command arg handling, system and subprocess commands

  * iteration (for-in-range / for-each / iterating over several collections / while)
  * conditionals (if / else if / else)
  * standard math/logical operations

  * a lot more in future

[standard library reference](docs/library_reference.md)


Those constructs and entities have almost the same behavior and very same-spirited api in a lot of the languages which Pseudo would support.

## examples

Each example contains a detailed README and working translations to Python, JS, Ruby, Go and C#, generated by Pseudo

[fibonacci](examples/fib)

[a football results processing command line tool](examples/football)

[a verbal expressions-like library ported to all the target languages](examples/verbal_expressions)

### architecture

```ruby
PSEUDO AST:
   NORMAL CODE     PSEUDO STANDARD LIBRARY INVOCATIONS     
      ||                    ||
      ||                    ||
      ||              API TRANSLATOR
      ||                    ||
      ||                    ||
      ||                    \/
      ||              IDIOMATIC TARGET LANGUAGE 
      ||              STANDARD LIBRARY INVOCATIONS        
      ||                    ||     
      \/                    \/
  STANDARD OR LANGUAGE-SPECIFIC MIDDLEWARES
              e.g.
    name camel_case/snake_case middleware
    convert-tuples-to-classes middleware
    convert-exception-based errors handling
    to return-based error handling middleware
              etc

              ||
              ||
              ||
              ||
  TARGET LANGUAGE CODE GENERATOR

      defined with a dsl aware
      that handles formatting
         automatically
              ||
              ||
              ||
              \/

      Python / C# / Go / JS / Ruby
```


## use cases

  * generate code for the same task/algorithm in different languages (parser generators etc)
  * port a library/codebase
  * develop core logic in one language and use it in other language codebases
  * write a compiler/dsl
  * bootstrap a codebase in another language / generate equivalent test suites in different languages
  * translate/support some algorithms in different languages
  * translate/support some text/data processing/command tool in different languages

## installation

```bash
pip install pseudo #only python 3 supported

# probably you'd like to try the python-to-pseudo-to-js/go/etc compiler
pip install pseudo-python
```

- [usage](#usage)
- [why?](#why)
- [language support](#language-support)
- [compilers targetting pseudo](#compilers-targetting-pseudo)
- [implementation](#implementation)
- [roadmap](#roadmap)
- [target language specific docs](#target-language-specific-docs)
- [Pseudo and Haxe?](#pseudo-and-haxe)
- [the name?](#the-name)


## usage

you can directly generate pseudo ast from Python using Pseudo-Python
```bash
pseudo-python a.py # generates a.pseudo.yaml
```
and then translate the ast
```bash
pseudo a.pseudo.yaml go # or ruby / js / csharp / py / cpp
```
or you can directly translate from python to another language

```bash
pseudo-python a.py b.rb # or c.cs
```



```python
pseudo.generate(pseudo_ast, language) # pseudo_ast is a plain dict or a pseudo Node-based tree
```

```python
pseudo.generate_from_yaml(pseudo_ast, language) # pseudo_ast is yaml-encoded pseudo ast
```

For quick experiments it's easier to use `generate_main`

```python
from pseudo import * # ok for a repl

print(generate_main([
  assignment(
    local('a', 'Int'),
    call(local('g'), [to_node(0), to_node('')], 'Int'))], 'rb'))

a = g(0, '')
```

In the future Pseudo can add a lisp-like dsl for fast manual creation of ast nodes, but currently it's more useful for its main goal: consuming automatically generated pseudo ast and then transpiling it to the target languages.


## why?

Supporting full-blown Ruby to Python/Javascript to C++ auto translation is hard.

However often we need to just express an algorithm, a self-contained core of a library, a simple command line tool and the act of manual porting to another languages feels somehow .. primitive. 

Often that code is(or can be) expressed in very similar way, with
similar constructs and basic types and data structures. On that level a lot of languages are very similar and the only real difference is syntax and methods api. That's a feasible task for automatic translation and actually the existance of `pseudo` is to fullfill the needs of several other existing projects/ideas.

Another powerful thing about Pseudo is its standard library.
It can accumulate a serious number of methods/idioms and it can act like e.g. a truly cross-platform, target-language-aware equivalent of lodash

Pseudo is still young (it's basically less than two weeks old), 
but it already has a base on which it can improve really quickly
(adding support for another language is basically just a matter of 3-4 hours currently)

## Language support

Using pseudo's DSL it's easy to add support for a new language, so it's feasible to expect support for most popular languages and even different versions of them (e.g. EcmaScript 6/7, Perl 5/6 Java 7 / 8)

## Compilers targetting pseudo

Currently [pseudo-python](https://github.com/alehander42/pseudo-python) is usable, and there are plans for `pseudo-ruby` or `pseudo-js`

## Intermediate AST format

The AST format uses basic data structures available in most languages. The nodes correspond to 
dictionaries with `type` key corresponding to the node type and `field_name` keys corresponding to
the node fields, similar to the widely popular `estree` ecmascript format.

Pseudo can consume ast either serialized in `.pseudo.yaml` files or directly as
dictionary objects through it's `pseudo.generate(ast, output_lang)` API

## Implementation



The implementation goal is to make the definitions of new supported languages  really clear and simple. 

If you dive in, you'll find out
a lot of the code/api transformations are defined using a declarative dsl with rare ocassions 
of edge case handling helpers. 

That has a lot of advantages:

* Less bugs: the core transformation code is really generalized, it's reused as a dsl and its results are well tested

* Easy to comprehend: it almost looks like a config file

* Easy to add support for other languages: I was planning to support just python and c# in the initial version but it is so easy to add support for a language similar to the current supported ones, that I
added support for 4 more.

* Easy to test: there is a simple test dsl too which helps all 
language tests to share input examples [like that](tests/test_ruby.py)

However language translation is related to a lot of details and
a lot of little gotchas, tuning and refining some of them took days. Pseudo uses different abstractions to streamline the process and to reuse logic across languages.

```ruby
PSEUDO AST:
   NORMAL CODE     PSEUDO STANDARD LIBRARY INVOCATIONS     
      ||                    ||
      ||                    ||
      ||              API TRANSLATOR
      ||                    ||
      ||                    ||
      ||                    \/
      ||              IDIOMATIC TARGET LANGUAGE 
      ||              STANDARD LIBRARY INVOCATIONS        
      ||                    ||     
      \/                    \/
  STANDARD OR LANGUAGE-SPECIFIC MIDDLEWARES
              e.g.
    name camel_case/snake_case middleware
    convert-tuples-to-classes middleware
    convert-exception-based errors handling
    to return-based error handling middleware
              etc

              ||
              ||
              ||
              ||
  TARGET LANGUAGE CODE GENERATOR

      defined with a dsl aware
      that handles formatting
         automatically
              ||
              ||
              ||
              \/

            OUTPUT
```



## Roadmap

[Roadmap](roadmap.md)

## Target language specific docs

* [python](docs/python.md)
* [c#](docs/csharp.md)
* [go](docs/go.md)
* [ruby](docs/ruby.md)
* [javascript](docs/javascript.md)
* [c++](docs/cpp.md)

## Pseudo and Haxe

They might seem comparable at a first glance, but they have completely different goals.

Pseudo wants to generate readable code, ideally something that looks like a human wrote it/ported it

Pseudo doesn't use a target language runtime, it uses the target language standard library for everything (except for JS, but even there is uses `lodash` which is pretty popular and standard)

Pseudo's goal is to help with automated translation for cases
like algorithm generation, parser generation, refactoring, porting codebases etc. The fact that you can write compilers targetting Pseudo and receiver translation to many languages for free is just a happy accident

## The name?

well.

pseudo(code)


## License

Copyright © 2015 2016 [Alexander Ivanov](https://twitter.com/alehander42)

Distributed under the MIT License.
