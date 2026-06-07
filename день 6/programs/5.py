import json
import os
from datetime import datetime

TICKETS_FILE = "tickets.json"
REPORT_FILE = "report.txt"

def load_tickets():
    """Загружает обращения из JSON-файла."""
    if not os.path.exists(TICKETS_FILE):
        return []
    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def generate_report(tickets, team_name):
    """Формирует текст отчёта."""
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # Считаем статусы
    total = len(tickets)
    new_count = sum(1 for t in tickets if t.get("status") == "Новое")
    in_progress = sum(1 for t in tickets if t.get("status") == "В работе")
    resolved = sum(1 for t in tickets if t.get("status") == "Решено")
    cancelled = sum(1 for t in tickets if t.get("status") == "Отменено")
    processed = resolved + cancelled  # обработанные (завершённые)
    
    lines = []
    lines.append("=" * 60)
    lines.append(" " * 20 + "О Т Ч Ё Т")
    lines.append("=" * 60)
    lines.append(f"Название команды: {team_name}")
    lines.append(f"Дата формирования: {now}")
    lines.append("-" * 60)
    
    # Список обращений
    lines.append("СПИСОК ОБРАЩЕНИЙ:")
    lines.append("")
    
    if not tickets:
        lines.append("  Обращения отсутствуют.")
    else:
        lines.append(f"{'№':<<4} {'ID':<<5} {'Дата':<<16} {'Статус':<<12} {'Категория':<<15} {'Имя':<<15} Описание")
        lines.append("-" * 60)
        for i, t in enumerate(tickets, 1):
            desc = t.get("description", "")
            # Обрезаем очень длинное описание
            if len(desc) > 35:
                desc = desc[:32] + "..."
            lines.append(f"{i:<4} {t['id']:<5} {t.get('date', '-'):<<16} {t.get('status', '-'):<<12} "
                        f"{t.get('category', '-'):<<15} {t.get('name', '-'):<<15} {desc}")
    
    lines.append("")
    lines.append("-" * 60)
    lines.append("СТАТИСТИКА:")
    lines.append(f"  Всего заявок:            {total}")
    lines.append(f"  Новых:                   {new_count}")
    lines.append(f"  В работе:                {in_progress}")
    lines.append(f"  Решено:                  {resolved}")
    lines.append(f"  Отменено:                {cancelled}")
    lines.append(f"  Обработано (завершено):  {processed}")
    lines.append("=" * 60)
    
    return "\n".join(lines)

def save_report(content):
    """Сохраняет отчёт в файл."""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✓ Отчёт сохранён в файл: {os.path.abspath(REPORT_FILE)}")

def main():
    print("=" * 50)
    print("       ПРОГРАММА СОХРАНЕНИЯ ОТЧЁТА")
    print("=" * 50)
    
    tickets = load_tickets()
    print(f"Загружено обращений из базы: {len(tickets)}")
    
    team_name = "EzKolobok"
    
    report_text = generate_report(tickets, team_name)
    
    # Показываем отчёт на экране
    print("\n" + "=" * 50)
    print("ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР:")
    print("=" * 50)
    print(report_text)
    
    # Сохраняем
    save_report(report_text)
    
    print("\nОтчёт готов! Можете открыть файл report.txt.")

main()