import locale
from io import StringIO
import random
import readline
import cowsay

FIELD_SIZE = 10

import gettext
import locale
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
#print(BASE_DIR)
LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation("mud", BASE_DIR / "po", ["ru"]),
    ("en_US", "UTF-8"): gettext.NullTranslations()
}
locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())


if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

def _(text):
    return LOCALES[locale.getlocale()].gettext(text)


class Weapon:
    """Class representing a weapon in the game.

    Attributes:
        weapon_dict (dict): Available weapons and their damage values

        name (str): Name of the weapon

        damage (int): Damage value of the weapon
    """
    weapon_dict = {'sword': 10, 'spear': 15, 'axe': 20}

    def __init__(self, name):
        """Initialize weapon instance.

            Args:
                name (str): Weapon name from available options in weapon_dict
            """
        self.name = name
        self.damage = self.weapon_dict[self.name]


class Player:
    """Class representing a player in the game.

    Attributes:
        x (int): X coordinate on the field

        y (int): Y coordinate on the field

        weapon (Weapon): Currently equipped weapon

        lang (tuple): Current locale settings (language, encoding)
    """
    def __init__(self):
        """Initialize player with default position and equipment."""

        self.x = 0
        self.y = 0
        self.weapon = Weapon('sword')
        self.lang = ("en_US", "UTF-8")

    def position(self):
        """Get current player coordinates.

            Returns:
                tuple: (x, y) coordinates
            """
        return self.x, self.y

    def move(self, direction):
        """Move player in specified direction.

            Args:
                direction (str): Movement direction (up/down/left/right)

            Returns:
                tuple: New (x, y) coordinates after movement
            """
        match direction:
            case 'up':
                self.y = (self.y - 1) % FIELD_SIZE
            case 'down':
                self.y = (self.y + 1) % FIELD_SIZE
            case 'left':
                self.x = (self.x - 1) % FIELD_SIZE
            case 'right':
                self.x = (self.x + 1) % FIELD_SIZE
        return self.x, self.y

    def damage(self):
        """Get current weapon damage.

            Returns:
                int: Damage value of equipped weapon
            """
        return self.weapon.damage

    def set_locale(self, args):
        """Set player's localization settings.

            Args:
                args (str): Locale string in format 'lang_REGION.encoding'

            Returns:
                str: Localized confirmation message
            """
        if args == 'ru_RU.UTF-8':
            self.lang = ("ru_RU", "UTF-8")
        elif args == 'en_US.UTF-8':
            self.lang = ("en_US", "UTF-8")
        locale.setlocale(locale.LC_ALL, self.lang)
        return _("Set up locale: {args}").format(args=args)


class Monster:
    """Class representing a game monster.

        Attributes:
            name (str): Monster name

            x (int): X coordinate on the field

            y (int): Y coordinate on the field

            hp (int): Hit points

            hello (str): Greeting message when encountered

        """
    def __init__(self, name, x, y, hp, hello):
        """Initialize monster instance.

           Args:
               name (str): Monster name

               x (int): Spawn X coordinate

               y (int): Spawn Y coordinate

               hp (int): Initial hit points

               hello (str): Encounter message
           """
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp
        self.hello = hello

    def __bool__(self):
        return True


class Game:
    """Main game class managing game state and logic.

        Attributes:

            field (list): 2D list representing game field cells

            monsters (dict): Active monsters with (x,y) keys

            players (dict): Active players with name keys

            move_monsters_enabled (bool): Flag for monster movement
        """
    def __init__(self):
        """Initialize game with empty field and default settings."""
        self.field = [[{"monster": None, "players": []} for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
        self.monsters = {}
        self.players = {}
        self.move_monsters_enabled = True

    def delplayer(self, name):
        """Remove player from the game.

            Args:
                name (str): Name of player to remove
            """
        pl = self.players[name]
        self.field[pl.x][pl.y]["players"].remove(name)
        del self.players[name]

    def move_random_monster(self):
        """Attempt to move a random monster on the field.

            Returns:
                dict or None: Movement details if successful, None otherwise
            """
        if not self.monsters:
            return None
        positions = list(self.monsters.keys())
        random.shuffle(positions)
        for old_pos in positions:
            directions = ['right', 'left', 'up', 'down']
            random.shuffle(directions)
            for direction in directions:
                old_x, old_y = old_pos
                new_x, new_y = old_x, old_y
                if direction == 'right':
                    new_x = (old_x + 1) % FIELD_SIZE
                elif direction == 'left':
                    new_x = (old_x - 1) % FIELD_SIZE
                elif direction == 'up':
                    new_y = (old_y - 1) % FIELD_SIZE
                elif direction == 'down':
                    new_y = (old_y + 1) % FIELD_SIZE
                new_pos = (new_x, new_y)
                if new_pos not in self.monsters:
                    monster = self.monsters[old_pos]
                    self.monsters.pop(old_pos)
                    self.field[old_x][old_y]['monster'] = None
                    self.monsters[new_pos] = monster
                    self.field[new_x][new_y]['monster'] = monster
                    return {
                        'name': monster.name,
                        'direction': direction,
                        'new_pos': new_pos,
                    }
        return None

    def register_player(self, name):
        """Register new player in the game.

            Args:

                name (str): Player name to register

            Returns:
                str: Localized registration result message
            """
        if name == 'test' or name not in self.players:
            self.players[name] = Player()
            self.field[0][0]["players"].append(name)
            return _("You have been registered as {name}\n").format(name=name)
        else:
            return _("{name} is already in use\n").format(name=name)

    def encounter(self, x, y):
        """Handle player-monster encounter and generate visual response.

            Args:

                x (int): X coordinate of encounter

                y (int): Y coordinate of encounter

            Returns:
                str: Formatted ASCII art representation of the encounter
            """
        monster = self.field[x][y]["monster"]
        if monster.name == "jgsbat":
            cow = cowsay.read_dot_cow(StringIO("""
                    $the_cow = <<EOC;
                       $thoughts
                        $thoughts
                        ,_                    _,
                        ) '-._  ,_    _,  _.-' (
                        )  _.-'.|\\\\--//|.'-._  (
                         )'   .'\\/o\\/o\\/'.   `(
                          ) .' . \\====/ . '. (
                           )  / <<    >> \\  (
                            '-._/``  ``\\_.-'
                      jgs     __\\\\'--'//__
                             (((""`  `"")))
                    EOC
                        """))
            return cowsay.cowsay(monster.hello, cowfile=cow)
        else:
            return cowsay.cowsay(monster.hello, cow=monster.name)

    def move_player(self, name, direction):
        """Move player and handle cell interactions.

            Args:

                name (str): Player name to move

                direction (str): Movement direction (up/down/left/right)

            Returns:
                str: Movement result message with possible encounter
            """
        x, y = self.players[name].position()
        self.field[x][y]["players"].remove(name)
        x, y = self.players[name].move(direction)
        res = _("Moved to ({x}, {y})").format(x=x, y=y)
        self.field[x][y]["players"].append(name)
        #print(self.field[x][y]["monster"])
        if self.field[x][y]["monster"] is not None:
            return res + '\n' + self.encounter(x, y)
        else:
            return res

    def addmon(self, args):
        """Add monster to the game field.

            Args:

                args (tuple): (name, hello, hp, x, y) monster parameters

            Returns:
                dict: Localized addmon messages for all supported locales
            """
        name, hello, hp, x, y = args
        x, y, hp = int(x), int(y), int(hp)
        replaced = self.field[x][y]["monster"] is not None
        self.field[x][y]["monster"] = Monster(name, x, y, hp, hello)
        self.monsters[(x, y)] = self.field[x][y]["monster"]
        res = {}
        for i in LOCALES:
            locale.setlocale(locale.LC_ALL, i)
            r = _("Added monster {name} to ({x}, {y}) saying '{hello}' with").format(name=name, x=x, y=y,
                                                                                                      hello=hello,
                                                                                                      hp=hp)
            nr = LOCALES[locale.getlocale()].ngettext(" {hp} hitpoint\n", " {hp} hitpoints\n", hp).format(hp=hp)
            r += nr
            if replaced:
                r += _("Replaced the old monster")
            res[i] = r
        return res

    def attack_exe(self, player_name, args):
        """Execute player attack on monster.

            Args:

                player_name (str): Attacking player's name

                args (tuple): (monster_name, weapon_name) attack parameters

            Returns:
                dict: Localized attack results for all supported locales
            """
        x, y = self.players[player_name].position()
        monster_name, weapon_name = args
        res = {}
        if monster_name == '.':
            if self.field[x][y]["monster"] is None:
                for i in LOCALES:
                    locale.setlocale(locale.LC_ALL, i)
                    r = _("No monster here")
                    res[i] = r
                return res
            else:
                return self.make_pvp(x, y, player_name, Weapon(weapon_name))
        else:
            if self.field[x][y]["monster"] is None or monster_name != self.field[x][y]["monster"].name:
                for i in LOCALES:
                    locale.setlocale(locale.LC_ALL, i)
                    r = _("No {monster_name} here").format(monster_name=monster_name)
                    res[i] = r
                return res
            else:
                return self.make_pvp(x, y, player_name, Weapon(weapon_name))

    def make_pvp(self, x, y, player_name, weapon=Weapon('sword')):
        """Calculate combat damage and update monster status.

            Args:

                x (int): Combat X coordinate

                y (int): Combat Y coordinate

                player_name (str): Attacking player's name

                weapon (Weapon): Weapon used for attack

            Returns:
                dict: Localized combat results for all supported locales
            """
        self.players[player_name].weapon = weapon
        damage = self.players[player_name].damage()
        monster = self.field[x][y]["monster"]
        if damage > monster.hp:
            damage = monster.hp
        res = {}
        for i in LOCALES:
            locale.setlocale(locale.LC_ALL, i)
            r = _("Attacked {monster_name} with {weapon_name}, damage").format(monster_name=monster.name,
                                                                                 weapon_name=weapon.name, damage=damage)
            nr = LOCALES[i].ngettext(" {hp} hp\n", " {hp} hps\n", damage).format(hp=damage)
            r += nr
            res[i] = r
        monster.hp -= damage
        match monster.hp:
            case 0:
                for i in LOCALES:
                    locale.setlocale(locale.LC_ALL, i)
                    res[i] += _("{monster_name} died").format(monster_name=monster.name)
                self.field[x][y]["monster"] = None
            case _:
                for i in LOCALES:
                    locale.setlocale(locale.LC_ALL, i)
                    res[i] += _("{monster_name} now has").format(monster_name=monster.name)
                    nr = LOCALES[locale.getlocale()].ngettext(" {hp} hp\n", " {hp} hps\n", monster.hp).format(hp=monster.hp)
                    res[i] += nr
        self.players[player_name].weapon = Weapon('sword')
        return res
