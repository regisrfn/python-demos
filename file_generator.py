import random
from datetime import datetime, timedelta

# Function to generate a random CPF (with valid check digits)
def generate_cpf():
    def calculate_digit(numbers):
        total = sum([int(number) * (len(numbers) + 1 - idx) for idx, number in enumerate(numbers)])
        digit = 11 - total % 11
        return str(digit if digit < 10 else 0)

    base_cpf = [random.randint(0, 9) for _ in range(9)]
    first_digit = calculate_digit(base_cpf)
    second_digit = calculate_digit(base_cpf + [int(first_digit)])
    return ''.join(map(str, base_cpf)) + first_digit + second_digit

# Function to generate a random CNPJ (with valid check digits)
def generate_cnpj():
    def calculate_digit(numbers, weights):
        total = sum([int(number) * weight for number, weight in zip(numbers, weights)])
        digit = 11 - total % 11
        return str(digit if digit < 10 else 0)

    base_cnpj = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_weights = [6] + first_weights
    first_digit = calculate_digit(base_cnpj, first_weights)
    second_digit = calculate_digit(base_cnpj + [int(first_digit)], second_weights)
    return ''.join(map(str, base_cnpj)) + first_digit + second_digit

# Function to generate a random name
def generate_name():
    first_names = ['João', 'Maria', 'Ana', 'Carlos', 'Fernanda', 'Lucas', 'Pedro', 'Isabela']
    last_names = ['Silva', 'Santos', 'Oliveira', 'Pereira', 'Costa', 'Almeida', 'Souza', 'Lima']
    return random.choice(first_names) + " " + random.choice(last_names)

# Function to generate a random date in the format YYYYMMDD
def generate_random_date():
    start_date = datetime(2000, 1, 1)
    random_days = random.randint(0, 365 * 20)  # Last 20 years
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y%m%d')

# Function to generate a random numeric "Chave Operacao" (up to 15 characters, padded to 50 characters in the field)
def generate_chave_operacao():
    return ''.join(random.choices('0123456789', k=random.randint(5, 15))).ljust(50)  # Pad to 50 characters

# Function to create random lines according to the exact size and sequence (15 fields)
def create_random_lines(num_lines):
    lines = []
    for i in range(1, num_lines + 1):  # Start line number from 1
        # Randomly choose whether to generate a CPF or CNPJ
        tipo_pessoa = random.choice(['F', 'J'])
        document = generate_cpf() if tipo_pessoa == 'F' else generate_cnpj()
        
        # Ensure the document (CPF or CNPJ) is always 14 characters, padded with zeros on the left
        document = document.zfill(14)

        # Generate other fields, padded with zeros on the left for 'empresa' and 'agencia'
        empresa = "60701190" # Empresa padded to 8 digits
        agencia_number = ''.join(random.choices('0123456789', k=4))
        agencia_dv = ''.join(random.choices('0123456789', k=2))
        agencia = (agencia_number + agencia_dv).zfill(6)  # Agencia padded to 6 digits
        chave_operacao = generate_chave_operacao()  # Chave da Operação padded to 50 characters, numeric up to 15
        nome_cliente = generate_name().ljust(40)[:40]  # Ensure name is exactly 40 chars
        tipo_bdv = random.choice(['01', '02', '03', '04', '05']).ljust(2)
        descricao_bdv = random.choice(['Contas Correntes', 'Contas de Poupança', 'Outros BDV', 'Contas CC5']).ljust(20)[:20]
        titularidade = random.choice(['T', 'C']).ljust(1)  # 1 for first holder, 2 for others
        start_date = generate_random_date()

        # Randomly decide if the end date should be empty or not
        end_date = generate_random_date() if random.choice([True, False]) else '        '  # 8 spaces if empty

        # Filler and "Número de registro" are fixed-size fields
        filler = ''.ljust(20)
        numero_registro = str(i).zfill(10)  # Use the line number, padded to 10 digits

        # Ensure start date is before or the same as end date if not empty
        if end_date.strip() and start_date > end_date:
            start_date, end_date = end_date, start_date

        # Build the line according to the specified sizes and sequence (15 fields)
        line = (
            f"C"  # Tipo de Registro (Fixed as 0)
            f"{tipo_pessoa:<1}"  # Tipo de Pessoa (F or J)
            f"{document:<14}"  # CPF or CNPJ, filled with zeros on the left if less than 14 characters
            f"{empresa:<8}"  # Empresa, padded with zeros on the left
            f"{agencia:<6}"  # Agência, padded with zeros on the left
            f"{chave_operacao}"  # Chave da Operação (exactly 50 characters, numeric up to 15 digits)
            f"{nome_cliente}"  # Nome do Cliente (exactly 40 characters)
            f"{tipo_bdv:<2}"  # Tipo de BDV (2 characters)
            f"{descricao_bdv}"  # Descrição BDV (exactly 20 characters)
            f"{titularidade:<1}"  # Titularidade (1 character)
            f"{start_date:<8}"  # Data de Início (YYYYMMDD, 8 characters)
            f"{end_date:<8}"  # Data de Encerramento (YYYYMMDD, or 8 spaces if empty)
            f"{filler}"  # Filler (20 spaces)
            f"{numero_registro:<10}"  # Número de Registro (10 characters, filled with line number)
        )
        
        lines.append(line.strip())  # Remove unnecessary spaces at the end

    return lines

# Main program to generate the specified number of lines and print them
def main():
    num_lines = 3
    random_lines = create_random_lines(num_lines)
    
    # Writing lines to a file
    with open("random_lines_fixed_size.txt", "w") as file:
        for line in random_lines:
            file.write(line + "\n")

    print(f"{num_lines} random lines generated and saved to 'random_lines_fixed_size.txt'.")

# Run the program
if __name__ == "__main__":
    main()
