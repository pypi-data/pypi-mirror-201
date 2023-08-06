from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer
from pygments.formatters import TerminalFormatter
from CodeChroma.colors import Colors
import re

class TerminalColors:
    """
        Class that colors different parts of the text.
    
        This object has all the methods for coloring text in the terminal.
        For this function it is necessary to use the class colors that helps to color the code easier.
        
        Colors:
            - yellow
            - light_yellow
            - red
            - light_red
            - blue
            - light_blue
            - green
            - light_green
            - cyan
            - light_cyan
            - magenta
            - light_magenta
        
        Features:
            - Color the code syntax
            - Colorize urls
            - Colorize text between quotation marks
            - Colorize text between brackets
            - Match titles
            - Search for text blocks
        
        ```python
        from CodeChroma import TerminalColors
        termcolor = TerminalColors()
        text = '''# Sintaxis de Java 
                ## Variables'''
        colored_text = termcolor.coloring_text(text)
        print(colored_text)
        ```
    
        This class defines a dictionary with different labels and their corresponding colors, which can be modified according to the user's needs.
        according to the user's needs. The dictionary is used to apply different colors to different parts of the text.
        of the text. The pattern used to find the different parts of the text is defined in the `pattern` property.
    
        Attributes:
            elements (dict): dictionary with different labels and their corresponding colors.
                ```
                    from CodeChroma import Colors
                    color = Colors()
                    termcolor.elements = {
                            "title" : colors.light_blue,
                            "block" : colors.light_green,
                            "list-item": colors.light_yellow,
                            "url" : colors.light_blue,
                            "parentheses" : colors.blue,
                            "string" : colors.magenta,
                            "code" : colors.light_cyan
                            }
                ```
    """
    
    def __init__(self, title='light_blue', block='light_green', list_item='light_yellow', url='light_blue', parentheses='blue', string='magenta', code='light_cyan', lang='green'):
        # Creates the instance that colors the text
        # Define a dictionary with different labels and their corresponding colors.
        # This dictionary will be used to apply different colors to different parts of the text.
        self._colors = Colors()
        self.elements = {
            "title": getattr(self._colors, title),
            "block": getattr(self._colors, block),
            "list-item": getattr(self._colors, list_item),
            "url": getattr(self._colors, url),
            "parentheses": getattr(self._colors, parentheses),
            "string": getattr(self._colors, string),
            "code": getattr(self._colors, code),
            "lang": getattr(self._colors, lang)
        }

        # Search pattern to be used by the class to obtain the elements to be colorized.
        self._pattern = r'(```.*?```|\'\'\'.*?\'\'\'|\'[^\n]*?\'|"[^\n]*?"|\'.*?\'|\`[^\n]*?\`|\(.*?\)|https?://\S+|- [^\n]*\n|#+[^\n]*\n|>.*?\n(?: {4}.*?\n)*)'
        # This property indicates whether the identified language is to be displayed or not.
        self.view_lang:bool = True
        self.format_code = True



    def coloring_text(self, text: str) -> str:
        """ This is the main function that colors the text passed by parameter. """
        return re.sub(self._pattern, self._replacement, text, flags=re.DOTALL)

    def _replacement(self, match):
        # This function looks for and validates the text what type of text it is and colors it.
        # It returns the colored text if it meets the condition.
        text = match.group(1)
        
        if self._is_code(text): return self.color_code(text)
        elif self._is_title(text): return self._color_title(text)
        elif self._is_string(text): return self._color_string(text)
        elif self._is_parentheses(text): return self._color_parentheses(text)
        elif self._is_block(text): return self._color_block(text)
        elif self._is_url(text): return self._color_url(text)
        elif self._is_list_item(text): return self._color_list_item(text)
        else: return text

    # Here are stored the methods that color the string found as defined
    
    def color_code(self, code: str) -> str:
        """This function colors the syntax of a code passed as a string.

        Args:
            code (str): Code to color syntax.

        Returns:
            str: Returns the code already colored correctly.Returns the string with the code already colored correctly and if desired with its language identified at the top of the code.
        """
        
        # First identify the language of the code passed as a string.
        # Once with the language get the lexer that will be used to color the code.
        try:
            lang = self.detect_code_language(code=code)
            lexer = get_lexer_by_name(lang)
        except:
            lexer = TextLexer()
        
        # Extracts only the part of the code you are interested in having
        if self.format_code:
            code_extract = self._extract_lang_in_string_markdown(text=code)
            if re.search(r'```|~~~', code):
                if code_extract is None:
                    code = code[code.index('```') + 3:code.rindex('```')]
                    code = code.replace('`', '')
                else:
                    code = code[code.index('```') + 3:code.rindex('```')]
                    code = code.replace('`', '')
                    code = code.replace(code_extract, '', 1)
        
        # Finally, color the text according to the language identified.
        result = highlight(code, lexer, TerminalFormatter())
        result = self.elements["code"](result)
        result_lang = self.elements["lang"](lexer.name)
        return f"\n{result_lang}\n\n{result}" if self.view_lang else f"\n{result}"

    def _color_string(self, string: str) -> str:
        return self.elements["string"](string)

    def _color_parentheses(self, parentheses: str) -> str:
        return self.elements["parentheses"](parentheses)

    def _color_url(self, url: str) -> str:
        return self._colors.bold(self.elements["url"](url))
    
    def _color_list_item(self, item: str) -> str:
        return self._colors.bold(self.elements["list-item"](item))
    
    def _color_title(self, title:str) -> str:
        return self.elements["title"](title)
    
    def _color_block(self, text:str) -> str:
        return self.elements["block"](text)
        
    # In these methods, the validation functionality is stored if a certain element is found in the text.
    
    def _is_code(self, text: str) -> bool:
        return (text.startswith('```') and text.endswith('```')) or (text.startswith("'''\n") and text.endswith("'''\n"))
    
    def _is_string(self, text: str) -> bool:
        return (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")) or (text.startswith("`") and text.endswith("`"))
    
    def _is_parentheses(self, text: str) -> bool:
        return text.startswith('(') and text.endswith(')')
    
    def _is_url(self, text: str) -> bool:
        return text.startswith('http')
    
    def _is_list_item(self, text: str) -> bool:
        return text.startswith('-')
    
    def _is_block(self, text: str) -> bool:
        return text.startswith('>')
    
    def _is_title(self, text: str) -> bool:
        return text.startswith('#')

    
    # Other functionalities such as identifying the language of a text as programming code.
    
    def detect_code_language(self, code:str) -> str:
        """This function allows you to identify the language of the code passed as a string.

        Args:
            code (str): Code to identify the language.

        Returns:
            str: Returns the string with the identified language.
        """
        
        lang = self._extract_lang_in_string_markdown(code)
        lang = self._detect_language_by_regex(code) if lang is None else lang
        if lang is None:
            if re.search(r'```|~~~', code):
                code = code[code.index('```') + 3:code.rindex('```')]
                code = code.replace('`', '')
                lang = guess_lexer(code).name
            else: 
                lang = guess_lexer(code).name
        return lang
        
    
    def _extract_lang_in_string_markdown(self, text:str) -> (str or None):
        """
        Esta función recibe un string y extrae el texto contenido entre los caracteres de comillas simples o dobles.
        Si no se encuentra ningún texto, retorna None.
        """
        try:
            lang = text.split("```")[1].split("\n")[0]
            if (len(lang) <= 0 or lang is None): return None
            else: return lang
        except:
            return None
        
    def _detect_language_by_regex(self, code: str) -> (str or None):
        """Esta función recibe un texto y detecta si contiene algún código de programación en él y retorna el código encontrado."""

        # Definir una lista de expresiones regulares para identificar los lenguajes de programación más comunes
        regex = [
            # Buscar las palabras def, print o elif seguidas de un nombre y paréntesis
            (r"(def|print|elif)\s+\w+\(.*\)", "Python"),
            # Buscar las palabras print import o from seguidas de un nombre y paréntesis
            (r"import\s+\w+|from\s+\w+\s+import\s+\w+|print\s*\(", "Python"),
            # Buscar el inicio de un documento HTML o algunas etiquetas comunes
            (r"<!DOCTYPE html>|<div.*?>|<a.*?>|<h[1-6].*?>|<p.*?>|<script.*?>|<img.*?>", "HTML"),
            # Buscar los modificadores de acceso seguidos de class o interface y un nombre
            (r"(public|private|protected)\s+(class|interface)\s+\w+", "Java"),
            # Buscar las palabras fun o println seguidas de un nombre y paréntesis
            (r"(fun|println)\s+\w+\(.*\)", "Kotlin"),
            # Buscar la palabra include seguida de un archivo de cabecera entre <>
            (r"#include\s+<\w+\.h>", "C"),
            # Buscar el uso de librerías o espacios de nombres
            (r"#include\s+<\w+\.h>|using namespace\s+\w+;", "C++"),
            # Buscar las palabras using o namespace seguidas de un nombre y punto y coma
            (r"(using|namespace)\s+\w+;", "C#"),
            # Buscar las funciones console.log, alert o document.write seguidas de un paréntesis
            (r"(console\.log|alert|document\.write)\(", "JavaScript"),
            # Buscar la función console.log o las palabras import o export
            (r"console\.log|import\s+\w+|export\s+\w+", "TypeScript"),
            # Buscar el inicio de un bloque PHP
            (r"<\?php", "PHP"),
            # Buscar la palabra func seguida de un nombre y paréntesis, seguido de una flecha
            (r"func\s+\w+\(.*\)->", "Swift"),
            # Buscar las palabras fun o println seguidas de un nombre y paréntesis
            (r"(fun|println)\s+\w+\(.*\):", "Kotlin"),
            # Buscar el inicio de un script Bash
            (r"\#\!\/bin\/bash", "Bash"),
            (r"\w\s-\w", "Bash"),
            # Buscar el inicio de un documento XML
            (r"<\?xml", "XML"),
            # Buscar una llave abierta seguida de cualquier cosa y una llave cerrada
            (r"\{.*?\}", "JSON"),
            # Buscar la palabra fn o let seguida de un nombre y paréntesis, seguido de una flecha
            (r"(fn|let)\s+\w+\(.*\)", "Rust"),
            (r"println!\(.*\)", "Rust"),
            # Buscar las palabras func o fmt.Println seguidas de un nombre y paréntesis
            (r"(func|fmt\.Println)\s+\w+\(.*\)", "Go"),
            # Buscar la palabra def seguida de un nombre y paréntesis opcionales
            (r"def\s+\w+\s*\(*\)*|puts\s+", "Ruby"),
            # Buscar la palabra def seguida de un nombre y paréntesis, seguido de un igual
            (r"def\s+\w+\(.*\)\s*=", "Scala"),
            # Buscar la palabra function seguida de un nombre y paréntesis
            (r"\bfunction\s+\w+\(.*\)\s*", "Lua"),
            # Buscar las palabras SELECT, FROM o WHERE seguidas de un nombre
            (r"(SELECT|FROM|WHERE)\s+\w+", "SQL"),
            # Busca la estructura de corchetes o de lista para saber si es un código JSON
            (r'\{\n?\s*"\w+":\s*\w+(?:,\n?\s*"\w+":\w+)*\n?\s*\}', "JSON"),
        ]

        # Iterar sobre la lista de expresiones regulares y aplicar cada una al código dado
        for r in regex:
            if re.search(r[0], code):
                return r[1]

        # Si ninguna expresión regular coincide, devolver "No se pudo detectar el lenguaje"
        return None