# scenzig
An engine for text-based adventure games and interactive prose using a scene-based system. The descendant of Agenzig.

As with Agenzig, the goal is to make a framework that reads all of it's content from external files in the human-readable .ini format. This is achieved with the ConfigObj module.

## Why?

For fun mostly. Also because as far as I can tell nothing quite like it exists. My inspiration was the Fighting Fantasy series of books. They would present you with options and a numbered section to turn to so see the result of your choice. They were good reads but the combat system is dull, overly simple and unintuitive.

## Differences from Agenzig

- Object-orientated from the start
- More commenting as I go
- Choices, Actions and Combat Actions will be combined. The actions that can be performed are determined by Whitelists and Blacklists
- Fewer in-script variables. Instead of actions affecting the scene directly, they will change the scene ID stored in the Character file and trigger a refresh. The script will then print scene description direct from the scene file and assemble valid actions from combined whitelists and blacklists.
- The only thing that will be stored in-script and not written to the Character file is the effects of equipment and items. On Character load and when equipment is taken off or put on, a script will run through inventory contents and genererate an action whitelist and a action blacklist. An equipment modifier will also be generated for each variable. When a varaible is requested, it will be read from the Character and then have the modifier applied to it.
- Character creation to be handled by the main engine i.e. based on Actions. A blank character will be created based on parameters provided by the main file with no randomisation or player input. It's up to the 
- Adventures to be divided into chapters. .scnz (equivilent of .agez) files in the folder of the Current chapter will over-ride the general (Chapter 0) .scnz files. Common usage will be to break scenes.scnz into more managable chunks but it could be used to make equipment and items work differently after progressing so far.
- I aim to actually implement encounters. Instead of being an alternative scene they will overlay on a Scene providing thier own Action whitelist and blacklist. 

## Implemented Features

Nothing! :P

## Roadmap

- Script finds Adventures, checks thier validity and offers to load the valid ones
- Script loads the Adventure that the player selects
- Script finds Characters (checks thier validity?) and offers to load them
- Script offers to create a new character

- Unequiping items
- More commenting
- Granting the ability to change scene and scene states as an item effect
- Improve equipment slot system
- Implement the ability to make choices
- Allow equipment to grant abilities, armor and attribute boosts
- Implement non-combat abilities
- Add a new character creation technique
- Implement combat


## Licenses
scenzig Copyright Thomas Sturges-Allard
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. http://creativecommons.org/licenses/by-nc-sa/3.0/

configobj Copyright (c) 2003-2010, Michael Foord & Nicola Larosa
All rights reserved.
E-mail : fuzzyman AT voidspace DOT org DOT uk

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the name of Michael Foord nor the name of Voidspace
      may be used to endorse or promote products derived from this
      software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
