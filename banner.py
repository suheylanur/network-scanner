import random
import os
import time


RESET = "\033[0m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"


#Terminal stilleri

BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"


SUCCESS = "[+]"
INFO = "[*]"
WARNING = "[!]"
ERROR = "[-]"
ARROW = "->"

#ASCII BANNERLAR
BANNERS= [
    
r"""
                 ,-._
           _.-'  '--.
         .'      _  -`\_
        / .----.`_.'----'
        ;/     `
 ...   /_;

    ._      ._      ._      ._
_.-._)`\_.-._)`\_.-._)`\_.-._)`\_.-._

""",
r"""
                          .
                          A       ;
                |   ,--,-/ \---,-/|  ,
               _|\,'. /|      /|   `/|-.
           \`.'    /|      ,            `;.
          ,'\   A     A         A   A _ /| `.;
        ,/  _              A       _  / _   /|  ;
       /\  / \   ,  ,           A  /    /     `/|
      /_| | _ \         ,     ,             ,/  \
     // | |/ `.\  ,-      ,       ,   ,/ ,/      \/
     / @| |@  / /'   \  \      ,              >  /|    ,--.
    |\_/   \_/ /      |  |           ,  ,/        \  ./' __:..
    |  __ __  |       |  | .--.  ,         >  >   |-'   /     `
  ,/| /  '  \ |       |  |     \      ,           |    /
 /  |<--.__,->|       |  | .    `.        >  >    /   (
/_,' \\  ^  /  \     /  /   `.    >--            /^\   |
      \\___/    \   /  /      \__'     \   \   \/   \  |
       `.   |/          ,  ,                  /`\    \  )
         \  '  |/    ,       V    \          /        `-\
          `|/  '  V      V           \    \.'            \_
           '`-.       V       V        \./'\
               `|/-.      \ /   \ /,---`\         
                /   `._____V_____V'
                           '     '

""",
r"""
                                            .      //
                                       /) \ |\    //
  ..                             (\\|  || \)u|   |F     /)
                                  \```.FF  \  \  |J   .'/
                               __  `.  `|   \  `-'J .'.'
        ______           __.--'  `-. \_ J    >.   `'.'   .
    _.-'      ""`-------'           `-.`.`. / )>.  /.' .<'
  .'                                   `-._>--' )\ `--''
  F .                                          ('.--'"
 (_/                                            '\
  \                                             'o`.
  |\                                                `.
  J \          |              /      |                \
   L \                       J       (             .  |
   J  \      .               F        _.--'`._  /`. \_)
    F  `.    |                       /        ""   "'
    F   /\   |_          ___|   `-_.'
   /   /  F  J `--.___.-'   F  - /
  /    F  |   L            J    /|
 (_   F   |   L            F  .'||
  L  F    |   |           |  /J  |
  | J     `.  |           | J  | |              ____.---.__
  |_|______ \  L          | F__|_|___.---------'
--'        `-`--`--.___.-'-'---
""",
r"""
                           ___________ _
                      __/   .::::.-'-(/-/)
                    _/:  .::::.-' .-'\/\_`,
                   /:  .::::./   -._-.  d\|
                    /: (""/    '.  (__/||
                     \::).-'  -._  \/ \\/\|
             __ _ .-'`)/  '-'. . '. |  (i_O
         .-'      \       -'      '\|
    _ _./      .-'|       '.  (    \\
 .-'   :      '_  \         '-'\  /|/
/      )\_      '- )_________.-|_/^\
(   .-'   )-._-:  /        \(/\'-._ `.
 (   )  _//_/|:  /          `\()   `\_\
  ( (   \()^_/)_/             )/      \\
   )     \\ \(_)             //        )\
         _o\ \\\            (o_       |__\
         \ /  \\\__          )_\
               ^)__\
""",
  
]
 
def clear_screen():
    os.system(
        "cls" if os.name == "nt" else "clear"
    )
    
def get_random_banner():
    return random.choice(BANNERS)

def show_banner():
    banner=get_random_banner()
    
    print(
        BRIGHT_CYAN +
        banner +
        RESET
    )
    print(
        BOLD +
        BRIGHT_GREEN +
        "              NETWORK SCANNER TOOL" +
        RESET
    )
    print(
        BRIGHT_BLACK +
        "------------------------------------------------------------" +
        RESET
    )
    time.sleep(2)
    
def show_messages():
    
    print(
        BRIGHT_GREEN +
        f"{SUCCESS} Initializing Network Scanner..." +
        RESET
    )
    time.sleep(0.5)

    print(
        BRIGHT_CYAN +
        f"{INFO} Loading scanner modules..." +
        RESET
    )
    time.sleep(0.5)

    print(
        BRIGHT_CYAN +
        f"{INFO} Loading terminal interface..." +
        RESET
    )
    time.sleep(0.5)

    print(
        BRIGHT_YELLOW +
        f"{INFO} Loading configuration..." +
        RESET
    )
    time.sleep(0.5)

    print(
        BRIGHT_GREEN +
        f"{SUCCESS} Scanner ready." +
        RESET
    )
    time.sleep(0.5)

    print()

    print(
        BRIGHT_WHITE +
        "Type " +
        BRIGHT_YELLOW +
        "'help'" +
        BRIGHT_WHITE +
        " to see available commands." +
        RESET
    )
    print()
    time.sleep(1)
def print_success(message):
    print(
        BRIGHT_GREEN +\
             f"{SUCCESS} {message}" +
        RESET
    ) 
def print_info(message):
    print(
        BRIGHT_CYAN +
        f"{INFO} {message}" +
        RESET
    )    
       
def print_warning(message):
    print(
        BRIGHT_YELLOW +
        f"{WARNING} {message}" +
        RESET
    ) 
def print_error(message):
    print(
        BRIGHT_RED +
        f"{ERROR} {message}" +
        RESET
    ) 
def print_section(title):
    print()
    print(
        BRIGHT_CYAN +
        "============================================================" +
        RESET
    )

    print(
        BOLD +
        BRIGHT_WHITE +
        f"  {title}" +
        RESET
    )

    print(
        BRIGHT_CYAN +
        "=============================================================" +
        RESET
    )

    print()

def get_prompt():
        return(
            BOLD +
            BRIGHT_MAGENTA +
            "nst"+
            BRIGHT_WHITE +
            ">" +
            RESET
        )
def show_help():
    print_section("AVAILABLE COMMANDS")
    print(
        BRIGHT_GREEN +
        "scan       " +
        RESET +
        "start network scan"
    )
    print(
        BRIGHT_GREEN +
        "ports      " +
        RESET +
         "show common ports"
    )
    print(
        BRIGHT_GREEN +
        "banner     " +
        RESET +
        "Display random banner"
    )

    print(
        BRIGHT_GREEN +
        "clear      " +
        RESET +
        "Clear terminal"
    )

    print(
        BRIGHT_GREEN +
        "help       " +
        RESET +
        "Show this help menu"
    )

    print(
        BRIGHT_GREEN +
        "exit       " +
        RESET +
        "Exit Network Scanner"
    )
    print()
    print_section("SCAN OPTIONS")

    print(
        BRIGHT_GREEN +
        "-t, --target" +
        RESET +
        "       Target IPv4 address"
    )

    print(
        BRIGHT_GREEN +
        "-p, --ports" +
        RESET +
        "        Ports to scan (e.g. 22,80,443 or 1-1000)"
    )

    print(
        BRIGHT_GREEN +
        "--timeout" +
        RESET +
        "         Timeout for each connection (default: 0.5)"
    )

    print(
        BRIGHT_GREEN +
        "--workers" +
        RESET +
        "         Number of concurrent threads (default: 100)"
    )

    print(
        BRIGHT_GREEN +
        "--banner" +
        RESET +
        "          Try to grab service banners"
    )

    print(
        BRIGHT_GREEN +
        "--txt FILE" +
        RESET +
        "        Save results as a TXT report"
    )

    print(
        BRIGHT_GREEN +
        "--json FILE" +
        RESET +
        "       Save results as a JSON report"
    )

    print(
        BRIGHT_GREEN +
        "--csv FILE" +
        RESET +
        "        Save results as a CSV report"
    )

    print()
        

    print()           
def show_exit_message():
    print()
    print(
        BRIGHT_YELLOW +
        f"{INFO} Shutting down Network Scanner..." +
        RESET 
    )   
    print(
        BRIGHT_GREEN +
        f"{SUCCESS} Goodbye!!!" +
        RESET
    )
    
    

    print()    
    
if __name__=="__main__":
    clear_screen()
    show_banner()
    show_messages()
    show_help()
    time.sleep(0.5)
    
    while True:
        command = input(get_prompt())  
        if command == "help":
            show_help()
        elif command == "clear":
            clear_screen()
        elif command == "banner":
            show_banner()
        elif command == "exit":
            show_exit_message()
        else:
            print_error(
                f" Unkown command: {command}"
            )                

    
        
        

        