
float soma(int a, int b) {
    return a + b;
    
    a = 10;
}

int main() {
    int contador = 0;
    int valor;
    
    for(int i = 0; i <= 10; i++){
        if (contador == i && valor > 1){
            contador++;
        }
    }
    
    string texto = "fim";
    char c = 'A';
    valor = 3;      

    c = texto;

    valor += soma(contador, 5);
    return 0;

}