# scenzig
An engine for text-based adventure games and interactive prose using a scene-based system. The descendant of Agenzig.

As with Agenzig, the goal is to make a framework that reads all of it's content from external files in the human-readable .ini format. This is achieved with the ConfigObj module.

## Why?
For fun mostly. Also because as far as I can tell nothing quite like it exists. My inspiration was the Fighting Fantasy series of books. They would present you with options and a numbered section to turn to so see the result of your choice. They were good reads but I didn't enjoy the combat system (based on die rolls) and found it got in the way.
The plan is to have the computer handle all the math so the player can focus on making choices.

## Implemented Features
- Script finds Adventures, checks thier validity and offers to load the valid ones
- Script loads the Adventure that the player selects
- Script finds Characters and offers to load them
- Script offers to create a new character
- Script generates a list of valid actions based on allow/block-lists
- Script prints scene text and scene state text (idea is scene state text is the detail)
- Scenes, Encounters, Items, Abilities, Attributes and Vitals all have states which are automatically updated based on custom criteria
- Actions have a number of outcomes. Which one occurs is based on custom criteria and evaluations.

## Roadmap
- Write more varied demo adventures
- Implement a bonus system. Plan is to borrow code from allow/block-listing so encounters, abilities, items etc can control whether bonuses are active.
- New .py file with some basic effects as functions
- Allow labels (replacement for classes) to be replaced into Scene descriptions
- Equipment slots
- Implement encounters

## Differences from Agenzig
- Object-orientated from the start
- More commenting as I go
- Choices, Actions and Combat Actions will be combined. The actions that can be performed are determined by allowLists and blockLists
- Items and Equipment will not be difrentiated. Instead equipping 'Iron Sword' will remove it from your inventory and replace it with 'Iron Sword (equipped)' which will allowList Actions. Equipment slots will be added later along with other Action conditions.
- Fewer in-script variables. Instead of actions affecting the scene directly, they will change the scene ID stored in the Character file and trigger a refresh. The script will then print scene description direct from the scene file and assemble valid actions from combined allowlists and blocklists.
- The only thing that will be stored in-script and not written to the Character file is the effects of items and abilities. At the top of the main game loop, the script will genererate a list of valid actions from the allow/block-lists of items and abilities the character has. The Attribute modifiers of items and abilities will also be combined for each Attribute. When a varaible is requested, it will be read from the Character and then have the modifier applied to it.
- The varied Effects an Action could have will each be a seperate function. This will result in a much shorter main script, improve readability and make the project much more managable and I can start with a relatively small stable of simple effects and easily add more later.
- Character creation to be handled by the main engine i.e. based on Actions. A Character will start out as a direct clone of a template character located in an adventure's character folder. If an adventure creator wants to allow initial character customisation or have characters be rolled, then this can be achieved via scenes.
- Adventures to be divided into chapters. .scnz (equivilent of .agez) files in the folder of the Current chapter will over-ride the general (Chapter 0) .scnz files. Common usage will be to break scenes.scnz into more managable chunks but it could be used to make equipment and items work differently after progressing so far.
- I aim to actually get round to implementing encounters. Instead of being an alternative scene they will overlay on a Scene providing thier own Action allowlist and blocklist.

## Licenses
scenzig Copyright Thomas Sturges-Allard
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

scenzig Adventures are licensed independantly of the scenzig program

configobj used under the BSD license.
Copyright (C) 2005-2014:
(name) : (email)
Michael Foord: fuzzyman AT voidspace DOT org DOT uk
Nicola Larosa: nico AT tekNico DOT net
Rob Dennis: rdennis AT gmail DOT com
Eli Courtwright: eli AT courtwright DOT org

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * None of the authors names may be used to endorse or
      promote products derived from this software without
      specific prior written permission.

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

six.py Copyright (c) 2010-2017 Benjamin Peterson
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
