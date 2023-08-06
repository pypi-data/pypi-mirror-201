<h1 align="center">CodeChroma</h1>

<p align="center" >
<img src="https://img.shields.io/github/last-commit/EddyBel/CodeChroma?color=%23AED6F1&style=for-the-badge" />
<img src="https://img.shields.io/github/license/EddyBel/CodeChroma?color=%23EAECEE&style=for-the-badge" />
<img src="https://img.shields.io/github/languages/top/EddyBel/CodeChroma?color=%23F9E79F&style=for-the-badge" />
<img src="https://img.shields.io/github/languages/count/EddyBel/CodeChroma?color=%23ABEBC6&style=for-the-badge" />
<img src="https://img.shields.io/github/languages/code-size/EddyBel/CodeChroma?color=%23F1948A&style=for-the-badge" />
</p>

<p align="center">Simple python text coloring package</p>

<p aling="center" >
<img src="./assets/Captura1.png" width="100%" />
<img src="./assets/Captura2.png" width="100%" />
<img src="./assets/Captura3.png" width="100%" />
</p>

The "CodeChroma" project is a Python library for highlighting and coloring text in the terminal. With this library, users can highlight code syntax and color specific markdown elements, such as titles, links, parentheses and text in quotation marks.

## Why the project?

The project was created with the aim of improving the readability and aesthetics of text in projects using the terminal. On many occasions, text in the terminal can be difficult to read due to its flat, uncolored format, which can make work difficult and decrease efficiency. For this reason, a Python library was developed to allow text highlighting and coloring in a simple and easy to implement way.

The library allows users to highlight code syntax and color specific markdown elements, such as titles, links, parentheses and text in quotation marks, which improves the readability of the text and makes it easier to understand. In addition, this library is easy to implement in any project as it can be used with a simple library method, making the integration process quick and easy.

## Requirements

- [x] [Python>=3.7](https://www.python.org/downloads/)
- [x] [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## Features

- [x] Allows to identify the code passed as a string and return the text with the syntax of the language colored.
- [x] Allows you to color key elements of the markdown syntax such as code, titles, links, etc.
- [x] Allows quick and easy implementation of the colors to be used.

## How to use

The library is simple to use and only requires installation and import.

The library allows you to color the text using only one method of the library for ease of use.

```python
from CodeChroma import TerminalColors

# We create an instance of the library
termcolor = TerminalColors()

#  Sample text for coloring
text = \
"""
# Sintaxis de Java

## Variables

En Java, existen diferentes tipos de variables, como enteros, flotantes, caracteres y booleanos.
Además de variables de tipo objeto como String o Arrays. Es importante declarar el tipo de
variable correcto para evitar errores en tiempo de ejecución. Por ejemplo, si quieres
almacenar un valor numérico entero, se debe utilizar "int" como el tipo de dato.

'''java
int numeroEntero = 10;
float decimal = 3.14f;
char letra = 'A';
boolean verdaderoOFalso = true;
'''
"""

# We color the text with its method "coloring_text", the text passed by parameter
# The function returns a new string with the text already colored.
colored_text = termcolor.coloring_text(text)
# We can display the new text
print(colored_text)
```

## Licence

<h3 align="center">MIT</h3>

---

<p align="center">
  <a href="https://github.com/EddyBel" target="_blank">
    <img alt="Github" src="https://img.shields.io/badge/GitHub-%2312100E.svg?&style=for-the-badge&logo=Github&logoColor=white" />
  </a> 
  <a href="https://www.linkedin.com/in/eduardo-rangel-eddybel/" target="_blank">
    <img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />
  </a> 
</p>
