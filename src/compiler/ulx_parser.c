#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* 
 * ULX Parser - Converte código ULX em código intermediário
 * Parte do compilador CLX
 */

typedef enum {
    TOKEN_FUNC,
    TOKEN_MAIN,
    TOKEN_PRINT,
    TOKEN_VAR,
    TOKEN_IF,
    TOKEN_WHILE,
    TOKEN_IDENTIFIER,
    TOKEN_NUMBER,
    TOKEN_STRING,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_SEMICOLON,
    TOKEN_COMMA,
    TOKEN_ASSIGN,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MULTIPLY,
    TOKEN_DIVIDE,
    TOKEN_EOF,
    TOKEN_UNKNOWN
} TokenType;

typedef struct {
    TokenType type;
    char value[256];
} Token;

typedef struct {
    char* source;
    int position;
    int length;
} Lexer;

Lexer* lexer_create(const char* source) {
    Lexer* lexer = (Lexer*)malloc(sizeof(Lexer));
    lexer->source = (char*)malloc(strlen(source) + 1);
    strcpy(lexer->source, source);
    lexer->position = 0;
    lexer->length = strlen(source);
    return lexer;
}

void lexer_skip_whitespace(Lexer* lexer) {
    while (lexer->position < lexer->length && isspace(lexer->source[lexer->position])) {
        lexer->position++;
    }
}

Token lexer_next_token(Lexer* lexer) {
    Token token;
    memset(token.value, 0, sizeof(token.value));
    
    lexer_skip_whitespace(lexer);
    
    if (lexer->position >= lexer->length) {
        token.type = TOKEN_EOF;
        return token;
    }
    
    char current = lexer->source[lexer->position];
    
    // Keywords and identifiers
    if (isalpha(current) || current == '_') {
        int start = lexer->position;
        while (lexer->position < lexer->length && 
               (isalnum(lexer->source[lexer->position]) || lexer->source[lexer->position] == '_')) {
            lexer->position++;
        }
        
        int length = lexer->position - start;
        strncpy(token.value, &lexer->source[start], length);
        token.value[length] = '\0';
        
        if (strcmp(token.value, "func") == 0) token.type = TOKEN_FUNC;
        else if (strcmp(token.value, "main") == 0) token.type = TOKEN_MAIN;
        else if (strcmp(token.value, "print") == 0) token.type = TOKEN_PRINT;
        else if (strcmp(token.value, "var") == 0) token.type = TOKEN_VAR;
        else if (strcmp(token.value, "if") == 0) token.type = TOKEN_IF;
        else if (strcmp(token.value, "while") == 0) token.type = TOKEN_WHILE;
        else token.type = TOKEN_IDENTIFIER;
        
        return token;
    }
    
    // Numbers
    if (isdigit(current)) {
        int start = lexer->position;
        while (lexer->position < lexer->length && isdigit(lexer->source[lexer->position])) {
            lexer->position++;
        }
        int length = lexer->position - start;
        strncpy(token.value, &lexer->source[start], length);
        token.value[length] = '\0';
        token.type = TOKEN_NUMBER;
        return token;
    }
    
    // Strings
    if (current == '"') {
        lexer->position++;
        int start = lexer->position;
        while (lexer->position < lexer->length && lexer->source[lexer->position] != '"') {
            lexer->position++;
        }
        int length = lexer->position - start;
        strncpy(token.value, &lexer->source[start], length);
        token.value[length] = '\0';
        if (lexer->position < lexer->length) lexer->position++; // Skip closing quote
        token.type = TOKEN_STRING;
        return token;
    }
    
    // Single character tokens
    switch (current) {
        case '(': token.type = TOKEN_LPAREN; token.value[0] = '('; break;
        case ')': token.type = TOKEN_RPAREN; token.value[0] = ')'; break;
        case '{': token.type = TOKEN_LBRACE; token.value[0] = '{'; break;
        case '}': token.type = TOKEN_RBRACE; token.value[0] = '}'; break;
        case ';': token.type = TOKEN_SEMICOLON; token.value[0] = ';'; break;
        case ',': token.type = TOKEN_COMMA; token.value[0] = ','; break;
        case '=': token.type = TOKEN_ASSIGN; token.value[0] = '='; break;
        case '+': token.type = TOKEN_PLUS; token.value[0] = '+'; break;
        case '-': token.type = TOKEN_MINUS; token.value[0] = '-'; break;
        case '*': token.type = TOKEN_MULTIPLY; token.value[0] = '*'; break;
        case '/': token.type = TOKEN_DIVIDE; token.value[0] = '/'; break;
        default: token.type = TOKEN_UNKNOWN; token.value[0] = current;
    }
    
    lexer->position++;
    return token;
}

void lexer_free(Lexer* lexer) {
    free(lexer->source);
    free(lexer);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Uso: ulx_parser <arquivo.ulx>\n");
        return 1;
    }
    
    FILE* file = fopen(argv[1], "r");
    if (!file) {
        fprintf(stderr, "Erro: Não foi possível abrir o arquivo '%s'\n", argv[1]);
        return 1;
    }
    
    // Read entire file
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    char* source = (char*)malloc(file_size + 1);
    fread(source, 1, file_size, file);
    source[file_size] = '\0';
    fclose(file);
    
    printf("[ULX-PARSER] Analisando: %s\n", argv[1]);
    printf("[ULX-PARSER] Tamanho do arquivo: %ld bytes\n", file_size);
    
    Lexer* lexer = lexer_create(source);
    
    printf("[ULX-PARSER] Tokens encontrados:\n");
    Token token;
    int token_count = 0;
    
    do {
        token = lexer_next_token(lexer);
        token_count++;
        
        if (token.type != TOKEN_EOF) {
            printf("  [%d] Type: %d, Value: '%s'\n", token_count, token.type, token.value);
        }
    } while (token.type != TOKEN_EOF);
    
    printf("[ULX-PARSER] Total de tokens: %d\n", token_count);
    printf("[ULX-PARSER] Análise concluída com sucesso!\n");
    
    lexer_free(lexer);
    free(source);
    
    return 0;
}
