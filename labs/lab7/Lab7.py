def Lab7Zad1():
    objects = [
        ("Containment Cell A", 4),
        ("Archive Vault", 1),
        ("Bio Lab Sector", 3),
        ("Observation Wing", 2)
    ]
    SortedObject = sorted(objects,key = lambda x:x[1])
    print(SortedObject)

# Lab7Zad1()



def Lab7Zad2():
    staff_shifts = [
        {"name": "Dr. Shaw", "shift_cost": 120, "shifts": 15},
        {"name": "Agent Torres", "shift_cost": 90, "shifts": 22},
        {"name": "Researcher Hall", "shift_cost": 150, "shifts": 10}
    ]

    lst2 = list(map(lambda x: x["shift_cost"] * x["shifts"], staff_shifts))
    print(lst2)
    print(f"MAx: {max(lst2)}")


# Lab7Zad2()



def LAb7Zad3():
    personnel = [
        {"name": "Dr. Klein", "clearance": 2},
        {"name": "Agent Brooks", "clearance": 4},
        {"name": "Technician Reed", "clearance": 1}
    ]
    personnelNew1 = list(map(
        lambda x: {
            "name": x["name"],
            "clearance": x["clearance"],
            "category": (
                "Restricted" if x["clearance"] == 1 else
                "Confidential" if 2 <= x["clearance"] <= 3 else
                "Top Secret"
            )
        },
        personnel
    ))
    print(personnelNew1)

# LAb7Zad3()



def Lab7Zad4():
    zones = [
        {"zone": "Sector-12", "active_from": 8, "active_to": 18},
        {"zone": "Deep Storage", "active_from": 0, "active_to": 24},
        {"zone": "Research Wing", "active_from": 9, "active_to": 17}
    ]

    #  с 8 до 18 включительно
    daytime_zones = list(filter(
        lambda zone: zone["active_from"] >= 8 and zone["active_to"] <= 18,
        zones
    ))

    print("Зоны (8:00-18:00):")
    for zone in daytime_zones:
        print(f"{zone['zone']}: {zone['active_from']}:00 - {zone['active_to']}:00")


# Lab7Zad4()


def Lab7Zad5():
    reports = [
        {"author": "Dr. Moss", "text": "Analysis completed. Reference: http://external-archive.net"},
        {"author": "Agent Lee", "text": "Incident resolved without escalation."},
        {"author": "Dr. Patel", "text": "Supplementary data available at https://secure-research.org"},
        {"author": "Supervisor Kane", "text": "No anomalies detected during inspection."},
        {"author": "Researcher Bloom", "text": "Extended observations uploaded to http://research-notes.lab"},
        {"author": "Agent Novak", "text": "Perimeter secured. No external interference observed."},
        {"author": "Dr. Hargreeve", "text": "Full containment log stored at https://internal-db.scp"},
        {"author": "Technician Moore", "text": "Routine maintenance completed successfully."},
        {"author": "Dr. Alvarez", "text": "Cross-reference materials: http://crosslink.foundation"},
        {"author": "Security Officer Tan", "text": "Shift completed without incidents."},
        {"author": "Analyst Wright", "text": "Statistical model published at https://analysis-hub.org"},
        {"author": "Dr. Kowalski", "text": "Behavioral deviations documented internally."},
        {"author": "Agent Fischer", "text": "Additional footage archived: http://video-storage.sec"},
        {"author": "Senior Researcher Hall", "text": "All test results verified and approved."},
        {"author": "Operations Lead Grant", "text": "Emergency protocol draft shared via https://ops-share.scp"}
    ]

    reports_with_links_simple = list(filter(
        lambda report: 'http://' in report["text"] or 'https://' in report["text"],
        reports
    ))

    for report in reports_with_links_simple:
        # Простая замена для каждой ссылки
        text = report["text"]
        for protocol in ['http://', 'https://']:
            if protocol in text:
                # Находим позицию начала ссылки
                start = text.find(protocol)
                # Находим конец ссылки (первый пробел после начала)
                end = text.find(' ', start)
                if end == -1:  # если ссылка в конце строки
                    end = len(text)
                # Заменяем ссылку
                text = text[:start] + '[ДАННЫЕ УДАЛЕНЫ]' + text[end:]

        print(f"{report['author']}: {text}")

# Lab7Zad5()

def Lab7Zad6():
    scp_objects = [
        {"scp": "SCP-096", "class": "Euclid"},
        {"scp": "SCP-173", "class": "Euclid"},
        {"scp": "SCP-055", "class": "Keter"},
        {"scp": "SCP-999", "class": "Safe"},
        {"scp": "SCP-3001", "class": "Keter"}
    ]

    enhanced_containment_scps = list(filter(
        lambda obj: obj["class"] != "Safe",
        scp_objects
    ))

    print("SCP-объекты, требующие усиленных мер содержания:")
    for obj in enhanced_containment_scps:
        print(f"{obj['scp']} - класс: {obj['class']}")


# Lab7Zad6()


def Lab7Zad7():
    incidents = [
        {"id": 101, "staff": 4},
        {"id": 102, "staff": 12},
        {"id": 103, "staff": 7},
        {"id": 104, "staff": 20}
    ]
    # 1. Сортируем инцидентыв по количеству персонала(по убываниию)
    sorted_incidents = sorted(incidents, key=lambda x: x["staff"], reverse=True)

    print("Все инциденты, отсортированные по количеству персонала (по убыванию):")
    for incident in sorted_incidents:
        print(f"Инцидент {incident['id']}: {incident['staff']} человек")

    # 2. Оставляем только три наиболее ресурсоемких инцидента
    top_three_incidents = sorted_incidents[:3]

    print("\nТри наиболее ресурсоемких инцидента:")
    for incident in top_three_incidents:
        print(f"Инцидент {incident['id']}: {incident['staff']} человек")


# Lab7Zad7()



def Lab7Zad8():
    protocols = [
        ("Lockdown", 5),
        ("Evacuation", 4),
        ("Data Wipe", 3),
        ("Routine Scan", 1)
        ]
    protocol_strings = list(map(
        lambda protocol: f"Protocol {protocol[0]} - Criticality {protocol[1]}",
        protocols
    ))

    print("Протоколы безопасности:")
    for protocol_str in protocol_strings:
        print(protocol_str)


# Lab7Zad8()

def Lab7Zad9():
    shifts = [6, 12, 8, 24, 10, 4]

    shifts2 = list(filter(
        lambda duration: 8 <= duration <= 12,
        shifts
    ))

    print("Все смены:", shifts)
    print("Смены от 8 до 12 часов включительно:", shifts2)


# Lab7Zad9()


def Lab7Zad10():
    evaluations = [
        {"name": "Agent Cole", "score": 78},
        {"name": "Dr. Weiss", "score": 92},
        {"name": "Technician Moore", "score": 61},
        {"name": "Researcher Lin", "score": 88}
    ]
    Luchsyi = max(evaluations, key=lambda emp: emp["score"])

    print(f"Сотрудник с наивысшей оценкой: {Luchsyi['name']} ({Luchsyi['score']} баллов)")

# Lab7Zad10()




