/**
 * Lexer for Maru DSL
 *
 */

lexer grammar MaruLexer;

@ lexer :: header
{package it.unive.lisa.delve.maru.antlr;}

// =========================== KEYWORDS ===========================
METHODS
    : 'methods'
    ;

ATTRIBUTES
    : 'attributes'

// =========================== SYMBOLS ===========================
LPAREN
    : '('
    ;

RPAREN
    : ')'
    ;

LBRACE
    : '{'
    ;

RBRACE
    : '}'
    ;


// =========================== RULES ===========================
fragment LetterOrDigit
    : Letter
    | [0-9]
    ;

fragment Letter
    : [a-zA-Z$_]
    ;