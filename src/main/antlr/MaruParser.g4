/**
 * Parser for Maru DSL
 *
 */
parser grammar MaruParser;

@ header
{
    package it.unive.lisa.delve.maru.antlr;
}

options { tokenVocab = IMPLexer; }

file : classDefinition+;

classDefinition
    : CLASS COLON HTTP_SERVER LCURLY classBody RCURLY
    ;

classBody
    : methodDefinition? attributeDefinition?
    ;

methodDefinition
    : METHODS LBRACE methodBody RBRACE
    ;

methodBody
    : method+
    ;

method
    : CLASS LPAREN RPAREN ARROW HTTP_SERVER
    ;

attributeDefinition
    : ATTRIBUTES LBRACE (attribute)* RBRACE
    ;

attribute
    : STRING
    ;