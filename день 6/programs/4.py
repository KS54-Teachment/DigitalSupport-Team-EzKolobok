import json
import os
from datetime import datetime

FILE_NAME = "tickets.json"

def load_tickets():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tickets(tickets):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

def generate_id(tickets):
    if not tickets:
        return 1
    return max(t["id"] for t in tickets) + 1

def add_ticket(tickets):
    print("\n--- Новое обращение ---")
    name = input("Ваше имя: ").strip()
    category = input("Категория (например, Техподдержка, Бухгалтерия, IT): ").strip()
    description = input("Описание проблемы: ").strip()
    
    if not name or not description:
        print("Ошибка: имя и описание не могут быть пустыми.")
        return
    
    ticket = {
        "id": generate_id(tickets),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": name,
        "category": category,
        "description": description,
        "status": "Новое"
    }
    
    tickets.append(ticket)
    save_tickets(tickets)
    print(f"\n✓ Обращение #{ticket['id']} успешно добавлено!")

def view_tickets(tickets):
    if not tickets:
        print("\nБаза обращений пуста.")
        return
    
    print("\n" + "=" * 80)
    print(f"{'ID':<<5} {'Дата':<<16} {'Статус':<<12} {'Категория':<<15} {'Имя':<<15} {'Описание'}")
    print("-" * 80)
    
    for t in tickets:
        desc = t["description"][:30] + "..." if len(t["description"]) > 30 else t["description"]
        print(f"{t['id']:<5} {t['date']:<16} {t['status']:<12} {t['category']:<15} {t['name']:<15} {desc}")
    
    print("=" * 80)
    print(f"Всего обращений: {len(tickets)}")

def delete_ticket(tickets):
    if not tickets:
        print("\nНет обращений для удаления.")
        return
    
    view_tickets(tickets)
    try:
        ticket_id = int(input("\nВведите ID обращения для удаления: "))
    except ValueError:
        print("Ошибка: введите число.")
        return
    
    for i, t in enumerate(tickets):
        if t["id"] == ticket_id:
            confirm = input(f"Удалить обращение #{ticket_id} от {t['name']}? (да/нет): ").strip().lower()
            if confirm in ("да", "д", "yes", "y"):
                tickets.pop(i)
                save_tickets(tickets)
                print(f"✓ Обращение #{ticket_id} удалено.")
            else:
                print("Удаление отменено.")
            return
    
    print(f"Обращение с ID {ticket_id} не найдено.")

def search_tickets(tickets):
    if not tickets:
        print("\nБаза обращений пуста.")
        return
    
    query = input("\nВведите ключевое слово для поиска: ").strip().lower()
    if not query:
        print("Ошибка: пустой запрос.")
        return
    
    results = []
    for t in tickets:
        if (query in t["name"].lower() or 
            query in t["category"].lower() or 
            query in t["description"].lower() or
            query in t["status"].lower() or
            query in str(t["id"])):
            results.append(t)
    
    if not results:
        print(f"По запросу «{query}» ничего не найдено.")
        return
    
    print(f"\nНайдено обращений: {len(results)}")
    print("-" * 80)
    for t in results:
        print(f"ID: {t['id']} | {t['date']} | {t['status']}")
        print(f"  Имя: {t['name']}")
        print(f"  Категория: {t['category']}")
        print(f"  Описание: {t['description']}")
        print("-" * 80)

def change_status(tickets):
    if not tickets:
        print("\nНет обращений.")
        return
    
    try:
        ticket_id = int(input("\nВведите ID обращения для изменения статуса: "))
    except ValueError:
        print("Ошибка: введите число.")
        return
    
    for t in tickets:
        if t["id"] == ticket_id:
            print(f"\nТекущий статус: {t['status']}")
            print("Доступные статусы: 1. Новое  2. В работе  3. Решено  4. Отменено")
            choice = input("Выберите статус (1-4): ").strip()
            
            statuses = {
                "1": "Новое",
                "2": "В работе",
                "3": "Решено",
                "4": "Отменено"
            }
            
            if choice in statuses:
                t["status"] = statuses[choice]
                save_tickets(tickets)
                print(f"✓ Статус обращения #{ticket_id} изменён на «{t['status']}».")
            else:
                print("Неверный выбор.")
            return
    
    print(f"Обращение с ID {ticket_id} не найдено.")

def main():
    tickets = load_tickets()
    
    while True:
        print("\n" + "=" * 40)
        print("         БАЗА ОБРАЩЕНИЙ")
        print("=" * 40)
        print("1. Добавить обращение")
        print("2. Просмотреть обращения")
        print("3. Удалить обращение")
        print("4. Поиск обращения")
        print("5. Изменить статус")
        print("0. Выход")
        print("-" * 40)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            add_ticket(tickets)
        elif choice == "2":
            view_tickets(tickets)
        elif choice == "3":
            delete_ticket(tickets)
        elif choice == "4":
            search_tickets(tickets)
        elif choice == "5":
            change_status(tickets)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

main()