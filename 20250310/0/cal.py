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
        args = map(int, arg.split())
        return calendar.TextCalendar().prmonth(*args)
if __name__ == '__main__':
    readline.parse_and_bind("bind ^I rl_complete")
    numbername().cmdloop()

