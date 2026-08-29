# BanglaCode v1.0 — Final Test Report

## Summary

Total Test Cases: 10  
Passed: 10  
Failed: 0  
Pass Rate: 100%

## Test Results

| Test ID | Test Case | Expected | Actual | Status |
|---|---|---|---|---|
| T01 | Variable declaration and print | 10 | 10 | PASS |
| T02 | Arithmetic expression | 20 | 20 | PASS |
| T03 | Operator precedence with parentheses | 30 | 30 | PASS |
| T04 | If-else statement | Pass | Pass | PASS |
| T05 | While loop | 1 | 2 | 3 | 1 | 2 | 3 | PASS |
| T06 | Boolean literal print | shotto | shotto | PASS |
| T07 | Undeclared variable error | Undeclared variable | Undeclared variable | PASS |
| T08 | Duplicate declaration error | Duplicate declaration | Duplicate declaration | PASS |
| T09 | Type mismatch error | Type mismatch | Type mismatch | PASS |
| T10 | Missing semicolon syntax error | Expected ';' | Expected ';' | PASS |

## Coverage

The test suite covers variable declaration, arithmetic expressions, operator precedence,
if-else control flow, while loops, boolean values, undeclared variables, duplicate
declarations, type mismatch detection, and syntax error detection.

## Conclusion

BanglaCode v1.0 successfully passed the prepared functional and error-handling test suite.
The tested compiler pipeline includes lexical analysis, parsing, AST construction,
semantic analysis, IR/TAC generation, C code generation, and GCC executable generation.
