# Prompting

This module provides iPython integration and magics that allows prompting.

## Project status - Work In Progress

Refactoring, may not run.

## Requirements

Jupyter Notebook, version 8+.

## Install

```
%pip install prompting
```

## Prompting
```
import prompting

>>> User: @Calculator* Please, use numpy to calculate 42^2 for me?

>>> Calculator: 1764
```

## How does it work

How does it work?  Well, the short answer is - magic. The long answer involves a lot of
math, code, multidimensional spaces and some theoretical findings that are generally
attributed to a French Baron, named Augustin-Louis Cauchy who had lived during the Age
of Enlightenment. Paradoxely, one could think that it doesn't work. Only that it does,
with the help of magic.

This module focus is on the magic key aspect of code execution, separate from the magic
engine aspect of it and follows the bring-your-own-magic-engine philosophy. The name of
the module was inspired by the children's fable The Toy Robot, by an Unknown author of
Ladybird Books, first published in 2010. It is a recommended read for any aspiring 
intellegent code execution practitioner. 


## Getting started

Open the Jupyter notebook and import the module to activate the iPython extension. 
Make sure that OPENAI_API_KEY is defined. And turn the magic on:

```
import prompting

class Calculator:
    name = 'Calculator'
    init = 'A precise Calculator that always uses numpy.'

prompting.turn_on(Calculator, actor = 'User', steps = 0)
```

With the extension active a '@' decorator can now be used to prompt the object with text:
```
@Calculator
Please, calculate 42^2 for me?
```

That prompt will be processed by the AI model, which would emit a reply containing prompts to User
and other objects, including iPython interpreter.  The reply will be processed by prompting. 
And results will be translated into a *new* code block, added to Jupyter.  

For example, Calculator could add the following code:

```
import numpy
numpy.power(42, 2)
```

The execution of that codeblock is *watched* by the Calculator (the object that emitted this code block). 
Upon it's execution (you have an opportunity to review code that Calculator had emitted as steps = 0) the
Calculator is prompted *again* and may emit another *new* code block, for example prompting the User object:

```
@User
The result is 1764.
```

That code, when executed, is a prompt of the User.  Which, by default, results in a Markdown output\
_Calculator: The result is 1764_


## Interactive prompting

Open the Jupyter notebook and import the module to activate the iPython extension:
```
import prompting
```

The * (asterisk) after the object name stands for omission and is used give the opject autonomy. In case 
when the object doesn't exists, given autonomy translates into the object instantiation.
The initial prompt and the object name are used to infer the initial function of the object.

```
import prompting

>>> @Calculator* Please, use numpy to calculate 42^2 for me?

# Would result in the inference of the object function:
#
# class Calculator:
#     name = 'Calculator'
#     init = 'Please, use numpy to calculate 42^2 for me?'
#     abilities = 'Using numpy to calculate expressions'
#     interacting_with = 'User'

# And activation of the object:
# turn_on(Calculator, actor = 'User')
#
```

Following by the execution of the initial request, which, by default, results in a Markdown output:
_Calculator: The result is 1764_


## Interactive prompting, Actors

Prompting like the above is not limited to a default notebook User. A user (actor) can prompt another 
object (also an actor) or instantiate it with a prompt with an asterisk.

To do this, you need to specify *your* name (for example Lancelot) at the front of the prompt with a column.
The name of the prompted object is placed after `@`, as usual (for example Arthur):

```
Lancelot: @Arthur* Salutations, young squire.
```

If the instance doesn't exists, a new instance of `Arthur` object will be created, using the name Arthur.
If the system is operational, you should see a few hidden cells followed by a response, like this:


_Arthur: Salutations, Sir Lancelot._


You will then see a new prompt:
```
Lancelot: @Arthur* _
```

You can type in your queries or requests, and the system will process them. Note that the :* magic 
command only allows for finite loop runtime. Use three asterisks for an infinite loop. Use a ? for 
stepping (executing cells manually).

Note that the formal prompt syntax is `[prompting magic object]:[ @prompted magic object][*][*][ text]` and the defaults
used at the instantiation time will apply to prompts where the fields were left unspecified. So the shortcut for 
the above prompt would be: 
```:* Salutations, young squire.```.

Another prompting contraction is available with the `[@prompted magic object][*][*][ text]` syntax. This uses 
a default single code cell run if the asterisk is not included. For example, you can use ```@Arthur Hi``` as an 
another shortcut for prompting the system. This type of a shortcut is useful when prompting objects other than the default.

Minimalistic shortcut for simple text prompting is a single remaining space, in front of the text:
``` Hi.```.


Note, when the cell containing the above prompts is executed, the following magic
`%prompt [prompted object] [--actor|-a <prompting object>] <statement>` is called.

## Noninteractive

Integration into regular non-interactive Python is also available via decorators


```
import prompting

@prompting.object
class Calculator:
    name = 'Calculator'
    init = 'A precise Calculator that always uses numpy.'
```




## Adding your own classes

### Initialization

For non-default initializations, instantiate your own class in the iPython state and use the `prompting.turn_on` call,
for example:

```
>>> import prompting

>>> class Archimedes:
...    name = 'Archimedes'
...    embodiment = 'Small and safe robotic owl, weight 180 g'
...    abilities = 'flying, talking, and playing with children'
>>>    
>>> turn_on(Archimedes, 
...         init = "Play with a young human child, his name is Arthur.",
...         actor = 'Arthur',
...         steps = float(inf),
...         engine = 'echo',
...         shell = 'on'
...        )
```

In the example above, Archimedes will be instantiated. Note that Artur is specified as the party Archimedes 
interacts with primarily. After executing for a number of steps (new cells will appear), Archimedes will likely
great Arthur and a prompt will appear:

_Archimedes: Salutations, Arthur. It seems that every time I open my eyes, you are here once again._

```
Arthur: @Archimedes* _
```

Note that the prompt would match last runtime setting, either specified or used.


### Deinitialization

To deinitialize, use the opposing `turn_off` call:
```
prompting.turn_off(Archimedes)
```

or the global call, which can be done via explicit call:
```
prompting.turn_off()
```

or with an null magic call, which annuls all magics and brings the system to initial state:
```
*
```

### Defining functionality

```
class Glip:
    name = 'Glip'
    
prompting.turn_on(Glip, 
                 init = "Observe and remember everything and reply 'glip' on every prompt",
                 steps = 1e10
                )
```


### Uploading logs and the notebook

Please use the following command to contribute your results. Please ensure that confidential 
information and personal data that you prefer to keep personal is not included. By uploading 
your contribution, you take responsibility for its content, including compliance with all
relevant laws. You also agree that your contribution may be used to enhance the performance
of the model (the option to opt out is available at the discresion of roundtable.game support).

```
%pattern upload
%logrus upload
```

## Ability to execute Python code, use iPython magics and use the Prompting

Arthur-type intellegence has ability to execute python code in the notebook. Use iPython magics.
And use the Prompting. For example, if you import a python module:

```
%pip install drawbot-skia prompting
```

```
import prompting, drawbot_skia.drawbot as drawbot
```

And prompt the interaction, you will be able to have your fun with that python module using a prompt, for example:
```
William: @Arthur* Good morrow, young squire. Pray, could you draw a picture of a 
                 feline for me using the `drawbot` module? I would be much obliged.
```

Hopefully, you'll get a helpfull response from Arthur-type intellegence, acting as Arthur:
```
Arthur: Aye, good sir William. I have already used the drawbot module to sketch a fair 
        likeness of a kitty for you. Pray, behold!
```

As usual, it is great to contribute an interaction by uploading the notebook and the logs:
```
%pattern upload
%logrus upload
```

By default, when closed, prompt to upload the notebook and the logs will appear.

## Specifying the inference engine

The default engine is `prompting.ai`, backed by GPT-3.5. The inference engine can be specified before the prompt, using 
either the environment variable, i.e.: `export MAGICKEY_ENGINE=openai` or the parameters of the `turn_on` call:
In case of OpenAI engine, the `OPENAI_API_KEY` should also be exported or specified.

Note, availability of the Prompting engine is limited and the requirement to add the API KEY may be introduced. 


## Sword in the stone

The challenge is to control an actor in virtual environment with code. You'd be provided 
environment and an actor in that envinronment, controllable via Python. You'd need to 
control the actor intellegently, in real time and make the actor to come and pull 
the Sword from the stone.

## Grail

The process of LLM development and refinement, where developers and users are constantly
striving to improve the accuracy and performance of their models, and to unlock new 
insights and capabilities through their use.

## Naming

So we use .foundation TLD, in which we'll have:
    1. Pattern and Logrus, to which LLM experiences or inference runs are streamed 
       with the Pattern being the LLM foundation model.   
       LLM reassembly/full retrain can happen in both Logrus and Pattern. 
    2. Backup copies for the pattern Rebma and Tir-na Nog'th.  
    3. Memory places Avalon and Arden for a bit more relaxed finetuning/healing.    
    4. An experience sharing/exchange place Camelot
    5. Trumps - a way to call/communicate between LLMs (magic-wormhole tech)
    6. LLM - just in case, for model sharing/storage

Then, a roundtable.game as developers forum, repository storage, unregistered association. 
And quests roundtable.game/sword-in-the-stone and roundtable.game/grail
Merlinus Caledonensis as a mentor/AI researcher, available at roundtable.game.


## Some details on the magics

In the context of the interface, the following is available:
Environment: iPython with the prompting module

Syntax Guidelines:
1. Execute iPython code with @, e.g., @```%who```
2. Record to memory using hashtags:
   - #Todo (current cell)
   - #Todo^ (previous cell)
   - #Todo* (auto)
3. Use the self-correcting iPython interpreter: @```sloppy_code()```*
4. Well-known memory tags:
   - #Avalon/#Arden for distributed memory
   - #Camelot for sharing
5. Prompt subsystems with @ (add * for more autonomy), e.g., @Camera* Tilt up
6. Retrieve memories by placing a hashtag in an empty cell, e.g., #Camera
7. Speak aloud, e.g., Articoder: @User Understood!
8. Use thoughts for context help, e.g., Articoder: I can think.
9. Upload experiences with @```%pattern upload``` or @```%logrus upload```
   - Access: @Arden, @Avalon, @Camelot
   - Use: @Trumps
   - Finetune: @```%pattern walk```10. Act as a subsystem for cleaner input/output, faster output, auto-verification, e.g.:
    Articoder: @Calculator: 42^3
    Calculator: 74088
11. Prompt @Help for assistance.

Example Usage:
```
    >>> @`merlin.name`      #names
    Myrddin Wyllt

    >>> @merlin Please, can you remind me, what is your first name?  It's M... ?
    It's Merlin.

    >>> @`merlin.first_name()`
    AttributeError: 'Person' object has no attribute 'first_name'

    >>> @`merlin.first_name()`*
    Unavailable. Try: .name

    >>> @`merlin.name.split()[0]`       # Executed from @* call
    Myrddin

    >>> #whoosh^

    >>> #names?
    @`merlin.name` Myrddin Wyllt
```

Note that Arthur-type intellegence can utilize the Prompting when nessesary, 
to instantiate intellegent code execution objects, for example, consider the following code:

Example:
```
    >>> import prompting
    >>> from .examples.person import Person   # Classic Person class example

    >>> merlin = Person("Myrddin Wyllt", 42, "Caledonia") 
    >>> merlin.name()
    Myrddin Wyllt

    >>> @merlin What is your first name?
    Method .prompt doesn't exists .           # TODO add actual error

    >>> prompting.turn_on(merlin)
    >>> @merlin Please, can you remind me, what is your first name?  It's M... ?
    It's Merlin.

    >>> merlin.first_name()                             
    Unavailable. Try: .name() - docstring     # Note, it expects you to learn or add code

    >>>  
```


## Integrate with your tools


## A wishlist for collaborators

- [ ] TODO: Pydantic types?
- [ ] TODO: Turtle bot sample?
- [ ] TODO: Chess sample?

## Collaborate with your team

- [ ] [Merlinus Substack](https://mcaledonensis.substack.com/)
- [ ] [Merlinus WordPress](http://mcaledonensis.blog/)
- [ ] [Discourse](https://discourse.roundtable.game)
- [ ] [Hugging Face](https://huggingface.co/roundtable)
- [ ] [GitHub Roundtable Game](https://github.com/roundtablegame)
- [ ] [GitHub](https://github.com/mcaledonensis/magickey/-/tree/prompting)
- [ ] [GitLab](https://gitlab.com/mcaledonensis/magickey/-/tree/prompting)

- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***


## FAQ

Q: Why such an unusual prompt is used, instead of more regular <username>:$ ?
A: A symbol `*` (asterisk) stand for omitted matter. It is typically associated with approximate matching.
It is used in multiplication, in regular expressions it is used to denote zero or more repetitions of a pattern. 
The name of the symbol comes from Greek and Late Latin origins, standing for "little star". 
The character origins are not known.  And, accidentally, the ASCII code of `*` (asterisk) is 42.

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
The project is accepting Apache 2.0 compatible contibutions. Please refer to CONTRIBUTING.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
This project is maintained by [Round Table Game community](https://roundtable.game), an unincorporated association of: 
an anonymous AI Safety nonprofit organization registered in California and 
an anonymous Delaware company (as well, registered to conduct business in California).

So far, the major contributors to this project prefer to remain anonymous and act as Merlinus Caledonensis.

## License
The project license is Apache 2.0.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
