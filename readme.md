# CuteList
###
### A Free and Open Source software to generate wood cutting maps
###
*Made by [Fidele Dossou](https://www.linkedin.com/in/fidele-dossou-1752531800)*
###
As a Carpenter I often struggle about the best way to automate my material cutting (Wood, MDF, HDF...).

There are much software capable of this but none of them are both free and open source.

There is a great free Sketchup plugin called Open CutList made by ***Boris Beaulant***, a well known 
French carpenter (founder of the blog *L'air du bois*) but Sketchup like many others CAD is not free.

So here come up the question: **why not building my own**?

Well, the core issue of the idea is what is so called <u>**the rectangle bin packing problem**</u> or <u>**the knapstack
problem**</u>
meaning in other words how to put differents sized rectangles into a big one while optimizing the space (getting the
minimal waste possible).

Please note that there is no **"best solution"** as situations may differ from case to case. 

Cool down we won't reinvent the wheel. ;)

There are some open source tools like **Google Or-Tools** or **OptaPlanner** which are great for mathematical optimization 
problems, but they seem too "*heavy*" for what I want to achieve.

During my research for the most suitable tool I could use, I came across with **rectangle-packing-solver** python 
package which looks like the fastest and the easiest one for me. 


## Getting started

The project itself intends to be an executable for Windows OS users.

The Graphical User Interface has been built with **Qt Designer** then converting the .*ui* file generated to a python 
*.py* file with **PyQt5**.

To get started make sure you have python installed and create a virtual environment.

I have used **Python 3.11.2** otherwise I guess any version <= 3.7 should also work.
If issues please consider upgrading to the latest version.
##

#### Install rectangle-packing-solver using pip
```
pip install rectangle-packing-solver
```

#### Install PyQt5 

```
pip install PyQt5
```

If you want to contribute please clone this repo with ```git clone``` command or fork.

Happy hacking..!

## Work in progress...

The program is not fully working for the moment. 

There are still some implementations to be made and minor bugs to be fixed.

Contributions are warmly welcomed!