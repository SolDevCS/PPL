import re

# Snake Game Interpreter (Interpreter only – no snake logic yet)

program = []
labels = {}
pc = 0  # program counter


def load_program(lines):
    """Reads the script and tokenizes each instruction."""
    global program, labels
    program = []
    labels = {}
    token_counter = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip blanks or comments

        parts = line.split()
        opcode = parts[0].upper()

        # Label definition (e.g. LOOP:)
        if opcode.endswith(":"):
            labels[opcode[:-1]] = token_counter
            continue

        # Regular instructions
        program.append(parts)
        token_counter += 1


def execute_program():
    """Main interpreter loop."""
    global pc
    pc = 0 # program counter
    loop_stack = []

    while pc < len(program):
        parts = program[pc]
        opcode = parts[0].upper()

        # --- MOVE direction steps ---
        if opcode == "MOVE":
            if len(parts) != 3:
                raise SyntaxError(f"Invalid MOVE syntax at line {pc+1}")
            direction = parts[1].upper()
            steps = int(parts[2])
            print(f"[INTERPRETER] Move {direction} by {steps} steps")
            pc += 1

        # --- EAT ---
        elif opcode == "EAT":
            print("[INTERPRETER] Eat fruit")
            # snake.eat()  <-- connect later
            pc += 1

        # --- LOOP count ---
        elif opcode == "LOOP":
            if len(parts) != 2:
                raise SyntaxError(f"Invalid LOOP syntax at line {pc+1}")
            count = int(parts[1])
            loop_stack.append({"start": pc + 1, "remaining": count})
            pc += 1

        # --- ENDLOOP ---
        elif opcode == "ENDLOOP":
            if not loop_stack:
                raise SyntaxError(f"ENDLOOP found without LOOP at line {pc+1}")
            loop = loop_stack[-1]
            loop["remaining"] -= 1
            if loop["remaining"] > 0:
                pc = loop["start"]  # go back inside loop
            else:
                loop_stack.pop()
                pc += 1

        # --- Unknown opcode ---
        else:
            raise SyntaxError(f"Unknown opcode '{opcode}' at line {pc+1}")


# ======================
# Example Input Script
# ======================

program_lines = [
    "MOVE RIGHT 3",
    "MOVE UP 2",
    "EAT",
    "LOOP 2",
    "MOVE LEFT 1",
    "MOVE DOWN 1",
    "ENDLOOP",
    "EAT"
]

# Load and run
load_program(program_lines)
execute_program()
