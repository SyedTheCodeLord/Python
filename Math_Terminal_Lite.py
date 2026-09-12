import re
import tkinter as tk
from tkinter import scrolledtext
import sympy as sp
from sympy import Eq, solve, simplify
from sympy.parsing.sympy_parser import parse_expr
import threading

class LinearEquationCalculator:
    def __init__(self):
        self.variables = set()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the terminal-like GUI window"""
        self.root = tk.Tk()
        self.root.title("Linear Equation Calculator")
        self.root.geometry("900x600")
        self.root.configure(bg='black')
        
        self.root.resizable(True, True)
        
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.output_area = scrolledtext.ScrolledText(
            main_frame,
            bg='black',
            fg='yellow',
            font=('Consolas', 11),
            insertbackground='white',
            selectbackground='#404040',
            selectforeground='white',
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=30
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        input_frame = tk.Frame(main_frame, bg='black')
        input_frame.pack(fill=tk.X)
        
        prompt_label = tk.Label(
            input_frame,
            text=">>> ",
            bg='black',
            fg='lime',
            font=('Consolas', 11, 'bold')
        )

        prompt_label.pack(side=tk.LEFT)
        self.input_field = tk.Entry(
            input_frame,
            bg='black',
            fg='white',
            font=('Consolas', 11),
            insertbackground='white',
            selectbackground='#404040',
            selectforeground='white',
            bd=0,
            highlightthickness=1,
            highlightcolor='lime',
            highlightbackground='gray'
        )
        self.input_field.pack(fill=tk.X, expand=True, padx=(5, 0))

        self.input_field.bind('<Return>', self.process_command)

        self.input_field.focus_set()
        
        self.display_welcome()
        
    def display_welcome(self):
        """Display welcome message"""
        welcome_msg = """╔══════════════════════════════════════════════════════════════════════╗
║                     MATH TERMINAL [OLD]                              ║
║                         Lite Version                                 ║
╚══════════════════════════════════════════════════════════════════════╝

By BRACISTONE STUDIOS.

Available Commands:
   equation("x")       - Solve equations
   verify("x")         - Check if equation is true
   simplify("x")       - Simplify expressions
   expression("x")     - Solve Arithmetic expressions

Ready to calculate!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        self.print_output(welcome_msg)
    
    def print_output(self, text, color='white'):
        """Print text to output area"""
        self.output_area.config(state=tk.NORMAL)
        
        if text.strip() and not text.startswith(('╔', '║', '╚', 'Ready', '━')):
            if text.startswith('\n'):
                text = text[1:]
            
        self.output_area.insert(tk.END, text + '\n')
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def process_command(self, event=None):
        """Process user command"""
        command = self.input_field.get().strip()
        if not command:
            return
            
        self.print_output(f">>> {command}", 'lime')
        
        self.input_field.delete(0, tk.END)
        
        thread = threading.Thread(target=self.execute_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def execute_command(self, command):
        try:
            if not self.parse_command(command):
                return
        except Exception as e:
            self.print_output(f"An error occurred: {e}")
    
    def validate_input(self, input_str):
        equals_count = input_str.count('=')
        if equals_count > 1:
            self.print_output("Error: Only 1 equals sign (=) allowed per equation")
            return False
            
        variables = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', input_str)
        excluded = {'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'pi', 'e'}
        variables = [var for var in variables if var not in excluded]
        
        if len(set(variables)) > 5:
            self.print_output("Error: Maximum 5 variables allowed")
            return False
            
        return True
    
    def parse_expression(self, expr_str):
        try:
            expr_str = expr_str.replace('^', '**')
            expr = parse_expr(expr_str)
            return expr
        except Exception as e:
            self.print_output(f"Error parsing expression: {e}")
            return None
    
    def expression(self, expr_str):
        self.print_output(f"Evaluating expression: {expr_str}")
        
        if not self.validate_input(expr_str):
            return
            
        expr = self.parse_expression(expr_str)
        if expr is None:
            return
            
        self.print_output(f"Parsed expression: {expr}")
        
        variables = list(expr.free_symbols)
        
        if not variables:
            result = float(expr)
            self.print_output(f"Result: {result}")
        else:
            self.print_output(f"Variables found: {[str(var) for var in variables]}")
            self.print_output("This expression contains variables and cannot be evaluated to a single number.")
            self.print_output("Use simplify() to simplify the expression or equation() to solve for variables.")
    
    def verify(self, equation_str):
        self.print_output(f"Verifying equation: {equation_str}")
        
        if not self.validate_input(equation_str):
            return
            
        if '=' not in equation_str:
            self.print_output("Error: Equation must contain an equals sign (=)")
            return
            
        try:
            left_str, right_str = equation_str.split('=', 1)
            left_expr = self.parse_expression(left_str.strip())
            right_expr = self.parse_expression(right_str.strip())
            
            if left_expr is None or right_expr is None:
                return
                
            all_vars = list((left_expr.free_symbols | right_expr.free_symbols))
            
            if not all_vars:
                if left_expr.equals(right_expr):
                    self.print_output("The equation is TRUE")
                else:
                    self.print_output("The equation is FALSE")
                    self.print_output(f"   Left side: {float(left_expr)}")
                    self.print_output(f"   Right side: {float(right_expr)}")
            else:
                equation = Eq(left_expr, right_expr)

                solutions = solve(equation, all_vars)

                simplified_diff = simplify(left_expr - right_expr)
                
                if simplified_diff == 0:
                    self.print_output("The equation is TRUE for all values")
                    self.print_output("This is an identity - both sides are mathematically equivalent")
                elif not solutions:
                    self.print_output("The equation is FALSE for all values")
                    self.print_output("This equation has no solution - it's a contradiction")
                elif len(solutions) == 1 and len(all_vars) == 1:
                    var = all_vars[0]
                    sol = solutions[0]
                    self.print_output(f"The equation is TRUE only when {var} = {sol}")
                    self.print_output(f"The equation is FALSE for all other values of {var}")
                else:
                    self.print_output(f"Variables found: {[str(var) for var in all_vars]}")
                    if solutions:
                        self.print_output("The equation is true for specific values:")
                        if isinstance(solutions[0], dict):
                            for sol in solutions:
                                vals = [f"{var} = {val}" for var, val in sol.items()]
                                self.print_output(f"   {', '.join(vals)}")
                        else:
                            for sol in solutions:
                                if len(all_vars) == 1:
                                    self.print_output(f"   {all_vars[0]} = {sol}")
                                else:
                                    vals = [f"{var} = {val}" for var, val in zip(all_vars, sol)]
                                    self.print_output(f"   {', '.join(vals)}")
                    else:
                        self.print_output("Cannot verify equation - use equation() to solve for the variables.")
                
        except Exception as e:
            self.print_output(f"Error verifying equation: {e}")
    
    def simplify_expr(self, expr_str):
        self.print_output(f"Simplifying: {expr_str}")
        
        if not self.validate_input(expr_str):
            return
            
        if '=' in expr_str:
            left_str, right_str = expr_str.split('=', 1)
            left_expr = self.parse_expression(left_str.strip())
            right_expr = self.parse_expression(right_str.strip())
            
            if left_expr is None or right_expr is None:
                return
                
            simplified_left = simplify(left_expr)
            simplified_right = simplify(right_expr)
            
            self.print_output(f"Simplified equation: {simplified_left} = {simplified_right}")
        else:
            expr = self.parse_expression(expr_str)
            if expr is None:
                return
                
            simplified = simplify(expr)
            self.print_output(f"Simplified expression: {simplified}")
    
    def solve_equation(self, equation_str):
        self.print_output(f"Solving equation: {equation_str}")
        
        if not self.validate_input(equation_str):
            return
            
        if '=' not in equation_str:
            self.print_output("Error: Must be an equation with an equals sign (=)")
            return
            
        try:
            left_str, right_str = equation_str.split('=', 1)
            left_expr = self.parse_expression(left_str.strip())
            right_expr = self.parse_expression(right_str.strip())
            
            if left_expr is None or right_expr is None:
                return
                
            equation = Eq(left_expr, right_expr)
            
            variables = list(equation.free_symbols)
            
            if not variables:
                self.print_output("No variables to solve for.")
                return
                
            self.print_output(f"Variables: {[str(var) for var in variables]}")
            
            solutions = solve(equation, variables)
            
            if not solutions:
                self.print_output("No solution found.")
            elif len(variables) == 1:
                self.print_output(f"Solution: {variables[0]} = {solutions[0]}")
            else:
                self.print_output("Solutions:")
                for sol in solutions:
                    if isinstance(sol, dict):
                        for var, val in sol.items():
                            self.print_output(f"   {var} = {val}")
                    else:
                        for i, var in enumerate(variables):
                            self.print_output(f"   {var} = {sol[i]}")
                            
        except Exception as e:
            self.print_output(f"Error solving equation: {e}")
    
    def parse_command(self, command):
        command = command.strip()
        
        patterns = [
            (r'^expression\("(.+)"\)$', self.expression),
            (r'^verify\("(.+)"\)$', self.verify),
            (r'^simplify\("(.+)"\)$', self.simplify_expr),
            (r'^equation\("(.+)"\)$', self.solve_equation)
        ]
        
        for pattern, func in patterns:
            match = re.match(pattern, command)
            if match:
                func(match.group(1))
                return True
        
        self.print_output(f"Invalid command: {command}")
        self.print_output("")
        return True
    
    def run(self):
        """Start the calculator"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    calculator = LinearEquationCalculator()
    calculator.run() 
