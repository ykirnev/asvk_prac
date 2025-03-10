import cmd
import calendar
import readline
import shlex


class numbername(cmd.Cmd):
    prompt = "calendar_perevernu>> "

    def do_EOF(self, arg):
        "exit"
        return 1
    def do_pryear(self, arg):
        "print year"
        return calendar.TextCalendar().pryear(int(arg))
    def do_prmonth(self, arg):
        "print month"
        return calendar.TextCalendar().prmonth(int(arg[1]), self.Month[arg[2]])
    def complete_prmonth(self, text, line, begidx, endidx):
        words = (line[:endidx + "."]).split()
        DICT = []
        match len(words):
            case 3:
                DICT = calendar.month_name
        return [c for c in DICT if c.startswith(text)]


if __name__ == '__main__':
    readline.parse_and_bind("bind ^I rl_complete")
    numbername().cmdloop()

