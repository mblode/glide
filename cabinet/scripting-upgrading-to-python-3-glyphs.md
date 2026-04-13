---
title: "Scripting: upgrading to Python\_3 | Glyphs"
source: 'https://glyphsapp.com/learn/scripting-upgrading-to-python3'
type: web
excerpt: "So you want to move your Python code to Glyphs\_3, but perhaps still need to support Glyphs\_2? Here is what you need to know."
siteName: 'https://glyphsapp.com/learn/scripting-upgrading-to-python3'
date: '2026-04-06T05:19:41.322Z'
---
Glyphs 3 is here, and Python 2 is on its way out. This tutorial is about getting the code for your scripts and plug-ins to work in both Glyphs 2 and 3, and in both Python 2 and 3. This way, you can ensure a smooth transition for your users.

OK, so this is about upgrading your code in such a way that it will work in _both_ environments. Yes, it can be done. And it is pretty cool, and requires less effort than you may think. We are going to do it in two steps: first we are going to transfer all existing code to Python 3, and in a later step, we will adapt it to the new API.

So, let’s make the changes in our code. Read on.

## Quick guide

First, we will _stay in Glyphs 2,_ but upgrade our code to Python 3 and at the same time, keep it compatible with Python 2. To achieve this, you need to do these couple of things in all of your scripts:

1. Make sure the heads of your scripts contain these `__future__` imports:

```python
#MenuTitle: SCRIPTNAME
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
```

2. Change all your `print x` statements into `print(x)` functions. (The `futurize` script can help you with that, see further below.)

3. Explicitly import all `NS` objects from `Foundation` (basic stuff) or `AppKit` (anything UI-related). When in doubt, import from `AppKit`, because `AppKit` includes `Foundation`. E.g., `from Foundation import NSPoint`, etc.


Now, if you want to keep the script working in Glyphs 2, verify if your scripts still work in Glyphs 2.

## In detail

### Getting Python 3

Check to see if you have Python 3 installed already. In Terminal.app, type:

```bash
python3 --version
```

… and press Return. You should get something like this as a result:

```bash
Python 3.7.5
```

If that is what you have, you’re good. Please skip to the next chapter.

If, however, you get a `command not found` error in return, then you need to install Python 3. Te best way to do this is to make sure you have a good internet connection and type this in Terminal.app:

```bash
brew install python3
```

Should you get permission errors, try again with a prepended `sudo`:

```bash
sudo brew install python3
```

If you have to resort to `sudo`, you will be asked to type your Mac password. Don't be alarmed if you do not see password bullets, that is just the way Terminal handles passwords. Just type your password ‘blindly’ and press the Return key to continue.

If the error you receive is about `brew` being unknown, you may need to [install Homebrew first](https://docs.brew.sh/Installation).

Once this is done, try the `python3 --version` command again.

Still getting an error? If you know how to handle homebrew, try `brew install python3` or `sudo brew install python3`, and then try again. If you still get an error, please make yourself heard in the forum. We will help you there.

**Update 2020-01-21:** Tim Ahrens reports difficulties under certain conditions: When you run `python3 --version` you will receive a _command not found_ error. However, when you do a `brew install python3`, it will tell you that no formulae were changed, perhaps adding that Python 3 is already installed but not linked. It will suggest to use `brew link python`. If that works for you, fine. You may however still run into trouble, especially symlink error messages. In that case, try `brew link --overwrite python` to force the symlink, or delete the offending directory and try `brew link python` again.

Again, verify with `python3 --version` if everything is done now.

### Batch replacing

All modern code editors (Sublime Text, TextMate, Atom, but also BBEdit) support finding and replacing across multiple files, or iterating through a folder of .py files. Take a closer look at the options in you Find dialog of your preferred editor. It’s easy.

![](<Base64-Image-Removed>)

### print()

This, by far, is going to be the biggest change. In fact, for the very most scripts, it will be the _only_ significant change in the code.

In Python 2, `print` was a _statement._ That means that you would write the word `print` followed by a space, followed by whatever expression you wanted to be evaluated and printed. In Python 3, `print()` is a _function._ That means it gets those parentheses at the end, and whatever expression you want it to evaluate and print, must be an argument inside those parentheses. In other words, what used to be `print "hello"` has now become `print("hello")`. Apart from that, it works pretty much the same way it used to do. That includes formatting strings like this: `print("Error in glyph %s."%glyphname)`, or chaining arguments like this: `print("a","b","c")`.

You can easily make your code compatible with both Python 2 and 3 by simply adding this import at the top, even before the `#MenuTitle` line:

```python
from __future__ import print_function
```

… and then converting every instance of `print "..."` into `print("...")`

One special case in Python 2 was the print statement with a comma at the end of the line. That way, the inherent newline at the end of each statement execution was suppressed. In order to replicate this in Python 3, you would have to write:

```python
print(letter, end='')
```

But that’s about it. So, add that import at the very top, add those parentheses to your `print` statements, and you’re all set.

### Strings

This is probably a non-issue. But there may be an edge case where this may make a difference. In Python 2, strings were 7-bit ASCII by default. In Python 3, they are UTF-8 by default. If you want to start coding this way, and still stay compatible with Python 2, you can add this import at the top of the `.py` file:

```python
from __future__ import unicode_literals
```

And all your strings will be UTF-8 strings. But do not worry too much about this, because the `u"..."` construction still is accepted in Python 3. However, if you like, you can start cleaning out these superfluous u’s now.

One thing you may still need to clean up are `str()` calls because they are more likely to throw errors at you. Get rid of them wherever possible and replace them with formatting strings. So, instead of `str(myNum)`, better use a construction like `"%i"%myNum`.

Or you don’t care and leave the strings as they are, and only add those imports if you get ‘Non-ASCII’ errors.

### Division

In Python 2, if all involved numbers were `int`, the whole calculation would be `int` only. Typically this would make for surprising results with the division, where `3/2` would yield `1` and not `1.5`. In other words, it would default to a floor division.

This is different in Python 3. `3/2` yields `1.5`. If, for whatever reason, you still need a floor division, you can still use the double slash: `3//2`, and get `1` as a result.

I recommend you switch to the Python 3 behavior and always import the new division operator:

```python
from __future__ import division
```

And feel free to get rid of any `float()` conversions you used to throw at your integers in order to prevent the floor division in Python 2.

### Exceptions

The `try` statement lets you catch errors, and if one actually happens, it will execute whatever you write after the following `except`. However, if you used this construction in Python 2:

```python
except Exception, e:
```

… you will now have to turn it into this:

```python
except Exception as e:
```

Note the word `as` instead of the comma.

### Futurize

There is a script for updating your `print` and `except` statements! You should already have it, but if not, you can `pip install future` (or `sudo pip install future` if you receive an error) in your Terminal, and then try this line inside a folder with `.py` files:

```python
futurize -1 -w *.py
```

And it will make all the changes above inside all `.py` files, and save them back into their files. Ta-daa!

> **Hint 1:** The futurize script also creates `.bak` copies of the `.py` files. You may want to keep them around for a short while, just in case. But you definitely do not want those backup files in your git repository. So make sure you include `*.bak` in your `.gitignore`.

> **Hint 2:** The script may also insert the `from builtins import str` line, which may cause problems if the user does not have `future` installed from `pip`. So you may want to (batch) remove that line again. See above.

### Glyphs 3 imports

One major change in Glyphs 3 is the fact that `Foundation` and `AppKit` are not imported automatically at the first script run anymore. Why? Because it _significantly_ slows down the first script the user runs in a session.

It is much better to import only the stuff you need, e.g., like this:

```python
from AppKit import NSPoint, NSRect
```

That way only the submodules are loaded that the script needs, and the first script runs much quicker. And the user is happy. And that is what we all want, isn't it.

So, what you have to do is go through your code and look for _any_ reference to objects that start with `NS`. That include some basic things like `NSPoint`, `NSRect`, and the like. But also more advanced stuff like `NSPasteboard` and `NSStringPboardType` for clipboard handling.

The good news: I updated the [Python for Glyphs](https://github.com/mekkablue/Python-for-Glyphs) snippets accordingly already. Each snippet includes the imports it needs, and where applicable, even the `__future__` imports for Python 2/3 compatibility.

> **Hint:** In Python 3 it is pretty safe (and fast) to use `from Foundation import *`. However, this will leave behind the people who use Glyphs 3 with Python 2. So better always import exactly what you need. That is considered better practice anyway.

### ObjectiveC decorators

Have you [written plug-ins](https://glyphsapp.com/learn/plugins) for Glyphs? You may also need to update their code. But don't worry, it is not much you have to do.

If you (a) have added self-baked method of your own to the plug-in class, and (b) that method’s name does _not_ adhere to the PyObjC-style underscore and camelcase structure, like `doStuffWithArg_andWithArg_(self, A, B)`, then you need to prepend a python-method decorator. This looks like this:

```python
@objc.python_method
def updateView(self, view=None):
    if view:
        view.update()
    return True
```

If you do not add `@objc.python_method`, a selector object will be created for the method. That is not necessarily a bad thing, but you would only want that if you want to access the method from outside the plug-in. And you would have to make it Objective-C compatible by adding underscores for the arguments and using camelcase. Otherwise you will get a lot of errors thrown at you. Or, in the words of the [PyObjC documentation](https://pyobjc.readthedocs.io/en/latest/api/module-objc.html):

> This is used to add “normal” python methods to a class that’s inheriting from a Cocoa class and makes it possible to use normal Python idioms in the part of the class that does not have to interact with the Objective-C world.

If you already have a decorator in front of the method (rare case), then add the `@objc.python_method` even _before_ that other decorator, e.g. `@property`:

```python
@objc.python_method
@property
def updateView(self, view=None):
    if view:
        view.update()
    return True
```

But again, this is a pretty unlikely scenario within the realm of Glyphs plug-ins, so chances are this does not affect you.

### Updated SDK

If you have a plug-in in the Plugin Manager, you may want to check out the updated SDK. It is now Python 3 compatible. And the templates have an updated ‘MacOS’ folder:

![](<Base64-Image-Removed>)

**Updated 2020-04-18:** In other words, if your plug-in is not exactly recent, make sure the `plugin` binary is updated to the current version. Update your `Info.plist` with the ones in the SDK, and throw out keys that are not necessary anymore.

#### Step-by-step guide for upgrading your plug-in

1. **Remove these files**from your plug-in if they are still there (hint: you can do this with the context menu inside the file navigators of TextMate or SublimeText):
   - /Content/ **PkgInfo**
   - /Content/MacOS/ **main.py**
   - /Content/MacOS/ **python**
   - /Content/Resources/ **\_\_boot\_\_.py**
   - /Content/Resources/ **\_\_error\_\_.sh**
   - /Content/Resources/ **site.py**
2. **Replace the binary /Content/MacOS/plugin** with the corresponding file from [the current SDK template](https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates). Again, drag&drop with the Opt key works in and between file navigators as well.
3. **Update your /Content/Info.plist** to the structure of the [current templates in the SDK](https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates). Best to keep them side by side so you see differences right away:
   - Make sure your header has:
     - `<?xml version="1.0" encoding="UTF-8"?>`
     - `<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">`
   - Remove `CFBundleDisplayName` and `CFBundlePackageType` if they are there. Do the same for `NSMainNibFile` and `CFBundleSignature` if you still have those hanging around.
   - The key `PyMainFileNames` should have an `<array><string>plugin.py</string></array>` and nothing else. Old versions pointed to the main.py file.
   - Delete everything after the `PyMainFileNames` array. Only the closing tags `</dict>` and `</plist>` should follow.
   - Consider updating `CFBundleVersion`, `CFBundleShortVersionString`, `productReleaseNotes`.
   - Compare your `<key></key>` elements with the ones in the SDK template. Consider throwing out keys that are not in the template. **You only need these:**`CFBundleDevelopmentRegion`, `CFBundleExecutable`, `CFBundleIdentifier`, `CFBundleInfoDictionaryVersion`, `CFBundleName`, `CFBundleShortVersionString`, `CFBundleVersion`, `UpdateFeedURL`, `productPageURL`, `productReleaseNotes`, `NSHumanReadableCopyright`, `NSPrincipalClass`, `PyMainFileNames`.
4. **Update your /Resources/plugin.py**:
   - _Right after_ the `# encoding: utf-8` line, add the future imports on the second line: `from __future__ import division, print_function, unicode_literals`. Hint: the `fut⇥` snippet from the [Python for Glyphs repository](https://github.com/mekkablue/Python-for-Glyphs) helps.
   - After that, make sure you have these imports:
     - `import objc`
     - `from GlyphsApp import *`
     - `from GlyphsApp.plugins import *`
     - …and whatever other imports you need for your code, I often see `math` there.
     - _Get rid of unnecessary legacy imports._ In old templates, we used to have `sys` and `os` imports. We do not need those anymore. If you are not sure, comment them out and see if the plug-in works without them.
     - If you only need one or two functions from a library, consider the `from ... import ...` style of importing, e.g., `from math import tan, hypot` and change any occurrences of `math.tan()` or `math.hypot()` to simply `tan()` and `hypot()`, etc.
   - _Decorate_ all functions (inside _and_ outside your class definition) that do not have a PyObjC-compatible name (=starting with lowercase, camel-cased, underscore for each argument) with `@objc.python_method` (this is called the decorator, Google _pyobjc decorator_ it if you are unfamiliar with the concept). I.e., simply put the decorator on the line before the `def` statement, with the same indent as the `def` statement. Hint: the `dec⇥` snippet from the [Python for Glyphs repository](https://github.com/mekkablue/Python-for-Glyphs) helps.
   - _Exception to the above:_ Functions called by a menu item or by a callback **must** be PyObjC-compatible, i.e., starting with lowercase, camel-cased, and contain an underscore for each argument, and they must have _no decorator._
   - Turn all `print` statements into `print()` functions.
   - Turn all `layer.paths.append()` and `layer.components.append()` into `layer.shapes.append()`, consider a try/except statement. Hint: the `g23⇥` snippet from the [Python for Glyphs repository](https://github.com/mekkablue/Python-for-Glyphs) helps.
   - Turn `if customParameters.has_key(x):` into `if x in customParameters:`
   - That should cover 99% of the changes you will make. For more details on these and other Python 3 changes, read on below.
5. **Test your plug-in:** Force restart Glyphs 3, and put the bundle name of your plug-in into the search field of Console.app, and see what happens. `!PrincipalClass` is the most frequent error. If it occurs:
   - Make sure `NSPrincipalClass` in your Info.plist matches the class name in plugin.py.
   - Make sure _all necessary decorators_ are in place.
   - Make sure all functions called by menu items and callbacks are _undecorated and have a PyObjC-compatible name._
   - Make sure you really replaced the /Contents/MacOS/plugin binary with the current one.

Good luck. Report back in the forum if you still have trouble, best in the [Upgrading Plug-ins thread](https://forum.glyphsapp.com/t/upgrading-your-plug-ins/14372/).

## Major API changes

Then, there is another big thing coming at you. Due to the changes under the hood, the [scripting API](https://docu.glyphsapp.com/) has changed as well. For the most part, we could keep it the same, but in some areas, the differences are huge.

- **Font Info:** The way it is going to be organized in Glyphs 3 is going to be very different from Glyphs 2, not in the least to accommodate changes for facilitating variable font production.
- **Shapes on the layer:** In order to access anything on the layer, including components and paths, you will find yourself looping through `GSLayer.shapes` in the future.

### Shapes: paths and components

Anything visible on a layer is now collected in `GSLayer.shapes`. Yet, `GSLayer.paths` and `GSLayer.components` are still around. But they are now merely wrapped shortcuts, and equivalent to `[s for s in GSLayer.shapes if type(s)==GSPath]` (and `GSComponent`, respectively… you get the idea). That means that this still works:

```python
for path in Layer.paths:
    print(path)
    for node in path.nodes:
        print(node)
```

But there is one thing you _cannot_ do anymore: delete paths or components by means of their index number. In Glyphs 3, `del Layer.paths[2]` will raise a `TypeError: 'GSProxyShapes' object doesn't support item deletion`. That is because only the `shapes` are properly enumerated now. Here is a sample snippet that shows how you would would recursively delete paths with the `del` statement now:

```python
# Delete all paths with less than 4 nodes:
for i in range(len(Layer.shapes)-1,-1,-1):
    shape = Layer.shapes[i]
    if type(shape) == GSPath: # NEW: check for paths
        if len(shape.nodes) < 4:
            del Layer.shapes[i]
```

Just in case you have never done that: You see the `range(...-1, -1, -1)` construction? This gives us all the index numbers in reverse order. That way, when we actually delete an item, the index number of the following shape in the loop does not change.

The other thing you cannot do anymore, is to _append_ a new `GSComponent` object to `GSLayer.components`, or a `GSPath` object to `GSLayer.paths`. You append to `GSLayer.shapes` instead, like this:

```python
newComp = GSComponent("A")
try:
    # GLYPHS 3:
    Layer.shapes.append(newComp)
except:
    # GLYPHS 2:
    Layer.paths.append(newComp)
```

The `shapes` restructuring means that you can do things like this now: iterate over `shapes`, and sort them out by `type` with appropriate `if` statements. That is, check if the shape is a `GSPath` or a `GSComponent`, and proceed accordingly. E.g., this is how you would loop over all shapes on a layer:

```python
for i, shape in enumerate(Layer.shapes):
    print(i, shape)
    if type(shape) == GSPath:
        for node in shape.nodes:
            print(node)
    elif type(shape) == GSComponent:
        print(shape.position)
```

Similarly, if you want to delete _all_ components but at the same time keep all paths that may be on a layer, you may have been used to do something like `Layer.components=None`. But that won’t work anymore. So you will have to iterate backwards through the enumerated `shapes` and `del` the ones that check out as `GSComponent`:

```python
for i in range(len(Layer.shapes)-1, -1, -1):
    if type(Layer.shapes[i]) == GSComponent:
        del Layer.shapes[i]
```

Likewise if you want to delete all `GSPath` objects and keep `GSComponent` objects. Just test for `GSPath` rather than `GSComponent`, of course.

This will be one of the biggest changes in your scripts and plug-ins.

### GSGuide

Guides are called guides now. In other words, there’s no more ‘Line’ at the end. That means: `GSGuide` is the new class name, and you would access `GSLayer.guides` and `GSFontMaster.guides`. Other than that, everything is the same.

### Supporting both Glyphs 2 and 3

Now, in your code transition to Glyphs 3, you may want to also support app version 2. And luckily, there is a way to do it without having to resort to maintaining two repositories. It is easy: check for `Glyphs.versionNumber`. Here is one of the examples from above:

```python
if Glyphs.versionNumber >= 3::
    # GLYPHS 3:
    for shape in Layer.shapes:
        if type(shape) == GSPath:
            print(shape)
            for node in shape.nodes:
                print(node)
else:
    # GLYPHS 2:
    for path in Layer.paths:
        print(path)
        for node in path.nodes:
            print(node)
```

It is that easy, works like a charm in both version two _and_ three.

## Resources

Further reading? Here you go:

- [Glyphs API](https://docu.glyphsapp.com/)
- [Python Future](http://python-future.org/), especially its [Cheatsheet](http://python-future.org/compatible_idioms.html) for writing 2 & 3 compatible code
- python.org: [Porting Python 2 Code to Python 3](https://docs.python.org/3/howto/pyporting.html)
- [PyObjC bridge](https://pyobjc.readthedocs.io/en/latest/api/module-objc.html) documentation
- [Homebrew](https://brew.sh/)
- [pip installation](https://pip.pypa.io/en/stable/installing/) and [quickstart](https://pip.pypa.io/en/stable/quickstart/)
- [Python for Glyphs](https://github.com/mekkablue/Python-for-Glyphs) snippets for TextMate and SublimeText
- The [Dev category in the forum](https://forum.glyphsapp.com/c/Dev): if you do not have access, ask @mekkablue for it.
- Get feedback from your users in the [Beta Test category in the forum](https://forum.glyphsapp.com/c/betatest), especially in the [Plug-ins thread](https://forum.glyphsapp.com/t/glyphs-3-0b-plug-ins/14370).

Update 2022-08-07: if…else instead of try…except for G2+G3 code. Removed some outdated code samples.

- ### [Scripting Glyphs, part 1](https://glyphsapp.com/learn/scripting-glyphs-part-1)



Tutorial



![](<Base64-Image-Removed>)



[Scripting](https://glyphsapp.com/learn?q=scripting)

- ### [Scripting Glyphs, part 2](https://glyphsapp.com/learn/scripting-glyphs-part-2)



Tutorial



![](<Base64-Image-Removed>)



[Scripting](https://glyphsapp.com/learn?q=scripting)

- ### [Scripting Glyphs, part 3](https://glyphsapp.com/learn/scripting-glyphs-part-3)



Tutorial



![](<Base64-Image-Removed>)



[Scripting](https://glyphsapp.com/learn?q=scripting)

- ### [Scripting Glyphs, part 4](https://glyphsapp.com/learn/scripting-glyphs-part-4)



Tutorial



![](<Base64-Image-Removed>)



[Scripting](https://glyphsapp.com/learn?q=scripting)


## Welcome to the community

Join designers, engineers, studios and foundries from all around the world.

- [![](<Base64-Image-Removed>)\\
\\
Jeremy Tankard\\
\\
Since 1998 we’ve been designing award-winning type and producing typographic solutions for clients across the world](https://typography.net/)
- [![](<Base64-Image-Removed>)\\
\\
FONTWALA\\
\\
Fonts, consulting, and resources for Indic scripts](http://www.fontwala.com/)
- [![](<Base64-Image-Removed>)\\
\\
FerCozzi\\
\\
My name is Fernanda Cozzi, I'm a letter-lover, chatty and passionate type designer.](https://fercozzi.com/)
- [![](<Base64-Image-Removed>)\\
\\
The Lazydogs Typefoundry\\
\\
Hello, we are Lazydogs. We do typefaces and love letters with a truly handmade heart.](https://lazydogs.net/)
- [![](<Base64-Image-Removed>)\\
\\
Briefcase Type Foundry\\
\\
Czech studio Briefcase digitises original font designs, offer original fonts by young authors and help publish older, previously unreleased fonts, created by typographers and graphic designers.](https://www.briefcasetype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Hagilda\\
\\
Power Couple Collective type foundry from Tel Aviv. Michal Sahar & Hatayas Designing Hebrew and Latin typefaces since 2003.](https://hagilda.com/)
- [![](<Base64-Image-Removed>)\\
\\
Etcetera Type\\
\\
We enjoy making fonts and want you to enjoy using them. Period.](https://etceteratype.co/)
- [![](<Base64-Image-Removed>)\\
\\
Mark Simonson Studio\\
\\
Mark Simonson works by himself out of a repurposed back bedroom in a modest 1920s-era bungalow in the quiet residential Saint Paul neighborhood of Saint Anthony Park.](https://www.marksimonson.com/)
- [![](<Base64-Image-Removed>)\\
\\
Alphabet Type\\
\\
Font-engineering and custom services for designers as they ready their first font for release. We assist in foundry production and execute large corporate projects.](https://www.alphabet-type.com/)
- [![](<Base64-Image-Removed>)\\
\\
Love Letters\\
\\
Sebastien Sanfillipo single-handedly drawing letters for world peace in Brussels.](https://www.futurefonts.xyz/loveletters)
- [![](<Base64-Image-Removed>)\\
\\
29Letters\\
\\
Indie type design business creating and publishing multi-script typefaces with a team of professional Arab and European type designers.](https://www.29lt.com/)
- [![](<Base64-Image-Removed>)\\
\\
Masterfont\\
\\
The leading type foundry in Tel Aviv, Israel, established by Zvika Rosenberg in 1986. All we love to do is typeface design in Hebrew, Latin, and Arabic.](https://www.masterfont.co.il/)
- [![](<Base64-Image-Removed>)\\
\\
Typejockeys\\
\\
High quality type design and lettering from Vienna, Austria.](https://www.typejockeys.com/)
- [![](<Base64-Image-Removed>)\\
\\
Resistenza Type\\
\\
Resistenza is a type foundry consisting of Giuseppe Salerno, a trained calligrapher who gained his graphic design skills in Torino, Italy, and Paco González](https://www.resistenza.es/)
- [![](<Base64-Image-Removed>)\\
\\
Sahar Afshar\\
\\
Sahar Afshar is a typeface designer and researcher from Iran. Since 2015, she has been working as a font developer with various clients and foundries.](https://www.saharafshar.com/)
- [![](<Base64-Image-Removed>)\\
\\
Sports Fonts\\
\\
High quality custom typefaces for all kinds of sports.](https://sportsfonts.com/)
- [![](<Base64-Image-Removed>)\\
\\
hrftype\\
\\
A multilingual type design studio based in Malaysia, founded by Tan Sueh Li. We provide typographic solutions and consultation in visual communication, from logos, and custom type to multilingual matchmaking.](https://www.instagram.com/hrftype/)
- [![](<Base64-Image-Removed>)\\
\\
LiebeFonts\\
\\
Hand-made fonts with lots of love](https://liebefonts.com/)
- [![](<Base64-Image-Removed>)\\
\\
Device Fonts\\
\\
Rian Hughes is an illustrator and type designer, famous for his comic strips and vinyl sleeves.](https://www.devicefonts.co.uk/)
- [![](<Base64-Image-Removed>)\\
\\
R-Typography\\
\\
Type foundry founded by Rui Abreu in 2008 and currently run with Catarina Vaz from sunny Lisbon, Portugal.](https://www.r-typography.com/)
- [![](<Base64-Image-Removed>)\\
\\
Cecilia del Castillo Daza\\
\\
Graphic Design, Calligraphy & Lettering by a proud Mexican living in Barcelona](http://www.ceciliadelcastillo.com/)
- [![](<Base64-Image-Removed>)\\
\\
Notdef Type\\
\\
Doing typography related services since 2018.](https://notdef.com.br/)
- [![](<Base64-Image-Removed>)\\
\\
Angel Kwong\\
\\
Typeface designer & graphic designer from Hong Kong](https://angelkwong.com/)
- [![](<Base64-Image-Removed>)\\
\\
Plau\\
\\
Music sparks conversations, brings people together and moves ideas forward. So does type. We make type pop.](https://www.plau.design/)
- [![](<Base64-Image-Removed>)\\
\\
Fontwerk\\
\\
Modern typefaces, innovative font engineering and type design services.](https://fontwerk.com/)
- [![](<Base64-Image-Removed>)\\
\\
Letters from Sweden\\
\\
Letters from Sweden designs retail and custom typefaces for local and international clients.](https://lettersfromsweden.se/)
- [![](<Base64-Image-Removed>)\\
\\
Dalton Maag\\
\\
Typeface design studio, founded 1991. We help clients and agencies worldwide hone their typographic expression, from logos and licensing to custom font suites.](https://daltonmaag.com/)
- [![](<Base64-Image-Removed>)\\
\\
Schultzschultz\\
\\
Independent Frankfurt-based design studio focusing on branding and serving an international client-base.](https://www.schultzschultz.com/)
- [![](<Base64-Image-Removed>)\\
\\
Viktoriya Grabowska\\
\\
Viktoriya specializes in multilingual design with a focus on the Cyrillic and Latin scripts.](https://viktoriyagrabowska.com/)
- [![](<Base64-Image-Removed>)\\
\\
The Northern Block\\
\\
The Northern Block is a collaborative type foundry internationally recognised for producing new typefaces that are fit for a modern purpose.](https://thenorthernblock.co.uk/)
- [![](<Base64-Image-Removed>)\\
\\
Fictionist\\
\\
Based in sunny Kuala Lumpur, Fictionist Studio is a multi-disciplinary creative studio, specialising in all platforms that involve the birth of an idea.](https://fictionistudio.com/)
- [![](<Base64-Image-Removed>)\\
\\
Roland Hüse\\
\\
I am helping businesses strengthening their visual appearance and cutting through the noise with my work.](https://www.rolandhuse.com/)
- [![](<Base64-Image-Removed>)\\
\\
Aravrit\\
\\
We join letters, joining people, joining ideas.](https://www.facebook.com/aravrit?ref=aymt_homepage_panel)
- [![](<Base64-Image-Removed>)\\
\\
Monotype\\
\\
Monotype empowers creative minds to build and express authentic brands through design, technology and expertise](https://www.monotype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Gina Serret\\
\\
Custom Calligraphy, Lettering and Type design](https://www.ginaserret.com/)
- [![](<Base64-Image-Removed>)\\
\\
Nova Type Foundry\\
\\
Independent digital type foundry founded by Joana Correia in 2018, based in Porto, Portugal. We sell our retail typefaces directly on our website.](https://novatypefoundry.com/)
- [![](<Base64-Image-Removed>)\\
\\
Reset\\
\\
Independent type studio from Montevideo, Uruguay. With more than 10 years of experience, teamwork is our strength & type our passion.](https://www.reset-type.com/)
- [![](<Base64-Image-Removed>)\\
\\
3type\\
\\
Typical & atypical type foundry based in Shanghai.](https://3type.cn/)
- [![](<Base64-Image-Removed>)\\
\\
Maria Montes\\
\\
Designer, calligrapher, letterer & illustrator, based in Melbourne, Australia](https://www.mariamontes.net/)
- [![](<Base64-Image-Removed>)\\
\\
Martina Flor\\
\\
Studio Martina Flor is a small design business specializing in lettering and custom type. We work for agencies, magazines, and publishing houses to create stunning typography and logotypes for large and small projects.](https://www.martinaflor.com/)
- [![](<Base64-Image-Removed>)\\
\\
bBoxType\\
\\
We have more than 20 years of experience in professional type design. We combine this with fresh ideas and the lust for new.](https://bboxtype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Sandoll\\
\\
We build fonts for the beautiful world! Korean type foundry Sandoll was founded in 1984 and since then, has developed nearly 600 fonts.](http://www.sandoll.co.kr/)
- [![](<Base64-Image-Removed>)\\
\\
HadiType\\
\\
HadiType is an independent digital type foundry based in Egypt, established by Muhammed Hadi in 2018, designing, manufacturing, and distributing a selection of high quality Arabic typefaces, We design typefaces in Hebrew, Arabic, and Latin. We offer typographical solutions for graphic design agencies, collaborate with international type foundries, and take custom projects.](https://www.instagram.com/_haditype_foundry/)
- [![](<Base64-Image-Removed>)\\
\\
SevenType Studio\\
\\
Vitória Neves combining her passion for languages and type to create well-crafted and contemporary multi-script fonts.](https://seventype.design/)
- [![](<Base64-Image-Removed>)\\
\\
Positype\\
\\
Founded in 2000 by Neil Summerour, Positype is a well-recognized, independent type foundry that offers both retail and bespoke/custom typeface development services.](https://positype.com/)
- [![](<Base64-Image-Removed>)\\
\\
NM Type\\
\\
A type studio based in Sweden and Spain, a creative collaboration between Noel Pretorius and María Ramos.](http://www.nmtype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Fontfabric\\
\\
A tight-knit group of accomplished, multidisciplinary designers who share a passion for high-quality typefaces, calligraphy and lettering.](https://www.fontfabric.com/)
- [![](<Base64-Image-Removed>)\\
\\
Fontef\\
\\
Fontef is an independent type foundry based in Tel Aviv, established by Yanek Iontef in 1994. We are a small team — Yanek Iontef is a well-known Israeli type designer and Daniel Grumer a graduate of the Type and Media program in The Hague (2016). We design typefaces in Hebrew, Latin and Arabic.](https://fontef.com/)
- [![](<Base64-Image-Removed>)\\
\\
Hoodzpah\\
\\
Southern California based brand identity & type design studio founded by twin sisters, Amy and Jennifer Hood. Hoodzpah specializes in personality-driven display typefaces.](https://www.hoodzpahdesign.com/fonts)
- [![](<Base64-Image-Removed>)\\
\\
Luzi Type\\
\\
Luzi Type is a Swiss type design studio that combines history of type with modernist clearness and reduction.](https://luzi-type.ch/)
- [![](<Base64-Image-Removed>)\\
\\
Dezcom Typefaces\\
\\
Independent type foundry that intends to push traditional boundaries and produce original contemporary work.](https://www.dezcom.com/)
- [![](<Base64-Image-Removed>)\\
\\
Dizajn Design\\
\\
Ján Filípek’s independent type foundry based in Bratislava, Slovakia.](https://www.dizajndesign.sk/)
- [![](<Base64-Image-Removed>)\\
\\
Typerepublic\\
\\
Independent type foundry based in Barcelona. Founder and principal designer Andreu Balius has experienced type design since the late eighties.](https://typerepublic.com/about)
- [![](<Base64-Image-Removed>)\\
\\
ArabicType\\
\\
Typefaces by award-winning Lebanese type designer Nadine Chahine.](https://arabictype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Arabic Typography\\
\\
Arabictypography.com is an independent type foundry designing and producing original multilingual digital fonts that respond to specific market needs. Our key expertise is in languages using the Arabic script and additional other scripts matching or working in harmony with Arabic.](https://www.arabictypography.com/)
- [![](<Base64-Image-Removed>)\\
\\
Harbor Type\\
\\
Type foundry of Henrique Beier. I design typefaces and provide font production services.](https://www.harbortype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Type-Ø-Tones\\
\\
Typographic design company founded in 1990 by Joan Barjau, Enric Jardí, Laura Meseguer and José Manuel Urós.](https://type-o-tones.com/)
- [![](<Base64-Image-Removed>)\\
\\
Katatrad\\
\\
A boutique type foundry based in Chonburi, Thailand. Subsidiary of Cadson Demak.](https://www.katatrad.com/)
- [![](<Base64-Image-Removed>)\\
\\
Universal Thirst\\
\\
Universal Thirst is a type foundry that specialises in Indic and Latin scripts. It was set up in 2016 by designer and engineer duo Gunnar Vilhjálmsson and Kalapi Gajjar, who draw on their contrasting visual heritage to offer a unique, dual perspective on type.](https://universalthirst.com/)
- [![](<Base64-Image-Removed>)\\
\\
205TF\\
\\
French type foundry that brings together the work of independent typeface designers.](https://www.205.tf/)
- [![](<Base64-Image-Removed>)\\
\\
AlefAlefAlef\\
\\
Israel-based type foundry thoroughly devoted to quality, original, multilingual typography, founded in 2011 by Avraham Cornfeld.](https://alefalefalef.co.il/en/)
- [![](<Base64-Image-Removed>)\\
\\
Azalam\\
\\
May name is Azza, I am specialized in Arabic & Latin Logo Matchmaking, Branding and Type Design](https://www.azalam.com/)
- [![](<Base64-Image-Removed>)\\
\\
Grilli Type\\
\\
Independent Swiss Type Foundry](https://www.grillitype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Nouvelle Noire\\
\\
Type design and development studio based in Zurich, Switzerland. Working in a traditional way, we design type with an emphasis on modern technique and technical options.](https://www.nouvellenoire.ch/)
- [![](<Base64-Image-Removed>)\\
\\
David Jonathan Ross\\
\\
I draw letters of all shapes and sizes for retail and custom typeface designs.](https://djr.com/)
- [![](<Base64-Image-Removed>)\\
\\
Stéphane Gabrielli\\
\\
Stéphane is a graphic & type designer from France, specializing in custom logos, typefaces, and layouts.](https://www.stephanegabrielli.com/)
- [![](<Base64-Image-Removed>)\\
\\
Sudtipos\\
\\
Collective type foundry designing fonts to be used in real works.](https://www.sudtipos.com/)
- [![](<Base64-Image-Removed>)\\
\\
justfont\\
\\
Fonts from Taipei.](https://justfont.com/)
- [![](<Base64-Image-Removed>)\\
\\
Mota Italic\\
\\
We specialize in designing complex & diverse type families — with a special focus on extended Latin & Indian scripts.](https://www.motaitalic.com/)
- [![](<Base64-Image-Removed>)\\
\\
TypeMates\\
\\
We are a straightforward type foundry – we distribute multifarious typefaces in our font collection and tailor exclusive custom fonts for small and large clients.](https://www.typemates.com/)
- [![](<Base64-Image-Removed>)\\
\\
Sumotype\\
\\
High quality fonts from Bogotá, Colombia:\\
\\
‘A single letter leads to an entire alphabet.’](http://www.sumotype.com/)
- [![](<Base64-Image-Removed>)\\
\\
Minjoo Ham\\
\\
Typedesigner for Hangul & Latin.](http://minjooham.com/)
- [![](<Base64-Image-Removed>)\\
\\
Lobster Phone\\
\\
Lobster Phone is a creative design studio based in San Francisco specializing in branding, packaging, and creative direction.](https://www.lobsterphone.co/)
- [![](<Base64-Image-Removed>)\\
\\
Signal\\
\\
Dublin-based type foundry and drawing office specialising in type design, lettering, and typographic branding.](https://signalfoundry.com/)
- [![](<Base64-Image-Removed>)\\
\\
Typofonderie\\
\\
Founded in 1994, Typofonderie is an independent digital type foundry in France, designing, manufacturing and distributing a selection of high quality typefaces for adventurous digital typographers.](https://typofonderie.com/)
- [![](<Base64-Image-Removed>)\\
\\
The Fontpad\\
\\
We are a small company making fonts for Southeast Asia. Our expertise covers Thai, Lao, Burmese, Khmer, Cham, Tham and Vietnamese. Working with experts around the world, we can also research other Southeast Asian writing systems and produce fonts for the languages they cover.](http://www.fontpad.co.uk/)
- [![](<Base64-Image-Removed>)\\
\\
Laura Meseguer\\
\\
Hello! I’m Laura Meseguer, a freelance graphic and type designer based in Barcelona.](https://www.laurameseguer.com/)

Start making today

Download a free trial of Glyphs 3 and start making things you love.

Close this Event
