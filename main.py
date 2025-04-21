functions = {
    "sin"   : "cos",
    "cos"   : "-sin",
    "tan"   : "1/cos^2",
    "ctg"   : "-1/sin^2",
    "arcsin": "1/sqrt(1-x^2)",
    "arccos": "-1/sqrt(1-x^2)",
    "arctg" : "1/(1+x^2)",
    "arcctg": "-1/(1+x^2)",
    "ln"    : "1/x",
    "sqrt"  : "1/(2sqrt(x))"
}

priority = {
    '^': 4,
    '*': 3,
    '/': 3,
    '+': 2,
    '-': 2,
    '(': 1
}


class Node:
    __slots__ = ["left", "right", "operation"]

    def __init__(self, operation=None, left=None, right=None):
        self.left = left
        self.right = right
        self.operation = operation

    def __str__(self):
        return self.operation


class AST:
    def __init__(self):
        self.root = None

    def __reverse_notation(self, expression):
        res = []
        stack = []
        i = 0

        while i < len(expression):
            token = expression[i]

            if token == " ":
                i += 1
                continue

            if token.isdigit():
                num_str = token
                while i + 1 < len(expression) and expression[i + 1].isdigit():
                    i += 1
                    num_str += expression[i]
                res.append(num_str)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                top = stack.pop()
                while top != '(':
                    res.append(top)
                    top = stack.pop()
            else:
                if token.isalpha():
                    func_str = token
                    while i + 1 < len(expression) and expression[i + 1].isalpha():
                        i += 1
                        func_str += expression[i]
                    if func_str in functions:
                        i += 2
                        balance = 1
                        arg = []
                        while i < len(expression) and balance > 0:
                            if expression[i] == '(':
                                balance += 1
                            elif expression[i] == ')':
                                balance -= 1
                            if balance > 0:
                                arg.append(expression[i])
                            i += 1
                        i -= 1
                        arg_rpn = self.__reverse_notation(''.join(arg))
                        res.extend(arg_rpn)
                        res.append(func_str)
                    else:
                        res.append(func_str)
                else:
                    while stack and priority.get(stack[-1], 0) >= priority.get(token, 0):
                        res.append(stack.pop())
                    stack.append(token)
            i += 1

        while stack:
            res.append(stack.pop())

        return res

    def build_tree(self, expression):
        rpn = self.__reverse_notation(expression)
        stack = []

        for token in rpn:
            if token.isdigit() or (token.isalpha() and token not in functions):
                stack.append(token)
            elif token in functions:
                arg = stack.pop()
                vertex = Node(operation=token, left=arg)
                stack.append(vertex)
            else:
                right = stack.pop()
                left = stack.pop()
                vertex = Node(operation=token, left=left, right=right)
                stack.append(vertex)
        self.root = stack.pop() if stack else None

    def __inorder(self, node):
        if isinstance(node, str):
            print(node, end=' ')
            return

        if node.operation in functions:
            print(f"{node.operation}(", end='')
            self.__inorder(node.left)
            print(")", end=' ')
            return

        if node.left:
            if isinstance(node.left, Node) and priority.get(node.left.operation, 0) < priority.get(node.operation, 0):
                print("(", end='')
                self.__inorder(node.left)
                print(")", end=' ')
            else:
                self.__inorder(node.left)
        print(node.operation, end=' ')
        if node.right:
            if isinstance(node.right, Node) and priority.get(node.right.operation, 0) < priority.get(node.operation, 0):
                print("(", end='')
                self.__inorder(node.right)
                print(")", end=' ')
            else:
                self.__inorder(node.right)

    def dfs(self):
        self.__inorder(self.root)
        print()

    def __differentiate(self, node):
        if isinstance(node, str):
            if node == "x":
                return "1"
            elif node.isnumeric() or (node.isalpha() and node != "x" or any([func in node for func in functions])):
                return "0"
            else:
                return node

        if node.operation == "+":
            left = self.__differentiate(node.left)
            right = self.__differentiate(node.right)
            if left == "0":
                return right
            elif right == "0":
                return left
            return Node(operation="+", left=left, right=right) if left != right else Node(operation="*", left="2",
                                                                                          right=left)

        elif node.operation == "-":
            left = self.__differentiate(node.left)
            right = self.__differentiate(node.right)
            if right == "0":
                return left
            return Node(operation="-", left=left, right=right)

        elif node.operation == "*":
            dleft = self.__differentiate(node.left)
            dright = self.__differentiate(node.right)
            left_term = Node(operation="*", left=dleft, right=node.right) if dleft != "0" else "0"
            right_term = Node(operation="*", left=node.left, right=dright) if dright != "0" else "0"
            if left_term == "0":
                return right_term
            elif right_term == "0":
                return left_term
            else:
                return Node(operation="+", left=left_term, right=right_term)

        elif node.operation == "/":
            dleft = self.__differentiate(node.left)
            dright = self.__differentiate(node.right)
            numerator = Node(operation="-",
                             left=Node(operation="*", left=dleft, right=node.right),
                             right=Node(operation="*", left=node.left, right=dright))
            denominator = Node(operation="^", left=node.right, right="2")
            return Node(operation="/", left=numerator, right=denominator)

        elif node.operation == "^":
            base = node.left
            exponent = node.right
            if isinstance(base, str) and base == "x" and exponent.isdigit():
                new_exponent = str(int(exponent) - 1)
                return Node(operation="*", left=exponent,
                            right=Node(operation="^", left=base, right=new_exponent))
            elif base.isalpha() and exponent == "x":
                return Node(operation="*", left=f"ln({base})",
                            right=Node(operation="^", left=base, right=exponent))
            return "0"

        elif node.operation in functions:
            func_deriv = functions[node.operation]
            inner_deriv = self.__differentiate(node.left)
            if func_deriv == "cos":
                derivative = Node(operation="cos", left=node.left)
            elif func_deriv == "-sin":
                derivative = Node(operation="*", left="-1", right=Node(operation="sin", left=node.left))
            elif func_deriv == "1/x":
                derivative = Node(operation="/", left="1", right=node.left)
            elif func_deriv == "1/sqrt(1-x^2)":
                derivative = Node(operation="/", left="1",
                                  right=Node(operation="sqrt", left=Node(operation="-", left="1",
                                                                         right=Node(operation="^", left="x",
                                                                                    right="2"))))
            elif func_deriv == "1/(2sqrt(x))":
                derivative = Node(operation="/", left="1",
                                  right=Node(operation="*", left="2", right=Node(operation="sqrt", left="x")))
            else:
                derivative = Node(operation=func_deriv, left=node.left)
            return Node(operation="*", left=derivative, right=inner_deriv)

        return Node(operation=node.operation, left=node.left, right=node.right)

    def differentiate_tree(self):
        self.root = self.__differentiate(self.root)


def main():
    exp = "a^x"
    tree = AST()
    tree.build_tree(exp)
    tree.differentiate_tree()
    tree.dfs()


if __name__ == "__main__":
    main()
