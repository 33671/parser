import lark
from lark import Lark
from ast_trans import AstTransformer
from tokens import AstNode
import pprint
from interpreter import Interpreter
c_grammar = ""
with open("grammar.ebnf", "r", encoding="utf-8") as f:
    c_grammar = f.read()



# 3. 创建 Lark 解析器实例
try:
    c_parser = Lark(
        c_grammar, start="program", parser="lalr", transformer=AstTransformer()
    )
    # 使用 LALR 解析器，它通常更快并且适合大多数编程语言语法
    # 传入 transformer 实例，让 Lark 在解析后自动转换
except lark.exceptions.LarkError as e:
    print(f"语法定义错误:\n{e}")
    exit()

# 4. 提供一个 C 风格的代码示例
with open("code_example.code", "r", encoding="utf-8") as f:
    code_example = f.read()


# 5. 解析代码
try:
    print("--- 源代码 ---")
    print(code_example.strip())
    print("\n--- Lark 解析树 (原始) ---")
    # 不使用 Transformer 生成原始树进行比较
    raw_parser = Lark(c_grammar, start="program", parser="lalr")
    parse_tree = raw_parser.parse(code_example.strip())
    # print(parse_tree.pretty())  # pretty() 方法可以很好地可视化树
    with open("ast_example_raw.txt", "w", encoding="utf-8") as f:
        f.write(parse_tree.pretty())
    print("\n--- 转换后的 AST (使用 Transformer) ---")
    ast :AstNode = c_parser.parse(code_example)  # 使用带 Transformer 的解析器
    # 打印更结构化的 AST (这里是嵌套元组)
    
    with open("ast_example.txt", "w", encoding="utf-8") as f:
        pprint.pprint(ast, stream=f)
    pprint.pprint(ast)
    Interpreter().visit(ast)




except lark.exceptions.UnexpectedToken as e:
    print(f"\n语法错误！意外的 token: {e.token}")
    print(f"期望的 tokens: {e.expected}")
    print(f"发生在第 {e.line} 行, 第 {e.column} 列")
except lark.exceptions.UnexpectedCharacters as e:
    print(f"\n语法错误！意外的字符: '{e.char}'")
    print(f"发生在第 {e.line} 行, 第 {e.column} 列")
    print(f"期望的字符: {e.allowed}")


print("\n--- 解析完成 ---")
