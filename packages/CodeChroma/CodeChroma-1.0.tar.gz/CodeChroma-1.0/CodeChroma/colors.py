import re


class Colors :
    """
      This object has the necessary methods to color text in the terminal with different libraries, in a simple way, condensing the methods of each library in a single function.
        - Colorama
        - Termcolor
        - Colored
    """
    
    def __init__(self) -> None:
        # Aqui se define la libreria a utilizar
        # * colorama
        # * termcolor
        # * colored
        self.color_library = "colorama"
        
        # Inicia las instancias de las librerias de color a utilizar
        if self.color_library == "colorama":
            from colorama import Style, Fore, init, Back
            init()
            self.st = Style
            self.fo = Fore
            self.bg = Back
        elif self.color_library == "termcolor":
            from termcolor import colored
            self.colored = colored
        elif self.color_library == "colored":
            from colored import fg, bg, attr
            self.fg = fg
            self.bg = bg
            self.attr = attr
            
    
    def clean(self, text:str):
        ansi_escape = re.compile(r'(x9B|x1B\[)[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
        
    def translucent(self, text: str):
        if self.color_library == "colorama":
            return f"{self.st.DIM}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, attrs=["dark"])
        elif self.color_library == "colored":
            return f"{self.attr('dim')}{text}{self.attr('reset')}"
        else: return text

    
    def bold(self, text: str):
        if self.color_library == "colorama":
            return f"{self.st.BRIGHT}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.attr('bold')}{text}{self.attr('reset')}"
        else: return text

    
    def yellow (self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.YELLOW}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "yellow")
        elif self.color_library == "colored":
            return f"{self.fg(226)}{text}{self.attr('reset')}"
        else: return text
    
    def light_yellow (self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.LIGHTYELLOW_EX}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "yellow", attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.fg(227)}{text}{self.attr('reset')}"
        else: return text
    
    def red (self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.RED}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "red")
        elif self.color_library == "colored":
            return f"{self.fg(1)}{text}{self.attr('reset')}"
        else: return text
    
    def light_red(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.LIGHTRED_EX}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "grey", "on_red", attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.fg(9)}{text}{self.attr('reset')}"
        else: return text
    
    def blue(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.BLUE}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "blue")
        elif self.color_library == "colored":
            return f"{self.fg(4)}{text}{self.attr('reset')}"
        else: return text
    
    def light_blue(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.LIGHTBLUE_EX}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "grey", "on_blue", attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.fg(12)}{text}{self.attr('reset')}"
        else: return text
    
    def green(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.GREEN}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "green", "on_black")
        elif self.color_library == "colored":
            return f"{self.fg(2)}{text}{self.attr('reset')}"
        else: return text
    
    def light_green(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.LIGHTGREEN_EX}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "grey", "on_green", attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.fg(10)}{text}{self.attr('reset')}"
        else: return text
    
    def cyan(self, text: str):
        if self.color_library == "colorama":
            return f"{self.fo.CYAN}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "cyan")
        elif self.color_library == "colored":
            return f"{self.fg(51)}{text}{self.attr('reset')}"
        else: return text
        
    def light_cyan(self, text: str):
        if self.color_library == "colorama":
            return f"{self.fo.LIGHTCYAN_EX}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "cyan", attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.fg(117)}{text}{self.attr('reset')}"
        else: return text
        
    def magenta(self, text: str):
        if self.color_library == "colorama":
            return f"{self.fo.MAGENTA}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "magenta")
        elif self.color_library == "colored":
            return f"{self.fg(201)}{text}{self.attr('reset')}"
        else: return text
        
           
    def light_magenta(self, text: str):
        if self.color_library == "colorama":
            return f"{self.fo.LIGHTMAGENTA_EX}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "magenta", attrs=["bold"])
        elif self.color_library == "colored":
            return f"{self.fg(13)}{text}{self.attr('reset')}"
        else: return text
        
    def bg_yellow(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.YELLOW}{self.bg.YELLOW}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "yellow", "on_yellow")
        elif self.color_library == "colored":
            return f"{self.bg(226)}{self.fg(0)}{text}{self.attr('reset')}"
        else:
            return text
    
    def bg_black(self, text: str):
        if self.color_library == "colorama":
            return f"{self.fo.WHITE}{self.bg.BLACK}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "white", "on_black")
        elif self.color_library == "colored":
            return f"{self.bg(16)}{self.fg(255)}{text}{self.attr('reset')}"
        else:
            return text
        
    def bg_blue(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.BLUE}{self.bg.BLUE}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "blue", "on_blue")
        elif self.color_library == "colored":
            return f"{self.bg(33)}{self.fg(15)}{text}{self.attr('reset')}"
        else:
            return text
        
    def bg_green(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.GREEN}{self.bg.GREEN}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "green", "on_green")
        elif self.color_library == "colored":
            return f"{self.bg(34)}{self.fg(15)}{text}{self.attr('reset')}"
        else:
            return text
        
    def bg_red(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.WHITE}{self.bg.RED}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "white", "on_red")
        elif self.color_library == "colored":
            return f"{self.bg(196)}{self.fg(15)}{text}{self.attr('reset')}"
        else:
            return text
    
    def bg_cyan(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.WHITE}{self.bg.CYAN}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "white", "on_cyan")
        elif self.color_library == "colored":
            return f"{self.bg(51)}{self.fg(15)}{text}{self.attr('reset')}"
        else:
            return text

    def bg_magenta(self, text:str):
        if self.color_library == "colorama":
            return f"{self.fo.WHITE}{self.bg.MAGENTA}{text}{self.st.RESET_ALL}"
        elif self.color_library == "termcolor":
            return self.colored(text, "white", "on_magenta")
        elif self.color_library == "colored":
            return f"{self.bg(201)}{self.fg(15)}{text}{self.attr('reset')}"
        else:
            return text