# 改版ESCODEGEN 暂时使用

# Copyright (C) 2012-2014 Yusuke Suzuki <utatane.tea@gmail.com>
# Copyright (C) 2015 Ingvar Stepanyan <me@rreverser.com>
# Copyright (C) 2014 Ivan Nikulin <ifaaan@gmail.com>
# Copyright (C) 2012-2013 Michael Ficarra <escodegen.copyright@michael.ficarra.me>
# Copyright (C) 2012-2013 Mathias Bynens <mathias@qiwi.be>
# Copyright (C) 2013 Irakli Gozalishvili <rfobic@gmail.com>
# Copyright (C) 2012 Robert Gust-Bardon <donate@robert.gust-bardon.org>
# Copyright (C) 2012 John Freeman <jfreeman08@gmail.com>
# Copyright (C) 2011-2012 Ariya Hidayat <ariya.hidayat@gmail.com>
# Copyright (C) 2012 Joost-Wim Boekesteijn <joost-wim@boekesteijn.nl>
# Copyright (C) 2012 Kris Kowal <kris.kowal@cixar.com>
# Copyright (C) 2012 Arpad Borsos <arpad.borsos@googlemail.com>
# Copyright (C) 2020 Apple Inc. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
import math
import esutils




class Syntax:
    AssignmentExpression = "AssignmentExpression"
    AssignmentPattern = "AssignmentPattern"
    ArrayExpression = "ArrayExpression"
    ArrayPattern = "ArrayPattern"
    ArrowFunctionExpression = "ArrowFunctionExpression"
    AwaitExpression = "AwaitExpression" # CAUTION = It"s deferred to ES7.
    BlockStatement = "BlockStatement"
    BinaryExpression = "BinaryExpression"
    BreakStatement = "BreakStatement"
    CallExpression = "CallExpression"
    CatchClause = "CatchClause"
    ChainExpression = "ChainExpression"
    ClassBody = "ClassBody"
    ClassDeclaration = "ClassDeclaration"
    ClassExpression = "ClassExpression"
    ComprehensionBlock = "ComprehensionBlock"  # CAUTION = It"s deferred to ES7.
    ComprehensionExpression = "ComprehensionExpression"  # CAUTION = It"s deferred to ES7.
    ConditionalExpression = "ConditionalExpression"
    ContinueStatement = "ContinueStatement"
    DebuggerStatement = "DebuggerStatement"
    DirectiveStatement = "DirectiveStatement"
    DoWhileStatement = "DoWhileStatement"
    EmptyStatement = "EmptyStatement"
    ExportAllDeclaration = "ExportAllDeclaration"
    ExportDefaultDeclaration = "ExportDefaultDeclaration"
    ExportNamedDeclaration = "ExportNamedDeclaration"
    ExportSpecifier = "ExportSpecifier"
    ExpressionStatement = "ExpressionStatement"
    ForStatement = "ForStatement"
    ForInStatement = "ForInStatement"
    ForOfStatement = "ForOfStatement"
    FunctionDeclaration = "FunctionDeclaration"
    FunctionExpression = "FunctionExpression"
    GeneratorExpression = "GeneratorExpression"  # CAUTION = It"s deferred to ES7.
    Identifier = "Identifier"
    IfStatement = "IfStatement"
    ImportExpression = "ImportExpression"
    ImportDeclaration = "ImportDeclaration"
    ImportDefaultSpecifier = "ImportDefaultSpecifier"
    ImportNamespaceSpecifier = "ImportNamespaceSpecifier"
    ImportSpecifier = "ImportSpecifier"
    Literal = "Literal"
    LabeledStatement = "LabeledStatement"
    LogicalExpression = "LogicalExpression"
    MemberExpression = "MemberExpression"
    MetaProperty = "MetaProperty"
    MethodDefinition = "MethodDefinition"
    ModuleSpecifier = "ModuleSpecifier"
    NewExpression = "NewExpression"
    ObjectExpression = "ObjectExpression"
    ObjectPattern = "ObjectPattern"
    PrivateIdentifier = "PrivateIdentifier"
    Program = "Program"
    Property = "Property"
    PropertyDefinition = "PropertyDefinition"
    RestElement = "RestElement"
    ReturnStatement = "ReturnStatement"
    SequenceExpression = "SequenceExpression"
    SpreadElement = "SpreadElement"
    Super = "Super"
    SwitchStatement = "SwitchStatement"
    SwitchCase = "SwitchCase"
    TaggedTemplateExpression = "TaggedTemplateExpression"
    TemplateElement = "TemplateElement"
    TemplateLiteral = "TemplateLiteral"
    ThisExpression = "ThisExpression"
    ThrowStatement = "ThrowStatement"
    TryStatement = "TryStatement"
    UnaryExpression = "UnaryExpression"
    UpdateExpression = "UpdateExpression"
    VariableDeclaration = "VariableDeclaration"
    VariableDeclarator = "VariableDeclarator"
    WhileStatement = "WhileStatement"
    WithStatement = "WithStatement"
    YieldExpression = "YieldExpression"


# Generation is done by generateExpression.
def isExpression(node):
    return hasattr(CodeGeneratorExpression, node.type)

# Generation is done by generateStatement.
def isStatement(node):
    return hasattr(CodeGeneratorStatement, node.type)

class Precedence:
    Sequence = 0
    Yield = 1
    Assignment = 1
    Conditional = 2
    ArrowFunction = 2
    Coalesce = 3
    LogicalOR = 4
    LogicalAND = 5
    BitwiseOR = 6
    BitwiseXOR = 7
    BitwiseAND = 8
    Equality = 9
    Relational = 10
    BitwiseSHIFT = 11
    Additive = 12
    Multiplicative = 13
    Exponentiation = 14
    Await = 15
    Unary = 15
    Postfix = 16
    OptionalChaining = 17
    Call = 18
    New = 19
    TaggedTemplate = 20
    Member = 21
    Primary = 22
    
BinaryPrecedence = {
    '??': Precedence.Coalesce,
    '||': Precedence.LogicalOR,
    '&&': Precedence.LogicalAND,
    '|': Precedence.BitwiseOR,
    '^': Precedence.BitwiseXOR,
    '&': Precedence.BitwiseAND,
    '==': Precedence.Equality,
    '!=': Precedence.Equality,
    '===': Precedence.Equality,
    '!==': Precedence.Equality,
    'is': Precedence.Equality,
    'isnt': Precedence.Equality,
    '<': Precedence.Relational,
    '>': Precedence.Relational,
    '<=': Precedence.Relational,
    '>=': Precedence.Relational,
    'in': Precedence.Relational,
    'instanceof': Precedence.Relational,
    '<<': Precedence.BitwiseSHIFT,
    '>>': Precedence.BitwiseSHIFT,
    '>>>': Precedence.BitwiseSHIFT,
    '+': Precedence.Additive,
    '-': Precedence.Additive,
    '*': Precedence.Multiplicative,
    '%': Precedence.Multiplicative,
    '/': Precedence.Multiplicative,
    '**': Precedence.Exponentiation
}

#Flags
F_ALLOW_IN = 1
F_ALLOW_CALL = 1 << 1
F_ALLOW_UNPARATH_NEW = 1 << 2
F_FUNC_BODY = 1 << 3
F_DIRECTIVE_CTX = 1 << 4
F_SEMICOLON_OPT = 1 << 5
F_FOUND_COALESCE = 1 << 6

#Expression flag sets
#NOTE: Flag order:
# F_ALLOW_IN
# F_ALLOW_CALL
# F_ALLOW_UNPARATH_NEW
E_FTT = F_ALLOW_CALL | F_ALLOW_UNPARATH_NEW
E_TTF = F_ALLOW_IN | F_ALLOW_CALL
E_TTT = F_ALLOW_IN | F_ALLOW_CALL | F_ALLOW_UNPARATH_NEW
E_TFF = F_ALLOW_IN
E_FFT = F_ALLOW_UNPARATH_NEW
E_TFT = F_ALLOW_IN | F_ALLOW_UNPARATH_NEW

#Statement flag sets
#NOTE: Flag order:
# F_ALLOW_IN
# F_FUNC_BODY
# F_DIRECTIVE_CTX
# F_SEMICOLON_OPT
S_TFFF = F_ALLOW_IN
S_TFFT = F_ALLOW_IN | F_SEMICOLON_OPT
S_FFFF = 0x00
S_TFTF = F_ALLOW_IN | F_DIRECTIVE_CTX
S_TTFF = F_ALLOW_IN | F_FUNC_BODY

class SimpleObj:

    _ignore = [
        'fromJsonString',
        'fromJsonFile',
        'fromDict',
        '_ignore',
        '_ignored'
    ]
    
    _ignored = False
        
    def __init__(self, obj=None):

        if self._ignored == False or SimpleObj == False:
            SimpleObj._ignored = True
            for k in dir(self):
                if k.startswith('__') and k.endswith('__'):
                    SimpleObj._ignore.append(k)

        if isinstance(obj, dict):
            for k,v in obj.items():
                if hasattr(self, k):
                    self[k] = v
                else:
                    setattr(self, k, v)
        elif isinstance(obj, SimpleObj):
            self = SimpleObj
    
    def __getattribute__(self, k):
        attribute = None
        try:
            attribute = object.__getattribute__(self, k)
        except:
            pass
        return attribute
        
    def __setitem__(self, k, v):
        setattr(self, k, v)
        
    def __getitem__(self, k):
        return getattr(self, k, None)
    
    def __iter__(self):
        return iter([i for i in self.__dir__() if not i in self._ignore])
        
    def __contains__(self, k):
        for attr in self.__iter__():
            if attr == k:
                return True
        return False
        
    def __len__(self):
        return len(list(self.__iter__()))
    
    def __repr__(self):
        string = '[\n'
        for k in self.__iter__():
            val = self[k]
            if isinstance(val, list):
                length = len(val)
                val = length > 0 and f'[... {length} items]' or '[]'
            elif isinstance(val, (dict, SimpleObj)):
                length = len(val)
                val = length > 0 and '{... ' + f'{length}' + ' items}' or '{}'
            elif isinstance(val, str):
                val = f'\"{val}\"'
            string += '    {' + f'{k}: ' + f'{val}' + '},\n'
        string = (string.endswith(',\n') and string[:-2] or string) + '\n]'
        return string
    
    @staticmethod
    def fromJsonString(string):
        import json as JSON
        return JSON.loads(string, object_hook=SimpleObj)
    
    @staticmethod
    def fromJsonFile(fp):
        import json as JSON
        with open(fp, 'rb') as f:
            return JSON.load(f, object_hook=SimpleObj)
    
    @staticmethod
    def fromDict(obj):
        import json as JSON
        return SimpleObj.fromJsonString(JSON.dumps(obj))
    
def getDefaultOptions():
    # default options
    return SimpleObj({
        'indent': None,
        'base': None,
        'parse': None,
        'comment': False,
        'format': SimpleObj({
            'indent': SimpleObj({
                'style': '    ',
                'base': 0,
                'adjustMultilineComment': False
            }),
            'newline': '\n',
            'space': ' ',
            'json': False,
            'renumber': False,
            'hexadecimal': False,
            'quotes': 'single',
            'escapeless': False,
            'compact': False,
            'parentheses': True,
            'semicolons': True,
            'safeConcatenation': False,
            'preserveBlankLines': False
        }),
        'moz': SimpleObj({
            'comprehensionExpressionStartsWithAssignment': False,
            'starlessGenerator': False
        }),
        'sourceMap': None,
        'sourceMapRoot': None,
        'sourceMapWithCode': False,
        'directive': False,
        'raw': True,
        'verbatim': None,
        'sourceCode': None
    })

def stringRepeat(string, num):
    result = ''
    num |= 0
    while num > 0:
        if (num & 1):
            result += string
        num >>= 1
        string += string
    return result

def hasLineTerminator(string):
    return bool(re.compile("[\r\n]").search(string))

def endsWithLineTerminator(string):
    length = len(string)
    return length and esutils.code.isLineTerminator(ord(string[length - 1]))

def updateDeeply(target, override):

    target = SimpleObj(target) if isinstance(target, dict) else target
    override = SimpleObj(override) if isinstance(override, dict) else override
 
    for key in override:

        val = SimpleObj(override[key]) if isinstance(override[key], dict) else override[key]
        
        if isinstance(val, (SimpleObj, dict)):
        
            if isinstance(target[key], (SimpleObj, dict)):
            
                target[key] = SimpleObj(target[key]) if isinstance(target[key], dict) else target[key]
                updateDeeply(target[key], val)
                
            else:
                target[key] = val
        else:
            target[key] = val
            
    return target

def to_base(n, _base):
    if _base == 10:
        return n
    
    result = 0
    counter = 0
    
    while n:
        r = n % _base
        n //= _base
        result += r * 10**counter
        counter+=1
    return str(result)

def splice(array, start, deleteCount, *items):
    head = array[:start]
    tail = array[start + (deleteCount or 0):]
    items = [i for i in items]
    array.clear()
    if deleteCount is None and not items:
        array.extend(head)
        return array
    array.extend(head + items + tail)
    return array

def generateNumber(value):

    if math.isnan(value):
        raise Exception('Numeric literal whose value is NaN')
    if value < 0 or (value == 0 and math.copysign(math.inf, value) < 0):
        raise Exception('Numeric literal whose value is negative')
    if  math.isinf(value):
        return json and 'null' or (renumber and '1e400' or '1e+400')
    
    result = str(value)
    if not renumber or len(result) < 3:
        return result
    
    point = result.index('.') if '.' in result else -1
    if not json and ord(result[0]) == 0x30 and point == 1:
        point = 0
        result = result[1:]
    temp = result
    result = result.replace('e+', 'e')
    exponent = 0
    pos = temp.index('e') if 'e' in temp else -1
    if (pos > 0):
        exponent = int(temp[pos + 1:])
        temp = temp[0:pos]
    if point >= 0:
        exponent -= len(temp) - point - 1
        temp = str(temp[0:point] + temp[point + 1])
    pos = 0
    while (len(temp) + pos - 1 >= len(temp)) and ord(temp[len(temp) + pos - 1]) == 0x30:
        pos -= 1
    if pos != 0:
        exponent -= pos
        temp = temp[0:pos]
    if exponent != 0:
        temp += 'e' + str(exponent)
    if temp == value:
        if len(temp) < len(result):
            result = temp
        else:
            temp = '0x' + to_base(value, 16)
            if hexadecimal and value > 1e12 and math.floor(value) == value and len(temp) < len(result):
                result = temp
    return result
    
# Generate valid RegExp expression.
# This function is based on https://github.com/Constellation/iv Engine

class RegExp(SimpleObj):
    
    def __init__(self, regex_str):
        
        _match = re.compile("\/(.*?)\/?([^/]*)$").search(regex_str)
        _pattern = _match.group(1)
        _flags = _match.group(2)
        self.re_pattern = _pattern
        self.re_flags = 0 | re.M if 'm' in _flags else 0 | re.I if 'i' in _flags else 0
        self.re_compiled = re.compile(_pattern, self.re_flags)
        self.regex = SimpleObj({
            'pattern': _pattern,
            'flags': _flags
        })
        self.raw = regex_str
        
    def toString(self):
        return '/' + self.regex.pattern + '/' + (self.regex.flags)
        
    @property
    def source(self):
        return self.regex.pattern
        
    @property
    def flags(self):
        return self.regex.flags

def escapeRegExpCharacter(ch, previousIsBackslash):
    if (ch & ~1) == 0x2028:
        return ('u' if previousIsBackslash else '\\u') + ('2028' if ch == 0x2028 else '2029')
    elif ch == 10 or ch == 13:
        return ('' if previousIsBackslash else '\\') + ('n' if ch == 10 else 'r')
    return chr(ch)

def generateRegExp(reg):

    # if '\\' in reg:
        # reg = fr'{reg}'
        # reg =  re.compile(r'\\').sub(r'\\\\', reg)
    
    reg = RegExp(reg)
    result = reg.toString() # Is regex pattern?
    
    if reg.source:
        # extract flag from toString result
        match = re.compile("\/([^/]*)$").search(result)
        if not bool(match):
            return result
        
        flags = match.group(1)
        result = ''
        
        characterInBrack = False
        previousIsBackslash = False
        
        i = 0
        iz = len(reg.source)
        for i in range(iz):
            ch = ord(reg.source[i])
            if not previousIsBackslash:
                if characterInBrack:
                    if ch == 93: # ]
                        characterInBrack = False
                else:
                    if ch == 47: # /
                        result += '\\'
                    elif ch == 91: # [
                        characterInBrack = True
                result += escapeRegExpCharacter(ch, previousIsBackslash)
                previousIsBackslash = ch == 92 # \
            else:
                # if new RegExp("\\\n') is provided, create /\n/
                result += escapeRegExpCharacter(ch, previousIsBackslash)
                # prevent like /\\[/]/
                previousIsBackslash = False
        return '/' + result + '/' + flags
    
    return result

def escapeAllowedCharacter(code, nextChar):

    if code == 0x08: # \b
        return '\\b'
        
    if code == 0x0c: # \f
        return '\\f'
        
    if code == 0x09: # \t
        return '\\t'
        
    _hex = to_base(code, 16).upper()
    if (json or code > 0xff):
        return '\\u' + '0000'[len(_hex):] + _hex
    elif code == 0x0000 and not esutils.code.isDecimalDigit(nextChar if not nextChar is None else 0x00):
        return '\\0'
    elif code == 0x000b: # \v
        return '\\x0b'
    else:
        return '\\x' + '00'[len(_hex):] + _hex

def escapeDisallowedCharacter(code):
    if code == 0x5c: # \
        return '\\\\'
    
    if code == 0x0a: # \n
        return '\\n'
        
    if code == 0x0d: # \r
        return '\\r'
        
    if code == 0x2028:
        return '\\u2028'
        
    if code == 0x2029:
        return '\\u2029'
    
    raise Exception('Incorrectly classified character')

def escapeDirective(string):
    
    quote = '"' if quotes == 'double' else '\''
    iz = len(string)
    i = 0
    while i < iz:
        code = ord(string[i])
        if code == 0x27: # '
            quote = '"'
            break
        elif code == 0x22: # "
            quote = '\''
            break
        elif code == 0x5c: # \
            i += 1
        i += 1
    
    return quote + string + quote

def escapeString(string):
    result = ''
    singleQuotes = 0
    doubleQuotes = 0
    
    for i in range(len(string)):
        code = ord(string[i])
        if code == 0x27: # "'"
            singleQuotes += 1
        elif code == 0x22: # '"'
            doubleQuotes += 1
        elif code == 0x2f and json: # '/'
            result += '\\'
        elif esutils.code.isLineTerminator(code) or code == 0x5c: # '\'
            result += escapeDisallowedCharacter(code)
            continue
        elif not esutils.code.isIdentifierPartES5(code) and (
                json and code < 0x20 or # 'SP'
                not json and not escapeless and (
                    code < 0x20 or # 'SP'
                    code > 0x7e # '~'
                )):
            nextChar = ord(string[i + 1]) if i + 1 < len(string) else None
            result += escapeAllowedCharacter(code, nextChar)
            continue
        result += chr(code)
        
    single = not (quotes == 'double' or (quotes == 'auto' and doubleQuotes < singleQuotes))
    quote = '\'' if single else '"'
    
    if not (singleQuotes if single else doubleQuotes):
        return quote + result + quote
        
    string = result
    result = quote
    
    for i in range(len(string)):
        code = ord(string[i])
        if (code == 0x27 and single) or (code == 0x22 and not single):
            result += chr(code)
    
    return result + quote

"""
 * flatten an array to a string, where the array can contain
 * either strings or nested arrays
"""
def flattenToString(arr):
    result = []
    for i in arr:
        result.append((flattenToString(i) if type(i) == list else i) or '')
    return ''.join(result)
"""
 * convert generated to a SourceNode when source maps are enabled.
"""
def toSourceNodeWhenNeeded(generated, node=None, toString=False):
    if not sourceMap:
        # with no source maps, generated is either an
        # array or a string.  if an array, flatten it.
        # if a string, just return it
        if isinstance(generated, list):
            return flattenToString(generated)
        else:
            return generated
    
    if node is None:
        if isinstance(generated, SourceNode):
            return generated
        else:
            node = SimpleObj()
            
    if node.loc is None:
        sn = SourceNode(None, None, sourceMap, generated, node.name or None)
    else:
        sn = SourceNode(node.loc.start.line, node.loc.start.column, (node.loc.source or None) if sourceMap == True else sourceMap, generated, node.name or None)
    return sn.toString() if toString else sn

def noEmptySpace():
    return space if space else ' '

def join(left, right):
    
    leftSource = toSourceNodeWhenNeeded(left, toString=True)
    if (len(leftSource) == 0):
        return [right]
    
    rightSource = toSourceNodeWhenNeeded(right, toString=True)
    if len(rightSource) == 0:
        return [left]
    
    leftCharCode = ord(leftSource[len(leftSource) - 1])
    rightCharCode = ord(rightSource[0])
    
    if ((leftCharCode == 0x2b or leftCharCode == 0x2d) and leftCharCode == rightCharCode or
        esutils.code.isIdentifierPartES5(leftCharCode) and esutils.code.isIdentifierPartES5(rightCharCode) or
        leftCharCode == 0x2f and rightCharCode == 0x69):
        return [left, noEmptySpace(), right]
    elif (esutils.code.isWhiteSpace(leftCharCode) or esutils.code.isLineTerminator(leftCharCode) or
            esutils.code.isWhiteSpace(rightCharCode) or esutils.code.isLineTerminator(rightCharCode)):
        return [left, right]
    return [left, space, right]
    
def addIndent(stmt):
    return [base, stmt]

def withIndent(func):
    global base
    previousBase = base
    base += indent
    func(base)
    base = previousBase

def calculateSpaces(string):
    i = len(string) - 1
    while i >= 0:
        if esutils.code.isLineTerminator(ord(string[i])):
            break
        i -= 1
    return (len(string) - 1) - i

def adjustMultilineComment(value, specialBase):
    global base
    
    array = re.compile('\r\n|[\r\n]').split(value)
    spaces = 1.7976931348623157e+308
    
    # first line doesn't have indentation
    i = 1
    while i < len(array):
        line = array[i]
        j = 0
        while j < len(line) and esutils.code.isWhiteSpace(ord(line[j])):
            j += 1
        if spaces > j:
            spaces = j
        i += 1
    
    if not specialBase is None:
        # pattern like
        # {
        #   var t = 20;  /*
        #                 * this is comment
        #                 */
        # }
        previousBase = base
        if array[1][spaces] == '*':
            specialBase += ' '
        base = specialBase
    else:
        if (spaces & 1):
            # /*
            #  *
            #  */
            # If spaces are odd number, above pattern is considered.
            # We waste 1 space.
            spaces -= 1
        previousBase = base
    
    i = 1
    while i < len(array):
        sn = toSourceNodeWhenNeeded(addIndent(array[i][spaces:]))
        array[i] = sn.join('') if sourceMap else sn
        i += 1
        
    base = previousBase
    
    return '\n'.join(array)
    
def generateComment(comment, specialBase=None):
    if comment.type == 'Line':
        if endsWithLineTerminator(comment.value):
            return '//' + comment.value
        else:
            result = '//' + comment.value
            if not preserveBlankLines:
                result += '\n'
            return result
    if extra.format.indent.adjustMultilineComment and bool(re.compile("[\n\r]").search(comment.value)):
        return adjustMultilineComment('/*' + comment.value + '*/', specialBase)
    return '/*' + comment.value + '*/';

def addComments(stmt, result):

    if stmt.leadingComments and len(stmt.leadingComments) > 0:

        save = result
        
        if preserveBlankLines:
            comment = stmt.leadingComments[0]
            result = []
        
            extRange = comment.extendedRange
            _range = comment.range
            
            prefix = sourceCode[extRange[0]:_range[0]]
            count = len(re.compile('\n').findall(prefix) or [])
            if count > 0:
                result.append(stringRepeat('\n', count))
                result.append(addIndent(generateComment(comment)))
            else:
                result.append(prefix)
                result.append(generateComment(comment))
            
            prevRange = _range
        
            i = 1
            while i < len(stmt.leadingComments):
                comment = stmt.leadingComments[i]
                _range = comment.range
                
                infix = sourceCode[prevRange[1]:_range[0]]
                count = len(re.compile('\n').findall(infix) or [])
                result.append(stringRepeat('\n', count))
                result.append(addIndent(generateComment(comment)))

                prevRange = _range
                i += 1

            suffix = sourceCode[_range[1], extRange[1]]
            count = len(re.compile('\n').findall(suffix) or [])
            result.append(stringRepeat('\n', count))
        else:
            comment = stmt.leadingComments[0]
            result = []
            if safeConcatenation and stmt.type == Syntax.Program and len(stmt.body) == 0:
                result.append('\n')
            result.append(generateComment(comment))
            if not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
                result.append('\n')
            
            for i in range(1, len(stmt.leadingComments)):
                comment = stmt.leadingComments[i]
                fragment = [generateComment(comment)]
                if not endsWithLineTerminator(toSourceNodeWhenNeeded(fragment, toString=True)):
                    fragment.append('\n')
                result.append(addIndent(fragment))
        
        result.append(addIndent(save))
    
    if stmt.trailingComments:
        
        if preserveBlankLines:
            comment = stmt.trailingComments[0]
            extRange = comment.extendedRange
            _range = comment.range
            
            prefix = sourceCode[extRange[0]:_range[0]]
            count = len(re.compile('\n').findall(prefix) or [])
            
            if count > 0:
                result.append(stringRepeat('\n', count))
                result.append(addIndent(generateComment(comment)))
            else:
                result.append(prefix)
                result.append(generateComment(comment))
        else:
            tailingToStatement = not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True))
            specialBase = stringRepeat(' ', calculateSpaces(toSourceNodeWhenNeeded([base, result, indent], toString=True)))
            length = len(stmt.trailingComments)
            for i in range(length):
                comment = stmt.trailingComments[i]
                if tailingToStatement:
                    # We assume target like following script
                    #
                    # var t = 20;  /**
                    #               * This is comment of t
                    #               */
                    if i == 0:
                        # first case
                        result = [result, indent]
                    else:
                        result = [result, specialBase]
                    result.append(generateComment(comment, specialBase))
                else:
                    result = [result, addIndent(generateComment(comment))]
                if i != length - 1 and not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
                    result = [result, '\n']

    return result
            
def generateBlankLines(start, end, result):
    newlineCount = 0
    
    for j in range(start, end):
        if sourceCode[j] == '\n':
            newlineCount += 1
    
    for j in range(1, newlineCount):
        result.append(newline)

def parenthesize(text, current, should):
    if current < should:
        return ['(', text, ')']
    return text

def generateVerbatimString(string):
    result = re.compile('\r\n|\n').split(string)
    for i in range(1, len(result)):
        result[i] = newline + base + result[i]
    return result

def generateVerbatim(expr, precedence):
    verbatim = expr[extra.verbatim]
    if isinstance(verbatim, str):
        result = parenthesize(generateVerbatimString(verbatim), Precedence.Sequence, precedence)
    else:
        # verbatim is object
        result = generateVerbatimString(verbatim.content)
        prec = verbatim.precedence if not verbatim.precedence is None else Precedence.Sequence
        result = parenthesize(result, prec, precedence)
        
    return toSourceNodeWhenNeeded(result, expr)

def generateIdentifier(node):
    return toSourceNodeWhenNeeded(node.name, node)

def generateAsyncPrefix(node, spaceRequired):
    return 'async' + (noEmptySpace() if spaceRequired else space) if node.isAsync else ''

def generateStarSuffix(node):
    isGenerator = node.generator and not extra.moz.starlessGenerator
    return '*' + space if isGenerator else ''

def generateMethodPrefix(prop):
    func = prop.value
    prefix = ''
    if func.isAsync:
        prefix += generateAsyncPrefix(func, not prop.computed)
    if func.generator:
        prefix += '*' if generateStarSuffix(func) else ''
    return prefix

def generateInternal(node):

    codegen = CodeGenerator()
    
    if isStatement(node):
        return codegen.generateStatement(node, S_TFFF)

    if isExpression(node):
        return codegen.generateExpression(node, Precedence.Sequence, E_TTT)

    raise Exception('Unknown node type: ' + node.type)

def generate(node, options=None):
    global base, indent, json, renumber, hexadecimal, quotes, escapeless, newline
    global space, parentheses, semicolons, safeConcatenation, directive
    global parse, sourceMap, sourceCode, preserveBlankLines, extra, SourceNode

    defaultOptions = getDefaultOptions()
    
    if not options is None:
        # Obsolete options
        #
        #   `options.indent`
        #   `options.base`
        #
        # Instead of them, we can use `option.format.indent`.
        if isinstance(options, dict):
            options = SimpleObj(options)

        if isinstance(options.indent, str):
            defaultOptions.format.indent.style = options.indent

        if isinstance(options.base, int):
            defaultOptions.format.indent.base = options.base
        options = updateDeeply(defaultOptions, options)

        indent = options.format.indent.style
        if isinstance(options.base, str):
            base = options.base
        else:
            base = stringRepeat(indent, options.format.indent.base)
    
    else:
        options = defaultOptions
        indent = options.format.indent.style
        base = stringRepeat(indent, options.format.indent.base)
    
    json = options.format.json
    renumber = options.format.renumber
    hexadecimal = False if json else options.format.hexadecimal
    quotes = 'double' if json else options.format.quotes
    escapeless = options.format.escapeless
    newline = options.format.newline
    space = options.format.space

    if options.format.compact:
        newline = space = indent = base = ''
        
    parentheses = options.format.parentheses
    semicolons = options.format.semicolons
    safeConcatenation = options.format.safeConcatenation
    directive = options.directive
    parse = None if json else options.parse
    sourceMap = options.sourceMap
    sourceCode = options.sourceCode
    
    preserveBlankLines = options.format.preserveBlankLines and not sourceCode is None

    extra = options

    if sourceMap:
        SourceNode = SimpleObj()
        
    if type(node) == dict:
        node = SimpleObj.fromDict(node)
    
    result = generateInternal(node)
    
    if not sourceMap:
        pair = SimpleObj({'code': result, 'map': None}) # result.toString()
        return pair if options.sourceMapWithCode else pair.code
    
    pair = result.toStringWithSourceMap(SimpleObj({
        'file': options.file,
        'sourceRoot': options.sourceMapRoot
    }))
    
    if options.sourceContent:
        pair.map.setSourceContent(options.sourceMap, options.sourceContent)
    
    if options.sourceMapWithCode:
        return pair

    return pair.map.toString()

# Statements.

class CodeGeneratorStatement:
    
    def BlockStatement(self, stmt, flags):
        _range = None
        content = None
        result = ['{', newline]
        that = self
        def fn(*args, **kwargs):
            nonlocal result
            if len(stmt.body) == 0 and preserveBlankLines:
                _range = stmt.range
                if _range[1] - _range[0] > 2:
                    content = sourceCode[_range[0] + 1:_range[1] - 1]
                    if content[0] == '\n':
                        result.clear()
                        result = ['{']

                    result.append(content)
         
            bodyFlags = S_TFFF
            if flags & F_FUNC_BODY:
                bodyFlags |= F_DIRECTIVE_CTX
            
            i = 0
            iz = len(stmt.body)
            while i < iz:
                if preserveBlankLines:
                    # handle spaces before the first line
                    if i == 0:
                        if stmt.body[0].leadingComments:
                            _range = stmt.body[0].leadingComments[0].extendedRange
                            content = sourceCode[_range[0]:_range[1]]
                            if content[0] == '\n':
                                result.clear()
                                result = ['{']

                        if not stmt.body[0].leadingComments:
                            generateBlankLines(stmt.range[0], stmt.body[0].range[0], result)

                    # handle spaces between lines
                    if i > 0:
                        if not stmt.body[i - 1].trailingComments and not stmt.body[i].leadingComments:
                            generateBlankLines(stmt.body[i - 1].range[1], stmt.body[i].range[0], result)

                if i == iz - 1:
                    bodyFlags |= F_SEMICOLON_OPT

                if stmt.body[i].leadingComments and preserveBlankLines:
                    fragment = that.generateStatement(stmt.body[i], bodyFlags)
                else:
                    fragment = addIndent(that.generateStatement(stmt.body[i], bodyFlags))

                result.append(fragment)
                
                if not endsWithLineTerminator(toSourceNodeWhenNeeded(fragment, toString=True)):

                    if (preserveBlankLines and i < iz - 1):
                        # don't add a new line if there are leading coments
                        # in the next statement
                        if not stmt.body[i + 1].leadingComments:
                            result.append(newline)
                    else:
                        result.append(newline)

                if preserveBlankLines:
                    # handle spaces after the last line
                    if i == iz - 1:
                        if not stmt.body[i].trailingComments:
                            generateBlankLines(stmt.body[i].range[1], stmt.range[1], result)
                
                i += 1
            
        withIndent(fn)
        result.append(addIndent('}'))
        return result
    
    def BreakStatement(self, stmt, flags):
        if stmt.label:
            return 'break ' + stmt.label.name + self.semicolon(flags)

        return 'break' + self.semicolon(flags)
    
    def ContinueStatement(self, stmt, flags):
        if stmt.label:
            return 'continue ' + stmt.label.name + self.semicolon(flags)

        return 'continue' + self.semicolon(flags)
    
    def ClassBody(self, stmt, flags):
        result = [ '{', newline]
        that = self
        
        def fn(indent, *args, **kwargs):
            nonlocal result
            iz = len(stmt.body)
            for i in range(iz):
                result.append(indent)
                result.append(that.generateExpression(stmt.body[i], Precedence.Sequence, E_TTT))
                if i + 1 < iz:
                    result.append(newline)
                    
        withIndent(fn)

        if not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
            result.append(newline)

        result.append(base)
        result.append('}')
        return result
    
    def ClassDeclaration(self, stmt, flags):
        result  = ['class']
        if stmt.id:
            result = join(result, self.generateExpression(stmt.id, Precedence.Sequence, E_TTT))
        
        if stmt.superClass:
            fragment = join('extends', self.generateExpression(stmt.superClass, Precedence.Unary, E_TTT))
            result = join(result, fragment)

        result.append(space)
        result.append(self.generateStatement(stmt.body, S_TFFT))
        return result
    
    def DirectiveStatement(self, stmt, flags):
        if extra.raw and stmt.raw:
            return stmt.raw + self.semicolon(flags)

        return escapeDirective(stmt.directive) + self.semicolon(flags)
        
    def DoWhileStatement(self, stmt, flags):
        # Because `do 42 while (cond)` is Syntax Error. We need semicolon.
        result = join('do', self.maybeBlock(stmt.body, S_TFFF))
        result = self.maybeBlockSuffix(stmt.body, result)
        return join(result, [
            'while' + space + '(',
            self.generateExpression(stmt.test, Precedence.Sequence, E_TTT),
            ')' + self.semicolon(flags)
        ])
        
    def CatchClause(self, stmt, flags):
        result = []
        that = self
        
        def fn(*args, **kwargs):
            nonlocal result
            if stmt.param:
                result = [
                    'catch' + space + '(',
                    that.generateExpression(stmt.param, Precedence.Sequence, E_TTT),
                    ')'
                ]
                if stmt.guard:
                    guard = that.generateExpression(stmt.guard, Precedence.Sequence, E_TTT)
                    splice(result, 2, 0, ' if ', guard)
            else:
                result = ['catch']

        withIndent(fn)
        result.append(self.maybeBlock(stmt.body, S_TFFF))
        return result
        
    def DebuggerStatement(self, stmt, flags):
        return 'debugger' + self.semicolon(flags)
        
    def EmptyStatement(self, stmt, flags):
        return ';'
        
    def ExportDefaultDeclaration(self, stmt, flags):
        result = [ 'export' ]
        
        bodyFlags = S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF
        
        # export default HoistableDeclaration[Default]
        # export default AssignmentExpression[In] 
        result = join(result, 'default')
        if isStatement(stmt.declaration):
            result = join(result, self.generateStatement(stmt.declaration, bodyFlags))
        else:
            result = join(result, self.generateExpression(stmt.declaration, Precedence.Assignment, E_TTT) + self.semicolon(flags))

        return result
        
    def ExportNamedDeclaration(self, stmt, flags):
        result = [ 'export' ]
        that = self
        
        bodyFlags = S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF
        
        # export VariableStatement
        # export Declaration[Default]
        if stmt.declaration:
            return join(result, self.generateStatement(stmt.declaration, bodyFlags))
        
        # export ExportClause[NoReference] FromClause 
        # export ExportClause 
        if stmt.specifiers:
            if len(stmt.specifiers) == 0:
                result = join(result, '{' + space + '}')
            else:
                result = join(result, '{')
                
                def fn(indent, *args, **kwargs):
                    nonlocal result
                    result.append(newline)
                    iz = len(stmt.specifiers)
                    for i in range(iz):
                        result.append(indent)
                        result.append(that.generateExpression(stmt.specifiers[i], Precedence.Sequence, E_TTT))
                        if i + 1 < iz:
                            result.append(',' + newline)

                withIndent(fn)
                
                if not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
                    result.append(newline)

                result.append(base + '}')

            if stmt.source:
                result = join(result, [
                    'from' + space,
                    # ModuleSpecifier
                    self.generateExpression(stmt.source, Precedence.Sequence, E_TTT),
                    self.semicolon(flags)
                ])
            else:
                result.append(self.semicolon(flags))

        return result
        
    def ExportAllDeclaration(self, stmt, flags):
        # export * FromClause 
        return [
            'export' + space,
            '*' + space,
            'from' + space,
            # ModuleSpecifier
            self.generateExpression(stmt.source, Precedence.Sequence, E_TTT),
            self.semicolon(flags)
        ]
        
    def ExpressionStatement(self, stmt, flags):

        def isClassPrefixed(fragment):
            if fragment[0:5] != 'class':
                return False
            code = ord(fragment[5])
            return (code == 0x7b or # '{'
                    esutils.code.isWhiteSpace(code) or
                    esutils.code.isLineTerminator(code))
            
        def isFunctionPrefixed(fragment):
            if fragment[0:8] != 'function':
                return False
            code = ord(fragment[8])
            return (code == 0x28 or # '('
                    esutils.code.isWhiteSpace(code) or
                    code == 0x2a or # '*'
                    esutils.code.isLineTerminator(code))

        def isAsyncPrefixed(fragment):
            
            if fragment[0:5] != 'async':
                return False

            if not esutils.code.isWhiteSpace(ord(fragment[5])):
                return False
            
            i = 6
            iz = len(fragment)
            while i < iz:
                if not esutils.code.isWhiteSpace(ord(fragment[i])):
                    break
                i += 1

            if i == iz:
                return False

            if fragment[i:i + 8] != 'function':
                return False

            code = ord(fragment[i + 8])
            return (code == 0x28 or # '('
                    esutils.code.isWhiteSpace(code) or
                    code == 0x2A or # '*'
                    esutils.code.isLineTerminator(code))
                    
        result = [self.generateExpression(stmt.expression, Precedence.Sequence, E_TTT)]
        # 12.4 '{', 'function', 'class' is not allowed in this position.
        # wrap expression with parentheses
        fragment = toSourceNodeWhenNeeded(result, toString=True)
        if (ord(fragment[0]) == 0x7B or # '{'
                # ObjectExpression
                isClassPrefixed(fragment) or
                isFunctionPrefixed(fragment) or
                isAsyncPrefixed(fragment) or
                (directive and (flags & F_DIRECTIVE_CTX) and stmt.expression.type == Syntax.Literal and isinstance(stmt.expression.value, str))
            ):
            result = ['(', result, ')' + self.semicolon(flags)]
        else:
            result.append(self.semicolon(flags))

        return result

    def ImportDeclaration(self, stmt, flags):
        # ES6: 15.2.1 valid import declarations:
        #     - import ImportClause FromClause 
        #     - import ModuleSpecifier 
        that = self

        # If no ImportClause is present,
        # this should be `import ModuleSpecifier` so skip `from`
        # ModuleSpecifier is StringLiteral.
        if len(stmt.specifiers) == 0:
            # import ModuleSpecifier 
            return [
                'import',
                space,
                # ModuleSpecifier
                self.generateExpression(stmt.source, Precedence.Sequence, E_TTT),
                self.semicolon(flags)
            ]
            
        # import ImportClause FromClause 
        result = [
            'import'
        ]
        cursor = 0
        
        # ImportedBinding
        if stmt.specifiers[cursor].type == Syntax.ImportDefaultSpecifier:
            result = join(result, [
                self.generateExpression(stmt.specifiers[cursor], Precedence.Sequence, E_TTT)
            ])
            cursor += 1
            
        if stmt.specifiers[cursor]:
            if cursor != 0:
                result.append(',')

            if stmt.specifiers[cursor].type == Syntax.ImportNamespaceSpecifier:
                # NameSpaceImport
                result = join(result, [
                    space,
                    self.generateExpression(stmt.specifiers[cursor], Precedence.Sequence, E_TTT)
                ])
            else:
                # NamedImports
                result.append(space + '{')

                if len(stmt.specifiers) - cursor == 1:
                    # import { ... } from "..."
                    result.append(space)
                    result.append(self.generateExpression(stmt.specifiers[cursor], Precedence.Sequence, E_TTT))
                    result.append(space + '}' + space)
                else:
                    # import {
                    #    ...,
                    #    ...,
                    # } from "..."
                    def fn(indent, *args, **kwargs):
                        nonlocal result
                        result.append(newline)
                        i = cursor
                        iz = len(stmt.specifiers)
                        while i < iz:
                            result.append(indent)
                            result.append(that.generateExpression(stmt.specifiers[i], Precedence.Sequence, E_TTT))
                            if i + 1 < iz:
                                result.append(',' + newline)
                            i += 1
                                
                    withIndent(fn)
                    if not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
                        result.append(newline)
                    result.append(base + '}' + space)

        result = join(result, [
            'from' + space,
            # ModuleSpecifier
            self.generateExpression(stmt.source, Precedence.Sequence, E_TTT),
            self.semicolon(flags)
        ])
        return result
        
    def VariableDeclarator(self, stmt, flags):
        itemFlags = E_TTT if (flags & F_ALLOW_IN) else E_FTT
        if stmt.init:
            return [
                self.generateExpression(stmt.id, Precedence.Assignment, itemFlags),
                space,
                '=',
                space,
                self.generateExpression(stmt.init, Precedence.Assignment, itemFlags)
            ]

        return self.generatePattern(stmt.id, Precedence.Assignment, itemFlags)
        
    def VariableDeclaration(self, stmt, flags):
        # VariableDeclarator is typed as Statement,
        # but joined with comma (not LineTerminator).
        # So if comment is attached to target node, we should specialize.
        result = [stmt.kind]
        that = self
        bodyFlags = S_TFFF if (flags & F_ALLOW_IN) else S_FFFF

        def fnBlock(*args, **kwargs):
            nonlocal result
            node = stmt.declarations[0]
            if extra.comment and node.leadingComments:
                result.append('\n')
                result.append(addIndent(that.generateStatement(node, bodyFlags)))
            else:
                result.append(noEmptySpace())
                result.append(that.generateStatement(node, bodyFlags))

            for i in range(1, len(stmt.declarations)):
                node = stmt.declarations[i]
                if extra.comment and node.leadingComments:
                    result.append(',' + newline)
                    result.append(addIndent(that.generateStatement(node, bodyFlags)))
                else:
                    result.append(',' + space)
                    result.append(that.generateStatement(node, bodyFlags))

        if len(stmt.declarations) > 1:
            withIndent(fnBlock)
        else:
            fnBlock()

        result.append(self.semicolon(flags))

        return result
        
    def ThrowStatement(self, stmt, flags):
        return [join(
            'throw',
            self.generateExpression(stmt.argument, Precedence.Sequence, E_TTT)
        ), self.semicolon(flags)]
        
    def TryStatement(self, stmt, flags):

        result = ['try', self.maybeBlock(stmt.block, S_TFFF)]
        result = self.maybeBlockSuffix(stmt.block, result)

        if stmt.handlers:
            # old interface
            iz = len(stmt.handlers)
            for i in range(iz):
                result = join(result, self.generateStatement(stmt.handlers[i], S_TFFF))
                if stmt.finalizer or (i + 1 != iz):
                    result = self.maybeBlockSuffix(stmt.handlers[i].body, result)
        else:
            guardedHandlers = stmt.guardedHandlers or []
            
            iz = len(guardedHandlers)
            for i in range(iz):
                result = join(result, self.generateStatement(guardedHandlers[i], S_TFFF))
                if stmt.finalizer or (i + 1 != iz):
                    result = self.maybeBlockSuffix(guardedHandlers[i].body, result)

            # new interface
            if stmt.handler:
                if isinstance(stmt.handler, list):
                    iz = len(stmt.handler)
                    for i in range(iz):
                        result = join(result, self.generateStatement(stmt.handler[i], S_TFFF))
                        if stmt.finalizer or (i + 1 != iz):
                            result = self.maybeBlockSuffix(stmt.handler[i].body, result)
                else:
                    result = join(result, self.generateStatement(stmt.handler, S_TFFF))
                    if stmt.finalizer:
                        result = self.maybeBlockSuffix(stmt.handler.body, result)

        if stmt.finalizer:
            result = join(result, ['finally', self.maybeBlock(stmt.finalizer, S_TFFF)])

        return result
        
    def SwitchStatement(self, stmt, flags):
        result = []
        that = self
        def fn(*args, **kwargs):
            nonlocal result
            result.extend([
                'switch' + space + '(',
                that.generateExpression(stmt.discriminant, Precedence.Sequence, E_TTT),
                ')' + space + '{' + newline
            ])
        withIndent(fn)
        if stmt.cases:
            bodyFlags = S_TFFF
            iz = len(stmt.cases)
            for i in range(iz):
                if i == (iz - 1):
                    bodyFlags |= F_SEMICOLON_OPT
                fragment = addIndent(self.generateStatement(stmt.cases[i], bodyFlags))
                result.append(fragment)
                if not endsWithLineTerminator(toSourceNodeWhenNeeded(fragment, toString=True)):
                    result.append(newline)

        result.append(addIndent('}'))
        return result
        
    def SwitchCase(self, stmt, flags):
        result = []
        that = self
        def fn(*args, **kwargs):
            nonlocal result
            
            if stmt.test:
                result.extend([
                    join('case', that.generateExpression(stmt.test, Precedence.Sequence, E_TTT)),
                    ':'
                ])
            else:
                result.extend(['default:'])

            i = 0
            iz = len(stmt.consequent)
            if iz and stmt.consequent[0].type == Syntax.BlockStatement:
                fragment = that.maybeBlock(stmt.consequent[0], S_TFFF)
                result.append(fragment)
                i = 1

            if i != iz and not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
                result.append(newline)

            bodyFlags = S_TFFF
            while i < iz:
                if i == iz - 1 and (flags & F_SEMICOLON_OPT):
                    bodyFlags |= F_SEMICOLON_OPT

                fragment = addIndent(that.generateStatement(stmt.consequent[i], bodyFlags))
                result.append(fragment)
                if i + 1 != iz and not endsWithLineTerminator(toSourceNodeWhenNeeded(fragment, toString=True)):
                    result.append(newline)
                i += 1

        withIndent(fn)
        return result

    def IfStatement(self, stmt, flags):
        result = []
        that = self
        def fn(*args, **kwargs):
            nonlocal result
            
            result.extend([
                'if' + space + '(',
                that.generateExpression(stmt.test, Precedence.Sequence, E_TTT),
                ')'
            ])
        withIndent(fn)
        semicolonOptional = flags & F_SEMICOLON_OPT
        bodyFlags = S_TFFF
        if semicolonOptional:
            bodyFlags |= F_SEMICOLON_OPT

        if stmt.alternate:
            result.append(self.maybeBlock(stmt.consequent, S_TFFF))
            result = self.maybeBlockSuffix(stmt.consequent, result)
            if (stmt.alternate.type == Syntax.IfStatement):
                result = join(result, ['else ', self.generateStatement(stmt.alternate, bodyFlags)])
            else:
                result = join(result, join('else', self.maybeBlock(stmt.alternate, bodyFlags)))

        else:
            result.append(self.maybeBlock(stmt.consequent, bodyFlags))

        return result

    def ForStatement(self, stmt, flags):
        that = self
        result = []
        def fn(*args, **kwargs):
            nonlocal result
            result.extend(['for' + space + '('])
            if stmt.init:
                if stmt.init.type == Syntax.VariableDeclaration:
                    result.append(that.generateStatement(stmt.init, S_FFFF))
                else:
                    # F_ALLOW_IN becomes false.
                    result.append(that.generateExpression(stmt.init, Precedence.Sequence, E_FTT))
                    result.append(';')
            else:
                result.append(';')

            if stmt.test:
                result.append(space)
                result.append(that.generateExpression(stmt.test, Precedence.Sequence, E_TTT))
                result.append(';')
            else:
                result.append(';')

            if stmt.update:
                result.append(space)
                result.append(that.generateExpression(stmt.update, Precedence.Sequence, E_TTT))
                result.append(')')
            else:
                result.append(')')

        withIndent(fn)

        result.append(self.maybeBlock(stmt.body, S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF))
        return result

    def ForInStatement(self, stmt, flags):
        return self.generateIterationForStatement('in', stmt, S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF)

    def ForOfStatement(self, stmt, flags):
        return self.generateIterationForStatement('of', stmt, S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF)

    def LabeledStatement(self, stmt, flags):
        return [stmt.label.name + ':', self.maybeBlock(stmt.body, S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF)]

    def Program(self, stmt, flags):
        iz = len(stmt.body)
        result = ['\n' if (safeConcatenation and iz > 0) else '']
        bodyFlags = S_TFTF
        for i in range(iz):
            if not safeConcatenation and i == iz - 1:
                bodyFlags |= F_SEMICOLON_OPT

            if preserveBlankLines:
                # handle spaces before the first line
                if i == 0:
                    if not stmt.body[0].leadingComments:
                        generateBlankLines(stmt.range[0], stmt.body[i].range[0], result)

                # handle spaces between lines
                if i > 0:
                    if not stmt.body[i - 1].trailingComments and not stmt.body[i].leadingComments:
                        generateBlankLines(stmt.body[i - 1].range[1], stmt.body[i].range[0], result)

            fragment = addIndent(self.generateStatement(stmt.body[i], bodyFlags))
            result.append(fragment)
            if i + 1 < iz and not endsWithLineTerminator(toSourceNodeWhenNeeded(fragment, toString=True)):
                if preserveBlankLines:
                    if not stmt.body[i + 1].leadingComments:
                        result.append(newline)
                else:
                    result.append(newline)

            if preserveBlankLines:
                # handle spaces after the last line
                if (i == iz - 1):
                    if not stmt.body[i].trailingComments:
                        generateBlankLines(stmt.body[i].range[1], stmt.range[1], result)
        
        return result

    def FunctionDeclaration(self, stmt, flags):
        return [
            generateAsyncPrefix(stmt, True),
            'function',
            generateStarSuffix(stmt) or noEmptySpace(),
            generateIdentifier(stmt.id) if stmt.id else '',
            self.generateFunctionBody(stmt)
        ]

    def ReturnStatement(self, stmt, flags):
        if stmt.argument:
            return [join(
                'return',
                self.generateExpression(stmt.argument, Precedence.Sequence, E_TTT)
            ), self.semicolon(flags)]

        return ['return' + self.semicolon(flags)]

    def WhileStatement(self, stmt, flags):
        result = []
        that = self
        def fn(*args, **kwargs):
            nonlocal result
            result.extend([
                'while' + space + '(',
                that.generateExpression(stmt.test, Precedence.Sequence, E_TTT),
                ')'
            ])

        withIndent(fn)
        result.append(self.maybeBlock(stmt.body, S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF))
        return result

    def WithStatement(self, stmt, flags):
        result = []
        that = self
        def fn(*args, **kwargs):
            nonlocal result
            result.extend([
                'with' + space + '(',
                that.generateExpression(stmt.test, Precedence.Sequence, E_TTT),
                ')'
            ])
        withIndent(fn)
        result.append(self.maybeBlock(stmt.body, S_TFFT if (flags & F_SEMICOLON_OPT) else S_TFFF))
        return result

# Expressions.

class CodeGeneratorExpression:

    def SequenceExpression(self, expr, precedence, flags):
        if Precedence.Sequence < precedence:
            flags |= F_ALLOW_IN

        result = []
        iz = len(expr.expressions)
        for i in range(iz):
            result.append(self.generateExpression(expr.expressions[i], Precedence.Assignment, flags))
            if i + 1 < iz:
                result.append(',' + space)

        return parenthesize(result, Precedence.Sequence, precedence)
    
    def AssignmentExpression(self, expr, precedence, flags):
        return self.generateAssignment(expr.left, expr.right, expr.operator, precedence, flags)
    
    def ArrowFunctionExpression(self, expr, precedence, flags):
        return parenthesize(self.generateFunctionBody(expr), Precedence.ArrowFunction, precedence)
    
    def ConditionalExpression(self, expr, precedence, flags):
        if Precedence.Conditional < precedence:
            flags |= F_ALLOW_IN
        return parenthesize(
            [
                self.generateExpression(expr.test, Precedence.Coalesce, flags),
                space + '?' + space,
                self.generateExpression(expr.consequent, Precedence.Assignment, flags),
                space + ':' + space,
                self.generateExpression(expr.alternate, Precedence.Assignment, flags)
            ],
            Precedence.Conditional,
            precedence
        )
    
    def LogicalExpression(self, expr, precedence, flags):
        if expr.operator == '??':
            flags |= F_FOUND_COALESCE

        return self.BinaryExpression(expr, precedence, flags)
    
    def BinaryExpression(self, expr, precedence, flags):
        
        result = []
        
        currentPrecedence = BinaryPrecedence[expr.operator]
        leftPrecedence = Precedence.Postfix if expr.operator == '**' else currentPrecedence
        rightPrecedence = currentPrecedence if expr.operator == '**' else currentPrecedence + 1

        if currentPrecedence < precedence:
            flags |= F_ALLOW_IN

        fragment = self.generateExpression(expr.left, leftPrecedence, flags)

        leftSource = fragment # TODO fragment.toString()

        if (ord(leftSource[len(leftSource) - 1]) == 0x2f and # '/'
                esutils.code.isIdentifierPartES5(ord(expr.operator[0]))):
            result = [fragment, noEmptySpace(), expr.operator]
        else:
            result = join(fragment, expr.operator)

        fragment = self.generateExpression(expr.right, rightPrecedence, flags)

        if (expr.operator == '/' and fragment[0] == '/' or # TODO fragment.toString()
                expr.operator[-1] == '<' and fragment[0:3] == '!--'): # TODO fragment.toString()
            # If '/' concats with '/' or `<` concats with `!--`, it is interpreted as comment start
            result.append(noEmptySpace())
            result.append(fragment)
        else:
            result = join(result, fragment)

        if expr.operator == 'in' and not (flags & F_ALLOW_IN):
            return ['(', result, ')']

        if (expr.operator == '||' or expr.operator == '&&') and (flags & F_FOUND_COALESCE):
            return ['(', result, ')']

        return parenthesize(result, currentPrecedence, precedence)
    
    def CallExpression(self, expr, precedence, flags):
        
        # F_ALLOW_UNPARATH_NEW becomes false.
        result = [self.generateExpression(expr.callee, Precedence.Call, E_TTF)]

        if expr.optional:
            result.append('?.')

        result.append('(')

        iz = len(expr.arguments)
        for i in range(iz):
            result.append(self.generateExpression(expr.arguments[i], Precedence.Assignment, E_TTT))
            if i + 1 < iz:
                result.append(',' + space)
        result.append(')')

        if not (flags & F_ALLOW_CALL):
            return ['(', result, ')']

        return parenthesize(result, Precedence.Call, precedence)
    
    def ChainExpression(self, expr, precedence, flags):
        if Precedence.OptionalChaining < precedence:
            flags |= F_ALLOW_CALL
        
        result = self.generateExpression(expr.expression, Precedence.OptionalChaining, flags)

        return parenthesize(result, Precedence.OptionalChaining, precedence)
    
    def NewExpression(self, expr, precedence, flags):

        length = len(expr.arguments)
        
        # F_ALLOW_CALL becomes false.
        # F_ALLOW_UNPARATH_NEW may become false.
        itemFlags = E_TFT if (flags & F_ALLOW_UNPARATH_NEW and not parentheses and length == 0) else E_TFF

        result = join(
            'new',
            self.generateExpression(expr.callee, Precedence.New, itemFlags)
        )

        if not (flags & F_ALLOW_UNPARATH_NEW) or parentheses or length > 0:
            result.append('(')
            iz = length
            for i in range(iz):
                result.append(self.generateExpression(expr.arguments[i], Precedence.Assignment, E_TTT))
                if i + 1 < iz:
                    result.append(',' + space)
            result.append(')')

        return parenthesize(result, Precedence.New, precedence)
    
    def MemberExpression(self, expr, precedence, flags):
        # F_ALLOW_UNPARATH_NEW becomes false.
        result = [self.generateExpression(expr.object, Precedence.Call, E_TTF if (flags & F_ALLOW_CALL) else E_TFF)]

        if expr.computed:
            if expr.optional:
                result.append('?.')
            result.append('[')
            result.append(self.generateExpression(expr.property, Precedence.Sequence, E_TTT if (flags & F_ALLOW_CALL) else E_TFT))
            result.append(']')
        else:
            if not expr.optional and (expr.object.type == Syntax.Literal) and isinstance(expr.object.value, (int, float)):
                fragment = toSourceNodeWhenNeeded(result, toString=True)
                # When the following conditions are all true,
                #   1. No floating point
                #   2. Don't have exponents
                #   3. The last character is a decimal digit
                #   4. Not hexadecimal OR octal number literal
                # we should add a floating point.
                if (not '.' in fragment and
                        not bool(re.compile("[eExX]").search(fragment)) and
                        esutils.code.isDecimalDigit(ord(fragment[len(fragment) - 1])) and
                        not (len(fragment) >= 2 and ord(fragment[0]) == 48)  # '0'
                    ):
                    result.append(' ')

            result.append('?.' if expr.optional else '.')
            result.append(generateIdentifier(expr.property))

        return parenthesize(result, Precedence.Member, precedence)
    
    def MetaProperty(self, expr, precedence, flags):
        result = []
        result.append(expr.meta if isinstance(expr.meta, str) else generateIdentifier(expr.meta))
        result.append('.')
        result.append(expr.property if isinstance(expr.property, str) else generateIdentifier(expr.property))
        return parenthesize(result, Precedence.Member, precedence)
    
    def UnaryExpression(self, expr, precedence, flags):
        fragment = self.generateExpression(expr.argument, Precedence.Unary, E_TTT)

        if space == '':
            result = join(expr.operator, fragment)
        else:
            result = [expr.operator]
            if len(expr.operator) > 2:
                # delete, void, typeof
                # get `typeof []`, not `typeof[]`
                result = join(result, fragment)
            else:
                # Prevent inserting spaces between operator and argument if it is unnecessary
                # like, `!cond`
                leftSource = toSourceNodeWhenNeeded(result, toString=True)
                leftCharCode = ord(leftSource[len(leftSource) - 1])
                rightCharCode = ord(fragment[0]) # TODO: fragment.toString()

                if (((  leftCharCode == 0x2B or # '+' 
                        leftCharCode == 0x2D # '-'
                        ) and leftCharCode == rightCharCode) or
                        (esutils.code.isIdentifierPartES5(leftCharCode) and esutils.code.isIdentifierPartES5(rightCharCode))
                    ):
                    result.append(noEmptySpace())
                    result.append(fragment)
                else:
                    result.append(fragment)

        return parenthesize(result, Precedence.Unary, precedence)
    
    def YieldExpression(self, expr, precedence, flags):
        if expr.delegate:
            result = 'yield*'
        else:
            result = 'yield'

        if expr.argument:
            result = join(
                result,
                self.generateExpression(expr.argument, Precedence.Yield, E_TTT)
            )

        return parenthesize(result, Precedence.Yield, precedence)
    
    def AwaitExpression(self, expr, precedence, flags):
        result = join(
            'await*' if expr.all else 'await',
            self.generateExpression(expr.argument, Precedence.Await, E_TTT)
        )
        return parenthesize(result, Precedence.Await, precedence)
    
    def UpdateExpression(self, expr, precedence, flags):
        if expr.prefix:
            return parenthesize(
                [
                    expr.operator,
                    self.generateExpression(expr.argument, Precedence.Unary, E_TTT)
                ],
                Precedence.Unary,
                precedence
            )

        return parenthesize(
            [
                self.generateExpression(expr.argument, Precedence.Postfix, E_TTT),
                expr.operator
            ],
            Precedence.Postfix,
            precedence
        )
    
    def FunctionExpression(self, expr, precedence, flags):
        result = [
            generateAsyncPrefix(expr, True),
            'function'
        ]
        if expr.id:
            result.append(generateStarSuffix(expr) or noEmptySpace())
            result.append(generateIdentifier(expr.id))
        else:
            result.append(generateStarSuffix(expr) or space)

        result.append(self.generateFunctionBody(expr))
        return result
    
    def ArrayPattern(self, expr, precedence, flags):
        return self.ArrayExpression(expr, precedence, flags, True)
    
    def ArrayExpression(self, expr, precedence, flags, isPattern=False):
        that = self
        if not len(expr.elements):
            return '[]'

        multiline = False if isPattern else len(expr.elements) > 1
        result = ['[', newline if multiline else '']
        def fn(indent, *args, **kwargs):
            nonlocal result
            iz = len(expr.elements)
            for i in range(iz):
                if not expr.elements[i]:
                    if multiline:
                        result.append(indent)
                    if i + 1 == iz:
                        result.append(',')
                else:
                    result.append(indent if multiline else '')
                    result.append(that.generateExpression(expr.elements[i], Precedence.Assignment, E_TTT))
                if i + 1 < iz:
                    result.append(',' + (newline if multiline else space))

        withIndent(fn)
        
        if multiline and not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
            result.append(newline)

        result.append(base if multiline else '')
        result.append(']')
        return result
    
    def RestElement(self, expr, precedence, flags):
        return '...' + self.generatePattern(expr.argument, precedence, flags)
    
    def ClassExpression(self, expr, precedence, flags):
        result = ['class']
        if expr.id:
            result = join(result, self.generateExpression(expr.id, Precedence.Sequence, E_TTT))

        if expr.superClass:
            fragment = join('extends', self.generateExpression(expr.superClass, Precedence.Unary, E_TTT))
            result = join(result, fragment)

        result.append(space)
        result.append(self.generateStatement(expr.body, S_TFFT))
        return result
    
    def MethodDefinition(self, expr, precedence, flags):

        if expr.static:
            result = ['static' + space]
        else:
            result = []

        if expr.kind == 'get' or expr.kind == 'set':
            fragment = [
                join(expr.kind, self.generatePropertyKey(expr.key, expr.computed)),
                self.generateFunctionBody(expr.value)
            ]
        else:
            fragment = [
                generateMethodPrefix(expr),
                self.generatePropertyKey(expr.key, expr.computed),
                self.generateFunctionBody(expr.value)
            ]

        return join(result, fragment)
    
    def Property(self, expr, precedence, flags):
        if expr.kind == 'get' or expr.kind == 'set':
            return [
                expr.kind, noEmptySpace(),
                self.generatePropertyKey(expr.key, expr.computed),
                self.generateFunctionBody(expr.value)
            ]

        if expr.shorthand:
            if expr.value.type == "AssignmentPattern":
                return self.AssignmentPattern(expr.value, Precedence.Sequence, E_TTT)
            return self.generatePropertyKey(expr.key, expr.computed)

        if expr.method:
            return [
                generateMethodPrefix(expr),
                self.generatePropertyKey(expr.key, expr.computed),
                self.generateFunctionBody(expr.value)
            ]

        return [
            self.generatePropertyKey(expr.key, expr.computed),
            ':' + space,
            self.generateExpression(expr.value, Precedence.Assignment, E_TTT)
        ]
    
    def ObjectExpression(self, expr, precedence, flags):
        that = self
        fragment = ''
        result = []
        if not len(expr.properties):
            return '{}'

        multiline = len(expr.properties) > 1

        def fn(*args, **kwargs):
            nonlocal fragment
            fragment = that.generateExpression(expr.properties[0], Precedence.Sequence, E_TTT)
        
        withIndent(fn)

        if not multiline:
            # issues 4
            # Do not transform from
            #   dejavu.Class.declare({
            #       method2: function () {}
            #   })
            # to
            #   dejavu.Class.declare({method2: function ():
            #       }})
            if not hasLineTerminator(toSourceNodeWhenNeeded(fragment, toString=True)):
                return [ '{', space, fragment, space, '}' ]

        def fn2(indent, *args, **kwargs):
            nonlocal result
            
            result.extend([ '{', newline, indent, fragment ])

            if multiline:
                result.append(',' + newline)
                iz = len(expr.properties)
                for i in range(1, iz):
                    result.append(indent)
                    result.append(that.generateExpression(expr.properties[i], Precedence.Sequence, E_TTT))
                    if i + 1 < iz:
                        result.append(',' + newline)

        withIndent(fn2)

        if not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
            result.append(newline)

        result.append(base)
        result.append('}')
        return result
    
    def AssignmentPattern(self, expr, precedence, flags):
        return self.generateAssignment(expr.left, expr.right, '=', precedence, flags)
    
    def ObjectPattern(self, expr, precedence, flags):
        that = self
        
        if not len(expr.properties):
            return '{}'

        multiline = False
        if len(expr.properties) == 1:
            property = expr.properties[0]
            if property.type == Syntax.Property and property.value.type != Syntax.Identifier:
                multiline = True
        else:
            iz = len(expr.properties)
            for i in range(iz):
                property = expr.properties[i]
                if (property.type == Syntax.Property and not property.shorthand):
                    multiline = True
                    break

        result = ['{', newline if multiline else '' ]

        def fn(indent, *args, **kwargs):
            nonlocal result
            iz = len(expr.properties)
            for i in range(iz):
                result.append(indent if multiline else '')
                result.append(that.generateExpression(expr.properties[i], Precedence.Sequence, E_TTT))
                if i + 1 < iz:
                    result.append(',' + (newline if multiline else space))

        withIndent(fn)

        if multiline and not endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True)):
            result.append(newline)

        result.append(base if multiline else '')
        result.append('}')
        return result
    
    def ThisExpression(self, expr, precedence, flags):
        return 'this'
    
    def Super(self, expr, precedence, flags):
        return 'super'
    
    def Identifier(self, expr, precedence, flags):
        return generateIdentifier(expr)
    
    def ImportDefaultSpecifier(self, expr, precedence, flags):
        return generateIdentifier(expr.id or expr.local)
    
    def ImportNamespaceSpecifier(self, expr, precedence, flags):
        result = ['*']
        _id = expr.id or expr.local
        if _id:
            result.append(space + 'as' + noEmptySpace() + generateIdentifier(_id))

        return result
    
    def ImportSpecifier(self, expr, precedence, flags):
        imported = expr.imported
        result = [ imported.name ]
        local = expr.local
        if local and local.name != imported.name:
            result.append(noEmptySpace() + 'as' + noEmptySpace() + generateIdentifier(local))

        return result
    
    def ExportSpecifier(self, expr, precedence, flags):
        local = expr.local
        result = [ local.name ]
        exported = expr.exported
        if exported and exported.name != local.name:
            result.append(noEmptySpace() + 'as' + noEmptySpace() + generateIdentifier(exported))

        return result
    
    def Literal(self, expr, precedence, flags):
        if hasattr(expr, 'raw') and parse and extra.raw:
            try:
                raw = parse(expr.raw).body[0].expression
                if raw.type == Syntax.Literal:
                    if raw.value == expr.value:
                        return expr.raw
            except:
                # not use raw property
                pass


        if expr.regex:
            return '/' + expr.regex.pattern + '/' + expr.regex.flags

        """
        # TODO: Approach needed?

        if (typeof expr.value == 'bigint'):
            return expr.value.toString() + 'n'

        # `expr.value` can be null if `expr.bigint` exists. We need to check
        # `expr.bigint` first.
        if (expr.bigint):
            return expr.bigint + 'n'

        """

        if expr.value is None:
            return 'null'
        if type(expr.value) == str:
            return repr(expr.value)

        if type(expr.value) in (int, float):
            return generateNumber(expr.value)

        if type(expr.value) == bool:
            return 'true' if expr.value else 'false'
        return generateRegExp(expr.value)
    
    def GeneratorExpression(self, expr, precedence, flags):
        return self.ComprehensionExpression(expr, precedence, flags)
    
    def ComprehensionExpression(self, expr, precedence, flags):
        # GeneratorExpression should be parenthesized with (...), ComprehensionExpression with [...]
        # Due to https://bugzilla.mozilla.org/show_bug.cgi?id=883468 position of expr.body can differ in Spidermonkey and ES6

        that = self
        result =  ['('] if (expr.type == Syntax.GeneratorExpression) else ['[']
        fragment = None
        
        if extra.moz.comprehensionExpressionStartsWithAssignment:
            fragment = self.generateExpression(expr.body, Precedence.Assignment, E_TTT)
            result.append(fragment)

        if expr.blocks:
            def fn(*args, **kwargs):
                nonlocal result, fragment
                for i in range(len(expr.blocks)):
                    fragment = that.generateExpression(expr.blocks[i], Precedence.Sequence, E_TTT)
                    if i > 0 or extra.moz.comprehensionExpressionStartsWithAssignment:
                        result = join(result, fragment)
                    else:
                        result.append(fragment)

            withIndent(fn)

        if expr.filter:
            result = join(result, 'if' + space)
            fragment = self.generateExpression(expr.filter, Precedence.Sequence, E_TTT)
            result = join(result, [ '(', fragment, ')' ])

        if not extra.moz.comprehensionExpressionStartsWithAssignment:
            fragment = self.generateExpression(expr.body, Precedence.Assignment, E_TTT)
            result = join(result, fragment)

        result.append(')' if (expr.type == Syntax.GeneratorExpression) else ']')
        return result
    
    def ComprehensionBlock(self, expr, precedence, flags):
        if expr.left.type == Syntax.VariableDeclaration:
            fragment = [
                expr.left.kind, noEmptySpace(),
                self.generateStatement(expr.left.declarations[0], S_FFFF)
            ]
        else:
            fragment = self.generateExpression(expr.left, Precedence.Call, E_TTT)


        fragment = join(fragment, 'of' if expr.of else 'in')
        fragment = join(fragment, self.generateExpression(expr.right, Precedence.Sequence, E_TTT))

        return [ 'for' + space + '(', fragment, ')' ]
    
    def SpreadElement(self, expr, precedence, flags):
        return [
            '...',
            self.generateExpression(expr.argument, Precedence.Assignment, E_TTT)
        ]
    
    def TaggedTemplateExpression(self, expr, precedence, flags):
        itemFlags = E_TTF
        if not (flags & F_ALLOW_CALL):
            itemFlags = E_TFF

        result = [
            self.generateExpression(expr.tag, Precedence.Call, itemFlags),
            self.generateExpression(expr.quasi, Precedence.Primary, E_FFT)
        ]
        return parenthesize(result, Precedence.TaggedTemplate, precedence)
    
    def TemplateElement(self, expr, precedence, flags):
        # Don't use "cooked". Since tagged template can use raw template
        # representation. So if we do so, it breaks the script semantics.
        return expr.value.raw
    
    def TemplateLiteral(self, expr, precedence, flags):
        result = [ '`' ]
        iz = len(expr.quasis)
        for i in range(iz):
            result.append(self.generateExpression(expr.quasis[i], Precedence.Primary, E_TTT))
            if i + 1 < iz:
                result.append('${' + space)
                result.append(self.generateExpression(expr.expressions[i], Precedence.Sequence, E_TTT))
                result.append(space + '}')

        result.append('`')
        return result
    
    def ModuleSpecifier(self, expr, precedence, flags):
        return self.Literal(expr, precedence, flags)
    
    def ImportExpression(self, expr, precedence, flags):
        return parenthesize([
            'import(',
            (expr.source and self.generateExpression(expr.source, Precedence.Assignment, E_TTT) or ''),
            ')'
        ], Precedence.Call, precedence)

class CodeGenerator(CodeGeneratorStatement, CodeGeneratorExpression):
    
    def maybeBlock(self, stmt, flags):
        that = self
        result = []
        noLeadingComment = not extra.comment or not stmt.leadingComments

        if stmt.type == Syntax.BlockStatement and noLeadingComment:
            return [space, self.generateStatement(stmt, flags)]

        if stmt.type == Syntax.EmptyStatement and noLeadingComment:
            return ';'

        def fn(*args, **kwargs):
            nonlocal result
            result.extend([
                newline,
                addIndent(that.generateStatement(stmt, flags))
            ])
        withIndent(fn)

        return result
    
    def maybeBlockSuffix(self, stmt, result):

        ends = endsWithLineTerminator(toSourceNodeWhenNeeded(result, toString=True))

        if stmt.type == Syntax.BlockStatement and (not extra.comment or not stmt.leadingComments) and not ends:
            return [result, space]

        if ends:
            return [result, base]

        return [result, newline, base]
    
    def generatePattern(self, node, precedence, flags):
        if node.type == Syntax.Identifier:
            return generateIdentifier(node)

        return self.generateExpression(node, precedence, flags)
    
    def generateFunctionParams(self, node):

        hasDefault = False

        if (node.type == Syntax.ArrowFunctionExpression and
                not node.rest and (not node.defaults or len(node.defaults) == 0) and
                len(node.params) == 1 and node.params[0].type == Syntax.Identifier):
            # arg => { } case
            result = [generateAsyncPrefix(node, True), generateIdentifier(node.params[0])]
        else:
            result = [generateAsyncPrefix(node, False)] if (node.type == Syntax.ArrowFunctionExpression) else []
            result.append('(')
            if node.defaults:
                hasDefault = True
            
            iz = len(node.params)
            for i in range(iz):
                if hasDefault and node.defaults[i]:
                    # Handle default values.
                    result.append(self.generateAssignment(node.params[i], node.defaults[i], '=', Precedence.Assignment, E_TTT))
                else:
                    result.append(self.generatePattern(node.params[i], Precedence.Assignment, E_TTT))
                if i + 1 < iz:
                    result.append(',' + space)
            if node.rest:
                if len(node.params):
                    result.append(',' + space)

                result.append('...')
                result.append(generateIdentifier(node.rest))

            result.append(')')

        return result
    
    def generateFunctionBody(self, node):

        result = self.generateFunctionParams(node)

        if node.type == Syntax.ArrowFunctionExpression:
            result.append(space)
            result.append('=>')

        if node.expression:
            result.append(space)
            expr = self.generateExpression(node.body, Precedence.Assignment, E_TTT)
            if expr[0] == '{': # TODO: expr.toString().charAt(0)
                expr = ['(', expr, ')']
            result.append(expr)
        else:
            result.append(self.maybeBlock(node.body, S_TTFF))

        return result
    
    def generateIterationForStatement(self, operator, stmt, flags):
        that = self
        result = ['for' + (noEmptySpace() + 'await' if stmt.allowAwait else '') + space + '('] # TODO: stmt.await => stmt.allowAwait ?
        
        def fn(*args, **kwargs):
            nonlocal result
            if stmt.left.type == Syntax.VariableDeclaration:
                def fn2(*args, **kwargs):
                    nonlocal result
                    result.append(stmt.left.kind + noEmptySpace())
                    result.append(that.generateStatement(stmt.left.declarations[0], S_FFFF))
                withIndent(fn2)
            else:
                result.append(that.generateExpression(stmt.left, Precedence.Call, E_TTT))

            result = join(result, operator)
            result = [join(
                result,
                that.generateExpression(stmt.right, Precedence.Assignment, E_TTT)
            ), ')']

        withIndent(fn)
        result.append(self.maybeBlock(stmt.body, flags))
        return result
    
    def generatePropertyKey(self, expr, computed):
        result = []

        if computed:
            result.append('[')

        result.append(self.generateExpression(expr, Precedence.Assignment, E_TTT))

        if computed:
            result.append(']')

        return result
    
    def generateAssignment(self, left, right, operator, precedence, flags):
        if Precedence.Assignment < precedence:
            flags |= F_ALLOW_IN

        return parenthesize(
            [
                self.generateExpression(left, Precedence.Call, flags),
                space + operator + space,
                self.generateExpression(right, Precedence.Assignment, flags)
            ],
            Precedence.Assignment,
            precedence
        )
    
    def semicolon(self, flags):
        if not semicolons and (flags & F_SEMICOLON_OPT):
            return ''

        return ';'
    
    def generateExpression(self, expr, precedence, flags):

        if extra.verbatim and hasattr(expr, extra.verbatim):
            return generateVerbatim(expr, precedence)

        result = getattr(self, expr.type or Syntax.Property)(expr, precedence, flags)
        
        if extra.comment:
            result = addComments(expr, result)

        return toSourceNodeWhenNeeded(result, expr)
    
    def generateStatement(self, stmt, flags):
        
        result = getattr(self, stmt.type)(stmt, flags)

        # Attach comments
        
        if extra.comment:
            result = addComments(stmt, result)
        
        fragment = toSourceNodeWhenNeeded(result, toString=True)
        if stmt.type == Syntax.Program and (not safeConcatenation) and newline == '' and (fragment[len(fragment) - 1] == '\n'):
            result = toSourceNodeWhenNeeded(result).replaceRight('\s+$', '') if sourceMap else re.compile('\s+$').sub('', fragment)
        
        return toSourceNodeWhenNeeded(result, stmt)



FORMAT_MINIFY = getDefaultOptions().format
FORMAT_MINIFY.indent.style = ''
FORMAT_MINIFY.indent.base = 0
FORMAT_MINIFY.renumber = True
FORMAT_MINIFY.hexadecimal = True
FORMAT_MINIFY.quotes = 'auto'
FORMAT_MINIFY.escapeless = True
FORMAT_MINIFY.compact = True
FORMAT_MINIFY.parentheses = True
FORMAT_MINIFY.semicolons = True

FORMAT_DEFAULTS = getDefaultOptions().format



