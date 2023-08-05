def secToHMS(sec: int):
    """Convert second into hh:mm:ss"""
    remain = sec % 3600
    hours = (sec - remain) // 3600
    sec = remain  # Remove the hours from the seconds

    remain = sec % 60
    minutes = (sec - remain) // 60
    sec = remain  # Remove the minutes from the seconds

    return f"{hours}:{minutes}:{sec}"
