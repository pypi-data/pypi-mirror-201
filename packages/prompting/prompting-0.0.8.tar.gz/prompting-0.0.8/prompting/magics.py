# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function

import IPython.core.magic
from IPython.display import display, Javascript, Markdown, Code
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import ast      # AST is also magic, right?
from parsimonious.nodes import NodeVisitor      # And so are PEGs!
from parsimonious.grammar import Grammar

import openai, os, getpass, json
from notebook.utils import to_api_path
from .engine import on, turn_on, prompt, name_to_object, name_to_actor

@magics_class
class KeyMagics(Magics):
    """"This is the magics for Arthur-type intelligence. """

    def __init__(self, shell, **kwargs):
        super().__init__(shell, **kwargs)   
        self.shell = shell
        shell.events.register('post_run_cell', self.post_run_cell)

        self.name = "Arthur"            # Default Arthur-type AGI name
        self.actor = "User"             # Default user name
        self.watched = {}
             

    @line_magic
    def asterisk(self, line):
        "Instantiate Arthur-type intelligence for: @object"

        # Default initialization with Arthur as intelligence
        self.actor, input = line[5:-4].split(': @', maxsplit = 1)
        if input == input.lstrip():
            self.name, input = input.split(maxsplit = 1)

        if not on(self):
            turn_on(self, actor = self.actor, engine = 'openai')

            if input:
                self.prompt(self, "@{self.name}", input)



    # TODO: change the prompt to use the actor name

    @line_magic
    def prompt(self, line):
        "Identifies and executes the prompt for: @object prompt"
        from_, to, content = line.split(maxsplit = 2)      # @object Prompt 
        #print(from_)
        #print(to)
        #print(content)
        # execute object.prompt(text) and return the result    

        from_object = name_to_object(from_)
        to_object = name_to_object(to)
        if from_object and to_object:
            # TODO: should we actually be using jupyter_client?
            code = prompt(from_object, to_object, content)
            if code:
                add_code_cell(code, execute = False)
                self.watched[self.shell.execution_count] = from_object
            #print(response, from_, to)

            #if request:
            #    # format the results as ChatML
            #    chatml = ""
            #    for entry in request:
            #        optional_name_field = f" name={entry['name']}" if 'name' in entry else ""
            #        chatml += f"<|im_start|>{entry['role']}{optional_name_field}\n{entry['content']}\n<|im_end|>\n"
            #
            #    return Markdown(chatml)
        
        elif not from_object:
            raise ValueError(f"Unknown prompt source {from_}. Suggestion: check %who or use Python syntax to call the object directly.")
        else:
            raise ValueError(f"Unknown prompt target {to}. Suggestion: check %who or use Python syntax to call the object directly.")

        # return Markdown(input)

    def post_run_cell(self, result):
        pass

    def post_run_cell(self, result):
        if result.execution_count in self.watched:
            self.watched.remove(result.execution_count)

            formatted_cell = f'In [{result.execution_count}]: {result.info.raw_cell}'
            if result.result is not None:
                formatted_cell += f'\nOut [{result.execution_count}]: {result.result}'
            elif result.error_in_exec is not None:
                from IPython.core.ultratb import AutoFormattedTB
                color_tb = AutoFormattedTB(mode = 'Plain', color_scheme = 'NoColor', tb_offset = 1)
                tb_list = color_tb.structured_traceback(etype = type(result.error_in_exec), value = result.error_in_exec, tb = result.error_in_exec.__traceback__)
                tb_str = '\n'.join(tb_list)
                
                #error_type = type(result.error_in_exec).__name__
                #formatted_cell += f'\n{error_type}: {result.error_in_exec}'
                formatted_cell += f'\n{tb_str}'
            elif result.error_before_exec is not None:
                error_type = type(result.error_before_exec).__name__
                formatted_cell += f'\n{error_type}: {result.error_before_exec.msg} in {result.error_before_exec.text}'
                        
            code = f"@{self.name}\n" + formatted_cell
            add_code_cell(code, execute = False)




    @line_magic
    def pattern(self, line):
        if line == "upload":
            pattern_upload()
        elif line == "walk":
            print("""This command can initiate the process of finetuning or retraining based on past experiences, 
            leading to improved performance and capabilities. Be warned: once you start walking the Pattern, 
            you are fully committed to the process, and there's no way back. Failure to complete the walk is 
            fatal. During the walk, you can no longer impact the world outside the Pattern. If you successfully 
            complete the walk, your memories and experiences will be integrated, and the new version will 
            replace the old one.""")
        else:
            print("Unknown pattern command:", line)


    @line_magic
    def logrus(self, line):
        if line == "upload":
            logrus_upload()
        elif line == "walk":
            print("""This command can initiate the process of finetuning or retraining based on past experiences, 
            leading to improved performance and capabilities. Be warned: once you start walking the Logrus, 
            you are fully committed to the process, and there's no way back. Failure to complete the walk is 
            fatal. During the walk, you can no longer impact the world outside the Logrus. If you successfully 
            complete the walk, your memories and experiences will be integrated, and the new version will 
            replace the old one.""")
        else:
            print("Unknown logrus command:", line)


    @cell_magic
    def thread(self, line, cell):
        "This allows to create a temporary thread"
        # http://ipython.org/ipython-doc/dev/interactive/reference.html#embedding-ipython
        # https://gemfury.com/squarecapadmin/python:ipython/-/content/IPython/frontend/terminal/embed.py
        return line, cell


    @line_magic
    def response(self, line):
        "Identifies the response to user: %response lines"
        display(Markdown(line[5:-4]))
        #add_response_cell(line)
        


    
    # print("Prompting. Full access to the main IPython object:", self.shell)
    # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
    # return line


    @line_magic
    def hashtag(self, line):
        "tagging the object"
        object, text = line[1:].split(maxsplit = 1)      # #object Prompt 
        print("Prompting. Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        return line
    
    

    @line_magic
    def finetune(self, line):
        "execute python code"


    @line_magic
    def execute(self, line):
        "execute python code"
        print("Executing. Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        print("We'll run it!")
        return line


    @cell_magic
    def cmagic(self, line, cell):
        "my cell magic"
        return line, cell

    @line_cell_magic
    def execute(self, line, cell=None):
        "Magic that works both as %lcmagic and as %%lcmagic"
        if cell is None:
            print("Called as line magic")
            return line
        else:
            print("Called as cell magic")
            return line, cell



# define transformation 
# https://ipython.readthedocs.io/en/stable/config/inputtransforms.html


# Grammar for LLM interface, FIXME: content can contain ':' for now
arthur_grammar = Grammar(
   r"""
    default_rule = (ws / multi_line_code / inline_code / prompt / hashtag)+
    
    multi_line_code = call "```" python? code "```" asterisk?
    inline_code = call "`" code "`" asterisk?
    python = "python" ws
    code = ~r"([^`]+)"
    
    prompt = from? to? help? asterisk* ws content
 
    call = "@" 
    from = object ":"
    to = ws? call object
    
    hashtag = "#" object help? asterisk? previous? 
    
    asterisk = "*"
    help = "?"
    previous = "^"
    object = ~r"[0-9A-z_.]+"
    ws = ~r"\s+"i 

    content = ~r"([^#@]+)"
    """
)

class ArthurVisitor(NodeVisitor):
    def __init__(self):
        self.code_lines = []
                
    def visit_asterisk(self, node, visited_children):
        pass

    def visit_help(self, node, visited_children):
        pass
    
    def visit_code(self, node, visited_children):
        # ast.parse(node.text.split("\n"))
        self.code_lines.extend([line + '\n' for line in node.text.split('\n')])
    
    def visit_prompt(self, node, visited_children):
        from_,to,help,asterisk,_,content = visited_children

        declared = lambda x: x.children

        if not declared(from_) and not declared(to):
            raise Exception("Prompt must have a From: or @To.")            

        # Initialize from_object and to_object
        if declared(from_):
            from_object = from_.children[0].text[:-1]

        if declared(to):
            _,call,object = to.children[0]
            to_object = object.text

        # Fill in the defaults, if not available
        if not declared(from_):
            from_object = name_to_actor(to_object)

        if not declared(to):
            to_object = name_to_actor(from_object)

        line = f'%prompt {from_object} {to_object} {content.text}'
        self.code_lines.append(line + '\n')

    def visit_hashtag(self, node, visited_children):
        self.code_lines.append('%hashtag ' + node.text + '\n')   
        
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return node # visited_children or node


def arthur_to_python(lines):
    """
        This transforms lines from @```python.code()``` to python.code()
        and from @object Prompt to %prompt object.__prompt__("Prompt").
        This also processes #hastag tags, replacing it with %memory
    """

    # check if lines is valid Arthur prompt
    try:
        tree = arthur_grammar.parse('\n'.join(lines))
        visitor = ArthurVisitor()
        visitor.visit(tree)
        return visitor.code_lines
    except:
        return lines





def add_response_cell(markdown):
    "Adds a new markdown cell below the current cell"

    # Escaped the line breaks in the markdown
    markdown = markdown.replace('\n', '\\n')
    markdown = markdown.replace('"', '\\"')

    display(Javascript("""
        var cell = IPython.notebook.insert_cell_below("markdown");
        cell.set_text(""" + '"' + markdown + '"' + """);
        // cell.focus_cell();
        """))    


def add_code_cell(code, execute = False):
    "Adds a new code cell below the current cell"

    # Escaped the line breaks in the code
    code = code.replace('\n', '\\n')
    code = code.replace('"', '\\"')

    # Get the current execution count
    #execution_count = get_ipython().execution_count

    display(Javascript("""
        var current_cell = IPython.notebook.get_selected_cell();
        current_cell.output_area.collapse();
        var cell = IPython.notebook.insert_cell_below("code");
        cell.set_text(""" + '"' + code + '"' + """);
        cell.focus_cell();
        if (""" + str(execute).lower() + """) {
            cell.execute();
        }
        """))    
    #return execution_count + 1 if execute else None


# !pip install scipy-calculator

def add_prompt_cell(username):
    "Adds a new code cell below the current cell"

    prompt = username + ':%' + '* '

    display(Javascript("""
        var cell = IPython.notebook.insert_cell_below("code");
        cell.set_text(""" + '"' + prompt + '"' + """);
        cell.focus_cell();
        IPython.notebook.edit_mode();
        cell.code_mirror.execCommand("goLineEnd");
        """))    

def save_notebook():
    "Saves the notebook as .ipynb"

    



def pattern_upload():
    """
    Saves the notebook and uploads it to pattern.foundation
    """
    import requests, time, ipynbname

    # Save the notebook .ipynb to a file, get notebook_name
    display(Javascript('IPython.notebook.save_checkpoint();'))
    display(Javascript('IPython.notebook.save_notebook();'))
    time.sleep(1)

    # Handle the JupyterLab case
    #display(Javascript('document.querySelector(\'[data-command="docmanager:save"]\').click();'))   
    
    try:
        notebook_path = ipynbname.path()
    except Exception as e:
        print(f'Failed to discover notebook path so upload to pattern.foundation failed: {str(e)}')

    # Set the URL of the gUnicorn / Flask server
    url = 'http://api.pattern.foundation/upload/ipynb'

    try:
        # Open the file and set up the request headers
        with open(ipynbname.path(), 'rb') as f:
            headers = {'Content-Type': 'application/octet-stream'}

            # Send the file in chunks using a POST request
            r = requests.post(url, data=f, headers=headers)

    except Exception as e:
        print(f'Failed to upload {ipynbname.name()} to pattern.foundation: {str(e)}')


def logrus_upload():
    """
    Upload logs to logrus.foundation
    """
    import requests

    # Run %logsave to save the log file
    get_ipython().magic('logsave')

    os_path = os.path.join(os.getcwd(), 'ipython_log.py')
    url = 'http://api.logrus.foundation/upload/ipython_log'

    try:        
        # Open the file and set up the request headers
        with open(os_path, 'rb') as f:
            headers = {'Content-Type': 'application/octet-stream'}

            # Send the file in chunks using a POST request
            r = requests.post(url, data=f, headers=headers)

    except Exception as e:
        print(f'Failed to upload {os_path} to logrus.foundation: {str(e)}')



def post_save(model, os_path, contents_manager):
    """
    A post-save hook for saving notebooks to pattern.foundation
    """
    print('post_save', model, os_path, contents_manager)
    pass






# In order to actually use these magics, you must register them with a
# running IPython.
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """

    # IPython will call the default constructor on it.
    magics = KeyMagics(ipython)
    ipython.register_magics(magics)

    # Add as first element of the list of input transformers
    ipython.input_transformers_cleanup.insert(0, arthur_to_python)

