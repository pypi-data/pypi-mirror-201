from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import TerminalFormatter
from CodeChroma.colors import Colors
import re

class TerminalColors:
    """
       This object has all the methods for coloring text in the terminal.
       For this function it is necessary to use the class colors that helps to color the code easier.
        - Color the code syntax
        - Colorize urls
        - Colorize text between quotation marks
        - Colorize text between brackets
        - Match titles
        - Search for text blocks
        
        Example
            ```python
            from CodeChroma import TerminalColors
            termcolor = TerminalColors()
            text = '''# Sintaxis de Java 
                    ## Variables'''
            colored_text = termcolor.coloring_text(text)
            print(colored_text)
            ```
    """
    
    def __init__(self):
        # Crea la instancia que colorea el texto
        self.colors = Colors()

        # Combinar los patrones utilizando el operador | (OR)
        self.pattern = r'(```.*?```|\'\'\'.*?\'\'\'|\'[^\n]*?\'|"[^\n]*?"|\'.*?\'|\`[^\n]*?\`|\(.*?\)|https?://\S+|- [^\n]*\n|#+[^\n]*\n|>.*?\n(?: {4}.*?\n)*)'


    def coloring_text(self, text: str) -> str:
        """
            Esta funcion es la principal que colorea el texto pasado por parametro
        """
        return re.sub(self.pattern, self._replacement, text, flags=re.DOTALL)

    def _replacement(self, match):
        """
            Esta función busca y valida el texto que tipo de texto es y lo colorea.
            Retorna el el texto coloreado si cumple la condicion.
        """
        text = match.group(1)
        
        if self._is_code(text): return self._color_code(text)
        elif self._is_title(text): return self._color_title(text)
        elif self._is_string(text): return self._color_string(text)
        elif self._is_parentheses(text): return self._color_parentheses(text)
        elif self._is_block(text): return self._color_block(text)
        elif self._is_url(text): return self._color_url(text)
        elif self._is_list_item(text): return self._color_list_item(text)
        else: return text

    # * Aqui se guarda los metodos que colorean el string encontrado segun se defina
    
    def _color_code(self, code: str) -> str:
        # Primero valida el lenguaje del codigo extraido como string
        # Primero revisa si el mismo bloque de codigo ya tiene el lenguaje especificado
        # Si no entonces pasalo a una segunda función quebuscara patrones para detectar el lenguaje
        # Si no entonces pasalo a una funcion dentro de la libreria pygments que detecte el lenguaje en automatico
        # Y si al final no detecta nada entonces colorea el codigo de cyan
        code_extract = self._extract_lang_in_string(code)
        lang = self._detect_code_language(code) if code_extract is None else code_extract
        code = code[3: -3] if code_extract is None else code[3 + len(lang):-3]
        lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
        result = highlight(code, lexer, TerminalFormatter())
        return f"\n{self.colors.light_green(lexer.name)}\n\n{self.colors.light_cyan(result)}\n"

    def _color_string(self, string: str) -> str:
        return self.colors.light_magenta(string)
    

    def _color_parentheses(self, parentheses: str) -> str:
        return self.colors.light_blue(parentheses)

    def _color_url(self, url: str) -> str:
        return self.colors.bold(self.colors.light_blue(url))

    
    def _color_list_item(self, item: str) -> str:
        return self.colors.bold(self.colors.light_yellow(item))
    
    def _color_title(self, title:str) -> str:
        return self.colors.light_blue(title)
    
    def _color_block(self, text:str) -> str:
        return self.colors.light_green(text)
        
    # * En estos metodos se almacena la funcionalidad de validación si se encuentra cierto elemento en el texto
    
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

    
    # * Otras funcionalidades como identificar el lenguaje de un texto como codigo de programación.
    
    def _extract_lang_in_string(self, text:str) -> (str or None):
        """
        Esta función recibe un string y extrae el texto contenido entre los caracteres de comillas simples o dobles.
        Si no se encuentra ningún texto, retorna None.
        """
        lang = text.split("```")[1].split("\n")[0]
        if (len(lang) <= 0 or lang is None): return None
        else: return lang
        
        
    def _detect_code_language(self, code: str) -> (str or None):
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