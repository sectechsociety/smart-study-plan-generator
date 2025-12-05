
from math import ceil

def schedule_hours(predicted_hours, free_slots, sessions_per_day=3):
    slots_needed = {s: max(1, int(ceil(h))) for s, h in predicted_hours.items()}
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    timetable = {d: [] for d in days}
    day_capacity = {d: min(free_slots.get(d,0), sessions_per_day) for d in days}
    subjects_sorted = sorted(slots_needed.items(), key=lambda x: -x[1])
    day_index = 0
    for subj, needed in subjects_sorted:
        placed = 0
        attempts = 0
        while placed < needed and attempts < 1000:
            d = days[day_index % len(days)]
            if len(timetable[d]) < day_capacity[d]:
                timetable[d].append(subj)
                placed += 1
            day_index += 1
            attempts += 1
        if placed < needed:
            for d in days:
                while placed < needed and len(timetable[d]) < free_slots.get(d,0):
                    timetable[d].append(subj)
                    placed += 1
    return timetable
