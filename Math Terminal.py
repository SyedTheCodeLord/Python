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
║                    🧮 MATH TERMINAL 🧮                               ║
║                        Standalone Terminal Version                   ║
╚══════════════════════════════════════════════════════════════════════╝

By BRACISTONE STUDIOS.

💡 Available Commands:
   • equation("your_equation")  - Solve equations
   • verify("your_equation")    - Check if equation is true
   • simplify("expression")     - Simplify expressions
   • expression("expression")   - Solve Arithmetic expressions
   • guide()                    - Show detailed tutorial

🚀 Quick Start: Try typing → equation("x + 5 = 10")
📚 Need help? Type → guide()
[Then Press Enter Key.]

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
║            📚 MATH TERMINAL (CALCULATOR) - TUTORIAL 📚               ║
╚══════════════════════════════════════════════════════════════════════╝

🎯 HOW TO USE THIS CALCULATOR:
Just type one of the 5 commands below, EXACTLY as shown!

🔢 1. SOLVE AN EQUATION (Find what x, y, etc. equals)
──────────────────────────────────────────────────────────────────────
   Type: equation("your_equation_here")
   What it does: Finds the value of variables.
   📝 Example: equation("2*x + 5 = 13")
   💡 This will tell you x = 4.
   🔅 This calculator will only return a single solution even for variables with finite multiple solutions!

✅ 2. CHECK IF AN EQUATION IS TRUE
──────────────────────────────────────────────────────────────────────
   Type: verify("your_equation_here")
   What it does: Checks if both sides are equal.
   📝 Example: verify("3 + 4 = 7")
   💡 This will say eithet TRUE or FALSE.

🔧 3. SIMPLIFY AN EXPRESSION
──────────────────────────────────────────────────────────────────────
   Type: simplify("your_expression_here")
   What it does: Makes expressions shorter/cleaner.
   📝 Example: simplify("x + x + x")
   💡 This will give you 3*x.

🧮 4. WORK WITH AN EXPRESSION (No Algebraic Manipulation!)
──────────────────────────────────────────────────────────────────────
   Type: expression("your_expression_here")
   What it does: Shows you the expression info and solves arithmetic expressions.
   📝 Example 1: expression("2*x + 3*y")
   💡 This tells you about the variables in it.
   📝 Example 2: expression("(900/4 + 25)*4 - 20")
   💡 This gives you the result 980.

❓ 5. SHOW THIS HELP AGAIN
──────────────────────────────────────────────────────────────────────
   Type: guide()
   💡 Shows this tutorial whenever you're confused.

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

🧠 Available Mathematical Functions:
──────────────────────────────────────────────────────────────────────
🍪 abs() --> Absolute Value.
🍪 sin() , cos() , tan() etc. --> Trigonometric Functions 😉.
🍪 log(x, b) --> Logarithm {a = Argument, b = Base}
🍪 ln(x) --> Natural Log (Log with base e {Euler's Number})
🍪 exp(x) --> Exponential {e**(x)}
🍪 sqrt(a) --> Square root of 'a'.
🍪 root(a, b) = a**(1/b)
🍪 factor(x) --> Factoring Polynomials.
🍪 diff(y, x) = dy/dx {Derivative of y with respect to x.} 🔥
🍪 integrate(y, (x, a, b)) =  {Integral of y with respect to x from a to b.} 💥

💡Type ' guide(functions) ' to get a complete list of all Mathematical Functions available!

NOTE:
──────────────────────────────────────────────────────────────────────
💡 'pi' is recognized as the famous irrational 3.141592...
❕ Euler's number (e = 2.71828...) is not recognized in input! You can express it as; exp(1) = e**1
🔷 Only Round Brackets '(' and ')' are valid!
🌐 This calculator can only compute Real Numbers.
📖 This calculator has no memory! It does not remember any previous data input by the user.

❗ COMMON MISTAKES TO AVOID:
──────────────────────────────────────────────────────────────────────
❌ DON'T type: equation(2*x + 3 = 11)  # Missing quotes!
✅ DO type: equation("2*x + 3 = 11")

❌ DON'T type: equation("2x + 3 = 11")  # Missing * for multiply!
✅ DO type: equation("2*x + 3 = 11")

❌ DON'T type: equation("x^2 = 4")  # Use ** not ^!
✅ DO type: equation("x**2 = 4")

❌ DON'T type: expression("5,000 + 2,000")  # Commas or Space between a single number is invalid!
✅ DO type: expression("5000 + 2000")

🚀 READY TO START? Try typing one of these:
──────────────────────────────────────────────────────────────────────
equation("x + 5 = 10")
simplify("2*x + 3*x")
verify("2 + 2 = 4")
expression("(cos(pi)*sqrt(1024)*log(729, 3))")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.print_output(guide_text)
    def guide_functions(self):
        """Display complete list of available mathematical functions"""
        functions_text = """
╔══════════════════════════════════════════════════════════════════════╗
║ 🧮 MATH TERMINAL — COMPLETE REFERENCE                                ║
╚══════════════════════════════════════════════════════════════════════╝

📐 TRIGONOMETRIC FUNCTIONS
──────────────────────────────────────────────────────────────────────
 sin(x), cos(x), tan(x) --> Basic trigonometric functions
 sec(x), csc(x), cot(x) --> Reciprocal trigonometric functions
 asin(x), acos(x), atan(x) --> Inverse trigonometric functions
 asec(x), acsc(x), acot(x) --> Inverse reciprocal trigonometric functions
 atan2(y, x) --> Two-argument arctangent

🌊 HYPERBOLIC FUNCTIONS
──────────────────────────────────────────────────────────────────────
 sinh(x), cosh(x), tanh(x) --> Hyperbolic functions
 sech(x), csch(x), coth(x) --> Reciprocal hyperbolic functions
 asinh(x), acosh(x), atanh(x) --> Inverse hyperbolic functions
 asech(x), acsch(x), acoth(x) --> Inverse reciprocal hyperbolic functions

📊 LOGARITHMIC / EXPONENTIAL
──────────────────────────────────────────────────────────────────────
 log(x), ln(x) --> Natural logarithm
 log(x, b) --> Logarithm with base b
 exp(x) --> Exponential function
 sqrt(x), root(x, n) --> Square and nth roots
 Pow(x, y) --> Symbolic power
 LambertW(x) --> Lambert W function

🔧 ALGEBRAIC SIMPLIFICATION
──────────────────────────────────────────────────────────────────────
 simplify(expr) --> General simplification
 factor(expr) --> Factor expression
 expand(expr) --> Expand products and powers
 collect(expr, x) --> Collect terms in x
 apart(expr) --> Partial-fraction decomposition
 together(expr) --> Combine rational terms
 cancel(expr) --> Cancel common factors
 ratsimp(expr) --> Rational simplification
 radsimp(expr) --> Radical simplification
 powsimp(expr) --> Simplify powers
 powdenest(expr) --> Combine nested powers
 sqrtdenest(expr) --> Simplify nested radicals
 trigsimp(expr) --> Simplify trigonometric expressions
 fu(expr) --> Advanced trigonometric simplification
 combsimp(expr) --> Simplify combinatorial expressions
 logcombine(expr) --> Combine logarithms
 expand_log(expr) --> Expand logarithms
 expand_power_base(expr) --> Expand power bases
 expand_power_exp(expr) --> Expand power exponents
 nsimplify(expr) --> Find simpler exact forms
 posify(expr) --> Replace symbols with positive equivalents
 hypersimp(expr) --> Simplify hypergeometric terms

🧮 POLYNOMIAL FUNCTIONS
──────────────────────────────────────────────────────────────────────
 Poly(expr, x) --> Polynomial object
 degree(expr, x) --> Polynomial degree
 LC(poly), LM(poly), LT(poly) --> Leading coefficient, monomial, term
 factor_list(expr) --> Factorization with multiplicities
 sqf(expr), sqf_list(expr) --> Square-free factorization
 div(f, g), quo(f, g), rem(f, g) --> Polynomial division operations
 gcd(f, g), lcm(f, g) --> Polynomial GCD and LCM
 gcdex(f, g), half_gcdex(f, g) --> Extended GCD operations
 resultant(f, g, x) --> Polynomial resultant
 discriminant(f, x) --> Polynomial discriminant
 subresultants(f, g, x) --> Subresultant sequence
 groebner(F, x, y, ...) --> Gröbner basis
 roots(poly), nroots(poly) --> Exact and numerical roots
 ground_roots(poly) --> Ground-domain roots
 terms_gcd(expr) --> Remove common term factors
 degree_list(expr) --> Degrees of polynomial generators

🔥 CALCULUS
──────────────────────────────────────────────────────────────────────
 diff(expr, x) --> Differentiate
 Derivative(expr, x) --> Unevaluated derivative
 integrate(expr, x) --> Integrate
 Integral(expr, x) --> Unevaluated integral
 limit(expr, x, a) --> Limit
 Limit(expr, x, a) --> Unevaluated limit
 series(expr, x, x0, n) --> Taylor/Laurent series
 aseries(expr, x) --> Asymptotic series
 Order(expr, x) --> Big-O order term
 Sum(expr, (i, a, b)) --> Symbolic summation object
 Product(expr, (i, a, b)) --> Symbolic product object
 summation(expr, (i, a, b)) --> Compute a summation
 product(expr, (i, a, b)) --> Compute a product

🔢 NUMBER THEORY
──────────────────────────────────────────────────────────────────────
 factorial(n), factorial2(n) --> Factorials
 subfactorial(n) --> Subfactorial / derangement count
 binomial(n, k) --> Binomial coefficient
 bell(n), bernoulli(n) --> Bell and Bernoulli numbers
 catalan(n), euler(n) --> Catalan and Euler numbers
 genocchi(n), harmonic(n) --> Genocchi and harmonic numbers
 fibonacci(n), lucas(n) --> Fibonacci and Lucas numbers
 tribonacci(n) --> Tribonacci numbers
 isprime(n) --> Test primality
 prime(n) --> nth prime
 primepi(n) --> Prime-counting function
 nextprime(n), prevprime(n) --> Adjacent primes
 factorint(n) --> Prime factorization
 primefactors(n) --> Distinct prime factors
 divisors(n) --> Positive divisors
 proper_divisors(n) --> Proper divisors
 divisor_count(n) --> Number of divisors
 divisor_sigma(n) --> Sum of divisor powers
 totient(n) --> Euler's totient
 reduced_totient(n) --> Carmichael function
 mobius(n) --> Möbius function
 mod_inverse(a, m) --> Modular inverse
 crt(moduli, residues) --> Chinese remainder theorem
 multiplicity(p, n) --> Multiplicity of p in n
 perfect_power(n) --> Test perfect powers
 legendre(n, k) --> Legendre symbol
 continued_fraction(x) --> Continued fraction
 continued_fraction_periodic(...) --> Periodic continued fraction
 continued_fraction_iterator(x) --> Continued-fraction iterator
 continued_fraction_convergents() --> Continued-fraction convergents

🎲 COMBINATORICS
──────────────────────────────────────────────────────────────────────
 Permutation(n, k) --> Permutation object
 Cycle(...) --> Permutation cycle
 RisingFactorial(x, k), rf(x, k) --> Rising factorial
 FallingFactorial(x, k), ff(x, k) --> Falling factorial
 MultiFactorial(n, k) --> Multifactorial
 stirling(n, k) --> Stirling numbers
 partition(n) --> Integer partitions
 andre(n) --> André numbers
 motzkin(n) --> Motzkin numbers

📏 ROUNDING / MAGNITUDE
──────────────────────────────────────────────────────────────────────
 Abs(x), abs(x) --> Absolute value
 floor(x), ceiling(x) --> Floor and ceiling
 frac(x) --> Fractional part
 sign(x) --> Sign of expression
 Min(...), Max(...) --> Minimum and maximum

🧠 COMPLEX NUMBERS
──────────────────────────────────────────────────────────────────────
 re(x), im(x) --> Real and imaginary parts
 conjugate(x) --> Complex conjugate
 arg(x) --> Complex argument
 polar_lift(x) --> Lift to polar representation
 periodic_argument(x) --> Periodic complex argument
 principal_branch(x) --> Principal branch

🌟 GAMMA / RELATED FUNCTIONS
──────────────────────────────────────────────────────────────────────
 gamma(x), loggamma(x) --> Gamma and logarithmic Gamma
 digamma(x) --> Digamma function
 polygamma(n, x) --> Polygamma function
 trigamma(x) --> Trigamma function
 beta(x, y) --> Beta function

📡 ERROR / INTEGRAL SPECIAL FUNCTIONS
──────────────────────────────────────────────────────────────────────
 erf(x), erfc(x), erfi(x) --> Error functions
 erf2(a, b) --> Generalized error function
 Ei(x), li(x) --> Exponential and logarithmic integrals
 Si(x), Ci(x) --> Sine and cosine integrals
 Shi(x), Chi(x) --> Hyperbolic integrals
 fresnelc(x), fresnels(x) --> Fresnel integrals

📈 BESSEL FUNCTIONS
──────────────────────────────────────────────────────────────────────
 besselj(n, x), bessely(n, x) --> Bessel functions of first/second kind
 besseli(n, x), besselk(n, x) --> Modified Bessel functions
 hankel1(n, x), hankel2(n, x) --> Hankel functions

🌌 AIRY FUNCTIONS
──────────────────────────────────────────────────────────────────────
 airyai(x), airybi(x) --> Airy functions
 airyaiprime(x), airybiprime(x) --> Airy derivatives

📜 ORTHOGONAL POLYNOMIALS
──────────────────────────────────────────────────────────────────────
 legendre(n, x) --> Legendre polynomial
 assoc_legendre(n, m, x) --> Associated Legendre polynomial
 hermite(n, x) --> Hermite polynomial
 hermite_prob(n, x) --> Probabilists' Hermite polynomial
 laguerre(n, x) --> Laguerre polynomial
 assoc_laguerre(n, k, x) --> Associated Laguerre polynomial
 chebyshevt(n, x) --> Chebyshev polynomial of first kind
 chebyshevu(n, x) --> Chebyshev polynomial of second kind
 gegenbauer(n, a, x) --> Gegenbauer polynomial
 jacobi(n, a, b, x) --> Jacobi polynomial

🌀 HYPERGEOMETRIC FUNCTIONS
──────────────────────────────────────────────────────────────────────
 hyper(a_s, b_s, z) --> Generalized hypergeometric function
 hyperexpand(expr) --> Expand hypergeometric functions
 meijerg(...) --> Meijer G-function
 appellf1(a,b1,b2,c,x,y) --> Appell F1 function

🟣 ELLIPTIC FUNCTIONS
──────────────────────────────────────────────────────────────────────
 elliptic_k(m) --> Complete elliptic integral K
 elliptic_e(m) --> Complete elliptic integral E
 elliptic_f(phi, m) --> Incomplete elliptic integral F
 elliptic_e(phi, m) --> Incomplete elliptic integral E
 elliptic_pi(n, m) --> Complete elliptic integral Π
 jacobi_sn(u, m) --> Jacobi elliptic sine
 jacobi_cn(u, m) --> Jacobi elliptic cosine
 jacobi_dn(u, m) --> Jacobi elliptic delta function

📊 ZETA / POLYLOGARITHMIC
──────────────────────────────────────────────────────────────────────
 zeta(s) --> Riemann/Hurwitz zeta function
 dirichlet_eta(s) --> Dirichlet eta function
 polylog(s, z) --> Polylogarithm
 lerchphi(z, s, a) --> Lerch transcendent

🔷 SETS
──────────────────────────────────────────────────────────────────────
 FiniteSet(...) --> Finite set
 Interval(a, b) --> Interval
 Union(...) --> Union of sets
 Intersection(...) --> Intersection of sets
 Complement(A, B) --> Set difference
 ProductSet(A, B) --> Cartesian product
 EmptySet --> Empty set
 UniversalSet --> Universal set
 Contains(x, S) --> Set membership
 S.Integers, S.Naturals --> Integer and natural-number sets
 S.Naturals0 --> Naturals including zero
 S.Rationals, S.Reals --> Rational and real sets
 S.Complexes --> Complex-number set

🧠 LOGIC AND BOOLEAN ALGEBRA
──────────────────────────────────────────────────────────────────────
 And(...), Or(...) --> Logical AND / OR
 Not(...), Xor(...) --> Logical NOT / XOR
 Nand(...), Nor(...) --> NAND / NOR
 Implies(p, q) --> Logical implication
 Equivalent(p, q) --> Logical equivalence
 simplify_logic(expr) --> Simplify Boolean logic
 to_cnf(expr) --> Convert to conjunctive normal form
 to_dnf(expr) --> Convert to disjunctive normal form
 to_nnf(expr) --> Convert to negation normal form
 to_anf(expr) --> Convert to algebraic normal form

🍪 MATRICES / LINEAR ALGEBRA
──────────────────────────────────────────────────────────────────────
 Matrix(...), ImmutableMatrix(...) --> Matrix objects
 zeros(r, c), ones(r, c) --> Zero and one matrices
 eye(n), diag(...) --> Identity and diagonal matrices
 Matrix.det() --> Determinant
 Matrix.inv() --> Inverse
 Matrix.transpose() --> Transpose
 Matrix.trace() --> Trace
 Matrix.rank() --> Rank
 Matrix.charpoly() --> Characteristic polynomial
 Matrix.eigenvals() --> Eigenvalues
 Matrix.eigenvects() --> Eigenvalues and eigenvectors
 Matrix.rref() --> Reduced row-echelon form
 Matrix.nullspace() --> Null space
 Matrix.columnspace() --> Column space
 Matrix.rowspace() --> Row space
 Matrix.adjugate() --> Adjugate matrix
 Matrix.cofactor() --> Cofactor
 Matrix.cofactor_matrix() --> Cofactor matrix
 Matrix.minor() --> Matrix minor
 Matrix.norm() --> Matrix norm
 Matrix.dot() --> Matrix/vector dot product
 Matrix.cross() --> Matrix/vector cross product
 Matrix.LUdecomposition() --> LU decomposition
 Matrix.QRdecomposition() --> QR decomposition
 Matrix.cholesky() --> Cholesky decomposition
 Matrix.LDLdecomposition() --> LDL decomposition
 Matrix.diagonalize() --> Diagonalization
 Matrix.jordan_form() --> Jordan normal form

➡️ VECTOR CALCULUS
──────────────────────────────────────────────────────────────────────
 CoordSys3D(...) --> 3D coordinate system
 Point(...) --> Point/vector geometry
 Vector(...) --> Vector object
 Dot(...) --> Dot product
 Cross(...) --> Cross product
 Del(...) --> Del operator
 gradient(...) --> Gradient
 divergence(...) --> Divergence
 curl(...) --> Curl
 Laplacian(...) --> Laplacian
 directional_derivative(...) --> Directional derivative

📐 DIFFERENTIAL EQUATIONS
──────────────────────────────────────────────────────────────────────
 dsolve(...) --> Differential-equation solver
 classify_ode(...) --> Classify an ODE
 checkodesol(...) --> Check an ODE solution
 ode_order(...) --> ODE order
 constantsimp(...) --> Simplify integration constants
 pdsolve(...) --> Partial differential-equation solver
 classify_pde(...) --> Classify a PDE
 checkpdesol(...) --> Check a PDE solution

🎲 PROBABILITY / STATISTICS
──────────────────────────────────────────────────────────────────────
 RandomSymbol(...) --> Random symbolic variable
 RandomIndexedSymbol(...) --> Indexed random variable
 P(...) --> Probability
 E(...) --> Expected value
 variance(...) --> Variance
 covariance(...) --> Covariance
 density(...) --> Probability density
 sample(...) --> Random sample
 Normal(...) --> Normal distribution
 Exponential(...) --> Exponential distribution
 Poisson(...) --> Poisson distribution
 Binomial(...) --> Binomial distribution
 Geometric(...) --> Geometric distribution
 Gamma(...) --> Gamma distribution
 Beta(...) --> Beta distribution
 Uniform(...) --> Uniform distribution
 DiscreteUniform(...) --> Discrete uniform distribution
 ContinuousUniform(...) --> Continuous uniform distribution

📊 VECTOR / TENSOR / GEOMETRY
──────────────────────────────────────────────────────────────────────
 TensorProduct(...) --> Tensor product
 TensorIndexType(...) --> Tensor index type
 tensor_indices(...) --> Tensor indices
 tensorhead(...) --> Tensor head
 Point(...) --> Geometric point
 Line(...) --> Line
 Segment(...) --> Line segment
 Circle(...) --> Circle
 Triangle(...) --> Triangle
 Polygon(...) --> Polygon
 Plane(...) --> Plane

📌 CONSTANTS
──────────────────────────────────────────────────────────────────────
 pi --> π
 E --> Euler's number
 I --> Imaginary unit
 oo --> Infinity
 zoo --> Complex infinity
 nan --> Not-a-Number
 EulerGamma --> Euler-Mascheroni constant
 Catalan --> Catalan's constant
 GoldenRatio --> Golden ratio

🔣 SYMBOLS / RELATIONS
──────────────────────────────────────────────────────────────────────
 Symbol(...), symbols(...) --> Create symbols
 Dummy(...) --> Dummy symbol
 Wild(...) --> Wildcard symbol
 Integer(...) --> Exact integer
 Rational(...) --> Exact rational number
 Float(...) --> Floating-point number
 Eq(...) --> Equality relation
 Ne(...) --> Not-equal relation
 Lt(...), Le(...) --> Less-than relations
 Gt(...), Ge(...) --> Greater-than relations

🔄 NUMERICAL EVALUATION
──────────────────────────────────────────────────────────────────────
 N(expr) --> Numerical evaluation
 evalf(expr) --> Numerical evaluation with precision
 lambdify(args, expr) --> Convert expression to numerical function
 nsimplify(expr) --> Convert numerical form to exact form

🛠️EXPRESSION / SYMBOL TOOLS
──────────────────────────────────────────────────────────────────────
 subs(expr, ...) --> Substitute values/expressions
 xreplace(expr, ...) --> Structural replacement
 replace(expr, ...) --> Pattern-based replacement
 count_ops(expr) --> Count operations
 free_symbols --> Get symbols in expression
 has(expr, ...) --> Test for contained objects
 preorder_traversal(expr) --> Preorder expression traversal
 postorder_traversal(expr) --> Postorder expression traversal

💫 THANK YOU!
═══════════════════════════════════════════════════════════════════════════════
"""
        self.print_output(functions_text)
        
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
            self.print_output("ℹ️ This expression contains variables and cannot be evaluated to a single number.")
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
            # Check for guide(functions)      
        if command == "guide(functions)":     
            self.guide_functions()            
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
        self.print_output("💡 Type ' guide() ' to see how this calculator works.")
        self.print_output("")
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
