import re
import tkinter as tk
from tkinter import scrolledtext
import sympy as sp
from sympy import symbols, Eq, solve, simplify, sympify
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
        
        # Make it look like cmd/terminal
        self.root.resizable(True, True)
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create output area (like terminal screen)
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
        
        # Create input frame
        input_frame = tk.Frame(main_frame, bg='black')
        input_frame.pack(fill=tk.X)
        
        # Command prompt label
        prompt_label = tk.Label(
            input_frame,
            text=">>> ",
            bg='black',
            fg='lime',
            font=('Consolas', 11, 'bold')
        )
        prompt_label.pack(side=tk.LEFT)
        
        # Input field
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
        
        # Bind enter key to process command
        self.input_field.bind('<Return>', self.process_command)
        
        # Focus on input field
        self.input_field.focus_set()
        
        # Display welcome message
        self.display_welcome()
        
    def display_welcome(self):
        """Display welcome message"""
        welcome_msg = """╔══════════════════════════════════════════════════════════════════════╗
║                    🧮 MATH TERMINAL 🧮                                ║
║                        Standalone Terminal Version                   ║
╚══════════════════════════════════════════════════════════════════════╝

💡 Available Commands:
   • equation("your_equation")  - Solve equations
   • verify("your_equation")    - Check if equation is true
   • simplify("expression")     - Simplify expressions
   • expression("expression")   - Analyze expressions
   • guide()                    - Show detailed tutorial

🚀 Quick Start: Try typing → equation("x + 5 = 10")
📚 Need help? Type → guide()

Ready to calculate! 🎯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        self.print_output(welcome_msg)
    
    def print_output(self, text, color='white'):
        """Print text to output area"""
        self.output_area.config(state=tk.NORMAL)
        
        # Add timestamp-like prompt for commands
        if text.strip() and not text.startswith(('╔', '║', '╚', '💡', '🚀', '📚', 'Ready', '━')):
            if text.startswith('\n'):
                text = text[1:]  # Remove leading newline
            
        self.output_area.insert(tk.END, text + '\n')
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)
        
        # Update the GUI
        self.root.update_idletasks()
    
    def process_command(self, event=None):
        """Process user command"""
        command = self.input_field.get().strip()
        if not command:
            return
            
        # Display the command with prompt
        self.print_output(f">>> {command}", 'lime')
        
        # Clear input field
        self.input_field.delete(0, tk.END)
        
        # Process command in separate thread to avoid GUI freezing
        thread = threading.Thread(target=self.execute_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def execute_command(self, command):
        """Execute the command"""
        try:
            if not self.parse_command(command):
                return
        except Exception as e:
            self.print_output(f"❌ An error occurred: {e}")
            self.print_output("💡 Type guide() for help.")
    
    def guide(self):
        """Display tutorial and usage instructions"""
        guide_text = """
╔══════════════════════════════════════════════════════════════════════╗
║            📚 LINEAR EQUATION CALCULATOR - TUTORIAL 📚               ║
╚══════════════════════════════════════════════════════════════════════╝

🎯 HOW TO USE THIS CALCULATOR:
Just type one of the 5 commands below, EXACTLY as shown!

🔢 1. SOLVE AN EQUATION (Find what x, y, etc. equals)
──────────────────────────────────────────────────────────────────────
   Type: equation("your_equation_here")
   What it does: Finds the value of variables
   📝 Example: equation("2*x + 5 = 13")
   💡 This will tell you x = 4

✅ 2. CHECK IF AN EQUATION IS TRUE
──────────────────────────────────────────────────────────────────────
   Type: verify("your_equation_here")
   What it does: Checks if both sides are equal
   📝 Example: verify("3 + 4 = 7")
   💡 This will say TRUE or FALSE

🔧 3. SIMPLIFY AN EXPRESSION
──────────────────────────────────────────────────────────────────────
   Type: simplify("your_expression_here")
   What it does: Makes expressions shorter/cleaner
   📝 Example: simplify("x + x + x")
   💡 This will give you 3*x

🧮 4. WORK WITH AN EXPRESSION (No solving)
──────────────────────────────────────────────────────────────────────
   Type: expression("your_expression_here")
   What it does: Shows you the expression info
   📝 Example: expression("2*x + 3*y")
   💡 This tells you about variables in it

❓ 5. SHOW THIS HELP AGAIN
──────────────────────────────────────────────────────────────────────
   Type: guide()
   💡 Shows this tutorial whenever you're confused

📋 IMPORTANT RULES (Please read!):
──────────────────────────────────────────────────────────────────────
✓ ALWAYS put your math inside double quotes: "like this"
✓ Use * for multiplication: 2*x (not 2x)
✓ Use ** for powers: x**2 (not x^2)
✓ Maximum 5 different variables (x, y, z, a, b)
✓ Only 1 equals sign (=) per equation
✓ Variables can be any letter: x, y, z, a, b, etc.

📖 STEP-BY-STEP EXAMPLES:
──────────────────────────────────────────────────────────────────────
🎯 To solve: 2x + 3 = 11
   You type: equation("2*x + 3 = 11")
   You get: x = 4

🎯 To check: Is 5 + 5 equal to 10?
   You type: verify("5 + 5 = 10")
   You get: TRUE

🎯 To simplify: x + x + x + 2x
   You type: simplify("x + x + x + 2*x")
   You get: 5*x

❗ COMMON MISTAKES TO AVOID:
──────────────────────────────────────────────────────────────────────
❌ DON'T type: equation(2*x + 3 = 11)  # Missing quotes!
✅ DO type: equation("2*x + 3 = 11")

❌ DON'T type: equation("2x + 3 = 11")  # Missing * for multiply!
✅ DO type: equation("2*x + 3 = 11")

❌ DON'T type: equation("x^2 = 4")  # Use ** not ^!
✅ DO type: equation("x**2 = 4")

🚀 READY TO START? Try typing one of these:
──────────────────────────────────────────────────────────────────────
equation("x + 5 = 10")
simplify("2*x + 3*x")
verify("2 + 2 = 4")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.print_output(guide_text)
    
    def validate_input(self, input_str):
        """Validate the input string for rules compliance"""
        # Check for equals signs
        equals_count = input_str.count('=')
        if equals_count > 1:
            self.print_output("❌ Error: Only 1 equals sign (=) allowed per equation")
            return False
            
        # Extract variables
        variables = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', input_str)
        # Filter out function names and mathematical constants
        excluded = {'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'pi', 'e'}
        variables = [var for var in variables if var not in excluded]
        
        if len(set(variables)) > 5:
            self.print_output("❌ Error: Maximum 5 variables allowed")
            return False
            
        return True
    
    def parse_expression(self, expr_str):
        """Parse string expression into sympy expression"""
        try:
            # Replace common mathematical notations
            expr_str = expr_str.replace('^', '**')
            expr = parse_expr(expr_str)
            return expr
        except Exception as e:
            self.print_output(f"❌ Error parsing expression: {e}")
            return None
    
    def expression(self, expr_str):
        """Evaluate mathematical expressions"""
        self.print_output(f"🧮 Evaluating expression: {expr_str}")
        
        if not self.validate_input(expr_str):
            return
            
        expr = self.parse_expression(expr_str)
        if expr is None:
            return
            
        self.print_output(f"📝 Parsed expression: {expr}")
        
        # Get all variables in the expression
        variables = list(expr.free_symbols)
        
        if not variables:
            # No variables, just evaluate
            result = float(expr)
            self.print_output(f"💡 Result: {result}")
        else:
            self.print_output(f"🔤 Variables found: {[str(var) for var in variables]}")
            self.print_output("ℹ️  This expression contains variables and cannot be evaluated to a single number.")
            self.print_output("💭 Use simplify() to simplify the expression or equation() to solve for variables.")
    
    def verify(self, equation_str):
        """Verify if an equation is true"""
        self.print_output(f"✅ Verifying equation: {equation_str}")
        
        if not self.validate_input(equation_str):
            return
            
        if '=' not in equation_str:
            self.print_output("❌ Error: Equation must contain an equals sign (=)")
            return
            
        try:
            left_str, right_str = equation_str.split('=', 1)
            left_expr = self.parse_expression(left_str.strip())
            right_expr = self.parse_expression(right_str.strip())
            
            if left_expr is None or right_expr is None:
                return
                
            # Get all variables
            all_vars = list((left_expr.free_symbols | right_expr.free_symbols))
            
            if not all_vars:
                # No variables, direct comparison
                if left_expr.equals(right_expr):
                    self.print_output("✅ The equation is TRUE")
                else:
                    self.print_output("❌ The equation is FALSE")
                    self.print_output(f"   Left side: {float(left_expr)}")
                    self.print_output(f"   Right side: {float(right_expr)}")
            else:
                # Check if the equation is an identity (always true) or contradiction (always false)
                equation = Eq(left_expr, right_expr)
                
                # Try to solve the equation
                solutions = solve(equation, all_vars)
                
                # Simplify both sides to see if they're identical
                simplified_diff = simplify(left_expr - right_expr)
                
                if simplified_diff == 0:
                    # The equation is always true (identity)
                    self.print_output("✅ The equation is TRUE for all values")
                    self.print_output("💡 This is an identity - both sides are mathematically equivalent")
                elif not solutions:
                    # No solutions exist - contradiction
                    self.print_output("❌ The equation is FALSE for all values")
                    self.print_output("💡 This equation has no solution - it's a contradiction")
                elif len(solutions) == 1 and len(all_vars) == 1:
                    # One specific solution
                    var = all_vars[0]
                    sol = solutions[0]
                    self.print_output(f"✅ The equation is TRUE only when {var} = {sol}")
                    self.print_output(f"❌ The equation is FALSE for all other values of {var}")
                else:
                    # Multiple variables or solutions
                    self.print_output(f"🔤 Variables found: {[str(var) for var in all_vars]}")
                    if solutions:
                        self.print_output("✅ The equation is true for specific values:")
                        if isinstance(solutions[0], dict):
                            for sol in solutions:
                                vals = [f"{var} = {val}" for var, val in sol.items()]
                                self.print_output(f"   📍 {', '.join(vals)}")
                        else:
                            for sol in solutions:
                                if len(all_vars) == 1:
                                    self.print_output(f"   📍 {all_vars[0]} = {sol}")
                                else:
                                    vals = [f"{var} = {val}" for var, val in zip(all_vars, sol)]
                                    self.print_output(f"   📍 {', '.join(vals)}")
                    else:
                        self.print_output("❓ Cannot verify equation - use equation() to solve for the variables.")
                
        except Exception as e:
            self.print_output(f"❌ Error verifying equation: {e}")
    
    def simplify_expr(self, expr_str):
        """Simplify mathematical expressions"""
        self.print_output(f"🔧 Simplifying: {expr_str}")
        
        if not self.validate_input(expr_str):
            return
            
        if '=' in expr_str:
            # Handle equation
            left_str, right_str = expr_str.split('=', 1)
            left_expr = self.parse_expression(left_str.strip())
            right_expr = self.parse_expression(right_str.strip())
            
            if left_expr is None or right_expr is None:
                return
                
            simplified_left = simplify(left_expr)
            simplified_right = simplify(right_expr)
            
            self.print_output(f"✨ Simplified equation: {simplified_left} = {simplified_right}")
        else:
            # Handle expression
            expr = self.parse_expression(expr_str)
            if expr is None:
                return
                
            simplified = simplify(expr)
            self.print_output(f"✨ Simplified expression: {simplified}")
    
    def solve_equation(self, equation_str):
        """Solve equations to find variable values"""
        self.print_output(f"🔢 Solving equation: {equation_str}")
        
        if not self.validate_input(equation_str):
            return
            
        if '=' not in equation_str:
            self.print_output("❌ Error: Must be an equation with an equals sign (=)")
            return
            
        try:
            left_str, right_str = equation_str.split('=', 1)
            left_expr = self.parse_expression(left_str.strip())
            right_expr = self.parse_expression(right_str.strip())
            
            if left_expr is None or right_expr is None:
                return
                
            # Create equation
            equation = Eq(left_expr, right_expr)
            
            # Get variables
            variables = list(equation.free_symbols)
            
            if not variables:
                self.print_output("❓ No variables to solve for.")
                return
                
            self.print_output(f"🔤 Variables: {[str(var) for var in variables]}")
            
            # Solve equation
            solutions = solve(equation, variables)
            
            if not solutions:
                self.print_output("❌ No solution found.")
            elif len(variables) == 1:
                self.print_output(f"🎯 Solution: {variables[0]} = {solutions[0]}")
            else:
                self.print_output("🎯 Solutions:")
                for sol in solutions:
                    if isinstance(sol, dict):
                        for var, val in sol.items():
                            self.print_output(f"   📍 {var} = {val}")
                    else:
                        for i, var in enumerate(variables):
                            self.print_output(f"   📍 {var} = {sol[i]}")
                            
        except Exception as e:
            self.print_output(f"❌ Error solving equation: {e}")
    
    def parse_command(self, command):
        """Parse and execute user command"""
        command = command.strip()
        
        # Check for guide()
        if command == "guide()":
            self.guide()
            return True
            
        # Parse function calls with parameters
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
        
        # Invalid command
        self.print_output(f"❌ Invalid command: {command}")
        self.print_output("💡 Running guide() to show available commands...")
        self.print_output("")
        self.guide()
        return True
    
    def run(self):
        """Start the calculator"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

# Run the calculator
if __name__ == "__main__":
    calculator = LinearEquationCalculator()
    calculator.run()