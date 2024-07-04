from src.common.pycompiler import EOF
from src.parser.parsing_tools import ShiftReduceParser
from src.semantics.hulk_ast import Node

def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    pos = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
            pos.append((token.row,token.col))
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(rule is None for rule in attributes[1:]), 'There must be only synthesized attributes.'
            rule = attributes[0]

            if len(body):
                synthesized = [None] + stack[-len(body):]
                value = rule(None, synthesized)
                cur_pos = pos[-len(body)]
                if isinstance(value, Node):
                    value.row = cur_pos[0]
                    value.col = cur_pos[1]
                stack[-len(body):] = [value]
                pos[-len(body):] = [cur_pos]
            else:
                stack.append(rule(None, None))
                pos.append((None,None))
        else:
            raise Exception('Invalid action!!!')

    assert len(stack) == 1
    assert isinstance(next(tokens).token_type, EOF)
    return stack[0]