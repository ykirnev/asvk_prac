import calendar


def generate_rest_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    if cal[0][0] != 1:
        return
    month_name = calendar.month_name[month]
    output = [
        f".. table:: {month_name} {year}",
        "",
        "    == == == == == == ==",
        "    Mo Tu We Th Fr Sa Su",
        "    == == == == == == =="
    ]
    for week in cal:
        week_str = "    " + " ".join(f"{day:2}" if day != 0 else "  " for day in week)
        output.append(week_str)
    output.append("    == == == == == == ==")
    return "\n".join(output)


print(generate_rest_calendar(2025, 12))