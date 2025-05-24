.. MOOD documentation master file, created by
   sphinx-quickstart on Sat May 24 18:00:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MOOD's documentation!
===============================

Task Description
----------------

**Task 1: Wandering Monsters and Sphinx**

Copy the solution from Task 2 of the previous session. Commit changes. Work on the `work` branch.

Add Sphinx to pipenv.

Add support for wandering monsters on the MUD server:
- Every 30 seconds (starting 30 seconds after the server starts), a random monster is selected and moves one cell in a random direction (right, left, up, down; the field is toroidal).
- If the move would place the monster on a cell already occupied by another monster, the move does NOT occur, and another monster and direction are chosen until a successful move is made.
- Upon moving, the server sends a message to all players: "<monster_name> moved one cell <direction>", e.g., "manticore moved one cell right".
- If a monster moves to a cell with a player(s), an "encounter" occurs, as if the player(s) moved to the monster's cell, including rendering the monster with its greeting phrase for the affected players.

For the server module, document all functions, classes, and the module in autodoc format.
Generate technical documentation for these classes/functions/module.
Ensure generated HTML documentation is not stored in git (use .gitignore), but Sphinx configuration files are included.

Create a title page for the documentation (at minimum, copy the task description).
Include a link to the technical documentation on the title page.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   server

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`