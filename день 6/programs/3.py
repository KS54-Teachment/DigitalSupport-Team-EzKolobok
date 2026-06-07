import random
import string

def generate_password(length):
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов.")
    
    letters = string.ascii_letters
    digits = string.digits 
    special = string.punctuation
    
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special)
    ]
    
    all_chars = letters + digits + special
    remaining_length = length - 3
    password += random.choices(all_chars, k=remaining_length)
    
    random.shuffle(password)
    
    return ''.join(password)

def main():
    print("=" * 40)
    print("   ГЕНЕРАТОР НАДЁЖНЫХ ПАРОЛЕЙ")
    print("=" * 40)
    
    while True:
        user_input = input("\nВведите длину пароля (или 'выход' для завершения): ").strip()
        
        if user_input.lower() in ("выход", "exit", "quit"):
            print("До свидания!")
            break
        
        if not user_input.isdigit():
            print("Ошибка: введите целое число.")
            continue
        
        length = int(user_input)
        
        try:
            password = generate_password(length)
            print(f"\nВаш пароль: {password}")
            print(f"Длина: {len(password)} символов")
            
            has_letter = any(c in string.ascii_letters for c in password)
            has_digit = any(c in string.digits for c in password)
            has_special = any(c in string.punctuation for c in password)
            
            print(f"Состав: Буквы — {'✓' if has_letter else '✗'} | "
                  f"Цифры — {'✓' if has_digit else '✗'} | "
                  f"Спецсимволы — {'✓' if has_special else '✗'}")
            
        except ValueError as e:
            print(f"Ошибка: {e}")

main()