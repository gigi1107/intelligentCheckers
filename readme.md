# AICheckers


<p align="center">
    <img src="https://imgur.com/amGpXY6.png" alt="Intelligent Checkers logo designed by Linh">
  </a>
</p>

<h3 align="center">Intelligent Checkers</h3>

<p align="center">
  This project is a checker game using artificial intelligence developed by 2 Seattle University students in our AI class. 
  
</p>


## Table of Contents
- [How to Install and Play](#how-to)
- [Implementation](#implementation)
- [Developers](#developers)
- [Project Goals](#project-goals)
- [Important Milestones](#important-milestones)
- [Similar Projects](#similar-projects)
- [Course Contact](#course-contact)
- [Copyright and license](#copyright-and-license)


## How to Install and Play 
In your command line, navigate to the folder directory with all the downloaded files. 
<br />
Type: 
<br />
`pip install numpy`
<br />
`pip install Flask`

Then, to run Flask, type:
On Unix Bash (Linux, Mac, etc.):

`$ export FLASK_APP=__init__.py`
<br />
`$ flask run`

Windows CMD:

`> set FLASK_APP=__init__.py`
<br />
`> flask run`

Windows PowerShell:

`> $env:FLASK_APP = "__init__.py"`
<br />
`> flask run`

Then locate to 127.0.0.1:5000 on **Google Chrome** to run the game. 
**Note**: The game MUST be run on Google Chrome. Mozilla Firefox, Internet Explorer, and other browsers may negatively affect gameplay.

## Implementation
<br />
Backend: Python
<br />
1. Minimax with limited depth
<br />
2. Alpha-beta pruning
<br />
3. Improved evaluation using Close Distance algorithm 
<br />
<br />
Frontend: HTML, CSS, JavaScript, Flask

## Developers

- Gigi Davidson: `davids31@seattleu.edu`
- Linh Nguyen: `nguye468@seattleu.edu`

## Project Goals 
- Understand artificial intelligence concepts, techniques, and algorithms. 
- Present information and material in an organized and methodical way, in both technical implementation and oral presentations.
- Apply core AI concepts into a basic board game by designing and implementing programs using common languages and tools to construct intelligent artifacts. 
- Showcase the project to the class and the community. 

## Important Milestones
- [x] Milestone 1: Find a teammate and register for a project (April 10, 2019)
- [x] Milestone 2: Publish the webpage and submit the link (May 1, 2019)
- [x] Milestone 3: Design, requirements, information representation, and one page poster submission (May 15, 2019)
- [x] Milestone 4: Final implementation and video on YouTube (June 10, 2019)


## Similar Projects
- [Draughts AI](https://github.com/Hsankesara/Draughts-AI)
- [AI Checkers using JavaScript](https://github.com/billjeffries/jsCheckersAI)

## Course Contact 
- Professor Pejman Khadivi: `khadivip@seattleu.edu`
- Artificial Intelligence - CPSC 4610, Spring Quarter 2019
- Seattle University, Computer Science Department

## Copyright and license
Code and documentation copyright 2019 by Gigi Davidson and Linh Nguyen. Code released under the [MIT License](https://github.com/twbs/bootstrap/blob/master/LICENSE). Docs released under [Creative Commons](https://github.com/twbs/bootstrap/blob/master/docs/LICENSE).


